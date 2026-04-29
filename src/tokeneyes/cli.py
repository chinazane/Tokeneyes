"""
CLI interface for Tokeneyes
Professional command-line interface using Click and Rich
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import asyncio
from pathlib import Path
import json
import sys
import os
import signal
from datetime import datetime, timedelta

from .daemon import TokenScannerDaemon
from .config import Config

console = Console()


def _setup_sdk_wrappers():
    """
    Set up automatic SDK wrapper imports via sitecustomize.py

    This creates a sitecustomize.py file that automatically installs
    import hooks when Python starts, making SDK tracking automatic.
    """
    import site
    import sys

    console.print("\n[cyan]🔧 Setting up automatic SDK tracking...[/cyan]\n")

    # Find site-packages directory
    site_packages = site.getsitepackages()

    # Prefer user site-packages (doesn't require sudo)
    user_site = site.getusersitepackages()

    # Ensure user site-packages exists
    Path(user_site).mkdir(parents=True, exist_ok=True)

    sitecustomize_path = Path(user_site) / 'sitecustomize.py'

    # Content for sitecustomize.py
    sitecustomize_content = '''"""
Tokeneyes auto-tracking setup

This file is automatically executed when Python starts.
It installs import hooks to automatically track AI SDK usage.

Created by: tokeneyes init
"""

import os

# Only activate if TOKENEYES_TRACK is set (opt-in)
# Or if ~/.aitracker/auto_track exists (permanent opt-in)
if os.getenv('TOKENEYES_TRACK') or os.path.exists(os.path.expanduser('~/.aitracker/auto_track')):
    try:
        from tokeneyes.sdk.autopatch import install_import_hooks
        install_import_hooks()
    except ImportError:
        # Tokeneyes not installed, skip silently
        pass
'''

    try:
        # Check if sitecustomize.py already exists
        if sitecustomize_path.exists():
            console.print(f"[yellow]⚠[/yellow]  {sitecustomize_path} already exists")

            # Read existing content
            with open(sitecustomize_path) as f:
                existing = f.read()

            # Check if Tokeneyes already configured
            if 'tokeneyes' in existing.lower():
                console.print("[green]✓[/green] Tokeneyes tracking already configured")
            else:
                # Append to existing
                console.print("Appending Tokeneyes configuration...")
                with open(sitecustomize_path, 'a') as f:
                    f.write('\n\n' + sitecustomize_content)
                console.print(f"[green]✓[/green] Updated {sitecustomize_path}")
        else:
            # Create new sitecustomize.py
            with open(sitecustomize_path, 'w') as f:
                f.write(sitecustomize_content)
            console.print(f"[green]✓[/green] Created {sitecustomize_path}")

        # Create auto_track marker file (permanent opt-in)
        auto_track_marker = Path.home() / '.aitracker' / 'auto_track'
        auto_track_marker.parent.mkdir(parents=True, exist_ok=True)
        auto_track_marker.touch()
        console.print(f"[green]✓[/green] Created auto-track marker: {auto_track_marker}")

        # Show success message
        console.print("\n[bold green]✓ SDK tracking enabled![/bold green]\n")

        console.print("[bold]How it works:[/bold]")
        console.print("  • Python automatically loads import hooks on startup")
        console.print("  • All OpenAI/Anthropic imports are automatically wrapped")
        console.print("  • Your code runs unchanged - tracking is transparent\n")

        console.print("[bold]In your code:[/bold]")
        console.print("  [dim]from openai import OpenAI  # ← Automatically tracked![/dim]")
        console.print("  [dim]from anthropic import Anthropic  # ← Automatically tracked![/dim]\n")

        console.print("[bold]To disable:[/bold]")
        console.print(f"  [dim]rm {auto_track_marker}[/dim]\n")

    except Exception as e:
        console.print(f"[red]✗[/red] Error setting up SDK tracking: {e}")
        console.print("\n[yellow]Alternative:[/yellow] Use manual imports:")
        console.print("  [dim]from tokeneyes.sdk import OpenAI[/dim]\n")


@click.group()
@click.version_option(version='0.1.0', prog_name='tokeneyes')
def main():
    """
    Tokeneyes - AI token usage tracker for vibe coding

    Track AI coding assistant usage across CLI tools, IDEs, and APIs.
    Privacy-first: only metadata, never prompts/responses.
    """
    pass


@main.command()
@click.option('--api-url', help='Backend API URL')
@click.option('--api-key', help='API authentication key')
@click.option('--scan-interval', type=int, help='Scan interval in seconds (default: 300)')
@click.option('--sync-interval', type=int, help='Sync interval in seconds (default: 300)')
@click.option('--setup-sdk-wrappers/--no-setup-sdk-wrappers', default=None, help='Setup automatic SDK wrapper imports')
def init(api_url, api_key, scan_interval, sync_interval, setup_sdk_wrappers):
    """
    Initialize Tokeneyes configuration

    Creates configuration file at ~/.aitracker/config.json
    and optionally sets up automatic SDK wrapper imports.
    """
    console.print(Panel.fit(
        "[bold cyan]Tokeneyes Configuration[/bold cyan]",
        subtitle="Setting up your AI token tracker"
    ))

    config = Config()

    # Interactive setup if no options provided
    if not any([api_url, api_key, scan_interval, sync_interval]):
        console.print("\n[yellow]Let's set up your configuration...[/yellow]\n")

        # API URL
        default_url = config.DEFAULT_CONFIG['api_url']
        url_input = console.input(f"API URL [[green]{default_url}[/green]]: ").strip()
        api_url = url_input if url_input else default_url

        # API Key (optional)
        key_input = console.input("API Key (optional, press Enter to skip): ").strip()
        api_key = key_input if key_input else None

        # Scan interval
        default_scan = config.DEFAULT_CONFIG['scan_interval']
        scan_input = console.input(f"Scan interval in seconds [[green]{default_scan}[/green]]: ").strip()
        scan_interval = int(scan_input) if scan_input.isdigit() else default_scan

        # Sync interval
        default_sync = config.DEFAULT_CONFIG['sync_interval']
        sync_input = console.input(f"Sync interval in seconds [[green]{default_sync}[/green]]: ").strip()
        sync_interval = int(sync_input) if sync_input.isdigit() else default_sync

    # Set configuration
    if api_url:
        config.set('api_url', api_url)
    if api_key:
        config.set('api_key', api_key)
    if scan_interval:
        config.set('scan_interval', scan_interval)
    if sync_interval:
        config.set('sync_interval', sync_interval)

    # Save configuration
    config.save()

    console.print(f"\n[green]✓[/green] Configuration saved to: {config.config_path}")

    # Show configuration
    table = Table(title="\nConfiguration Summary")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("API URL", config.get('api_url'))
    table.add_row("API Key", "***" + config.get('api_key')[-4:] if config.get('api_key') else "Not set")
    table.add_row("Scan Interval", f"{config.get('scan_interval')} seconds")
    table.add_row("Sync Interval", f"{config.get('sync_interval')} seconds")

    console.print(table)

    # SDK Wrapper Setup
    console.print("\n" + "="*60)
    console.print("[bold cyan]SDK Wrapper Setup[/bold cyan]")
    console.print("="*60 + "\n")

    console.print("Tokeneyes can automatically track API calls in your Python code.")
    console.print("This requires a one-time setup to enable import hooks.\n")

    # Ask if user wants SDK wrapper setup (if not specified via CLI option)
    if setup_sdk_wrappers is None:
        setup_choice = console.input(
            "Enable automatic SDK tracking? [[green]Y[/green]/n]: "
        ).strip().lower()
        setup_sdk_wrappers = setup_choice != 'n'

    if setup_sdk_wrappers:
        _setup_sdk_wrappers()
    else:
        console.print("\n[yellow]ℹ[/yellow]  SDK wrapper setup skipped.")
        console.print("You can manually use SDK wrappers by changing imports:")
        console.print("  [dim]from tokeneyes.sdk import OpenAI[/dim]\n")

    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Start the scanner: [cyan]tokeneyes start -d[/cyan]")
    console.print("  2. Check status: [cyan]tokeneyes status[/cyan]")
    console.print("  3. View stats: [cyan]tokeneyes stats[/cyan]\n")


@main.command()
@click.option('--daemon', '-d', is_flag=True, help='Run as background daemon')
@click.option('--config', '-c', type=click.Path(exists=True), help='Config file path')
def start(daemon, config):
    """
    Start the token scanner daemon

    Monitors AI tool logs and tracks token usage.
    """
    # Check if already running
    if TokenScannerDaemon.is_running():
        console.print("[yellow]⚠[/yellow]  Daemon is already running")
        console.print("Check status with: [cyan]tokeneyes status[/cyan]")
        sys.exit(1)

    if daemon:
        # Background daemon mode
        console.print("[cyan]🚀 Starting Tokeneyes daemon in background...[/cyan]")

        # Fork process
        pid = os.fork()
        if pid > 0:
            # Parent process
            console.print(f"[green]✓[/green] Daemon started with PID: {pid}")
            console.print("Check status with: [cyan]tokeneyes status[/cyan]")
            sys.exit(0)

        # Child process - detach from terminal
        os.setsid()
        os.chdir('/')

        # Redirect stdout/stderr to log file
        log_dir = Path.home() / '.aitracker'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / 'tokeneyes.log'

        sys.stdout = open(log_file, 'a')
        sys.stderr = open(log_file, 'a')

        # Run daemon
        config_path = Path(config) if config else None
        daemon_instance = TokenScannerDaemon(config_path=config_path)
        asyncio.run(daemon_instance.start())

    else:
        # Foreground mode
        console.print(Panel.fit(
            "[bold cyan]Tokeneyes Scanner Daemon[/bold cyan]",
            subtitle="Press Ctrl+C to stop"
        ))

        try:
            config_path = Path(config) if config else None
            daemon_instance = TokenScannerDaemon(config_path=config_path)
            asyncio.run(daemon_instance.start())
        except KeyboardInterrupt:
            console.print("\n[yellow]⏸[/yellow]  Stopping daemon...")
            sys.exit(0)


@main.command()
def stop():
    """
    Stop the running daemon

    Gracefully shuts down the background daemon process.
    """
    if not TokenScannerDaemon.is_running():
        console.print("[yellow]⚠[/yellow]  Daemon is not running")
        sys.exit(1)

    # Get PID
    pid_file = Path.home() / '.aitracker' / 'tokeneyes.pid'
    try:
        with open(pid_file) as f:
            pid = int(f.read().strip())

        # Send SIGTERM
        os.kill(pid, signal.SIGTERM)

        console.print(f"[green]✓[/green] Daemon stopped (PID: {pid})")

        # Remove PID file
        pid_file.unlink()

    except (FileNotFoundError, ProcessLookupError):
        console.print("[red]✗[/red] Could not stop daemon (PID file not found or process dead)")
        # Clean up stale PID file
        if pid_file.exists():
            pid_file.unlink()
        sys.exit(1)


@main.command()
def status():
    """
    Show scanner daemon status

    Displays current daemon state, parsers, and recent activity.
    """
    console.print(Panel.fit("[bold cyan]Tokeneyes Status[/bold cyan]"))

    if TokenScannerDaemon.is_running():
        # Get PID
        pid_file = Path.home() / '.aitracker' / 'tokeneyes.pid'
        with open(pid_file) as f:
            pid = int(f.read().strip())

        console.print(f"\n[green]✓[/green] Daemon is [bold green]running[/bold green] (PID: {pid})\n")

        # Show status table
        table = Table()
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Status", "Running")
        table.add_row("PID", str(pid))
        table.add_row("Parsers", "10 providers")

        # Check log file for last activity
        log_file = Path.home() / '.aitracker' / 'tokeneyes.log'
        if log_file.exists():
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            time_ago = datetime.now() - mtime
            if time_ago.seconds < 60:
                last_activity = f"{time_ago.seconds} seconds ago"
            elif time_ago.seconds < 3600:
                last_activity = f"{time_ago.seconds // 60} minutes ago"
            else:
                last_activity = f"{time_ago.seconds // 3600} hours ago"
            table.add_row("Last Activity", last_activity)

        # Check event queue
        queue_file = Path.home() / '.aitracker' / 'events.jsonl'
        if queue_file.exists():
            with open(queue_file) as f:
                events = [line for line in f if line.strip()]
            unsynced = sum(1 for e in events if '"synced":false' in e or '"synced": false' in e)
            table.add_row("Queue Size", f"{unsynced} unsynced events")

        console.print(table)

        console.print(f"\n[dim]Log file: {log_file}[/dim]")

    else:
        console.print(f"\n[red]✗[/red] Daemon is [bold red]not running[/bold red]\n")
        console.print("Start with: [cyan]tokeneyes start -d[/cyan]")


@main.command()
@click.option('--days', '-d', default=7, help='Number of days to show')
@click.option('--service', '-s', help='Filter by service (e.g., openai, anthropic)')
def stats(days, service):
    """
    Show token usage statistics

    Displays usage summary from local event queue.
    """
    console.print(Panel.fit(f"[bold cyan]Token Usage - Last {days} Days[/bold cyan]"))

    queue_file = Path.home() / '.aitracker' / 'events.jsonl'

    if not queue_file.exists():
        console.print("\n[yellow]⚠[/yellow]  No usage data found")
        console.print("Start the daemon to begin tracking: [cyan]tokeneyes start -d[/cyan]\n")
        return

    # Parse events
    cutoff_date = datetime.now() - timedelta(days=days)
    events_by_service = {}
    total_tokens = 0

    try:
        with open(queue_file) as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    event = json.loads(line)

                    # Filter by date
                    event_time = datetime.fromisoformat(event.get('timestamp', '').replace('Z', '+00:00'))
                    if event_time < cutoff_date:
                        continue

                    # Filter by service if specified
                    event_service = event.get('service', 'unknown')
                    if service and event_service != service:
                        continue

                    # Aggregate
                    if event_service not in events_by_service:
                        events_by_service[event_service] = {
                            'count': 0,
                            'prompt_tokens': 0,
                            'completion_tokens': 0,
                            'total_tokens': 0
                        }

                    events_by_service[event_service]['count'] += 1
                    events_by_service[event_service]['prompt_tokens'] += event.get('prompt_tokens', 0)
                    events_by_service[event_service]['completion_tokens'] += event.get('completion_tokens', 0)
                    events_by_service[event_service]['total_tokens'] += event.get('total_tokens', 0)

                    total_tokens += event.get('total_tokens', 0)

                except (json.JSONDecodeError, ValueError):
                    continue

        if not events_by_service:
            console.print(f"\n[yellow]⚠[/yellow]  No usage data in last {days} days\n")
            return

        # Display table
        table = Table(title=f"\nUsage Summary")
        table.add_column("Service", style="cyan")
        table.add_column("Requests", style="yellow", justify="right")
        table.add_column("Prompt Tokens", style="blue", justify="right")
        table.add_column("Completion Tokens", style="green", justify="right")
        table.add_column("Total Tokens", style="magenta", justify="right")

        for svc, stats in sorted(events_by_service.items()):
            table.add_row(
                svc,
                f"{stats['count']:,}",
                f"{stats['prompt_tokens']:,}",
                f"{stats['completion_tokens']:,}",
                f"{stats['total_tokens']:,}"
            )

        console.print(table)
        console.print(f"\n[bold]Total tokens across all services:[/bold] [magenta]{total_tokens:,}[/magenta]\n")

    except Exception as e:
        console.print(f"[red]Error reading usage data: {e}[/red]")


@main.command()
def dashboard():
    """
    Open the web dashboard

    Opens your default browser to the Tokeneyes dashboard.
    """
    config = Config()
    api_url = config.get('api_url', 'https://api.tokeneyes.dev')

    # Extract dashboard URL from API URL
    dashboard_url = api_url.replace('/api/v1/track', '').replace('/v1/track', '')

    console.print(f"[cyan]🌐 Opening dashboard...[/cyan]")
    console.print(f"URL: {dashboard_url}\n")

    import webbrowser
    try:
        webbrowser.open(dashboard_url)
        console.print("[green]✓[/green] Dashboard opened in browser")
    except Exception as e:
        console.print(f"[red]✗[/red] Could not open browser: {e}")
        console.print(f"Open manually: {dashboard_url}")


if __name__ == '__main__':
    main()
