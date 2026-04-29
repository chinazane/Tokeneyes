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

__all__ = [
    'TokenScannerDaemon',
    'Config',
    'ParserRegistry',
    'TokenEvent',
]
