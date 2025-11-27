# Frontend User Guide 🎨

Complete guide to using the PR Review Agent Streamlit frontend.

## Getting Started

### 1. Start the Backend API

First, ensure the backend API is running:

```bash
# From project root
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Start the Frontend

```bash
# Option 1: Using the convenience script
python run_frontend.py

# Option 2: Direct streamlit command
streamlit run frontend/app.py
```

### 3. Access the UI

Open your browser to: `http://localhost:8501`

## Features Overview

### 🔍 GitHub PR Review Mode

Review pull requests directly from GitHub.

**Steps:**
1. Select "GitHub PR URL" in the sidebar
2. Enter the full GitHub PR URL (e.g., `https://github.com/owner/repo/pull/123`)
3. (Optional) Add GitHub token for private repositories
4. Configure analysis settings:
   - **Severity Threshold**: Minimum severity to report (low/medium/high/critical)
   - **Analysis Categories**: Select which types of issues to check
   - **Custom Rules**: Add specific review rules
5. Click "🚀 Start Review"
6. Wait for analysis (may take 1-5 minutes depending on PR size)

**Example:**
```
PR URL: https://github.com/facebook/react/pull/12345
GitHub Token: ghp_xxxxxxxxxxxx (optional)
Severity: medium
Categories: logic, security, performance
```

### 📝 Manual Diff Review Mode

Review code changes from git diff output.

**Steps:**
1. Select "Manual Diff" in the sidebar
2. Enter repository name (e.g., `owner/repo`)
3. (Optional) Enter PR number
4. Paste your git diff content:
   ```bash
   # Generate diff in your terminal
   git diff main..feature-branch > diff.txt
   # Copy and paste the content
   ```
5. Configure analysis settings
6. Click "🚀 Start Review"

**Example Diff:**
```diff
diff --git a/src/api.py b/src/api.py
index abc123..def456 100644
--- a/src/api.py
+++ b/src/api.py
@@ -10,7 +10,7 @@ def get_user(user_id):
-    query = "SELECT * FROM users WHERE id = " + user_id
+    query = "SELECT * FROM users WHERE id = ?"
-    return db.execute(query)
+    return db.execute(query, (user_id,))
```

### 📚 Review History Mode

Browse and filter past reviews.

**Steps:**
1. Select "View History" in the sidebar
2. (Optional) Apply filters:
   - Repository name
   - PR number
   - Results limit
3. Click "🔍 Load History"
4. Expand items to see detailed findings

## Understanding Results

### Review Summary

The summary section shows:
- **Repository & PR Info**: Where the code came from
- **Total Findings**: Number of issues detected
- **Files Analyzed**: How many files were reviewed
- **Lines Changed**: Total lines modified

### Findings by Severity

Issues are categorized by severity:

- 🔴 **Critical**: Must fix immediately (security vulnerabilities, data loss risks)
- 🟠 **High**: Should fix soon (logic errors, major bugs)
- 🟡 **Medium**: Should address (code quality, minor bugs)
- 🟢 **Low**: Nice to fix (style issues, suggestions)

### Findings by Category

Issues are grouped by type:

- **Logic**: Bugs, errors, edge cases
- **Security**: Vulnerabilities, unsafe practices
- **Performance**: Inefficiencies, optimization opportunities
- **Readability**: Code clarity, maintainability

### Individual Findings

Each finding shows:
- **Severity Level**: Color-coded indicator
- **Category**: Type of issue
- **File & Line**: Exact location
- **Issue Description**: What's wrong
- **Suggestion**: How to fix it

## Configuration Options

### Severity Threshold

Controls which findings to show:
- **Low**: Show all findings (most verbose)
- **Medium**: Show medium, high, and critical
- **High**: Show only high and critical
- **Critical**: Show only critical issues

### Analysis Categories

Enable/disable specific analysis types:
- ✅ **Logic**: Detect bugs and logical errors
- ✅ **Security**: Find security vulnerabilities
- ✅ **Performance**: Identify performance issues
- ✅ **Readability**: Check code quality

### Custom Rules

Add specific requirements for your codebase:

```
Example custom rules:
- All functions must have docstrings
- Maximum function length: 50 lines
- No hardcoded credentials
- Use type hints for all parameters
```

## Exporting Results

### Download JSON

Complete review data in JSON format:
- All findings with full details
- Metadata and timestamps
- Summary statistics
- Useful for automation and integration

### Download Comments

Formatted markdown comments ready to paste:
- Human-readable format
- Organized by file and severity
- Can be posted directly to GitHub
- Great for manual review workflows

## Tips & Best Practices

### For Best Results

1. **Use Specific Categories**: If you know what you're looking for, disable unneeded categories for faster reviews
2. **Set Appropriate Threshold**: Use "medium" for most reviews, "low" for thorough audits
3. **Review Large PRs in Chunks**: Break very large PRs into smaller diffs for better analysis
4. **Add Custom Rules**: Tailor the review to your team's standards

### Performance Tips

1. **Large PRs**: Reviews of 1000+ lines may take 3-5 minutes
2. **Private Repos**: Always provide a GitHub token for private repositories
3. **API Limits**: Be mindful of LLM API rate limits for many reviews

### Troubleshooting

**"API is not running" Error**
- Start the backend: `python main.py`
- Check port 8000 is not in use
- Verify no firewall blocking

**"Review Failed" Error**
- Check backend logs for details
- Verify LLM API keys are configured
- Ensure diff format is valid

**No Findings Returned**
- May indicate clean code (good!)
- Or LLM configuration issue
- Check backend logs for errors

**Slow Performance**
- Large PRs take longer
- Check your internet connection
- Verify LLM API is responding

## Keyboard Shortcuts

Streamlit provides these shortcuts:
- `R`: Rerun the app
- `C`: Clear cache
- `?`: Show keyboard shortcuts

## Privacy & Security

- **API Keys**: Never shared or logged
- **Code Content**: Sent only to configured LLM provider
- **Local Processing**: All orchestration happens locally
- **No Data Storage**: Frontend doesn't store any data (backend may persist reviews)

## Advanced Usage

### Custom API Endpoint

Edit `frontend/app.py` to change the API URL:

```python
API_BASE_URL = "http://your-api-server:8000"
```

### Theming

Customize colors in `frontend/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

### Running on Different Port

```bash
streamlit run frontend/app.py --server.port=8502
```

## Support

For issues or questions:
1. Check backend logs: Look for errors in the API console
2. Check frontend logs: Look for errors in the browser console
3. Review documentation: See main README.md
4. Open an issue: Report bugs on GitHub

---

Happy reviewing! 🚀
