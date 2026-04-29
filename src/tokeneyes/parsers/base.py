"""
Base parser interface for all AI model providers
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import json


@dataclass
class TokenEvent:
    """Standardized token usage event"""
    timestamp: datetime
    service: str  # openai, anthropic, google, etc.
    tool: str     # chatgpt-web, claude-code, gemini-api, etc.
    model: str    # gpt-4, claude-3-5-sonnet, gemini-1.5-pro, etc.
    interface: str  # web, api, cli

    # Token counts
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0

    # Performance
    request_duration_ms: Optional[int] = None

    # Attribution
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    project_id: Optional[str] = None

    # Metadata
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'service': self.service,
            'tool': self.tool,
            'model': self.model,
            'interface': self.interface,
            'prompt_tokens': self.prompt_tokens,
            'completion_tokens': self.completion_tokens,
            'total_tokens': self.total_tokens,
            'cache_read_tokens': self.cache_read_tokens,
            'cache_creation_tokens': self.cache_creation_tokens,
            'request_duration_ms': self.request_duration_ms,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'project_id': self.project_id,
            'metadata': self.metadata
        }


class BaseParser(ABC):
    """Base class for all AI model log parsers"""

    def __init__(self):
        self.service_name: str = ""
        self.supported_models: List[str] = []

    @abstractmethod
    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """
        Parse log file from given offset and extract token usage events

        Args:
            file_path: Path to log file
            start_offset: Byte offset to start reading from

        Returns:
            List of TokenEvent objects
        """
        pass

    @abstractmethod
    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage information from log entry

        Args:
            data: Parsed log entry (usually JSON)

        Returns:
            Dictionary with token counts or None if no usage found
        """
        pass

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count from text
        Rough approximation: 1 token ≈ 4 characters

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        if not text:
            return 0
        return len(text) // 4

    def parse_timestamp(self, timestamp_str: str) -> datetime:
        """
        Parse timestamp from various formats

        Args:
            timestamp_str: Timestamp string

        Returns:
            datetime object
        """
        # Try common formats
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue

        # Fallback to current time
        return datetime.utcnow()


class ParserRegistry:
    """Registry for all available parsers"""

    _parsers: Dict[str, type] = {}

    @classmethod
    def register(cls, service: str):
        """Decorator to register a parser"""
        def decorator(parser_class):
            cls._parsers[service] = parser_class
            return parser_class
        return decorator

    @classmethod
    def get_parser(cls, service: str) -> Optional[BaseParser]:
        """Get parser instance for a service"""
        parser_class = cls._parsers.get(service)
        if parser_class:
            return parser_class()
        return None

    @classmethod
    def get_all_parsers(cls) -> Dict[str, BaseParser]:
        """Get all registered parsers"""
        return {
            service: parser_class()
            for service, parser_class in cls._parsers.items()
        }

    @classmethod
    def list_services(cls) -> List[str]:
        """List all registered service names"""
        return list(cls._parsers.keys())
