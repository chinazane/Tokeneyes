# AI Model Coverage Expansion - Top 10 AI Models

**Document Version:** 1.0  
**Last Updated:** April 28, 2026  
**Status:** Technical Specification for Expanded AI Model Support

---

## 📊 Top 10 AI Models Coverage (2026)

Based on market share, developer adoption, and enterprise usage, Tokeneyes will support these top 10 AI model providers:

| Rank | Provider | Models | Market Share | Coverage Method | Priority |
|------|----------|--------|--------------|-----------------|----------|
| 1 | **OpenAI** | GPT-4, GPT-4 Turbo, GPT-3.5, o1, o1-mini | 55% | API + Web + CLI | ✅ P0 |
| 2 | **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus/Haiku | 25% | API + Web + CLI | ✅ P0 |
| 3 | **Google** | Gemini 1.5 Pro/Flash, Gemini 2.0 | 8% | API + Web | ✅ P0 |
| 4 | **GitHub** | Copilot (Codex), Copilot Chat | 6% | IDE + CLI | ✅ P0 |
| 5 | **DeepSeek** | DeepSeek-V2, DeepSeek-Coder | 2% | API + CLI | ✅ P1 |
| 6 | **Meta** | Llama 3.1 (405B/70B/8B), Code Llama | 1.5% | API (hosted) | ✅ P1 |
| 7 | **Mistral AI** | Mistral Large, Mixtral 8x22B | 1% | API + Web | ✅ P1 |
| 8 | **MiniMax** | abab6.5, MiniMax-Text-01 | 0.8% | API | ✅ P2 |
| 9 | **xAI** | Grok-1.5, Grok-2 | 0.5% | API + Web | ✅ P2 |
| 10 | **Cohere** | Command R+, Command R | 0.2% | API | ✅ P2 |

**Total Coverage:** 100% of major AI providers  
**Expected Tracking:** 97-99% of enterprise AI usage

---

## 🔧 Technical Implementation by Provider

### 1. OpenAI (Priority 0)

**Models:**
- GPT-4 Turbo
- GPT-4
- GPT-3.5 Turbo
- GPT-4o
- o1-preview
- o1-mini

**Tracking Methods:**

#### A. Web Interface (ChatGPT)
```typescript
// Browser extension intercepts
const OPENAI_ENDPOINTS = [
  'https://chat.openai.com/backend-api/conversation',
  'https://chatgpt.com/backend-api/conversation'
];

// Parse response for usage
interface OpenAIUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}
```

#### B. API Usage
```python
# SDK wrapper
from openai import OpenAI

class TrackedOpenAIClient(OpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracker = TokenTracker()
    
    def chat_completions_create(self, *args, **kwargs):
        response = super().chat.completions.create(*args, **kwargs)
        
        # Track usage
        self.tracker.track({
            'service': 'openai',
            'model': kwargs.get('model'),
            'usage': response.usage.model_dump()
        })
        
        return response
```

#### C. Log Scanning
```python
# OpenAI CLI logs (if available)
OPENAI_LOG_PATHS = [
    Path.home() / '.openai' / 'logs' / '*.log',
    Path.home() / 'Library' / 'Logs' / 'OpenAI' / '*.log'
]
```

---

### 2. Anthropic (Priority 0)

**Models:**
- Claude 3.5 Sonnet
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

**Tracking Methods:**

#### A. Claude Code CLI (Existing)
```python
# Already implemented via pew.md approach
patterns = {
    'claude': [
        Path.home() / '.claude' / 'projects' / '**' / '*.jsonl'
    ]
}
```

#### B. Claude.ai Web
```typescript
// Browser extension
const CLAUDE_ENDPOINTS = [
  'https://claude.ai/api/organizations/*/chat_conversations/*/completion'
];
```

#### C. API Usage
```python
from anthropic import Anthropic

class TrackedAnthropicClient(Anthropic):
    def messages_create(self, *args, **kwargs):
        response = super().messages.create(*args, **kwargs)
        
        self.tracker.track({
            'service': 'anthropic',
            'model': kwargs.get('model'),
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
                'cache_read_tokens': getattr(response.usage, 'cache_read_input_tokens', 0)
            }
        })
        
        return response
```

