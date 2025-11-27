# 🧪 Testing Guide for PR Review Agent

## ✅ Current Status

Your PR Review Agent is **UP AND RUNNING**! 🎉

- ✅ Server running on `http://localhost:8000`
- ✅ Google Gemini API configured
- ✅ GitHub token configured
- ✅ All 4 analyzer agents ready (Logic, Readability, Performance, Security)
- ⚠️ Database disabled (reviews won't be saved - that's OK for testing)

## 🎯 How to Test

### Option 1: Interactive API Docs (Easiest!)

1. Open in browser: `http://localhost:8000/docs`
2. Click on **POST /api/reviews**
3. Click **"Try it out"**
4. Paste this test request:

```json
{
  "diff_content": "diff --git a/app.py b/app.py\nnew file mode 100644\nindex 0000000..abc1234\n--- /dev/null\n+++ b/app.py\n@@ -0,0 +1,10 @@\n+def divide_numbers(a, b):\n+    result = a / b\n+    return result\n+\n+def get_user(user_id):\n+    query = 'SELECT * FROM users WHERE id = ' + str(user_id)\n+    cursor.execute(query)\n+    return cursor.fetchone()\n+\n+API_KEY = 'hardcoded_secret_key_12345'",
  "config": {
    "severity_threshold": "low",
    "enabled_categories": ["logic", "security", "performance", "readability"]
  }
}
```

5. Click **"Execute"**
6. Check the response - should find:
   - 🐛 Division by zero risk
   - 🔒 SQL injection vulnerability
   - 🔒 Hardcoded API key

### Option 2: Test with a Real GitHub PR

Use the interactive docs (`http://localhost:8000/docs`) and try:

```json
{
  "pr_url": "https://github.com/YOUR_USERNAME/YOUR_REPO/pull/PR_NUMBER",
  "config": {
    "severity_threshold": "medium",
    "enabled_categories": ["logic", "security"]
  }
}
```

Replace with an actual PR from your repositories!

### Option 3: PowerShell Command

```powershell
$testRequest = @'
{
  "diff_content": "diff --git a/test.py b/test.py\n+def unsafe_query(user_input):\n+    query = 'SELECT * FROM users WHERE name = ' + user_input\n+    return execute(query)",
  "config": {
    "severity_threshold": "low",
    "enabled_categories": ["security"]
  }
}
'@

Invoke-RestMethod -Uri "http://localhost:8000/api/reviews" -Method Post -Body $testRequest -ContentType "application/json"
```

## 🔍 What to Expect

The review should return findings like:

```json
{
  "review_id": "...",
  "findings": [
    {
      "file_path": "app.py",
      "line_number": 6,
      "severity": "critical",
      "category": "security",
      "description": "SQL Injection vulnerability: User input directly concatenated into SQL query",
      "suggestion": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
      "agent_source": "security_analyzer"
    }
  ],
  "summary": {
    "total_findings": 3,
    "findings_by_severity": {"critical": 1, "high": 1, "medium": 1},
    "findings_by_category": {"security": 2, "logic": 1}
  },
  "formatted_comments": "# Code Review Results\n\n## Summary\n..."
}
```

## 🐛 Troubleshooting

### No findings returned?

Check server logs in the terminal where you ran `python main.py`:
- Look for "Logic analyzer found X issues"
- Look for "Security analyzer found X issues"
- Check for any errors from Gemini API

### "GitHub API error"?

- Make sure your `GITHUB_TOKEN` is valid
- Check the PR URL is correct and accessible
- Try with a public repository first

### "Google API key is required"?

- Verify `GOOGLE_API_KEY` is set in `.env`
- Make sure the key starts with `AIza`
- Test your key at: https://aistudio.google.com/

## 📊 Test Results

After testing, you should see:

1. **Server logs** showing agent execution
2. **Findings** from each analyzer agent
3. **Formatted markdown** review comments
4. **Summary statistics** by severity and category

## 🎯 Recommended Test PRs

Try these small, public PRs for testing:
- Any small PR from your own repositories
- Look for PRs with 5-20 lines of changes
- PRs with obvious issues (SQL queries, missing error handling, etc.)

## 📝 Next Steps

1. Test with the interactive docs first (easiest!)
2. Try a real GitHub PR from your repository
3. Check the formatted markdown output
4. Review the findings from each agent

---

**Server running?** Check: `http://localhost:8000/health`  
**Need help?** Check the terminal logs where you ran `python main.py`
