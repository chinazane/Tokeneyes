# Tokeneyes - Project Scope

**Last Updated:** April 29, 2026  
**Focus:** Vibe Coding (CLI/IDE Usage Tracking)

---

## 🎯 **Current Scope: Vibe Coding**

Tokeneyes is focused on tracking AI token usage for **developers using CLI tools and IDEs** for coding tasks.

### In Scope

**Target Users:**
- Software engineers using AI coding assistants
- Teams using Claude Code, Cursor, GitHub Copilot
- Developers using API-based AI tools (OpenAI API, Anthropic API, etc.)
- Companies wanting to track AI coding costs

**Target Interfaces:**
- ✅ CLI tools (Claude Code, OpenAI CLI, etc.)
- ✅ IDE extensions (Copilot, Cursor)
- ✅ API usage (OpenAI, Anthropic, Google, etc.)
- ✅ Local deployments (Ollama, local Llama)
- ✅ SDK integrations (Python/Node.js wrappers)

**Use Cases:**
- Tracking AI coding assistant usage
- Monitoring API costs for development
- Team-level visibility into AI tool spending
- Personal usage analytics
- Budget compliance for engineering teams

---

## 🚫 **Out of Scope (Current Phase)**

**Browser Extensions:**
- ❌ ChatGPT web interface tracking
- ❌ Claude.ai web tracking
- ❌ Gemini web tracking
- ❌ Browser-based AI tools

**Rationale:**
- Vibe coding focuses on **CLI/IDE workflows**, not web browsing
- Browser extension would track general AI usage, not coding-specific
- Different user personas (general users vs. developers)
- Can be added as future enhancement if needed

---

## 📊 **Current Implementation Status**

### ✅ Phase 1-3: Complete (100%)
- **Scanner Daemon:** Monitors log files for all 10 AI providers
- **10 Parsers:** OpenAI, Claude, Gemini, Copilot, DeepSeek, Llama, Mistral, MiniMax, Grok, Cohere
- **50+ Models:** Complete coverage of major AI models
- **Log Discovery:** Automatic detection of CLI/IDE log files
- **Event Queue:** Offline-capable with retry logic
- **Cursor Store:** Incremental log parsing

### 📋 Phase 4: SDK Wrappers (Planned)
**Goal:** Zero-code integration for developers

**Python SDK:**
```python
# Drop-in replacement for OpenAI SDK
from tokeneyes import OpenAI  # Auto-tracked!
client = OpenAI(api_key="...")
```

**Node.js SDK:**
```javascript
// Drop-in replacement for OpenAI/Anthropic SDK
const { OpenAI } = require('tokeneyes');
const client = new OpenAI({ apiKey: '...' });
```

**Benefits:**
- No code changes required (just import path)
- Automatic token tracking
- Works with all existing code
- Transparent to developers

### 📋 Phase 5: Backend Infrastructure (Planned)
- FastAPI REST API
- TimescaleDB for time-series data
- Redis for caching
- Authentication & authorization
- SQS message queue for async processing

### 📋 Phase 6: Dashboard (Planned)
- Personal usage dashboard
- Team analytics
- Cost tracking & budgets
- Real-time charts (ECharts)
- Export & reporting

---

## 🎨 **Target Workflow**

### Developer Experience

1. **Install Scanner (one-time):**
   ```bash
   pip install tokeneyes
   tokeneyes init
   tokeneyes start
   ```

2. **Use AI tools normally:**
   ```bash
   # Claude Code
   claude "implement login feature"
   
   # OpenAI CLI
   openai api chat.completions.create -m gpt-4 ...
   
   # GitHub Copilot (in VS Code)
   # Just code normally, Copilot suggestions tracked
   ```

3. **Optional: Use SDK wrapper for API calls:**
   ```python
   from tokeneyes import OpenAI
   client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   # All API calls automatically tracked!
   ```

4. **View usage:**
   ```bash
   tokeneyes dashboard
   # Opens web UI showing usage/costs
   ```

---

## 💰 **Value Proposition (Vibe Coding Focus)**

### For Individual Developers
- Track personal AI coding costs
- Optimize model selection (GPT-4 vs GPT-3.5 vs Claude)
- Understand usage patterns
- Stay within personal budgets

### For Engineering Teams
- Team-level visibility into AI tool costs
- Identify heavy users
- Budget compliance
- Cost allocation per project/team

### For Engineering Managers
- Company-wide AI coding costs
- ROI analysis of AI coding tools
- Department budgets
- Cost optimization opportunities

**Expected Savings:** 15-40% through:
- Smart model selection (DeepSeek vs GPT-4)
- Identifying inefficient usage patterns
- Prompt caching optimization
- Budget awareness

---

## 🔍 **What We Track**

### Automatically Tracked
- ✅ Token counts (prompt, completion, cached)
- ✅ Model used
- ✅ Timestamp
- ✅ Cost (calculated from pricing)
- ✅ Tool/interface (CLI, API, IDE)
- ✅ Session ID

### Never Tracked (Privacy)
- ❌ Prompt content
- ❌ Response content
- ❌ Code snippets
- ❌ User data
- ❌ File paths

**Privacy-First:** Only metadata, never content.

---

## 📈 **Coverage**

### AI Providers (10/10) ✅
1. OpenAI (ChatGPT, GPT-4, GPT-3.5)
2. Anthropic (Claude 3.5, Claude 3)
3. Google (Gemini 1.5, Gemini 2.0)
4. GitHub (Copilot)
5. DeepSeek
6. Meta (Llama 3.1, Code Llama)
7. Mistral AI
8. MiniMax
9. xAI (Grok)
10. Cohere

### Expected Coverage
**95-98%** of enterprise AI coding usage

---

## 🚀 **Next Steps**

Based on current scope (vibe coding), the implementation order is:

1. **Phase 4: SDK Wrappers** ← Next priority
   - Enables zero-code integration
   - Covers API usage not captured by log scanning
   - Critical for production code using AI APIs

2. **Phase 5: Backend Infrastructure**
   - Central data storage
   - Multi-user support
   - Team dashboards

3. **Phase 6: Dashboard**
   - Web UI for visualization
   - Reports & analytics
   - Budget management

---

## 🔮 **Future Enhancements (Out of Current Scope)**

These may be added later if needed:

- **Browser Extension:** Track web-based AI tools (ChatGPT web, Claude.ai)
- **Mobile Apps:** iOS/Android tracking
- **Slack Integration:** Usage notifications
- **CI/CD Integration:** Track AI usage in automated pipelines
- **VSCode Extension:** In-IDE usage display

---

**Focus:** Stay laser-focused on vibe coding (CLI/IDE) to deliver value to developers quickly.

**Principle:** Ship core functionality first, expand scope based on user feedback.
