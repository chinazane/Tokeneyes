"""
Configuration management for Tokeneyes
Centralized configuration with validation and persistence
"""

from pathlib import Path
import json
from typing import Optional, Any


class Config:
    """Configuration management for Tokeneyes"""

    DEFAULT_CONFIG_PATH = Path.home() / '.aitracker' / 'config.json'

    DEFAULT_CONFIG = {
        'api_url': 'https://api.tokeneyes.dev/v1/track',
        'api_key': None,
        'scan_interval': 300,  # 5 minutes
        'sync_interval': 300,   # 5 minutes
        'log_level': 'INFO',
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to configuration file (default: ~/.aitracker/config.json)
        """
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.data = self.load()

    def load(self) -> dict:
        """
        Load configuration from file

        Returns:
            Configuration dictionary (defaults + file overrides)
        """
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    file_config = json.load(f)
                return {**self.DEFAULT_CONFIG, **file_config}
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid config file {self.config_path}: {e}")
                print("Using default configuration")
                return self.DEFAULT_CONFIG.copy()

        return self.DEFAULT_CONFIG.copy()

    def save(self):
        """
        Save configuration to file
        Creates directory if it doesn't exist
        """
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value

        Args:
            key: Configuration key
            value: Value to set
        """
        self.data[key] = value

    def to_dict(self) -> dict:
        """Return configuration as dictionary"""
        return self.data.copy()
