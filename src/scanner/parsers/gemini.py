"""
Google Gemini parser
Supports: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash
"""

from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

from .base import BaseParser, TokenEvent, ParserRegistry


@ParserRegistry.register('google')
class GeminiParser(BaseParser):
    """Parser for Google Gemini (AI Studio, Vertex AI)"""

    def __init__(self):
        super().__init__()
        self.service_name = 'google'
        self.supported_models = [
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-2.0-flash-exp',
            'gemini-ultra',
            'gemini-pro'
        ]

    async def parse(self, file_path: Path, start_offset: int = 0) -> List[TokenEvent]:
        """Parse Gemini log file"""
        events = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(start_offset)

                for line in f:
                    if not line.strip():
                        continue

                    # Look for token-related lines
                    if 'token' not in line.lower():
                        continue

                    try:
                        data = json.loads(line)

                        usage = self.extract_usage(data)

                        if usage:
                            event = TokenEvent(
                                timestamp=self.parse_timestamp(
                                    data.get('timestamp', data.get('createTime', ''))
                                ) or datetime.utcnow(),
                                service='google',
                                tool=self._determine_tool(data),
                                model=self._extract_model(data),
                                interface=self._determine_interface(data),
                                session_id=data.get('id', data.get('name')),
                                request_duration_ms=data.get('latencyMs'),
                                **usage
                            )
                            events.append(event)

                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        print(f"Error parsing Gemini log line: {e}")
                        continue

        except Exception as e:
            print(f"Error reading Gemini log file {file_path}: {e}")

        return events

    def extract_usage(self, data: dict) -> Optional[dict]:
        """
        Extract usage from Gemini response

        Gemini usage format:
        {
          "usageMetadata": {
            "promptTokenCount": 100,
            "candidatesTokenCount": 200,
            "totalTokenCount": 300
          }
        }

        Or Vertex AI format:
        {
          "metadata": {
            "tokenMetadata": {
              "inputTokenCount": 100,
              "outputTokenCount": 200
            }
          }
        }
        """
        # Try usageMetadata (Gemini API format)
        usage_metadata = data.get('usageMetadata')

        if usage_metadata:
            return {
                'prompt_tokens': usage_metadata.get('promptTokenCount', 0),
                'completion_tokens': usage_metadata.get('candidatesTokenCount', 0),
                'total_tokens': usage_metadata.get('totalTokenCount', 0),
                'cache_read_tokens': usage_metadata.get('cachedContentTokenCount', 0)
            }

        # Try Vertex AI format
        metadata = data.get('metadata', {})
        token_metadata = metadata.get('tokenMetadata')

        if token_metadata:
            input_tokens = token_metadata.get('inputTokenCount', 0)
            output_tokens = token_metadata.get('outputTokenCount', 0)

            return {
                'prompt_tokens': input_tokens,
                'completion_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens
            }

        return None

    def _extract_model(self, data: dict) -> str:
        """Extract model name from various fields"""
        # Try direct model field
        model = data.get('model')

        if model:
            # Extract just the model name from full path
            # e.g., "models/gemini-1.5-pro" -> "gemini-1.5-pro"
            if '/' in model:
                return model.split('/')[-1]
            return model

        # Try modelVersion
        model_version = data.get('modelVersion')
        if model_version:
            return model_version

        return 'unknown'

    def _determine_tool(self, data: dict) -> str:
        """Determine which Gemini tool was used"""
        if data.get('source') == 'ai-studio':
            return 'gemini-studio'
        elif data.get('source') == 'vertex-ai':
            return 'vertex-ai'
        elif 'generativelanguage.googleapis.com' in data.get('endpoint', ''):
            return 'gemini-api'
        else:
            return 'gemini-api'

    def _determine_interface(self, data: dict) -> str:
        """Determine interface type"""
        tool = self._determine_tool(data)

        if 'studio' in tool:
            return 'web'
        else:
            return 'api'
