# PR Review Agent - Streamlit Frontend

A user-friendly web interface for the PR Review Agent.

## Features

- 🔍 **GitHub PR Review**: Submit GitHub PR URLs for automated review
- 📝 **Manual Diff Review**: Paste git diff content for analysis
- 📚 **Review History**: View past reviews with filtering options
- ⚙️ **Configurable Analysis**: Customize severity thresholds and analysis categories
- 📊 **Visual Results**: Clear presentation of findings with severity indicators
- 📥 **Export Results**: Download review results as JSON or formatted comments

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure the backend API is running:
```bash
# From the project root
python main.py
```

2. Start the Streamlit frontend:
```bash
# From the frontend directory
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Configuration

The frontend connects to the API at `http://localhost:8000` by default. You can modify this in `app.py`:

```python
API_BASE_URL = "http://localhost:8000"
```

## Usage Guide

### Review GitHub PR
1. Select "GitHub PR URL" mode
2. Enter the full GitHub PR URL
3. (Optional) Add GitHub token for private repos
4. Configure analysis settings in the sidebar
5. Click "Start Review"

### Review Manual Diff
1. Select "Manual Diff" mode
2. Enter repository name
3. Paste your git diff content
4. Configure analysis settings
5. Click "Start Review"

### View History
1. Select "View History" mode
2. (Optional) Apply filters
3. Click "Load History"
4. Expand items to see details

## Troubleshooting

**API Connection Error**
- Ensure the backend is running on port 8000
- Check that no firewall is blocking the connection

**Review Takes Too Long**
- Large PRs may take several minutes to analyze
- The spinner will show progress

**No Findings Returned**
- Check backend logs for errors
- Verify LLM API keys are configured correctly
- Ensure the diff content is valid