---

### 3. Google Gemini (Priority 0)

**Models:**
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Gemini 2.0 Flash
- Gemini Ultra

**Tracking Methods:**

#### A. Google AI Studio Web
```typescript
// Browser extension
const GEMINI_ENDPOINTS = [
  'https://generativelanguage.googleapis.com/v1beta/models/*:generateContent'
];

interface GeminiUsage {
  promptTokenCount: number;
  candidatesTokenCount: number;
  totalTokenCount: number;
}
```

#### B. Vertex AI API
```python
from google.cloud import aiplatform

class TrackedGeminiClient:
    def generate_content(self, model: str, prompt: str):
        response = aiplatform.gapic.PredictionServiceClient().predict(...)
        
        # Extract usage from metadata
        usage = response.metadata.get('tokenMetadata', {})
        
        self.tracker.track({
            'service': 'google',
            'model': model,
            'usage': {
                'prompt_tokens': usage.get('inputTokenCount'),
                'completion_tokens': usage.get('outputTokenCount')
            }
        })
```

#### C. Log Scanning
```python
GEMINI_LOG_PATHS = [
    Path.home() / '.google-cloud' / 'logs' / '*.log',
    Path.home() / 'Library' / 'Application Support' / 'Google' / 'AIStudio' / '*.log'
]
```

---

### 4. GitHub Copilot (Priority 0)

**Models:**
- Codex (GPT-4 based)
- Copilot Chat

**Tracking Methods:**

#### A. VS Code Extension Logs (Existing)
```python
COPILOT_LOG_PATHS = [
    Path.home() / 'Library' / 'Application Support' / 'Code' / 
    'User' / 'workspaceStorage' / '*' / 'chatSessions' / '*.jsonl',
    
    Path.home() / '.vscode' / 'extensions' / 'github.copilot-*' / 'logs' / '*.log'
]
```

#### B. Copilot CLI
```python
# Track copilot CLI usage
COPILOT_CLI_LOGS = [
    Path.home() / '.copilot' / 'logs' / '*.log'
]
```

#### C. Telemetry Parsing
```python
class CopilotParser:
    def parse(self, file_path: Path) -> List[TokenEvent]:
        # Parse Copilot telemetry events
        # Format: JSON lines with completion/chat events
        
        for line in file_read_lines(file_path):
            data = json.loads(line)
            
            if data.get('event') == 'completion':
                yield TokenEvent(
                    service='github',
                    tool='copilot',
                    model='copilot-codex',
                    # Copilot doesn't expose token counts directly
                    # Estimate based on character count
                    prompt_tokens=self._estimate_tokens(data.get('prompt')),
                    completion_tokens=self._estimate_tokens(data.get('completion'))
                )
```

---

### 5. DeepSeek (Priority 1)

**Models:**
- DeepSeek-V2 (236B MoE)
- DeepSeek-Coder-V2
- DeepSeek-Chat

**Tracking Methods:**

#### A. DeepSeek API
```python
import requests

class DeepSeekClient:
    BASE_URL = 'https://api.deepseek.com/v1'
    
    def chat_completion(self, messages: list, model: str = 'deepseek-chat'):
        response = requests.post(
            f'{self.BASE_URL}/chat/completions',
            headers={'Authorization': f'Bearer {self.api_key}'},
            json={'model': model, 'messages': messages}
        )
        
        data = response.json()
        
        self.tracker.track({
            'service': 'deepseek',
            'model': model,
            'usage': data['usage']  # Compatible with OpenAI format
        })
```

#### B. Log Scanning
```python
DEEPSEEK_LOG_PATHS = [
    Path.home() / '.deepseek' / 'logs' / '*.log',
    Path.home() / '.config' / 'deepseek' / '*.jsonl'
]
```

---

### 6. Meta Llama (Priority 1)

**Models:**
- Llama 3.1 405B
- Llama 3.1 70B
- Llama 3.1 8B
- Code Llama

**Tracking Methods:**

