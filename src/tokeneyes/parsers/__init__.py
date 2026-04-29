"""
Parser module for all AI model providers
Auto-imports all registered parsers
"""

from .base import BaseParser, TokenEvent, ParserRegistry

# Phase 1: Core providers (P0)
from .openai import OpenAIParser
from .claude import ClaudeParser
from .gemini import GeminiParser
from .copilot import CopilotParser

# Phase 2: Major providers (P1)
from .deepseek import DeepSeekParser
from .llama import LlamaParser
from .mistral import MistralParser

# Phase 3: Additional providers (P2)
from .minimax import MiniMaxParser
from .grok import GrokParser
from .cohere import CohereParser

# All parsers are auto-registered via @ParserRegistry.register() decorator

__all__ = [
    'BaseParser',
    'TokenEvent',
    'ParserRegistry',
    # Phase 1
    'OpenAIParser',
    'ClaudeParser',
    'GeminiParser',
    'CopilotParser',
    # Phase 2
    'DeepSeekParser',
    'LlamaParser',
    'MistralParser',
    # Phase 3
    'MiniMaxParser',
    'GrokParser',
    'CohereParser'
]


def get_parser(service: str) -> BaseParser:
    """Convenience function to get a parser"""
    return ParserRegistry.get_parser(service)


def list_supported_services() -> list:
    """List all supported AI services"""
    return ParserRegistry.list_services()
