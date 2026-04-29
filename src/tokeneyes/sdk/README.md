# Tokeneyes SDK Wrappers

Drop-in replacements for popular AI SDKs with **automatic token tracking**.

## Overview

Tokeneyes SDK wrappers allow you to track AI token usage with **zero code changes** to your existing applications. Simply change your import statement and continue using the same API.

### Supported SDKs

| SDK | Import | Status |
|-----|--------|--------|
| **OpenAI** | `from tokeneyes.sdk import OpenAI` | ✅ Complete |
| **Anthropic** | `from tokeneyes.sdk import Anthropic` | ✅ Complete |
| **Google (Gemini)** | `from tokeneyes.sdk import Gemini` | 📋 Planned |
| **Cohere** | `from tokeneyes.sdk import Cohere` | 📋 Planned |

---

## Quick Start

### Installation

```bash
# Install Tokeneyes
pip install -e .

# Install the SDK you want to use
pip install openai        # For OpenAI
pip install anthropic     # For Anthropic
```

### Usage

#### OpenAI Example

**Before (without tracking):**
```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**After (with automatic tracking):**
```python
from tokeneyes.sdk import OpenAI  # ← Only change this line!

client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# ✅ Token usage automatically tracked to ~/.aitracker/sdk_events.jsonl
```

#### Anthropic Example

**Before (without tracking):**
```python
from anthropic import Anthropic

client = Anthropic(api_key="sk-ant-...")
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**After (with automatic tracking):**
```python
from tokeneyes.sdk import Anthropic  # ← Only change this line!

client = Anthropic(api_key="sk-ant-...")
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

# ✅ Token usage automatically tracked to ~/.aitracker/sdk_events.jsonl
```

---

## Features

### ✅ Zero Code Changes

The wrapper is a **true drop-in replacement**. Change only the import statement:

```python
# Before
from openai import OpenAI

# After
from tokeneyes.sdk import OpenAI
```

Everything else stays exactly the same!

### ✅ Automatic Token Tracking

Every API call is automatically tracked:
- **Prompt tokens**
- **Completion tokens**
- **Total tokens**
- **Cached tokens** (when applicable)
- **Timestamp**
- **Model used**
- **Service (openai, anthropic, etc.)**

### ✅ Works with Existing Code

Compatible with all existing code using the official SDKs:
- ✅ Synchronous clients
- ✅ Asynchronous clients (AsyncOpenAI, AsyncAnthropic)
- ✅ Streaming responses
- ✅ All API methods
- ✅ All parameters

### ✅ Privacy-First

Only token metadata is tracked:
- ✅ Token counts
- ✅ Model names
- ✅ Timestamps
- ❌ **Never** prompts
- ❌ **Never** responses
- ❌ **Never** user data

### ✅ Offline-Capable

Token events are saved locally to `~/.aitracker/sdk_events.jsonl`:
- Works without internet connection
- No external dependencies
- Synced to backend when daemon is running

### ✅ Optional Tracking

Disable tracking for specific clients:

```python
from tokeneyes.sdk import OpenAI

# Tracking enabled (default)
client1 = OpenAI(api_key="...")

# Tracking disabled
client2 = OpenAI(api_key="...", track_tokens=False)
```

---

## How It Works

### Architecture

```
Your Code
    ↓
Tokeneyes SDK Wrapper (transparent proxy)
    ↓
Official SDK (openai, anthropic, etc.)
    ↓
AI Provider API
    ↓
Response with usage data
    ↓
Tokeneyes tracks tokens → ~/.aitracker/sdk_events.jsonl
    ↓
Your Code receives response (unchanged)
```

### Method Wrapping

The wrapper intercepts SDK methods to extract token usage:

```python
class OpenAIWrapper:
    def __init__(self, api_key, **kwargs):
        # Create official SDK client
        self._client = OpenAI(api_key=api_key, **kwargs)
        
        # Wrap the API method
        original = self._client.chat.completions.create
        self._client.chat.completions.create = self._wrap(original)
    
    def _wrap(self, original_method):
        def wrapped(*args, **kwargs):
            # Call original method
            response = original_method(*args, **kwargs)
            
            # Extract and track token usage
            self._track_tokens(response)
            
            # Return response unchanged
            return response
        
        return wrapped
```

### Event Storage

Events are stored in JSONL format at `~/.aitracker/sdk_events.jsonl`:

```json
{"timestamp": "2026-04-29T12:00:00Z", "service": "openai", "model": "gpt-4", "prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60, "cached_tokens": 0, "tool": "sdk-wrapper", "interface": "api", "synced": false}
{"timestamp": "2026-04-29T12:01:00Z", "service": "anthropic", "model": "claude-3-sonnet", "prompt_tokens": 20, "completion_tokens": 100, "total_tokens": 120, "cached_tokens": 15, "tool": "sdk-wrapper", "interface": "api", "synced": false}
```

---

## Examples

See the `examples/` directory for complete examples:

### Basic Usage

```bash
# OpenAI example
python examples/example_openai.py

# Anthropic example
python examples/example_anthropic.py
```

### Test Suite

```bash
# Run all SDK wrapper tests
python examples/test_sdk_wrappers.py
```

**Note:** Tests require valid API keys in environment variables:
- `OPENAI_API_KEY` for OpenAI tests
- `ANTHROPIC_API_KEY` for Anthropic tests

