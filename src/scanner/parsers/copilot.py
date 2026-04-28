"""
GitHub Copilot parser
Supports: Copilot (Codex-based), Copilot Chat
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('github')
class CopilotParser(BaseParser):
    """Parser for GitHub Copilot logs"""

    def __init__(self):
        super().__init__()
        self.service_name = 'github'
        self.supported_models = [
            'copilot-codex',
            'gpt-4-copilot',
            'gpt-3.5-turbo-copilot'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Copilot log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    # Look for completion or chat events
                    if 'completion' not in line.lower() and 'chat' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', '')
                                ) or datetime.utcnow(),
                                service='github',
                                tool='copilot',
                                model=data.get('model', 'copilot-codex'),
                                interface='ide',
                                session_id=data.get('sessionId'),
                                request_duration_ms=data.get('duration'),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Copilot log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Copilot log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Copilot telemetry

        Note: Copilot doesn't expose token counts directly
        We estimate based on prompt and completion lengths
        """
        # Check if usage is explicitly provided
        usage = data.get('usage')
        if usage:
            return {
                'prompt_tokens': usage.get('prompt_tokens', 0),
                'completion_tokens': usage.get('completion_tokens', 0),
                'total_tokens': usage.get('total_tokens', 0)
            }

        # Estimate from text if available
        prompt = data.get('prompt', '')
        completion = data.get('completion', '')

        if not prompt and not completion:
            return None

        prompt_tokens = self.estimate_tokens(prompt)
        completion_tokens = self.estimate_tokens(completion)

        return {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens
        }
