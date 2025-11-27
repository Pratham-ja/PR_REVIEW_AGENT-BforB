# PR Review Agent 🤖

An intelligent, multi-agent system for automated Pull Request code reviews using LangGraph and LLM-powered analysis.

## 🌟 Features

- **Multi-Agent Architecture**: Four specialized AI agents analyze code concurrently:
  - 🐛 **Logic Analyzer**: Detects logical errors, null pointers, unreachable code
  - 📖 **Readability Analyzer**: Evaluates code clarity, complexity, and maintainability
  - ⚡ **Performance Analyzer**: Identifies inefficient algorithms and optimization opportunities
  - 🔒 **Security Analyzer**: Finds vulnerabilities like SQL injection, XSS, and auth issues

- **Flexible Input**: Review code from GitHub PR URLs or manual diff input
- **Comprehensive Analysis**: Supports Python, JavaScript, Java, C/C++, and Go
- **Fault Tolerant**: Individual agent failures don't prevent review completion
- **Configurable**: Adjust severity thresholds, enable/disable categories, add custom rules
- **Persistent Storage**: Full review history with queryable database
- **REST API**: Easy integration with CI/CD pipelines

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Docker)
- OpenAI API key or Anthropic API key

### Quick Start (Backend + Frontend)

The fastest way to get started:

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start both backend and frontend
python run_all.py
```

Then open `http://localhost:8501` in your browser! 🎉

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd pr-review-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 🎨 Frontend (Streamlit UI)

### Installation

1. **Install frontend dependencies**
```bash
pip install -r frontend/requirements.txt
```

2. **Start the backend API** (if not already running)
```bash
python main.py
```

3. **Start the frontend**
```bash
python run_frontend.py
# Or directly:
streamlit run frontend/app.py
```

4. **Access the UI**
Open your browser to `http://localhost:8501`

### Frontend Features

- 🔍 **GitHub PR Review**: Submit PR URLs with one click
- 📝 **Manual Diff Review**: Paste git diff content for instant analysis
- 📚 **Review History**: Browse and filter past reviews
- ⚙️ **Configurable Settings**: Customize severity thresholds and analysis categories
- 📊 **Visual Results**: Color-coded findings with severity indicators
- 📥 **Export Options**: Download results as JSON or formatted comments

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. **Start services**
```bash
docker-compose up -d
```

3. **Check status**
```bash
docker-compose ps
docker-compose logs -f api
```

4. **Stop services**
```bash
docker-compose down
```

### Using Docker only

```bash
# Build image
docker build -t pr-review-agent .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  --name pr-review-api \
  pr-review-agent
```

## 📖 API Documentation

### Interactive Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Create Review

**POST** `/api/reviews`

Review a GitHub PR or manual diff.

**Request Body:**
```json
{
  "pr_url": "https://github.com/owner/repo/pull/123",
  "github_token": "optional_token",
  "config": {
    "severity_threshold": "medium",
    "enabled_categories": ["logic", "security", "performance", "readability"],
    "custom_rules": {}
  }
}
```

Or with manual diff:
```json
{
  "diff_content": "diff --git a/file.py...",
  "repository": "owner/repo",
  "pr_number": 123,
  "config": {...}
}
```

**Response:**
```json
{
  "review_id": "uuid",
  "pr_metadata": {...},
  "findings": [
    {
      "file_path": "src/api.py",
      "line_number": 42,
      "severity": "high",
      "category": "security",
      "description": "SQL injection vulnerability detected",
      "suggestion": "Use parameterized queries",
      "agent_source": "security_analyzer"
    }
  ],
  "summary": {
    "total_findings": 5,
    "findings_by_severity": {"high": 2, "medium": 3},
    "findings_by_category": {"security": 2, "performance": 3}
  },
  "formatted_comments": "# Code Review Results\n...",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Get Review History

**GET** `/api/reviews/history`

Query parameters:
- `repository`: Filter by repository
- `pr_number`: Filter by PR number
- `start_date`: Filter by start date
- `end_date`: Filter by end date
- `severity`: Filter by severity level
- `category`: Filter by category
- `limit`: Maximum results (default: 100)
- `offset`: Pagination offset (default: 0)

#### Get Review Status

**GET** `/api/reviews/{review_id}/status`

Returns the status of a specific review.

#### Get Review Details

**GET** `/api/reviews/{review_id}`

Returns complete review details including all findings.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token

# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4  # or claude-3-opus-20240229

# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/pr_review_agent

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RATE_LIMIT=10  # requests per minute per IP

# Logging
LOG_LEVEL=INFO

# Agent Configuration
AGENT_TIMEOUT=30  # seconds
MAX_FILES_PER_REVIEW=50
MAX_DIFF_LINES=10000
```

