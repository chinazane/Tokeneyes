"""
Cursor storage for tracking file read positions
Enables incremental parsing (like pew.md's cursors.json)
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import json


class CursorStore:
    """
    Track file read positions for incremental parsing
    Prevents re-processing already-parsed log entries
    """

    def __init__(self, state_dir: Path):
        """
        Initialize cursor store

        Args:
            state_dir: Directory to store cursor file
        """
        self.cursor_file = state_dir / 'cursors.json'
        self.cursors: Dict[str, dict] = self._load()

    def get(self, file_path: str) -> Dict:
        """
        Get cursor for a file

        Args:
            file_path: Path to file

        Returns:
            Cursor dictionary with offset, size, mtime, inode
        """
        if file_path in self.cursors:
            return self.cursors[file_path]

        # New file - start from beginning
        return {
            'offset': 0,
            'size': 0,
            'mtime': 0,
            'inode': 0
        }

    def update(self, file_path: str, offset: int):
        """
        Update cursor after reading a file

        Args:
            file_path: Path to file
            offset: New byte offset
        """
        path = Path(file_path)

        if not path.exists():
            return

        stat = path.stat()

        self.cursors[file_path] = {
            'offset': offset,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'inode': stat.st_ino,
            'updated_at': datetime.utcnow().isoformat()
        }

        self._save()

    def reset(self, file_path: str):
        """
        Reset cursor for a file (re-read from beginning)

        Args:
            file_path: Path to file
        """
        if file_path in self.cursors:
            del self.cursors[file_path]
            self._save()

    def reset_all(self):
        """Reset all cursors"""
        self.cursors = {}
        self._save()

    def _load(self) -> Dict[str, dict]:
        """Load cursors from disk"""
        if self.cursor_file.exists():
            try:
                with open(self.cursor_file) as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cursors: {e}")
                return {}
        return {}

    def _save(self):
        """Save cursors to disk"""
        self.cursor_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.cursor_file, 'w') as f:
                json.dump(self.cursors, f, indent=2)
        except Exception as e:
            print(f"Error saving cursors: {e}")