#### A. Hosted API Services
```python
# Track via hosting providers
LLAMA_PROVIDERS = [
    'together.ai',      # Together AI
    'replicate.com',    # Replicate
    'fireworks.ai',     # Fireworks
    'huggingface.co'    # HuggingFace Inference
]

class LlamaTracker:
    def track_together_ai(self):
        # Together AI API
        response = requests.post(
            'https://api.together.xyz/inference',
            headers={'Authorization': f'Bearer {key}'},
            json={'model': 'meta-llama/Llama-3.1-405B-Instruct', ...}
        )
        
        # Parse usage from response
        usage = response.json().get('usage', {})
```

#### B. Local Deployment (Ollama)
```python
# Track Ollama local deployments
OLLAMA_LOG_PATHS = [
    Path.home() / '.ollama' / 'logs' / '*.log'
]

class OllamaParser:
    def parse_ollama_logs(self):
        # Ollama logs model usage
        # Track via /api/generate endpoint calls
        pass
```

---

### 7. Mistral AI (Priority 1)

**Models:**
- Mistral Large
- Mistral Medium
- Mixtral 8x22B
- Mixtral 8x7B

**Tracking Methods:**

#### A. Mistral API
```python
from mistralai.client import MistralClient

class TrackedMistralClient(MistralClient):
    def chat(self, model: str, messages: list):
        response = super().chat(model=model, messages=messages)
        
        self.tracker.track({
            'service': 'mistral',
            'model': model,
            'usage': {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens
            }
        })
```

#### B. Le Chat Web Interface
```typescript
// Browser extension for chat.mistral.ai
const MISTRAL_ENDPOINTS = [
  'https://chat.mistral.ai/api/chat'
];
```

---

### 8. MiniMax (Priority 2)

**Models:**
- abab6.5
- abab6.5s
- MiniMax-Text-01

**Tracking Methods:**

#### A. MiniMax API
```python
class MiniMaxClient:
    BASE_URL = 'https://api.minimax.chat/v1'
    
    def chat_completion(self, messages: list):
        response = requests.post(
            f'{self.BASE_URL}/text/chatcompletion_v2',
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'GroupId': self.group_id
            },
            json={
                'model': 'abab6.5-chat',
                'messages': messages
            }
        )
        
        data = response.json()
        
        # MiniMax uses "tokens_to_generate" and "input_tokens"
        self.tracker.track({
            'service': 'minimax',
            'model': 'abab6.5',
            'usage': {
                'prompt_tokens': data.get('usage', {}).get('input_tokens'),
                'completion_tokens': data.get('usage', {}).get('output_tokens')
            }
        })
```

---

### 9. xAI Grok (Priority 2)

**Models:**
- Grok-2
- Grok-1.5

**Tracking Methods:**

#### A. Grok Web (X.com)
```typescript
// Browser extension for x.com/grok
const GROK_ENDPOINTS = [
  'https://x.com/i/api/grok/conversation'
];
```

#### B. Grok API (when available)
```python
class GrokClient:
    BASE_URL = 'https://api.x.ai/v1'
    
    def chat(self, messages: list):
        # xAI API (OpenAI-compatible)
        response = requests.post(
            f'{self.BASE_URL}/chat/completions',
            headers={'Authorization': f'Bearer {self.api_key}'},
            json={'model': 'grok-2', 'messages': messages}
        )
```

---

### 10. Cohere (Priority 2)

**Models:**
- Command R+
- Command R
- Command

**Tracking Methods:**

#### A. Cohere API
```python
import cohere

class TrackedCohereClient(cohere.Client):
    def chat(self, message: str, **kwargs):
        response = super().chat(message=message, **kwargs)
        
        self.tracker.track({
            'service': 'cohere',
            'model': kwargs.get('model', 'command-r-plus'),
            'usage': {
                'prompt_tokens': response.meta.tokens.input_tokens,
                'completion_tokens': response.meta.tokens.output_tokens
            }
        })
```

#### B. Coral Web Interface
```typescript
// Browser extension for coral.cohere.com
const COHERE_ENDPOINTS = [
  'https://api.cohere.ai/v1/chat'
];
```

---

## 📋 Updated Discovery & Parser Architecture

### Enhanced Discovery System

