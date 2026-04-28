"""
DeepSeek parser
Supports: DeepSeek-V2 (236B MoE), DeepSeek-Coder-V2, DeepSeek-Chat
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('deepseek')
class DeepSeekParser(BaseParser):
    """Parser for DeepSeek API and CLI logs"""

    def __init__(self):
        super().__init__()
        self.service_name = 'deepseek'
        self.supported_models = [
            'deepseek-chat',
            'deepseek-coder',
            'deepseek-v2',
            'deepseek-v2-chat',
            'deepseek-v2-coder'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse DeepSeek log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    # DeepSeek uses OpenAI-compatible format
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
                                service='deepseek',
                                tool=self._determine_tool(data),
                                model=self._extract_model(data),
                                interface=self._determine_interface(data),
                                session_id=data.get('id'),
                                request_duration_ms=data.get('duration_ms'),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing DeepSeek log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading DeepSeek log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from DeepSeek response

        DeepSeek uses OpenAI-compatible format:
        {
          "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300,
            "prompt_cache_hit_tokens": 50,
            "prompt_cache_miss_tokens": 50
          }
        }
        """
        usage = data.get('usage')

        if not usage:
            # Try nested in response
            usage = data.get('response', {}).get('usage')

        if not usage:
            return None

        # DeepSeek-specific: cache hit/miss tokens
        cache_hit = usage.get('prompt_cache_hit_tokens', 0)
        cache_miss = usage.get('prompt_cache_miss_tokens', 0)

        return {
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0),
            'cache_read_tokens': cache_hit,
            'cache_creation_tokens': cache_miss
        }

    def _extract_model(self, data: dict) -> str:
        """Extract model name"""
        model = data.get('model', '')

        # DeepSeek API returns full model names
        # e.g., "deepseek-chat" or "deepseek-coder"
        if model:
            return model

        # Fallback
        return 'deepseek-chat'

    def _determine_tool(self, data: dict) -> str:
        """Determine which DeepSeek tool was used"""
        source = data.get('source', '')

        if 'api' in source:
            return 'deepseek-api'
        elif 'cli' in source:
            return 'deepseek-cli'
        elif 'web' in source:
            return 'deepseek-web'
        else:
            return 'deepseek-api'  # Default

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'cli' in tool:
            return 'cli'
        elif 'web' in tool:
            return 'web'
        else:
            return 'api'
