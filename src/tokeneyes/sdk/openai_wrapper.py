"""
OpenAI SDK Wrapper

Drop-in replacement for OpenAI Python SDK with automatic token tracking.

Usage:
    # Instead of:
    from openai import OpenAI

    # Use:
    from tokeneyes.sdk import OpenAI

    # Everything else stays the same!
    client = OpenAI(api_key="...")
    response = client.chat.completions.create(...)
"""

from typing import Any, Dict, Optional
from pathlib import Path

try:
    from openai import OpenAI as _OpenAI
    from openai import AsyncOpenAI as _AsyncOpenAI
    from openai.types.chat import ChatCompletion
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    _OpenAI = None
    _AsyncOpenAI = None
    ChatCompletion = None

from .base import BaseSDKWrapper


class OpenAIWrapper(BaseSDKWrapper):
    """OpenAI SDK wrapper with token tracking"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        track_tokens: bool = True,
        state_dir: Path = None,
        **kwargs
    ):
        """
        Initialize OpenAI client with token tracking

        Args:
            api_key: OpenAI API key
            track_tokens: Enable token tracking (default: True)
            state_dir: Directory for event storage
            **kwargs: Additional arguments passed to OpenAI client
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI SDK not installed. Install with: pip install openai"
            )

        super().__init__(track_tokens=track_tokens, state_dir=state_dir)

        # Create underlying OpenAI client
        self._client = _OpenAI(api_key=api_key, **kwargs)

        # Wrap the chat.completions.create method
        self._original_chat_create = self._client.chat.completions.create
        self._client.chat.completions.create = self._wrapped_chat_create

    def _wrapped_chat_create(self, *args, **kwargs) -> ChatCompletion:
        """
        Wrapped version of chat.completions.create that tracks tokens

        Args:
            *args: Positional arguments for the API call
            **kwargs: Keyword arguments for the API call

        Returns:
            ChatCompletion response
        """
        # Call the original method
        response = self._original_chat_create(*args, **kwargs)

        # Track token usage
        if self.track_tokens and response:
            model = kwargs.get('model') or (args[0] if args else 'unknown')
            self._track_response(response, service='openai', model=model)

        return response

    def _extract_usage(self, response: ChatCompletion) -> Dict[str, int]:
        """
        Extract token usage from OpenAI response

        Args:
            response: ChatCompletion response object

        Returns:
            Dictionary with token counts
        """
        if not hasattr(response, 'usage') or not response.usage:
            return {}

        usage = response.usage

        return {
            'prompt_tokens': usage.prompt_tokens or 0,
            'completion_tokens': usage.completion_tokens or 0,
            'total_tokens': usage.total_tokens or 0,
            'cached_tokens': getattr(usage, 'cached_tokens', 0) or 0
        }

    def __getattr__(self, name: str) -> Any:
        """
        Proxy all other attributes to the underlying OpenAI client

        Args:
            name: Attribute name

        Returns:
            Attribute from underlying client
        """
        return getattr(self._client, name)


class AsyncOpenAIWrapper(BaseSDKWrapper):
    """Async OpenAI SDK wrapper with token tracking"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        track_tokens: bool = True,
        state_dir: Path = None,
        **kwargs
    ):
        """
        Initialize async OpenAI client with token tracking

        Args:
            api_key: OpenAI API key
            track_tokens: Enable token tracking (default: True)
            state_dir: Directory for event storage
            **kwargs: Additional arguments passed to AsyncOpenAI client
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI SDK not installed. Install with: pip install openai"
            )

        super().__init__(track_tokens=track_tokens, state_dir=state_dir)

        # Create underlying AsyncOpenAI client
        self._client = _AsyncOpenAI(api_key=api_key, **kwargs)

        # Wrap the chat.completions.create method
        self._original_chat_create = self._client.chat.completions.create
        self._client.chat.completions.create = self._wrapped_chat_create

    async def _wrapped_chat_create(self, *args, **kwargs) -> ChatCompletion:
        """
        Wrapped async version of chat.completions.create

        Args:
            *args: Positional arguments for the API call
            **kwargs: Keyword arguments for the API call

        Returns:
            ChatCompletion response
        """
        # Call the original method
        response = await self._original_chat_create(*args, **kwargs)

        # Track token usage
        if self.track_tokens and response:
            model = kwargs.get('model') or (args[0] if args else 'unknown')
            self._track_response(response, service='openai', model=model)

        return response

    def _extract_usage(self, response: ChatCompletion) -> Dict[str, int]:
        """Extract token usage from OpenAI response"""
        if not hasattr(response, 'usage') or not response.usage:
            return {}

        usage = response.usage

        return {
            'prompt_tokens': usage.prompt_tokens or 0,
            'completion_tokens': usage.completion_tokens or 0,
            'total_tokens': usage.total_tokens or 0,
            'cached_tokens': getattr(usage, 'cached_tokens', 0) or 0
        }

    def __getattr__(self, name: str) -> Any:
        """Proxy all other attributes to the underlying client"""
        return getattr(self._client, name)


# Export with same names as official SDK
OpenAI = OpenAIWrapper
AsyncOpenAI = AsyncOpenAIWrapper
