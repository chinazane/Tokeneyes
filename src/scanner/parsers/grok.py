"""
xAI Grok parser
Supports: Grok-1.5, Grok-2
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('xai')
class GrokParser(BaseParser):
    """Parser for xAI Grok (primarily web-based via X.com)"""

    def __init__(self):
        super().__init__()
        self.service_name = 'xai'
        self.supported_models = [
            'grok-2',
            'grok-1.5',
            'grok-1'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Grok log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    if '"usage"' not in line and 'token' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('created_at', ''))
                                ) or datetime.utcnow(),
                                service='xai',
                                tool=self._determine_tool(data),
                                model=data.get('model', 'grok-2'),
                                interface=self._determine_interface(data),
                                session_id=data.get('conversation_id', data.get('id')),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Grok log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Grok log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Grok response

        xAI API format (OpenAI-compatible):
        {
          "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300
          }
        }
        """
        usage = data.get('usage')

        if not usage:
            # Try nested
            usage = data.get('response', {}).get('usage')

        if not usage:
            return None

        return {
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0)
        }

    def _determine_tool(self, data: dict) -> str:
        """Determine which Grok interface was used"""
        source = data.get('source', '')

        if 'x.com' in source or 'twitter.com' in source:
            return 'grok-web'
        elif 'api.x.ai' in source:
            return 'grok-api'
        else:
            return 'grok-web'  # Default (most common)

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'web' in tool:
            return 'web'
        else:
            return 'api'