### Review Configuration

Configure reviews via API request:

```json
{
  "config": {
    "severity_threshold": "medium",  // "low", "medium", "high", "critical"
    "enabled_categories": [
      "logic",
      "readability", 
      "performance",
      "security"
    ],
    "custom_rules": {
      "max_function_length": 50,
      "require_docstrings": true
    }
  }
}
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI REST API                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  PR Review Service                       │
│  (Coordinates: Fetch → Parse → Analyze → Format)        │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│GitHub Client │  │ Diff Parser  │  │ Orchestrator │
└──────────────┘  └──────────────┘  └──────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
            ┌──────────────┐        ┌──────────────┐        ┌──────────────┐
            │Logic Analyzer│        │Readability   │        │Performance   │
            │    Agent     │        │Analyzer Agent│        │Analyzer Agent│
            └──────────────┘        └──────────────┘        └──────────────┘
                    ▼                         ▼                         ▼
            ┌──────────────┐        ┌──────────────────────────────────────┐
            │Security      │        │      Comment Generator               │
            │Analyzer Agent│        │  (Formats findings as markdown)      │
            └──────────────┘        └──────────────────────────────────────┘
                    │                         │
                    └─────────────────────────┼─────────────────────────┘
                                              ▼
                                    ┌──────────────────┐
                                    │Review Repository │
                                    │  (PostgreSQL)    │
                                    └──────────────────┘
```

## 🧪 Testing

Run tests:
```bash
# All tests
pytest

# Specific test file
pytest tests/test_security_analyzer.py

# With coverage
pytest --cov=. --cov-report=html
```

## 📝 Example Usage

### Python Script

```python
import asyncio
from services import PRReviewService, LLMClientFactory, LLMProvider
from models import ReviewConfig

async def review_pr():
    # Create LLM client
    llm_factory = LLMClientFactory()
    llm = llm_factory.create_client(
        provider=LLMProvider.OPENAI,
        api_key="your_key",
        model="gpt-4"
    )
    
    # Create service
    service = PRReviewService(
        llm=llm,
        github_token="your_github_token"
    )
    
    # Configure review
    config = ReviewConfig(
        severity_threshold="medium",
        enabled_categories=["logic", "security"]
    )
    
    # Review PR
    response = await service.review_pr_from_url(
        pr_url="https://github.com/owner/repo/pull/123",
        config=config
    )
    
    print(f"Found {len(response.findings)} issues")
    print(response.formatted_comments)

asyncio.run(review_pr())
```

### cURL

```bash
# Review a PR
curl -X POST http://localhost:8000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "pr_url": "https://github.com/owner/repo/pull/123",
    "github_token": "your_token",
    "config": {
      "severity_threshold": "medium",
      "enabled_categories": ["logic", "security"]
    }
  }'

# Get review history
curl "http://localhost:8000/api/reviews/history?repository=owner/repo&limit=10"

# Get review status
curl http://localhost:8000/api/reviews/{review_id}/status
```

## 🔒 Security

- **Rate Limiting**: 10 requests per minute per IP (configurable)
- **API Key Authentication**: Optional API key support
- **CORS**: Configurable cross-origin resource sharing
- **Security Headers**: Automatic security headers on all responses
- **Token Security**: GitHub and API tokens never logged or exposed

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for the REST API
- Uses [OpenAI](https://openai.com/) or [Anthropic](https://anthropic.com/) LLMs for analysis

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Made with ❤️ by the PR Review Agent team
