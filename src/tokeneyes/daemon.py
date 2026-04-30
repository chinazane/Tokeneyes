"""
Main token scanner daemon
Orchestrates log scanning across all AI providers
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Set
from datetime import datetime
import json
import os
import logging
from collections import defaultdict

from .discovery import LogDiscovery
from .parsers import ParserRegistry, TokenEvent
from .storage.cursor_store import CursorStore
from .storage.event_queue import EventQueue
from .config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('tokeneyes.daemon')


class TokenScannerDaemon:
    """
    Main daemon process for scanning AI tool logs
    Runs as background service on employee machine
    Optimized for concurrent processing and low resource usage
    """

    # Configuration constants
    MAX_CONCURRENT_FILES = 10  # Process up to 10 files concurrently
    MAX_FILE_SIZE_MB = 100  # Skip files larger than 100MB
    CHUNK_SIZE = 8192  # Read files in 8KB chunks

    def __init__(self, config_path: Path = None):
        """
        Initialize scanner daemon

        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path=config_path)
        self.state_dir = Path.home() / '.aitracker'
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Initialize storage
        self.cursor_store = CursorStore(self.state_dir)
        self.event_queue = EventQueue(self.state_dir)

        # Get all registered parsers
        self.parsers = ParserRegistry.get_all_parsers()

        # Discovery service
        self.discovery = LogDiscovery()

        # File modification time cache for efficient scanning
        self._file_mtimes: Dict[str, float] = {}

        # Semaphore for limiting concurrent file operations
        self._file_semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_FILES)

        logger.info(f"Initialized with {len(self.parsers)} parsers")
        logger.info(f"Supported services: {', '.join(self.parsers.keys())}")

    async def start(self):
        """Start the scanner daemon"""
        logger.info("Starting daemon...")

        # Write PID file
        self._write_pid_file()

        try:
            # Initial scan
            await self.scan_all_logs()

            # Start background tasks
            tasks = [
                self.periodic_scan(),
                self.periodic_sync()
            ]

            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Daemon error: {e}", exc_info=True)
        finally:
            # Clean up PID file on exit
            self._remove_pid_file()
            logger.info("Daemon stopped")

    async def scan_all_logs(self):
        """
        Scan all log files for all providers
        Optimized version with concurrent processing and smart filtering
        """
        logger.info("Scanning all logs...")
        start_time = datetime.now()

        # Discover all log files
        all_logs = self.discovery.discover_all()

        # Group files by provider for batch processing
        scan_tasks = []
        for provider, log_files in all_logs.items():
            # Filter out files that haven't changed and are too large
            files_to_scan = self._filter_files_to_scan(log_files)

            if not files_to_scan:
                logger.debug(f"No new changes in {provider} logs")
                continue

            logger.info(f"Scanning {provider}: {len(files_to_scan)} files (filtered from {len(log_files)})")

            # Map provider name to parser service name
            service = self._map_provider_to_service(provider)
            parser = self.parsers.get(service)

            if not parser:
                logger.warning(f"No parser for {provider}, skipping")
                continue

            # Create task for this provider's files
            scan_tasks.append(
                self._scan_provider_files(provider, service, parser, files_to_scan)
            )

        # Process all providers concurrently
        if scan_tasks:
            results = await asyncio.gather(*scan_tasks, return_exceptions=True)

            # Count total events and log errors
            total_events = 0
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Provider scan failed: {result}")
                else:
                    total_events += result

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Scan complete: {total_events} events in {elapsed:.2f}s")
        else:
            logger.info("No files to scan")

    def _filter_files_to_scan(self, log_files: List[Path]) -> List[Path]:
        """
        Filter files that need scanning based on modification time and size

        Args:
            log_files: List of log file paths

        Returns:
            Filtered list of files that need scanning
        """
        files_to_scan = []

        for log_file in log_files:
            try:
                # Check file size
                stat = log_file.stat()
                if stat.st_size > self.MAX_FILE_SIZE_MB * 1024 * 1024:
                    logger.warning(f"Skipping large file: {log_file.name} ({stat.st_size / 1024 / 1024:.1f}MB)")
                    continue

                # Check modification time
                file_key = str(log_file)
                current_mtime = stat.st_mtime
                cached_mtime = self._file_mtimes.get(file_key)

                if cached_mtime is not None and current_mtime <= cached_mtime:
                    # File hasn't been modified, skip it
                    logger.debug(f"Skipping unchanged file: {log_file.name}")
                    continue

                # Update cache and add to scan list
                self._file_mtimes[file_key] = current_mtime
                files_to_scan.append(log_file)

            except Exception as e:
                logger.warning(f"Error checking file {log_file}: {e}")

        return files_to_scan

    async def _scan_provider_files(self, provider: str, service: str, parser, log_files: List[Path]) -> int:
        """
        Scan all files for a specific provider concurrently

        Args:
            provider: Provider name
            service: Parser service name
            parser: Parser instance
            log_files: List of log files to scan

        Returns:
            Total number of events found
        """
        # Create tasks for each file with semaphore limiting
        tasks = [
            self._scan_single_file(log_file, parser)
            for log_file in log_files
        ]

        # Process with controlled concurrency
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Count events and log errors
        total_events = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error scanning {log_files[i].name}: {result}")
            else:
                total_events += result
                if result > 0:
                    logger.debug(f"{log_files[i].name}: {result} events")

        return total_events

    async def _scan_single_file(self, log_file: Path, parser) -> int:
        """
        Scan a single log file with resource limiting

        Args:
            log_file: Path to log file
            parser: Parser instance

        Returns:
            Number of events found
        """
        async with self._file_semaphore:
            try:
                # Get last read position
                cursor = self.cursor_store.get(str(log_file))

                # Parse from offset
                events = await parser.parse(
                    file_path=log_file,
                    start_offset=cursor.get('offset', 0)
                )

                if events:
                    # Queue events for upload
                    for event in events:
                        self.event_queue.add(event)

                    # Update cursor
                    file_size = log_file.stat().st_size
                    self.cursor_store.update(str(log_file), file_size)

                    return len(events)

                return 0

            except Exception as e:
                logger.error(f"Error scanning {log_file}: {e}")
                raise

    async def periodic_scan(self):
        """Scan logs periodically"""
        scan_interval = self.config.get('scan_interval', 300)
        logger.info(f"Starting periodic scan (every {scan_interval}s)")

        while True:
            await asyncio.sleep(scan_interval)
            logger.debug("Running periodic scan...")
            try:
                await self.scan_all_logs()
            except Exception as e:
                logger.error(f"Periodic scan failed: {e}", exc_info=True)

    async def periodic_sync(self):
        """Sync queued events to server with retry logic"""
        sync_interval = self.config.get('sync_interval', 300)
        logger.info(f"Starting periodic sync (every {sync_interval}s)")

        max_retries = 3
        retry_delay = 5  # seconds

        while True:
            await asyncio.sleep(sync_interval)

            # Get unsynced events
            events = self.event_queue.get_unsynced(limit=100)

            if not events:
                logger.debug("No events to sync")
                continue

            logger.info(f"Syncing {len(events)} events to server...")

            # Retry loop
            for attempt in range(max_retries):
                try:
                    # Upload to server
                    success = await self._upload_to_server(events)

                    if success:
                        # Mark as synced
                        self.event_queue.mark_synced([e.id for e in events])
                        logger.info(f"Sync successful: {len(events)} events")
                        break
                    else:
                        logger.warning(f"Sync failed (attempt {attempt + 1}/{max_retries})")

                except Exception as e:
                    logger.error(f"Sync error (attempt {attempt + 1}/{max_retries}): {e}")

                # Wait before retry (exponential backoff)
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
            else:
                logger.error(f"Sync failed after {max_retries} attempts, will retry next cycle")

    async def _upload_to_server(self, events: List[TokenEvent]) -> bool:
        """
        Upload events to central server with timeout

        Args:
            events: List of token events

        Returns:
            True if successful, False otherwise
        """
        api_url = self.config.get('api_url', 'https://api.company.com/api/v1/track')
        api_key = self.config.get('api_key')

        if not api_key:
            logger.warning("No API key configured, skipping upload")
            return False

        try:
            import aiohttp

            timeout = aiohttp.ClientTimeout(total=30)  # 30 second timeout

            async with aiohttp.ClientSession(timeout=timeout) as session:
                payload = {
                    'events': [event.to_dict() for event in events]
                }

                async with session.post(
                    api_url,
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    },
                    json=payload
                ) as response:
                    if response.status == 202:  # Accepted
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"Upload failed: HTTP {response.status} - {error_text}")
                        return False

        except asyncio.TimeoutError:
            logger.error("Upload timeout after 30s")
            return False
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False

    def _map_provider_to_service(self, provider: str) -> str:
        """Map provider name from discovery to parser service name"""
        mapping = {
            'openai': 'openai',
            'anthropic-cli': 'anthropic',
            'anthropic-web': 'anthropic',
            'google-gemini': 'google',
            'github-copilot': 'github',
            'deepseek': 'deepseek',
            'meta-llama-ollama': 'meta',
            'mistral': 'mistral',
            'minimax': 'minimax',
            'xai-grok': 'xai',
            'cohere': 'cohere',
            'cursor': 'cursor',
            'continue-dev': 'continue',
            'codeium': 'codeium'
        }

        return mapping.get(provider, provider)

    def _write_pid_file(self):
        """Write PID file for daemon tracking"""
        pid_file = self.state_dir / 'tokeneyes.pid'
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def _remove_pid_file(self):
        """Remove PID file on shutdown"""
        pid_file = self.state_dir / 'tokeneyes.pid'
        if pid_file.exists():
            pid_file.unlink()

    @staticmethod
    def is_running() -> bool:
        """Check if daemon is already running"""
        pid_file = Path.home() / '.aitracker' / 'tokeneyes.pid'
        if not pid_file.exists():
            return False

        # Check if process is alive
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Signal 0 checks existence
            return True
        except (OSError, ProcessLookupError, ValueError):
            # Stale PID file - process is dead
            return False

    def _load_config(self, config_path: Path = None) -> dict:
        """
        Deprecated: Use Config class instead
        Kept for backward compatibility
        """
        if not config_path:
            config_path = Path.home() / '.aitracker' / 'config.json'

        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)

        # Default configuration
        return {
            'api_url': 'https://api.company.com/api/v1/track',
            'scan_interval': 300,  # 5 minutes
            'sync_interval': 300    # 5 minutes
        }


# CLI entry point
async def main():
    """Main entry point for daemon"""
    daemon = TokenScannerDaemon()
    await daemon.start()


if __name__ == '__main__':
    asyncio.run(main())
