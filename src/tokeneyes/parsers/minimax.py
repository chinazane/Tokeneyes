"""
MiniMax parser
Supports: abab6.5, abab6.5s, MiniMax-Text-01
Popular in Chinese market
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('minimax')
class MiniMaxParser(BaseParser):
    """Parser for MiniMax API logs"""

    def __init__(self):
        super().__init__()
        self.service_name = 'minimax'
        self.supported_models = [
            'abab6.5-chat',
            'abab6.5s-chat',
            'abab5.5-chat',
            'minimax-text-01'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse MiniMax log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    # MiniMax uses "tokens" in various fields
                    if 'token' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('created', ''))
                                ) or datetime.utcnow(),
                                service='minimax',
                                tool='minimax-api',
                                model=data.get('model', 'abab6.5-chat'),
                                interface='api',
                                session_id=data.get('id', data.get('reply_id')),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing MiniMax log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading MiniMax log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from MiniMax response

        MiniMax usage format:
        {
          "usage": {
            "total_tokens": 300
          }
        }
        Or:
        {
          "base_resp": {
            "status_code": 0
          },
          "reply": "...",
          "input_sensitive": false,
          "output_sensitive": false,
          "choices": [{
            "messages": [...],
            "finish_reason": "stop"
          }],
          "usage": {
            "total_tokens": 100
          }
        }
        """
        usage = data.get('usage')

        if not usage:
            return None

        # MiniMax typically only provides total_tokens
        # We estimate the split
        total_tokens = usage.get('total_tokens', 0)

        # Try to get input_tokens and output_tokens if available
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)

        if input_tokens == 0 and output_tokens == 0 and total_tokens > 0:
            # Estimate: assume 1/3 prompt, 2/3 completion (typical for chat)
            input_tokens = total_tokens // 3
            output_tokens = total_tokens - input_tokens

        return {
            'prompt_tokens': input_tokens,
            'completion_tokens': output_tokens,
            'total_tokens': total_tokens
        }