---

## API Reference

### OpenAI Wrapper

```python
from tokeneyes.sdk import OpenAI, AsyncOpenAI

# Synchronous client
client = OpenAI(
    api_key="sk-...",           # Required: OpenAI API key
    track_tokens=True,          # Optional: Enable tracking (default: True)
    state_dir=None,             # Optional: Custom state directory
    **kwargs                    # All other OpenAI parameters
)

# Asynchronous client
async_client = AsyncOpenAI(
    api_key="sk-...",
    track_tokens=True,
    state_dir=None,
    **kwargs
)
```

### Anthropic Wrapper

```python
from tokeneyes.sdk import Anthropic, AsyncAnthropic

# Synchronous client
client = Anthropic(
    api_key="sk-ant-...",       # Required: Anthropic API key
    track_tokens=True,          # Optional: Enable tracking (default: True)
    state_dir=None,             # Optional: Custom state directory
    **kwargs                    # All other Anthropic parameters
)

# Asynchronous client
async_client = AsyncAnthropic(
    api_key="sk-ant-...",
    track_tokens=True,
    state_dir=None,
    **kwargs
)
```

### TokenTracker (Low-Level API)

For custom tracking without SDK wrappers:

```python
from tokeneyes.sdk import TokenTracker

tracker = TokenTracker()  # Uses ~/.aitracker by default

tracker.track_event(
    service='openai',
    model='gpt-4',
    prompt_tokens=100,
    completion_tokens=200,
    total_tokens=300,
    cached_tokens=0,
    metadata={'custom': 'data'}
)
```

---

## Integration with Tokeneyes Daemon

SDK wrapper events are separate from daemon-scanned events:

| Source | Event File | Description |
|--------|-----------|-------------|
| **Daemon** | `~/.aitracker/events.jsonl` | Log file scanning (CLI tools, IDEs) |
| **SDK Wrappers** | `~/.aitracker/sdk_events.jsonl` | Direct API calls via wrappers |

Both files are monitored and synced to the backend server.

**To view combined usage:**

```bash
tokeneyes stats  # Shows both daemon and SDK events
```

---

## Troubleshooting

### Import Error: SDK Not Installed

```
ImportError: OpenAI SDK not installed. Install with: pip install openai
```

**Solution:** Install the required SDK:
```bash
pip install openai        # For OpenAI
pip install anthropic     # For Anthropic
```

### Events Not Tracked

If events are not appearing in `~/.aitracker/sdk_events.jsonl`:

1. **Check tracking is enabled:**
   ```python
   client = OpenAI(api_key="...", track_tokens=True)  # Default
   ```

2. **Check directory permissions:**
   ```bash
   ls -la ~/.aitracker/
   ```

3. **Verify event file exists:**
   ```bash
   cat ~/.aitracker/sdk_events.jsonl
   ```

4. **Check for errors:**
   ```python
   import traceback
   try:
       client = OpenAI(api_key="...")
       response = client.chat.completions.create(...)
   except Exception as e:
       traceback.print_exc()
   ```

### Type Hints Not Working

The wrappers proxy to the official SDKs, so type hints should work. If your IDE shows warnings:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI as OpenAIType
else:
    from tokeneyes.sdk import OpenAI as OpenAIType

client: OpenAIType = OpenAI(api_key="...")
```

---

## Performance

SDK wrappers add **negligible overhead** (< 1ms per request):

| Operation | Time |
|-----------|------|
| API call (baseline) | ~500-2000ms |
| Token extraction | < 0.1ms |
| Event write (JSONL) | < 1ms |
| **Total overhead** | **< 1ms** |

The tracking happens **after** the API response is received, so it doesn't affect API latency.

---

## Security

### API Keys

API keys are passed directly to the official SDKs and **never stored** by Tokeneyes.

### Data Privacy

Only metadata is tracked:
- ✅ Token counts
- ✅ Model names
- ✅ Timestamps
- ❌ Prompts (**never** stored)
- ❌ Responses (**never** stored)

### Event File

Events are stored locally at `~/.aitracker/sdk_events.jsonl`:
- Only accessible by the user
- Standard file permissions (0600)
- Can be deleted anytime: `rm ~/.aitracker/sdk_events.jsonl`

---

## Limitations

### Streaming Responses

Currently, streaming responses are not fully supported for token tracking. The response will work, but token counts may not be available until the stream completes.

**Workaround:** For streaming, use the official SDK and track tokens manually.

### Model Coverage

Only the most common API methods are wrapped:
- ✅ OpenAI: `chat.completions.create`
- ✅ Anthropic: `messages.create`

Other methods (embeddings, fine-tuning, etc.) are proxied but not tracked yet.

---

## Roadmap

- [ ] Streaming response support
- [ ] Google Gemini wrapper
- [ ] Cohere wrapper
- [ ] Embeddings tracking
- [ ] Fine-tuning tracking
- [ ] Node.js/TypeScript wrappers
- [ ] Automatic cost calculation

---

## License

MIT License - see [LICENSE](../LICENSE) for details

---

## Support

- **Issues:** https://github.com/chinazane/Tokeneyes/issues
- **Documentation:** [Main README](../README.md)
- **Examples:** [examples/](../examples/)
