# Tokeneyes Installation Guide

## System Requirements

- Python 3.9 or higher
- pip (Python package installer)
- macOS, Linux, or Windows

## Installation Methods

### Method 1: Install from Source (Development)

**For developers and contributors:**

```bash
# Clone the repository
git clone https://github.com/chinazane/Tokeneyes.git
cd Tokeneyes

# Install in development mode
pip install -e .

# Verify installation
tokeneyes --version
```

Development mode (`-e` flag) allows you to make changes to the code and see them immediately without reinstalling.

### Method 2: Install from PyPI (Coming Soon)

**For end users (when released to PyPI):**

```bash
# Install from PyPI
pip install tokeneyes

# Verify installation
tokeneyes --version
```

## Quick Setup

### 1. Initialize Configuration

Run the interactive setup wizard:

```bash
tokeneyes init
```

This will prompt you for:
- API URL (backend server endpoint)
- API Key (authentication token)
- Scan interval (how often to check logs, default: 300s)
- Sync interval (how often to upload events, default: 300s)

**Non-interactive setup:**

```bash
tokeneyes init --api-url=https://api.tokeneyes.dev/v1/track --api-key=your-key-here
```

### 2. Start the Daemon

**Background mode (recommended):**

```bash
tokeneyes start -d
```

The daemon will run in the background and continue tracking even after you close the terminal.

**Foreground mode (for testing/debugging):**

```bash
tokeneyes start
```

Press `Ctrl+C` to stop.

### 3. Verify It's Running

```bash
tokeneyes status
```

You should see:
```
✓ Daemon is running (PID: 12345)
```

## Configuration

### Configuration File Location

Configuration is stored at: `~/.aitracker/config.json`

### Default Configuration

```json
{
  "api_url": "https://api.tokeneyes.dev/v1/track",
  "api_key": null,
  "scan_interval": 300,
  "sync_interval": 300,
  "log_level": "INFO"
}
```

### Manual Configuration

You can edit the config file directly:

```bash
# Edit config file
nano ~/.aitracker/config.json

# Or use your favorite editor
vim ~/.aitracker/config.json
code ~/.aitracker/config.json
```

## Usage

### Check Daemon Status

```bash
tokeneyes status
```

### View Token Usage Statistics

```bash
# Last 7 days (default)
tokeneyes stats

# Last 30 days
tokeneyes stats --days=30

# Filter by service
tokeneyes stats --service=openai
```

### Stop the Daemon

```bash
tokeneyes stop
```

### Open Dashboard

```bash
tokeneyes dashboard
```

Opens your default browser to the web dashboard (requires backend server).

## Logs and Data

### Log File

Scanner daemon logs are stored at: `~/.aitracker/tokeneyes.log`

```bash
# View logs
tail -f ~/.aitracker/tokeneyes.log

# Last 50 lines
tail -50 ~/.aitracker/tokeneyes.log
```

### Event Queue

Token usage events are stored locally at: `~/.aitracker/events.jsonl`

This file contains all tracked events (synced and unsynced) in JSONL format.

### Cursor Store

File read positions are tracked at: `~/.aitracker/cursors.json`

This enables incremental parsing of log files.

### PID File

Daemon process ID is stored at: `~/.aitracker/tokeneyes.pid` when running.

## Troubleshooting

### Command Not Found

If `tokeneyes` command is not found after installation:

```bash
# Verify pip installation location
pip show tokeneyes

# Check if pip bin directory is in PATH
echo $PATH

# Try running with python -m
python -m tokeneyes --version
```

### Daemon Won't Start

1. Check if already running:
   ```bash
   tokeneyes status
   ```

2. Stop any existing daemon:
   ```bash
   tokeneyes stop
   ```

3. Check logs for errors:
   ```bash
   tail -50 ~/.aitracker/tokeneyes.log
   ```

4. Try foreground mode to see errors:
   ```bash
   tokeneyes start
   ```

### No Usage Data

If `tokeneyes stats` shows no data:

1. Ensure daemon is running:
   ```bash
   tokeneyes status
   ```

2. Check if log files exist for your AI tools:
   ```bash
   # Claude Code logs
   ls ~/.claude/

   # OpenAI logs
   ls ~/.config/openai/

   # GitHub Copilot logs (VS Code)
   ls ~/Library/Application\ Support/Code/logs/
   ```

3. Wait a few minutes for the scanner to detect and parse logs

4. Check event queue:
   ```bash
   cat ~/.aitracker/events.jsonl
   ```

### Permission Errors

If you get permission errors accessing log files:

```bash
# Ensure your user has read access to AI tool logs
ls -la ~/.claude/
ls -la ~/.config/openai/
```

Some AI tools may require additional permissions to access their logs.

## Updating

### Development Installation

```bash
cd Tokeneyes
git pull origin main
pip install -e . --upgrade
```

### PyPI Installation (when available)

```bash
pip install --upgrade tokeneyes
```

## Uninstallation

```bash
# Stop daemon if running
tokeneyes stop

# Uninstall package
pip uninstall tokeneyes

# Optionally remove data directory
rm -rf ~/.aitracker
```

## Platform-Specific Notes

### macOS

- Default AI tool log locations:
  - Claude Code: `~/.claude/`
  - VS Code: `~/Library/Application Support/Code/logs/`
  - Cursor: `~/Library/Application Support/Cursor/logs/`

### Linux

- Default AI tool log locations:
  - Claude Code: `~/.claude/`
  - VS Code: `~/.config/Code/logs/`
  - Cursor: `~/.config/Cursor/logs/`

### Windows

- Default AI tool log locations:
  - Claude Code: `%USERPROFILE%\.claude\`
  - VS Code: `%APPDATA%\Code\logs\`
  - Cursor: `%APPDATA%\Cursor\logs\`

- Configuration directory: `%USERPROFILE%\.aitracker\`

## Support

For issues and questions:

- **GitHub Issues**: https://github.com/chinazane/Tokeneyes/issues
- **Documentation**: https://github.com/chinazane/Tokeneyes/tree/main/design
- **Project Scope**: [SCOPE.md](../SCOPE.md)

## Next Steps

After installation:

1. Read [SCOPE.md](../SCOPE.md) to understand the project focus
2. Check [Implementation Status](../IMPLEMENTATION_COMPLETE.md) for current features
3. Explore the [Design Documents](../design/) for architecture details
