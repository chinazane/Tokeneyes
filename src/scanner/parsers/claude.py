"""
Anthropic Claude parser
Supports: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku
Based on pew.md's proven approach
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('anthropic')
class ClaudeParser(BaseParser):
    """
    Parser for Anthropic Claude logs
    Supports Claude Code CLI, Claude.ai web, and API usage
    """

    def __init__(self):
        super().__init__()
        self.service_name = 'anthropic'
        self.supported_models = [
            'claude-3-5-sonnet-20241022',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307',
            'claude-2.1',
            'claude-2.0'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """
        Parse Claude Code JSONL logs
        Based on pew's parseClaudeFile implementation
        """
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Seek to last read position
                f.seek(start_offset)

                for line in f:
                    # Fast-path: skip lines without usage
                    # (Performance optimization from pew)
                    if '"usage"' not in line:
                        continue

                    try:
                        data = json.loads(line)

                        # Extract usage
                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', '')
                                ) or datetime.utcnow(),
                                service='anthropic',
                                tool=self._determine_tool(data),
                                model=data.get('message', {}).get('model') or data.get('model', 'unknown'),
                                interface=self._determine_interface(data),
                                session_id=data.get('conversation_id', data.get('id')),
                                request_duration_ms=data.get('duration_ms'),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Claude log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Claude log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Claude log entry

        Claude usage format:
        {
          "usage": {
            "input_tokens": 100,
            "output_tokens": 200,
            "cache_creation_input_tokens": 50,
            "cache_read_input_tokens": 30
          }
        }
        """
        # Try message.usage first (Claude Code format)
        usage = data.get('message', {}).get('usage')

        # Fallback to top-level usage (API format)
        if not usage:
            usage = data.get('usage')

        if not usage:
            return None

        # Normalize to standard format
        input_tokens = usage.get('input_tokens', 0)
        cache_creation = usage.get('cache_creation_input_tokens', 0)
        cache_read = usage.get('cache_read_input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)

        return {
            'prompt_tokens': input_tokens + cache_creation,
            'completion_tokens': output_tokens,
            'total_tokens': input_tokens + cache_creation + output_tokens,
            'cache_read_tokens': cache_read,
            'cache_creation_tokens': cache_creation
        }

    def _determine_tool(self, data: dict) -> str:
        """Determine which Claude tool was used"""
        # Check for source markers
        source = data.get('source', '')

        if 'claude-code' in source or data.get('cli_version'):
            return 'claude-code'
        elif 'claude.ai' in source or data.get('web_version'):
            return 'claude-web'
        elif data.get('api_version'):
            return 'claude-api'
        else:
            # Default based on file path context
            return 'claude-code'  # Most common

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'code' in tool:
            return 'cli'
        elif 'web' in tool:
            return 'web'
        else:
            return 'api'
