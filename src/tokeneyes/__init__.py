"""
Tokeneyes - AI Token Usage Tracker

Track AI coding assistant usage across CLI tools, IDEs, and APIs.
Privacy-first: only metadata, never prompts/responses.
"""

__version__ = '0.1.0'
__author__ = 'Tokeneyes Team'

from .daemon import TokenScannerDaemon
from .config import Config
from .parsers import ParserRegistry, TokenEvent


def auto_track():
    """
    Enable automatic SDK tracking via import hooks.

    Call this at the start of your application to automatically track
    all OpenAI/Anthropic API calls without changing imports.

    Usage:
        import tokeneyes
        tokeneyes.auto_track()

        # Now these imports are automatically wrapped:
        from openai import OpenAI
        from anthropic import Anthropic

    This must be called BEFORE importing the SDKs.
    """
    from .sdk.autopatch import install_import_hooks
    install_import_hooks()


__all__ = [
    'TokenScannerDaemon',
    'Config',
    'ParserRegistry',
    'TokenEvent',
    'auto_track',
]