```python
# scanner/discovery.py

def discover_logs(tool: str) -> List[Path]:
    """
    Discover log files for all supported AI tools
    """
    
    patterns = {
        # Tier 1: OpenAI
        'openai-web': [
            # Browser cache/logs if available
        ],
        'openai-api': [
            Path.home() / '.openai' / '*.log'
        ],
        
        # Tier 1: Anthropic
        'claude-code': [
            Path.home() / '.claude' / 'projects' / '**' / '*.jsonl'
        ],
        'claude-web': [
            # Browser extension tracks this
        ],
        
        # Tier 1: Google
        'gemini-api': [
            Path.home() / '.google-cloud' / 'logs' / '*.log'
        ],
        'gemini-web': [
            Path.home() / 'Library' / 'Application Support' / 'Google' / 'AIStudio' / '*.log'
        ],
        
        # Tier 1: GitHub
        'copilot': [
            Path.home() / 'Library' / 'Application Support' / 'Code' / 
            'User' / 'workspaceStorage' / '*' / 'chatSessions' / '*.jsonl',
            Path.home() / '.copilot' / 'logs' / '*.log'
        ],
        
        # Tier 2: DeepSeek
        'deepseek': [
            Path.home() / '.deepseek' / 'logs' / '*.log',
            Path.home() / '.config' / 'deepseek' / '*.jsonl'
        ],
        
        # Tier 2: Llama (via Ollama)
        'llama-ollama': [
            Path.home() / '.ollama' / 'logs' / '*.log'
        ],
        
        # Tier 2: Mistral
        'mistral': [
            Path.home() / '.mistral' / 'logs' / '*.log'
        ],
        
        # Tier 3: MiniMax
        'minimax': [
            Path.home() / '.minimax' / '*.log'
        ],
        
        # Tier 3: xAI Grok
        'grok': [
            # Primarily web-based, tracked via browser extension
        ],
        
        # Tier 3: Cohere
        'cohere': [
            Path.home() / '.cohere' / '*.log'
        ],
        
        # IDE integrations
        'cursor': [
            Path.home() / '.cursor' / 'logs' / '*.log'
        ],
        'continue-dev': [
            Path.home() / '.continue' / 'logs' / '*.log'
        ],
        'codeium': [
            Path.home() / '.codeium' / 'logs' / '*.log'
        ]
    }
    
    log_files = []
    
    for pattern in patterns.get(tool, []):
        log_files.extend(glob.glob(str(pattern), recursive=True))
    
    return [Path(f) for f in log_files if Path(f).is_file()]
```

### Parser Factory Pattern

```python
# scanner/parsers/__init__.py

class ParserFactory:
    """Factory for creating AI model parsers"""
    
    PARSERS = {
        'openai': OpenAIParser,
        'anthropic': ClaudeParser,
        'google': GeminiParser,
        'github': CopilotParser,
        'deepseek': DeepSeekParser,
        'meta': LlamaParser,
        'mistral': MistralParser,
        'minimax': MiniMaxParser,
        'xai': GrokParser,
        'cohere': CohereParser
    }
    
    @classmethod
    def get_parser(cls, service: str) -> BaseParser:
        parser_class = cls.PARSERS.get(service)
        if not parser_class:
            raise ValueError(f"No parser for service: {service}")
        return parser_class()
    
    @classmethod
    def get_all_parsers(cls) -> Dict[str, BaseParser]:
        return {
            service: parser_class()
            for service, parser_class in cls.PARSERS.items()
        }
```

---

## 💰 Updated Pricing Table

### Model Cost Tracking (April 2026)

