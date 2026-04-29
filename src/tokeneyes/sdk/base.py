"""
SDK Wrapper Base Classes

Provides automatic token tracking for AI SDK calls by wrapping
official SDKs (OpenAI, Anthropic, etc.) and intercepting responses.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
import json
from abc import ABC, abstractmethod


class TokenTracker:
    """
    Tracks token usage events locally
    Works independently of the daemon for immediate tracking
    """

    def __init__(self, state_dir: Path = None):
        """
        Initialize token tracker

        Args:
            state_dir: Directory for event storage (default: ~/.aitracker)
        """
        self.state_dir = state_dir or Path.home() / '.aitracker'
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.event_file = self.state_dir / 'sdk_events.jsonl'

    def track_event(
        self,
        service: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int = 0,
        cached_tokens: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track a token usage event

        Args:
            service: Service name (openai, anthropic, etc.)
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            total_tokens: Total tokens (if different from sum)
            cached_tokens: Cached tokens (if applicable)
            metadata: Additional metadata
        """
        if total_tokens == 0:
            total_tokens = prompt_tokens + completion_tokens

        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'service': service,
            'tool': 'sdk-wrapper',
            'model': model,
            'interface': 'api',
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens,
            'cached_tokens': cached_tokens,
            'synced': False,
            'metadata': metadata or {}
        }

        # Append to JSONL file
        with open(self.event_file, 'a') as f:
            f.write(json.dumps(event) + '\n')


class BaseSDKWrapper(ABC):
    """
    Base class for SDK wrappers
    Provides common functionality for tracking token usage
    """

    def __init__(self, track_tokens: bool = True, state_dir: Path = None):
        """
        Initialize SDK wrapper

        Args:
            track_tokens: Enable token tracking (default: True)
            state_dir: Directory for event storage
        """
        self.track_tokens = track_tokens
        self.tracker = TokenTracker(state_dir=state_dir) if track_tokens else None

    @abstractmethod
    def _extract_usage(self, response: Any) -> Dict[str, int]:
        """
        Extract token usage from response

        Args:
            response: API response object

        Returns:
            Dictionary with token counts
        """
        pass

    def _track_response(self, response: Any, service: str, model: str):
        """
        Track token usage from response

        Args:
            response: API response object
            service: Service name
            model: Model name
        """
        if not self.track_tokens:
            return

        usage = self._extract_usage(response)

        if usage:
            self.tracker.track_event(
                service=service,
                model=model,
                **usage
            )
