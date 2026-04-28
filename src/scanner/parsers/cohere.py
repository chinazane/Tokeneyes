"""
Cohere parser
Supports: Command R+, Command R, Command
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('cohere')
class CohereParser(BaseParser):
    """Parser for Cohere API and Coral web interface"""

    def __init__(self):
        super().__init__()
        self.service_name = 'cohere'
        self.supported_models = [
            'command-r-plus',
            'command-r',
            'command',
            'command-light'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Cohere log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    if 'token' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', '')
                                ) or datetime.utcnow(),
                                service='cohere',
                                tool=self._determine_tool(data),
                                model=data.get('model', 'command-r-plus'),
                                interface=self._determine_interface(data),
                                session_id=data.get('id', data.get('generation_id')),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Cohere log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Cohere log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Cohere response

        Cohere usage format:
        {
          "meta": {
            "tokens": {
              "input_tokens": 100,
              "output_tokens": 200
            }
          }
        }
        Or API v2 format:
        {
          "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300
          }
        }
        """
        # Try API v2 format (OpenAI-compatible)
        usage = data.get('usage')

        if usage:
            return {
                'prompt_tokens': usage.get('prompt_tokens', 0),
                'completion_tokens': usage.get('completion_tokens', 0),
                'total_tokens': usage.get('total_tokens', 0)
            }

        # Try Cohere native format
        meta = data.get('meta', {})
        tokens = meta.get('tokens', {})

        if tokens:
            input_tokens = tokens.get('input_tokens', 0)
            output_tokens = tokens.get('output_tokens', 0)

            return {
                'prompt_tokens': input_tokens,
                'completion_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens
            }

        return None

    def _determine_tool(self, data: dict) -> str:
        """Determine which Cohere tool was used"""
        source = data.get('source', '')

        if 'coral' in source or 'coral.cohere.com' in source:
            return 'coral-web'
        elif 'api.cohere' in source:
            return 'cohere-api'
        else:
            return 'cohere-api'  # Default

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'web' in tool:
            return 'web'
        else:
            return 'api'
