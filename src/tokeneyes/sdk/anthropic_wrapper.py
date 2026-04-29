"""
Anthropic SDK Wrapper

Drop-in replacement for Anthropic Python SDK with automatic token tracking.

Usage:
    # Instead of:
    from anthropic import Anthropic

    # Use:
    from tokeneyes.sdk import Anthropic

    # Everything else stays the same!
    client = Anthropic(api_key="...")
    response = client.messages.create(...)
"""

from typing import Any, Dict, Optional
from pathlib import Path

try:
    from anthropic import Anthropic as _Anthropic
    from anthropic import AsyncAnthropic as _AsyncAnthropic
    from anthropic.types import Message
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    _Anthropic = None
    _AsyncAnthropic = None
    Message = None

from .base import BaseSDKWrapper


class AnthropicWrapper(BaseSDKWrapper):
    """Anthropic SDK wrapper with token tracking"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        track_tokens: bool = True,
        state_dir: Path = None,
        **kwargs
    ):
        """
        Initialize Anthropic client with token tracking

        Args:
            api_key: Anthropic API key
            track_tokens: Enable token tracking (default: True)
            state_dir: Directory for event storage
            **kwargs: Additional arguments passed to Anthropic client
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "Anthropic SDK not installed. Install with: pip install anthropic"
            )

        super().__init__(track_tokens=track_tokens, state_dir=state_dir)

        # Create underlying Anthropic client
        self._client = _Anthropic(api_key=api_key, **kwargs)

        # Wrap the messages.create method
        self._original_messages_create = self._client.messages.create
        self._client.messages.create = self._wrapped_messages_create

    def _wrapped_messages_create(self, *args, **kwargs) -> Message:
        """
        Wrapped version of messages.create that tracks tokens

        Args:
            *args: Positional arguments for the API call
            **kwargs: Keyword arguments for the API call

        Returns:
            Message response
        """
        # Call the original method
        response = self._original_messages_create(*args, **kwargs)

        # Track token usage
        if self.track_tokens and response:
            model = kwargs.get('model') or (args[0] if args else 'unknown')
            self._track_response(response, service='anthropic', model=model)

        return response

    def _extract_usage(self, response: Message) -> Dict[str, int]:
        """
        Extract token usage from Anthropic response

        Args:
            response: Message response object

        Returns:
            Dictionary with token counts
        """
        if not hasattr(response, 'usage') or not response.usage:
            return {}

        usage = response.usage

        # Anthropic uses input_tokens and output_tokens
        prompt_tokens = usage.input_tokens or 0
        completion_tokens = usage.output_tokens or 0

        # Handle prompt caching
        cache_creation = getattr(usage, 'cache_creation_input_tokens', 0) or 0
        cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0

        return {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens,
            'cached_tokens': cache_creation + cache_read,
            'metadata': {
                'cache_creation_input_tokens': cache_creation,
                'cache_read_input_tokens': cache_read
            }
        }

    def __getattr__(self, name: str) -> Any:
        """
        Proxy all other attributes to the underlying Anthropic client

        Args:
            name: Attribute name

        Returns:
            Attribute from underlying client
        """
        return getattr(self._client, name)


class AsyncAnthropicWrapper(BaseSDKWrapper):
    """Async Anthropic SDK wrapper with token tracking"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        track_tokens: bool = True,
        state_dir: Path = None,
        **kwargs
    ):
        """
        Initialize async Anthropic client with token tracking

        Args:
            api_key: Anthropic API key
            track_tokens: Enable token tracking (default: True)
            state_dir: Directory for event storage
            **kwargs: Additional arguments passed to AsyncAnthropic client
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "Anthropic SDK not installed. Install with: pip install anthropic"
            )

        super().__init__(track_tokens=track_tokens, state_dir=state_dir)

        # Create underlying AsyncAnthropic client
        self._client = _AsyncAnthropic(api_key=api_key, **kwargs)

        # Wrap the messages.create method
        self._original_messages_create = self._client.messages.create
        self._client.messages.create = self._wrapped_messages_create

    async def _wrapped_messages_create(self, *args, **kwargs) -> Message:
        """
        Wrapped async version of messages.create

        Args:
            *args: Positional arguments for the API call
            **kwargs: Keyword arguments for the API call

        Returns:
            Message response
        """
        # Call the original method
        response = await self._original_messages_create(*args, **kwargs)

        # Track token usage
        if self.track_tokens and response:
            model = kwargs.get('model') or (args[0] if args else 'unknown')
            self._track_response(response, service='anthropic', model=model)

        return response

    def _extract_usage(self, response: Message) -> Dict[str, int]:
        """Extract token usage from Anthropic response"""
        if not hasattr(response, 'usage') or not response.usage:
            return {}

        usage = response.usage

        prompt_tokens = usage.input_tokens or 0
        completion_tokens = usage.output_tokens or 0

        cache_creation = getattr(usage, 'cache_creation_input_tokens', 0) or 0
        cache_read = getattr(usage, 'cache_read_input_tokens', 0) or 0

        return {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens,
            'cached_tokens': cache_creation + cache_read,
            'metadata': {
                'cache_creation_input_tokens': cache_creation,
                'cache_read_input_tokens': cache_read
            }
        }

    def __getattr__(self, name: str) -> Any:
        """Proxy all other attributes to the underlying client"""
        return getattr(self._client, name)


# Export with same names as official SDK
Anthropic = AnthropicWrapper
AsyncAnthropic = AsyncAnthropicWrapper
