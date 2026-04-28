"""
Meta Llama parser (via Ollama and hosted providers)
Supports: Llama 3.1 (405B/70B/8B), Code Llama
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('meta')
class LlamaParser(BaseParser):
    """
    Parser for Meta Llama models
    Supports Ollama (local) and hosted providers (Together AI, Replicate, etc.)
    """

    def __init__(self):
        super().__init__()
        self.service_name = 'meta'
        self.supported_models = [
            'llama-3.1-405b',
            'llama-3.1-70b',
            'llama-3.1-8b',
            'llama-3-70b',
            'llama-3-8b',
            'codellama-70b',
            'codellama-34b',
            'codellama-13b'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Llama/Ollama log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    # Look for generation or API call logs
                    if 'generate' not in line.lower() and 'tokens' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('created_at', ''))
                                ) or datetime.utcnow(),
                                service='meta',
                                tool=self._determine_tool(data),
                                model=self._normalize_model(data.get('model', 'unknown')),
                                interface=self._determine_interface(data),
                                session_id=data.get('id', data.get('request_id')),
                                request_duration_ms=data.get('total_duration', 0) // 1_000_000,  # ns to ms
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Llama log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Llama log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Llama/Ollama response

        Ollama format:
        {
          "prompt_eval_count": 100,
          "eval_count": 200,
          "total_duration": 5000000000
        }

        Hosted provider format (OpenAI-compatible):
        {
          "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 200,
            "total_tokens": 300
          }
        }
        """
        # Try OpenAI-compatible format (hosted providers)
        usage = data.get('usage')

        if usage:
            return {
                'prompt_tokens': usage.get('prompt_tokens', 0),
                'completion_tokens': usage.get('completion_tokens', 0),
                'total_tokens': usage.get('total_tokens', 0)
            }

        # Try Ollama format
        prompt_eval_count = data.get('prompt_eval_count')
        eval_count = data.get('eval_count')

        if prompt_eval_count is not None or eval_count is not None:
            prompt_tokens = prompt_eval_count or 0
            completion_tokens = eval_count or 0

            return {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens
            }

        # Try estimating from text if available
        prompt = data.get('prompt', '')
        response = data.get('response', '')

        if prompt or response:
            prompt_tokens = self.estimate_tokens(prompt)
            completion_tokens = self.estimate_tokens(response)

            return {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': prompt_tokens + completion_tokens
            }

        return None

    def _normalize_model(self, model: str) -> str:
        """
        Normalize Llama model names

        Examples:
        - "meta-llama/Llama-3.1-405B-Instruct" -> "llama-3.1-405b"
        - "llama3.1:70b" -> "llama-3.1-70b"
        - "codellama:13b" -> "codellama-13b"
        """
        model_lower = model.lower()

        # Remove provider prefixes
        model_lower = model_lower.split('/')[-1]

        # Normalize separators
        model_lower = model_lower.replace('_', '-').replace(':', '-')

        # Remove common suffixes
        for suffix in ['-instruct', '-chat', '-text']:
            if model_lower.endswith(suffix):
                model_lower = model_lower[:-len(suffix)]

        return model_lower

    def _determine_tool(self, data: dict) -> str:
        """Determine which tool was used"""
        # Check for Ollama-specific fields
        if 'prompt_eval_count' in data or 'eval_count' in data:
            return 'ollama'

        # Check for hosted provider markers
        if 'together' in data.get('provider', '').lower():
            return 'together-ai'
        elif 'replicate' in data.get('provider', '').lower():
            return 'replicate'
        elif 'huggingface' in data.get('provider', '').lower():
            return 'huggingface'
        elif 'fireworks' in data.get('provider', '').lower():
            return 'fireworks'
        else:
            return 'llama-api'

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if tool == 'ollama':
            return 'cli'
        else:
            return 'api'
