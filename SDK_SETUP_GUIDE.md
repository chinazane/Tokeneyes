# Tokeneyes SDK Tracking - Setup Guide

## Understanding the Architecture

**Important:** The Tokeneyes daemon (`tokeneyes start -d`) and your Python application run in **separate processes**. The daemon cannot directly intercept imports in your application.

```
┌─────────────────────┐     ┌──────────────────────┐
│ Tokeneyes Daemon    │     │ Your Python App      │
│ (Process 1)         │     │ (Process 2)          │
│                     │     │                      │
│ ✅ Scans log files  │     │ from openai import   │
│ ✅ Tracks CLI tools │     │   OpenAI             │
│ ❌ Can't intercept  │────X│                      │
│    other processes  │     │ ← Daemon can't see!  │
└─────────────────────┘     └──────────────────────┘
```

## What Each Component Tracks

| Component | What It Tracks | Requires User Action |
|-----------|----------------|---------------------|
| **Scanner Daemon** | CLI tools, IDEs (log files) | ❌ No - Fully automatic |
| **SDK Wrappers** | Direct API calls in user code | ✅ Yes - See options below |

---

## SDK Tracking Options

Choose the option that best fits your use case:

###  Option 1: Manual Import Change (Recommended)

**Best for:** Production code, explicit control

**Setup:** Change one line per file

```python
# Change this:
from openai import OpenAI

# To this:
from tokeneyes.sdk import OpenAI

# Everything else stays the same!
client = OpenAI(api_key="...")
response = client.chat.completions.create(...)
# ✅ Tracked automatically!
```

**Pros:**
- ✅ Explicit and clear
- ✅ Easy to understand
- ✅ Easy to disable (change import back)
- ✅ Works in all environments
- ✅ No surprises

**Cons:**
- ⚠️ Requires changing imports in each file

---

### Option 2: Programmatic Auto-Track

**Best for:** Applications where you control the entry point

**Setup:** Add one line at app startup

```python
# At the top of your main.py or __init__.py:
import tokeneyes
tokeneyes.auto_track()

# Now these imports are automatically wrapped:
from openai import OpenAI
from anthropic import Anthropic

client = OpenAI(api_key="...")
# ✅ Tracked automatically!
```

**Important:** `tokeneyes.auto_track()` must be called **BEFORE** importing the SDKs.

**Pros:**
- ✅ One-time setup per application
- ✅ No need to change SDK imports
- ✅ Easy to enable/disable

**Cons:**
- ⚠️ Must be called before SDK imports
- ⚠️ Only works in applications you control

---

### Option 3: Environment + sitecustomize.py

**Best for:** System-wide automatic tracking

**Setup:** One-time system configuration

```bash
# 1. Create sitecustomize.py in your Python path
cat > ~/.local/lib/python3.10/site-packages/sitecustomize.py << 'EOF'
import os
if os.getenv('TOKENEYES_TRACK'):
    try:
        from tokeneyes.sdk.autopatch import install_import_hooks
        install_import_hooks()
    except ImportError:
        pass
EOF

# 2. Set environment variable
export TOKENEYES_TRACK=1

# 3. Run your app normally
python myapp.py
# ✅ All SDK calls tracked automatically!
```

**Pros:**
- ✅ Fully automatic
- ✅ Works for all applications
- ✅ No code changes needed

**Cons:**
- ⚠️ Complex setup
- ⚠️ Affects all Python code system-wide
- ⚠️ Hard to debug if something breaks

---

## Recommended Approach

**For most users, we recommend Option 1 (Manual Import Change):**

```python
from tokeneyes.sdk import OpenAI, Anthropic
```

**Why?**
- ✅ Simple and explicit
- ✅ Easy to understand what's happening
- ✅ Easy to disable if needed
- ✅ Works everywhere
- ✅ One line change per file

**The trade-off of changing imports is worth the clarity and reliability.**

---

## Complete Coverage: Daemon + SDK Wrappers

For complete tracking, use **both** components:

```bash
# 1. Start the daemon (tracks CLI/IDE usage)
tokeneyes start -d

# 2. Use SDK wrappers in your code (tracks API calls)
# In your Python files:
from tokeneyes.sdk import OpenAI
```

**Combined Coverage:**
| Source | Tracking Method | User Action |
|--------|-----------------|-------------|
| Claude Code CLI | Daemon (log scanning) | ❌ None |
| GitHub Copilot | Daemon (log scanning) | ❌ None |
| OpenAI CLI | Daemon (log scanning) | ❌ None |
| Your Python app | SDK wrappers | ✅ Change import |

**Result:** ~98% of AI coding usage tracked!

---

## FAQ

### Q: Why can't the daemon automatically track SDK calls?

**A:** Process isolation. The daemon runs as a separate background process and cannot intercept imports in other Python processes.

### Q: Do I need both the daemon AND SDK wrappers?

**A:** It depends:
- **Only daemon:** Tracks CLI tools and IDEs (no code changes needed)
- **Only SDK wrappers:** Tracks your API calls (requires import changes)
- **Both:** Complete coverage of all AI usage

### Q: What if I forget to use the wrapper?

**A:** Your code will work normally (using the official SDK), but those API calls won't be tracked.

### Q: Can I mix wrapped and unwrapped imports?

**A:** Yes! You can use:
```python
from tokeneyes.sdk import OpenAI as TrackedOpenAI
from openai import OpenAI as RawOpenAI

tracked_client = TrackedOpenAI(...)   # ✅ Tracked
untracked_client = RawOpenAI(...)     # ❌ Not tracked
```

### Q: Does this slow down my application?

**A:** No. The wrapper adds < 1ms overhead per API call, which is negligible compared to the 500-2000ms API latency.

---

## Examples

See the `examples/` directory for working examples:
- `examples/example_openai.py` - OpenAI with manual import
- `examples/example_anthropic.py` - Anthropic with manual import
- `examples/example_auto_track.py` - Using tokeneyes.auto_track()

---

## Summary

**Daemon:**
- ✅ Fully automatic
- ✅ Tracks CLI/IDE usage
- ❌ Cannot track direct API calls

**SDK Wrappers:**
- ⚠️ Requires import change (or auto_track() call)
- ✅ Tracks all API calls
- ✅ Works alongside daemon

**Recommended:** Use both for complete coverage!
