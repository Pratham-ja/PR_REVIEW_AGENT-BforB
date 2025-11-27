# 🚀 Google Gemini 2.5 Pro Setup Guide

## Quick Setup for Gemini

### Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key (starts with `AIza...`)

### Step 2: Configure Your .env File

Create or edit your `.env` file with:

```env
# Google Gemini Configuration
GOOGLE_API_KEY=AIzaSy...your_actual_key_here

# LLM Provider Selection
LLM_PROVIDER=google
LLM_MODEL=gemini-2.0-flash-exp

# Optional: GitHub Token (for PR URL reviews)
GITHUB_TOKEN=ghp_your_github_token_here

# Database (Optional - skip for testing)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pr_review_agent

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Step 3: Available Gemini Models

You can use any of these models:

| Model | Best For | Cost |
|-------|----------|------|
| `gemini-2.0-flash-exp` | Fast, cost-effective (Recommended) | Free (experimental) |
| `gemini-1.5-pro` | High quality, longer context | $0.00125 / 1K chars |
| `gemini-1.5-flash` | Fast, balanced | $0.000075 / 1K chars |

### Step 4: Test Your Setup

```bash
# Test the import
python -c "from services.llm_client import LLMClientFactory, LLMProvider; print('✓ Gemini support loaded')"

# Start the server
python main.py
```

## Example API Request with Gemini

```bash
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "diff_content": "diff --git a/test.py b/test.py\n+def hello():\n+    print(\"Hello World\")",
    "config": {
      "severity_threshold": "medium",
      "enabled_categories": ["logic", "security", "performance", "readability"]
    }
  }'
```

## Why Gemini 2.5 Pro?

✅ **Free tier available** - Great for testing
✅ **Fast responses** - Optimized for speed
✅ **Long context** - Can handle large PRs
✅ **Multimodal** - Can analyze code and diagrams
✅ **Cost-effective** - Lower cost than GPT-4

## Troubleshooting

### Error: "Google API key is required"
- Make sure `GOOGLE_API_KEY` is set in your `.env` file
- Check that the key starts with `AIza`

### Error: "Module not found: langchain_google_genai"
```bash
pip install langchain-google-genai
```

### Want to switch providers?
Just change `LLM_PROVIDER` in your `.env`:
- `LLM_PROVIDER=google` - Use Gemini
- `LLM_PROVIDER=openai` - Use GPT-4
- `LLM_PROVIDER=anthropic` - Use Claude

## Rate Limits

- **Free tier**: 60 requests per minute
- **Paid tier**: Higher limits based on your plan

Check your usage at: https://aistudio.google.com/app/apikey

---

🎉 **You're all set!** Your PR Review Agent is now powered by Google Gemini 2.5 Pro!
