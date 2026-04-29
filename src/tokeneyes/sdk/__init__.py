"""
Tokeneyes SDK Wrappers

Drop-in replacements for popular AI SDKs with automatic token tracking.

Usage:
    # OpenAI
    from tokeneyes.sdk import OpenAI, AsyncOpenAI
    client = OpenAI(api_key="...")
    response = client.chat.completions.create(...)

    # Anthropic
    from tokeneyes.sdk import Anthropic, AsyncAnthropic
    client = Anthropic(api_key="...")
    response = client.messages.create(...)

All API calls are tracked automatically and saved to ~/.aitracker/sdk_events.jsonl

To disable tracking for a specific client:
    client = OpenAI(api_key="...", track_tokens=False)
"""

from .base import BaseSDKWrapper, TokenTracker

# Import wrappers (will fail gracefully if SDKs not installed)
try:
    from .openai_wrapper import OpenAI, AsyncOpenAI
except ImportError:
    OpenAI = None
    AsyncOpenAI = None

try:
    from .anthropic_wrapper import Anthropic, AsyncAnthropic
except ImportError:
    Anthropic = None
    AsyncAnthropic = None


__all__ = [
    'BaseSDKWrapper',
    'TokenTracker',
    'OpenAI',
    'AsyncOpenAI',
    'Anthropic',
    'AsyncAnthropic',
]
