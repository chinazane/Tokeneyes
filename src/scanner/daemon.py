"""
Main token scanner daemon
Orchestrates log scanning across all AI providers
"""

import asyncio
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import json

from .discovery import LogDiscovery
from .parsers import ParserRegistry, TokenEvent
from .storage.cursor_store import CursorStore
from .storage.event_queue import EventQueue


class TokenScannerDaemon:
    """
    Main daemon process for scanning AI tool logs
    Runs as background service on employee machine
    """

    def __init__(self, config_path: Path = None):
        """
        Initialize scanner daemon

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.state_dir = Path.home() / '.aitracker'
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # Initialize storage
        self.cursor_store = CursorStore(self.state_dir)
        self.event_queue = EventQueue(self.state_dir)

        # Get all registered parsers
        self.parsers = ParserRegistry.get_all_parsers()

        # Discovery service
        self.discovery = LogDiscovery()

        print(f"[TokenScanner] Initialized with {len(self.parsers)} parsers")
        print(f"[TokenScanner] Supported services: {', '.join(self.parsers.keys())}")

    async def start(self):
        """Start the scanner daemon"""
        print("[TokenScanner] Starting daemon...")

        # Initial scan
        await self.scan_all_logs()

        # Start background tasks
        tasks = [
            self.periodic_scan(),
            self.periodic_sync()
        ]

        await asyncio.gather(*tasks)

    async def scan_all_logs(self):
        """Scan all log files for all providers"""
        print("[TokenScanner] Scanning all logs...")

        # Discover all log files
        all_logs = self.discovery.discover_all()

        total_events = 0

        for provider, log_files in all_logs.items():
            print(f"[TokenScanner] Scanning {provider}: {len(log_files)} files")

            # Map provider name to parser service name
            service = self._map_provider_to_service(provider)
            parser = self.parsers.get(service)

            if not parser:
                print(f"[TokenScanner] No parser for {provider}, skipping")
                continue

            for log_file in log_files:
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

                        total_events += len(events)

                        # Update cursor
                        file_size = log_file.stat().st_size
                        self.cursor_store.update(str(log_file), file_size)

                        print(f"[TokenScanner]   {log_file.name}: {len(events)} events")

                except Exception as e:
                    print(f"[TokenScanner] Error scanning {log_file}: {e}")

        print(f"[TokenScanner] Scan complete: {total_events} events queued")

    async def periodic_scan(self):
        """Scan logs periodically (every 5 minutes)"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            print("[TokenScanner] Running periodic scan...")
            await self.scan_all_logs()

    async def periodic_sync(self):
        """Sync queued events to server (every 5 minutes)"""
        while True:
            await asyncio.sleep(300)  # 5 minutes

            # Get unsynced events
            events = self.event_queue.get_unsynced(limit=100)

            if events:
                print(f"[TokenScanner] Syncing {len(events)} events to server...")

                try:
                    # Upload to server
                    success = await self._upload_to_server(events)

                    if success:
                        # Mark as synced
                        self.event_queue.mark_synced([e.id for e in events])
                        print(f"[TokenScanner] Sync successful: {len(events)} events")
                    else:
                        print(f"[TokenScanner] Sync failed, will retry later")

                except Exception as e:
                    print(f"[TokenScanner] Sync error: {e}")

    async def _upload_to_server(self, events: List[TokenEvent]) -> bool:
        """
        Upload events to central server

        Args:
            events: List of token events

        Returns:
            True if successful, False otherwise
        """
        # TODO: Implement actual HTTP upload
        # For now, just simulate success
        import aiohttp

        api_url = self.config.get('api_url', 'https://api.company.com/api/v1/track')
        api_key = self.config.get('api_key')

        if not api_key:
            print("[TokenScanner] No API key configured, skipping upload")
            return False

        try:
            async with aiohttp.ClientSession() as session:
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
                        print(f"[TokenScanner] Upload failed: HTTP {response.status}")
                        return False

        except Exception as e:
            print(f"[TokenScanner] Upload error: {e}")
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

    def _load_config(self, config_path: Path = None) -> dict:
        """Load configuration from file"""
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
