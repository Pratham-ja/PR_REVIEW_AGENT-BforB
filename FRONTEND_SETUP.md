# Frontend Setup Guide 🚀

Complete setup guide for the PR Review Agent Streamlit frontend.

## What You Get

A beautiful, user-friendly web interface with:
- ✅ GitHub PR review with one click
- ✅ Manual diff paste and review
- ✅ Review history browser
- ✅ Configurable analysis settings
- ✅ Visual results with color-coded severity
- ✅ Export to JSON or formatted comments

## Installation

### Step 1: Install Dependencies

```bash
# Install all dependencies (includes Streamlit)
pip install -r requirements.txt

# Or install just frontend dependencies
pip install -r frontend/requirements.txt
```

### Step 2: Configure Backend

Make sure your `.env` file is configured:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here
```

### Step 3: Test Connection

```bash
# Test if backend can connect to frontend
python test_frontend.py
```

## Running the Application

### Option 1: Run Everything (Recommended)

Start both backend and frontend with one command:

```bash
python run_all.py
```

This will:
1. Start the backend API on port 8000
2. Start the frontend UI on port 8501
3. Open your browser automatically
4. Monitor both processes

Press `Ctrl+C` to stop both services.

### Option 2: Run Separately

**Terminal 1 - Backend:**
```bash
python main.py
```

**Terminal 2 - Frontend:**
```bash
python run_frontend.py
# Or directly:
streamlit run frontend/app.py
```

### Option 3: Custom Configuration

```bash
# Run on different port
streamlit run frontend/app.py --server.port=8502

# Run on specific address
streamlit run frontend/app.py --server.address=0.0.0.0

# Disable CORS
streamlit run frontend/app.py --server.enableCORS=false
```

## Accessing the UI

Once running, open your browser to:
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## First Time Usage

### 1. Check API Status

The UI will show a green checkmark if the backend is running:
```
✅ API is running
```

If you see an error:
```
⚠️ API is not running. Please start the backend server.
```

Start the backend with: `python main.py`

### 2. Try a Sample Review

**Using Manual Diff:**

1. Select "Manual Diff" mode
2. Enter repository: `test/repo`
3. Copy the example diff from `frontend/example_diff.txt`
4. Paste into the "Diff Content" field
5. Click "🚀 Start Review"
6. Wait 30-60 seconds for results

**Using GitHub PR:**

1. Select "GitHub PR URL" mode
2. Enter a public PR URL (e.g., from a popular open-source project)
3. Click "🚀 Start Review"
4. Wait 1-5 minutes depending on PR size

### 3. Explore Results

- View findings organized by severity
- Filter by category
- Download results as JSON
- Export formatted comments

## Configuration

### Analysis Settings (Sidebar)

**Severity Threshold:**
- `low`: Show all findings
- `medium`: Show medium, high, critical
- `high`: Show high and critical only
- `critical`: Show only critical issues

**Analysis Categories:**
- ✅ Logic: Bugs and logical errors
- ✅ Security: Vulnerabilities
- ✅ Performance: Optimization opportunities
- ✅ Readability: Code quality

**Custom Rules:**
Add specific requirements for your codebase.

### API Configuration

Edit `frontend/app.py` to change the API URL:

```python
API_BASE_URL = "http://localhost:8000"
```

For remote backend:
```python
API_BASE_URL = "https://your-api-server.com"
```

### Theme Customization

Edit `frontend/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"      # Blue
backgroundColor = "#ffffff"    # White
secondaryBackgroundColor = "#f0f2f6"  # Light gray
textColor = "#262730"         # Dark gray
```

## Troubleshooting

### API Connection Issues

**Problem:** "API is not running" error

**Solutions:**
1. Start backend: `python main.py`
2. Check port 8000 is not in use: `netstat -ano | findstr :8000`
3. Verify no firewall blocking
4. Check backend logs for errors

### Review Failures

**Problem:** "Review failed" error

**Solutions:**
1. Check backend logs for details
2. Verify LLM API keys in `.env`
3. Ensure diff format is valid
4. Try with smaller diff content

### Slow Performance

**Problem:** Reviews take too long

**Causes:**
- Large PRs (1000+ lines) take 3-5 minutes
- LLM API rate limits
- Network latency

**Solutions:**
- Break large PRs into smaller chunks
- Check internet connection
- Verify LLM API is responding

### Port Already in Use

**Problem:** Port 8501 already in use

**Solutions:**
```bash
# Find process using port
netstat -ano | findstr :8501

# Kill the process (Windows)
taskkill /PID <process_id> /F

# Or run on different port
streamlit run frontend/app.py --server.port=8502
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
pip install streamlit
# Or
pip install -r frontend/requirements.txt
```

## Advanced Usage

### Running in Production

For production deployment:

1. **Use a reverse proxy** (nginx, Apache)
2. **Enable authentication** (add auth middleware)
3. **Use HTTPS** (SSL certificates)
4. **Set proper CORS** (restrict origins)
5. **Monitor logs** (centralized logging)

Example nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Docker Deployment

Create `Dockerfile.frontend`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ ./frontend/

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -f Dockerfile.frontend -t pr-review-frontend .
docker run -p 8501:8501 pr-review-frontend
```

### Environment Variables

Set these for production:

```bash
# Backend API URL
export API_BASE_URL=https://api.your-domain.com

# Streamlit config
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Development

### Making Changes

1. Edit `frontend/app.py`
2. Save the file
3. Streamlit auto-reloads (or press `R`)

### Adding Features

The app structure:
```
frontend/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── .streamlit/
│   └── config.toml    # Streamlit config
├── README.md          # Frontend docs
└── example_diff.txt   # Sample data
```

Key functions in `app.py`:
- `check_api_health()`: Test API connection
- `submit_review()`: Send review request
- `get_review_history()`: Fetch past reviews
- `display_finding()`: Render a finding
- `display_review_results()`: Show results

### Testing

```bash
# Test API connection
python test_frontend.py

# Manual testing
streamlit run frontend/app.py

# Check for errors in browser console (F12)
```

## Support

### Getting Help

1. **Check logs**: Look for errors in terminal
2. **Browser console**: Press F12 to see JavaScript errors
3. **Backend logs**: Check API console for errors
4. **Documentation**: See FRONTEND_GUIDE.md

### Common Questions

**Q: Can I use this without the backend?**
A: No, the frontend requires the backend API to function.

**Q: Can I customize the UI?**
A: Yes! Edit `frontend/app.py` and `.streamlit/config.toml`.

**Q: Does it work on mobile?**
A: Yes, Streamlit is responsive and works on mobile browsers.

**Q: Can I add authentication?**
A: Yes, you can add Streamlit authentication or use a reverse proxy.

**Q: How do I deploy to cloud?**
A: Use Streamlit Cloud, Heroku, AWS, or any platform supporting Python.

## Next Steps

1. ✅ Complete setup
2. ✅ Test with sample diff
3. ✅ Review a real PR
4. ✅ Explore history
5. ✅ Customize settings
6. ✅ Share with team

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Frontend User Guide](FRONTEND_GUIDE.md)
- [API Documentation](http://localhost:8000/docs)
- [Main README](README.md)

---

Happy reviewing! 🎉