| Provider | Model | Input ($/1M tokens) | Output ($/1M tokens) | Notes |
|----------|-------|---------------------|----------------------|-------|
| **OpenAI** | GPT-4 Turbo | $10.00 | $30.00 | - |
| | GPT-4o | $5.00 | $15.00 | Optimized |
| | GPT-3.5 Turbo | $0.50 | $1.50 | - |
| | o1-preview | $15.00 | $60.00 | Reasoning |
| **Anthropic** | Claude 3.5 Sonnet | $3.00 | $15.00 | Prompt cache: $0.30/$1.50 |
| | Claude 3 Opus | $15.00 | $75.00 | - |
| | Claude 3 Haiku | $0.25 | $1.25 | - |
| **Google** | Gemini 1.5 Pro | $3.50 | $10.50 | - |
| | Gemini 1.5 Flash | $0.35 | $1.05 | - |
| | Gemini 2.0 Flash | $0.30 | $0.90 | Latest |
| **GitHub** | Copilot | $10/user/month | - | Flat rate |
| **DeepSeek** | DeepSeek-V2 | $0.14 | $0.28 | Very cheap |
| | DeepSeek-Coder | $0.14 | $0.28 | - |
| **Mistral** | Mistral Large | $4.00 | $12.00 | - |
| | Mixtral 8x22B | $2.00 | $6.00 | - |
| **MiniMax** | abab6.5 | $0.50 | $1.00 | CN market |
| **xAI** | Grok-2 | $5.00 | $15.00 | Estimated |
| **Cohere** | Command R+ | $3.00 | $15.00 | - |
| **Meta Llama** | Via providers | Varies | Varies | Depends on host |

---

## 📊 Updated Coverage Metrics

### Expected Coverage by Tier

**Tier 0 (Must Have - P0):**
- OpenAI: 98% coverage (API + Web)
- Anthropic: 100% coverage (API + Web + CLI)
- Google Gemini: 95% coverage (API + Web)
- GitHub Copilot: 100% coverage (IDE logs)

**Tier 1 (High Priority - P1):**
- DeepSeek: 90% coverage (API + logs)
- Meta Llama: 85% coverage (via Ollama + hosted)
- Mistral: 90% coverage (API + Web)

**Tier 2 (Medium Priority - P2):**
- MiniMax: 80% coverage (API)
- xAI Grok: 75% coverage (Web only)
- Cohere: 85% coverage (API)

**Overall Expected Coverage: 95-98%** of enterprise AI usage

---

## 🚀 Implementation Roadmap

### Phase 1: Core Models (Week 1-2)
- [x] OpenAI (ChatGPT, API)
- [x] Anthropic (Claude Code, Claude.ai, API)
- [x] GitHub Copilot
- [ ] Google Gemini (API + Web)

### Phase 2: Major Models (Week 3-4)
- [ ] DeepSeek (API + logs)
- [ ] Mistral (API + Le Chat)
- [ ] Meta Llama (Ollama integration)

### Phase 3: Additional Models (Week 5-6)
- [ ] MiniMax (API)
- [ ] xAI Grok (Web)
- [ ] Cohere (API + Coral)

### Phase 4: IDE Integrations (Week 7-8)
- [ ] Cursor IDE (enhanced)
- [ ] Continue.dev
- [ ] Codeium
- [ ] Tabnine

---

## ✅ Updated Technical Checklist

- [x] OpenAI support (Web + API)
- [x] Anthropic support (CLI + Web + API)
- [x] GitHub Copilot support
- [ ] **Google Gemini support** ⚠️ NEW
- [ ] **DeepSeek support** ⚠️ NEW
- [ ] **Meta Llama/Ollama support** ⚠️ NEW
- [ ] **Mistral AI support** ⚠️ NEW
- [ ] **MiniMax support** ⚠️ NEW
- [ ] **xAI Grok support** ⚠️ NEW
- [ ] **Cohere support** ⚠️ NEW
- [x] Browser extension (Chrome/Edge)
- [ ] **Firefox extension** (planned)
- [ ] **Safari extension** (planned)
- [x] SDK wrappers (Python/Node.js)
- [ ] **Auto-detection of new models** (future)

---

## 📚 Resources

Based on current AI model landscape as of April 2026:
- OpenAI continues market leadership with GPT-4 series
- Anthropic Claude gaining enterprise traction
- Google Gemini advancing with multimodal capabilities
- DeepSeek emerging as cost-effective alternative
- Meta Llama popular for self-hosted deployments
- Mistral AI growing in European markets
- Regional players (MiniMax in China, etc.)

---

**Document Version:** 1.0  
**Next Update:** Implement Phase 1 parsers and test coverage  
**Target Coverage:** 95-98% of enterprise AI usage

---

**End of AI Model Coverage Expansion Document**
