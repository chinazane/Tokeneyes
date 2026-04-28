"""
Log file discovery for all supported AI model providers
"""

from pathlib import Path
from typing import List, Dict
import glob
import os


class LogDiscovery:
    """Discover log files for all supported AI tools"""

    # Log file patterns for all providers
    LOG_PATTERNS = {
        # Tier 0: Core providers (P0)
        'openai': [
            '~/.openai/logs/*.log',
            '~/.openai/*.jsonl',
            '~/Library/Logs/OpenAI/*.log',
            '~/AppData/Local/OpenAI/logs/*.log'
        ],

        'anthropic-cli': [
            '~/.claude/projects/**/*.jsonl',
            '~/.claude/logs/*.log'
        ],

        'anthropic-web': [
            # Tracked via browser extension
        ],

        'google-gemini': [
            '~/.google-cloud/logs/*.log',
            '~/Library/Application Support/Google/AIStudio/*.log',
            '~/AppData/Local/Google/AIStudio/*.log'
        ],

        'github-copilot': [
            '~/Library/Application Support/Code/User/workspaceStorage/*/chatSessions/*.jsonl',
            '~/Library/Application Support/Code/logs/*.log',
            '~/.copilot/logs/*.log',
            '~/AppData/Roaming/Code/User/workspaceStorage/*/chatSessions/*.jsonl',
            '~/.vscode/extensions/github.copilot-*/logs/*.log'
        ],

        # Tier 1: Major providers (P1)
        'deepseek': [
            '~/.deepseek/logs/*.log',
            '~/.config/deepseek/*.jsonl',
            '~/.deepseek/*.log'
        ],

        'meta-llama-ollama': [
            '~/.ollama/logs/*.log',
            '~/Library/Application Support/Ollama/logs/*.log',
            '~/AppData/Local/Ollama/logs/*.log'
        ],

        'mistral': [
            '~/.mistral/logs/*.log',
            '~/.config/mistral/*.jsonl'
        ],

        # Tier 2: Additional providers (P2)
        'minimax': [
            '~/.minimax/*.log',
            '~/.config/minimax/*.jsonl'
        ],

        'xai-grok': [
            # Primarily web-based, tracked via browser extension
        ],

        'cohere': [
            '~/.cohere/*.log',
            '~/.config/cohere/*.jsonl'
        ],

        # IDE integrations
        'cursor': [
            '~/.cursor/logs/*.log',
            '~/Library/Application Support/Cursor/logs/*.log'
        ],

        'continue-dev': [
            '~/.continue/logs/*.log'
        ],

        'codeium': [
            '~/.codeium/logs/*.log',
            '~/Library/Application Support/Codeium/logs/*.log'
        ],

        'tabnine': [
            '~/.tabnine/logs/*.log',
            '~/Library/Application Support/TabNine/logs/*.log'
        ]
    }

    @classmethod
    def discover_logs(cls, provider: str) -> List[Path]:
        """
        Discover log files for a specific provider

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic-cli')

        Returns:
            List of Path objects to log files
        """
        patterns = cls.LOG_PATTERNS.get(provider, [])
        log_files = []

        for pattern in patterns:
            # Expand user home directory
            expanded_pattern = os.path.expanduser(pattern)

            # Find matching files
            matches = glob.glob(expanded_pattern, recursive=True)

            for match in matches:
                path = Path(match)
                if path.is_file():
                    log_files.append(path)

        # Sort by modification time (newest first)
        log_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return log_files

    @classmethod
    def discover_all(cls) -> Dict[str, List[Path]]:
        """
        Discover log files for all providers

        Returns:
            Dictionary mapping provider name to list of log files
        """
        all_logs = {}

        for provider in cls.LOG_PATTERNS.keys():
            logs = cls.discover_logs(provider)
            if logs:
                all_logs[provider] = logs

        return all_logs

    @classmethod
    def get_providers(cls) -> List[str]:
        """Get list of all supported providers"""
        return list(cls.LOG_PATTERNS.keys())

    @classmethod
    def add_custom_pattern(cls, provider: str, pattern: str):
        """
        Add a custom log pattern for a provider

        Args:
            provider: Provider name
            pattern: Glob pattern for log files
        """
        if provider not in cls.LOG_PATTERNS:
            cls.LOG_PATTERNS[provider] = []

        cls.LOG_PATTERNS[provider].append(pattern)
