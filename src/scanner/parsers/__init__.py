"""
Parser module for all AI model providers
Auto-imports all registered parsers
"""

from .base import BaseParser, TokenEvent, ParserRegistry
from .openai import OpenAIParser
from .claude import ClaudeParser
from .gemini import GeminiParser
from .copilot import CopilotParser

# All parsers are auto-registered via @ParserRegistry.register() decorator

__all__ = [
    'BaseParser',
    'TokenEvent',
    'ParserRegistry',
    'OpenAIParser',
    'ClaudeParser',
    'GeminiParser',
    'CopilotParser'
]


def get_parser(service: str) -> BaseParser:
    """Convenience function to get a parser"""
    return ParserRegistry.get_parser(service)


def list_supported_services() -> list:
    """List all supported AI services"""
    return ParserRegistry.list_services()
