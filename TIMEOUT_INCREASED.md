# Timeout Settings Increased

## Changes Made

I've increased all timeout settings to give the agents more time to analyze code:

### 1. Environment Configuration (`.env`)
```env
AGENT_TIMEOUT=300  # Changed from 30 to 300 seconds (5 minutes per agent)
```

### 2. Agent Configuration (`agents/base_agent.py`)
```python
timeout: int = 300  # Changed from 30 to 300 seconds
max_tokens: int = 4000  # Increased from 2000 for more detailed analysis
```

### 3. Frontend Timeout (`frontend/app.py`)
```python
timeout=600  # Changed from 300 to 600 seconds (10 minutes total)
```

## What This Means

- **Each agent** now has up to 5 minutes to analyze the code
- **Total review time** can be up to 10 minutes for large PRs
- **More detailed analysis** with increased token limit

## Testing the Changes

The backend has been restarted with the new settings. Try reviewing a PR now:

1. Open http://localhost:8501
2. Enter a PR URL
3. Click "Start Review"
4. **Be patient** - it may take several minutes

## Important Note About the "No Findings" Issue

The timeout increase will help, but there's a deeper issue: **the agents are completing quickly (7 seconds) but returning 0 findings**. This suggests:

1. **The LLM might not be responding properly** - Google Gemini might need different configuration
2. **The agents might not be calling the LLM** - There could be a logic issue
3. **The LLM response might not be parsed correctly** - JSON parsing could be failing

### Recommended Next Steps

1. **Check if Gemini is actually being called:**
   - Look at backend logs during a review
   - Should see LLM API calls

2. **Test with a simple diff:**
   ```python
   # Use manual diff mode with obvious bugs
   def divide(a, b):
       return a / b  # No zero check!
   
   password = "admin123"  # Hardcoded!
   ```

3. **Check Gemini API quota:**
   - Go to https://console.cloud.google.com/
   - Check if API is enabled and has quota

4. **Try switching to OpenAI temporarily:**
   - Update `.env`:
     ```env
     LLM_PROVIDER=openai
     OPENAI_API_KEY=your_key_here
     ```
   - This will help determine if it's a Gemini-specific issue

## Current Status

✅ Timeouts increased
✅ Backend restarted
⚠️ Root cause of "no findings" still needs investigation

The system is now configured to be more patient, but we may need to debug why the LLM isn't returning findings even when given enough time.
