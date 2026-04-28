"""
OpenAI parser for ChatGPT and GPT API usage
Supports: GPT-4, GPT-4 Turbo, GPT-3.5, o1, o1-mini
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('openai')
class OpenAIParser(BaseParser):
    """Parser for OpenAI (ChatGPT, GPT API) logs"""

    def __init__(self):
        super().__init__()
        self.service_name = 'openai'
        self.supported_models = [
            'gpt-4-turbo',
            'gpt-4',
            'gpt-4-32k',
            'gpt-4o',
            'gpt-3.5-turbo',
            'o1-preview',
            'o1-mini'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """
        Parse OpenAI log file

        Supports multiple log formats:
        1. API response logs (JSON)
        2. CLI logs (structured)
        3. SDK wrapper logs (custom format)
        """
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Seek to last read position
                f.seek(start_offset)

                for line in f:
                    # Skip empty lines
                    if not line.strip():
                        continue

                    # Fast-path: skip lines without usage
                    if '"usage"' not in line and 'tokens' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        # Extract usage
                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('created_at', ''))
                                ) or datetime.utcnow(),
                                service='openai',
                                tool=self._determine_tool(data),
                                model=data.get('model', 'unknown'),
                                interface=self._determine_interface(data),
                                session_id=data.get('id', data.get('conversation_id')),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        # Not JSON, might be plain text log
                        continue
                    except Exception as e:
                        # Log error but continue processing
                        print(f"Error parsing OpenAI log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading OpenAI log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from OpenAI response

        OpenAI usage format:
        {
          "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300
          }
        }
        """
        # Try direct usage field
        usage = data.get('usage')

        # Try nested in response
        if not usage and 'response' in data:
            usage = data['response'].get('usage')

        # Try nested in choices (streaming format)
        if not usage and 'choices' in data:
            for choice in data['choices']:
                if 'message' in choice:
                    usage = choice.get('usage')
                    if usage:
                        break

        if not usage:
            return None

        return {
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0),
            # o1 models have reasoning tokens
            'cache_read_tokens': usage.get('cached_tokens', 0),
            'request_duration_ms': data.get('duration_ms')
        }

    def _determine_tool(self, data: dict) -> str:
        """Determine which OpenAI tool was used"""
        # Check for specific markers
        if data.get('source') == 'chatgpt-web':
            return 'chatgpt-web'
        elif data.get('source') == 'api':
            return 'openai-api'
        elif 'user_agent' in data and 'curl' in data['user_agent'].lower():
            return 'openai-cli'
        else:
            return 'openai-api'  # Default to API

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'web' in tool:
            return 'web'
        elif 'cli' in tool:
            return 'cli'
        else:
            return 'api'
