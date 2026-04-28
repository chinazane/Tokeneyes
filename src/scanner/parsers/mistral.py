"""
Mistral AI parser
Supports: Mistral Large, Mistral Medium, Mixtral 8x22B, Mixtral 8x7B
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('mistral')
class MistralParser(BaseParser):
    """Parser for Mistral AI (API and Le Chat)"""

    def __init__(self):
        super().__init__()
        self.service_name = 'mistral'
        self.supported_models = [
            'mistral-large-latest',
            'mistral-large-2402',
            'mistral-medium-latest',
            'mixtral-8x22b',
            'mixtral-8x22b-instruct',
            'mixtral-8x7b',
            'mixtral-8x7b-instruct',
            'mistral-small-latest',
            'mistral-tiny'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Mistral log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    if '"usage"' not in line:
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('created', ''))
                                ) or datetime.utcnow(),
                                service='mistral',
                                tool=self._determine_tool(data),
                                model=data.get('model', 'unknown'),
                                interface=self._determine_interface(data),
                                session_id=data.get('id'),
                                request_duration_ms=data.get('duration_ms'),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Mistral log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Mistral log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Mistral response

        Mistral usage format (OpenAI-compatible):
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
            # Try nested in response
            usage = data.get('response', {}).get('usage')

        if not usage:
            return None

        return {
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0)
        }

    def _determine_tool(self, data: dict) -> str:
        """Determine which Mistral tool was used"""
        source = data.get('source', '')

        if 'le-chat' in source or 'chat.mistral.ai' in source:
            return 'le-chat'
        elif 'api.mistral.ai' in source or data.get('api_version'):
            return 'mistral-api'
        else:
            return 'mistral-api'  # Default

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'chat' in tool:
            return 'web'
        else:
            return 'api'
