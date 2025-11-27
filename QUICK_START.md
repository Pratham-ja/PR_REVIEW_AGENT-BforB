# 🚀 Quick Start Guide

## Step 1: Add Your Gemini API Key

Edit `.env` file and replace `your_google_gemini_api_key_here` with your actual key:

```env
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

**Get your key here:** https://aistudio.google.com/app/apikey

## Step 2: Start the Server

```bash
python main.py
```

The server will start at: `http://localhost:8000`

## Step 3: Test the API

### Option A: Use the Interactive Docs
Open in browser: `http://localhost:8000/docs`

### Option B: Test with cURL

```bash
# Simple test with manual diff
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "diff_content": "diff --git a/test.py b/test.py\n+def calculate(x, y):\n+    return x / y",
    "config": {
      "severity_threshold": "medium",
      "enabled_categories": ["logic", "security"]
    }
  }'
```

## Current Configuration

✅ **LLM Provider:** Google Gemini  
✅ **Model:** gemini-2.0-flash-exp (Free!)  
⚠️ **Database:** Disabled (reviews won't be saved)  
⚠️ **GitHub:** Not configured (can't review PR URLs)

## Optional: Add GitHub Token

If you want to review GitHub PRs by URL:

1. Get token: https://github.com/settings/tokens
2. Add to `.env`:
```env
GITHUB_TOKEN=ghp_your_token_here
```

## Optional: Enable Database

If you want to save review history:

1. Install PostgreSQL
2. Create database: `pr_review_agent`
3. Uncomment in `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pr_review_agent
```

## Troubleshooting

### Server won't start?
```bash
# Install missing dependencies
pip install langchain-google-genai asyncpg fastapi uvicorn
```

### "Google API key is required" error?
- Check your `.env` file has `GOOGLE_API_KEY=AIza...`
- Make sure the key is valid

### Want to test without database?
The server will work fine without PostgreSQL - reviews just won't be saved to history.

## What's Next?

- Check `GEMINI_SETUP.md` for detailed Gemini configuration
- Check `README.md` for full documentation
- Visit `http://localhost:8000/docs` for API documentation

---

**Need help?** Check the logs in the terminal where you ran `python main.py`
