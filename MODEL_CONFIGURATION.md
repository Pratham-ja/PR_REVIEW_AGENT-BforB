# NVIDIA NIM Model Configuration

## Current Setup

Your PR Review Agent now uses **agent-specific NVIDIA NIM models** for optimal performance:

### Model Assignment by Agent

| Agent | Model | Purpose |
|-------|-------|---------|
| **Logic Analyzer** | `meta/llama-3.1-70b-instruct` | Detect logical errors, bugs, null checks |
| **Readability Analyzer** | `meta/llama-3.1-70b-instruct` | Code style, naming, documentation |
| **Performance Analyzer** | `meta/llama-3.1-70b-instruct` | Performance issues, optimization |
| **Security Analyzer** | `meta/llama-3.1-405b-instruct` | Security vulnerabilities (strongest model) |

### Why Different Models?

- **70B models** (Logic, Readability, Performance): Fast and efficient for general code analysis
- **405B model** (Security): Most powerful model for critical security analysis

## Configuration Files

### `.env`
```bash
NVIDIA_API_KEY=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
LLM_PROVIDER=nvidia
LLM_MODEL=meta/llama-3.1-8b-instruct  # Default fallback
```

### Model Selection Logic

The `NimLlmClient` class automatically selects the appropriate model based on the agent name:

```python
AGENT_MODELS = {
    "logic_analyzer": "meta/llama-3.1-70b-instruct",
    "readability_analyzer": "meta/llama-3.1-70b-instruct",
    "performance_analyzer": "meta/llama-3.1-70b-instruct",
    "security_analyzer": "meta/llama-3.1-405b-instruct",
    "default": "meta/llama-3.1-8b-instruct"
}
```

## How It Works

1. **SimpleOrchestrator** creates agent-specific LLM clients
2. Each agent gets a `NimLlmClient` configured with its optimal model
3. When an agent analyzes code, it uses its assigned model
4. Security analysis uses the most powerful 405B model for maximum accuracy

## Available NVIDIA NIM Models

Based on testing, these models are available on your API:

- ✅ `meta/llama-3.1-8b-instruct` - Fast, lightweight
- ✅ `meta/llama-3.1-70b-instruct` - Balanced performance
- ✅ `meta/llama-3.1-405b-instruct` - Most powerful
- ❌ `nvidia/nemotron-nano-9b-v2` - Not available on API
- ❌ `qwen/qwen3-next-80b-a3b-thinking` - Quota issues

## Customization

### Change Model for Specific Agent

Edit `services/llm_client.py`:

```python
AGENT_MODELS = {
    "logic_analyzer": "meta/llama-3.1-70b-instruct",
    "security_analyzer": "meta/llama-3.1-405b-instruct",  # Change this
    # ...
}
```

### Use Same Model for All Agents

Set in `.env`:

```bash
LLM_MODEL=meta/llama-3.1-70b-instruct
```

Then modify `SimpleOrchestrator` to use the same LLM for all agents.

## Performance Characteristics

### Model Comparison

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| 8B | ⚡⚡⚡ Fast | ⭐⭐ Good | Quick reviews, testing |
| 70B | ⚡⚡ Medium | ⭐⭐⭐ Great | Production reviews |
| 405B | ⚡ Slow | ⭐⭐⭐⭐ Excellent | Critical security analysis |

### Typical Review Times

- **Small PR** (< 100 lines): 30-60 seconds
- **Medium PR** (100-500 lines): 1-3 minutes
- **Large PR** (500+ lines): 3-5 minutes

## API Endpoint

All models use the same NVIDIA NIM endpoint:

```
POST https://integrate.api.nvidia.com/v1/chat/completions
```

Headers:
```
Authorization: Bearer ${NVIDIA_API_KEY}
Content-Type: application/json
```

Payload:
```json
{
  "model": "meta/llama-3.1-70b-instruct",
  "messages": [
    {"role": "system", "content": "You are a code reviewer..."},
    {"role": "user", "content": "Analyze this code..."}
  ],
  "temperature": 0.1,
  "max_tokens": 2000
}
```

## Testing

### Test Individual Model

```python
from services.llm_client import NimLlmClient
from config import settings

# Test security analyzer model
client = NimLlmClient(
    api_key=settings.nvidia_api_key,
    agent_name="security_analyzer"
)

print(f"Using model: {client.model}")
# Output: Using model: meta/llama-3.1-405b-instruct
```

### Test All Agents

```bash
python test_api_endpoint.py
```

## Troubleshooting

### Models Not Working?

1. Check API key is valid
2. Verify model names are correct
3. Check NVIDIA NIM API status
4. Review logs for specific errors

### Slow Performance?

- 405B model is slower but more accurate
- Consider using 70B for all agents if speed is critical
- Reduce `max_tokens` in agent config

### Rate Limits?

- NVIDIA NIM has rate limits on free tier
- Wait a few minutes between large reviews
- Consider upgrading API plan

## Next Steps

1. **Test with different PRs** to see model performance
2. **Monitor which agent finds what** to optimize model assignment
3. **Adjust models** based on your needs (speed vs accuracy)
4. **Track costs** if using paid tier

---

**Your PR Review Agent now uses optimized models for each type of analysis!** 🚀
