# Design Document: PR Review Agent

## Overview

The PR Review Agent is a backend system that automates code review for GitHub Pull Requests using a multi-agent architecture. The system fetches PR diffs via GitHub API, parses the changes, and orchestrates multiple specialized AI agents to analyze code across four dimensions: logic correctness, readability, performance, and security. Results are aggregated and formatted into structured review comments accessible via REST API.

### Key Design Principles

1. **Multi-Agent Architecture**: Independent specialized agents analyze different aspects of code quality
2. **Concurrent Processing**: Agents run in parallel to minimize review time
3. **Language Agnostic**: Core architecture supports multiple programming languages
4. **Extensibility**: New analyzer agents can be added without modifying core orchestration
5. **Fault Tolerance**: Individual agent failures don't prevent overall review completion

### Technology Stack

- **Backend Framework**: FastAPI (Python) for REST API
- **Agent Orchestration**: LangGraph for multi-agent workflow management
- **LLM Integration**: OpenAI GPT-4 or Anthropic Claude for agent reasoning
- **Database**: PostgreSQL for review history persistence
- **GitHub Integration**: PyGithub library for GitHub API interactions
- **Diff Parsing**: unidiff library for parsing git diffs

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer (FastAPI)                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ Review Endpoint  │  │ History Endpoint │  │ Config Endpoint│ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Service Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PR Review Service                            │  │
│  │  • Coordinates overall review workflow                    │  │
│  │  • Manages configuration and context                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
┌──────────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  GitHub API Client   │ │ Diff Parser  │ │ Review Repository│
│  • Fetch PR data     │ │ • Parse diffs│ │ • Store results  │
│  • Handle auth       │ │ • Extract    │ │ • Query history  │
└──────────────────────┘ │   changes    │ └──────────────────┘
                         └──────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              Review Orchestrator (LangGraph)                     │
│  • Distributes work to analyzer agents                          │
│  • Manages concurrent execution                                 │
│  • Aggregates results                                           │
└─────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                        ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│Logic Analyzer│  │Readability       │  │Performance       │
│Agent         │  │Analyzer Agent    │  │Analyzer Agent    │
└──────────────┘  └──────────────────┘  └──────────────────┘
        ▼                        ▼                        ▼
┌──────────────┐  ┌──────────────────────────────────────────┐
│Security      │  │      Comment Generator                   │
│Analyzer Agent│  │  • Format findings                       │
└──────────────┘  │  • Group by file/line                    │
        │         │  • Generate markdown                     │
        └─────────►└──────────────────────────────────────────┘
```

### Data Flow

1. **Request Reception**: API receives PR URL or diff content with optional configuration
2. **Data Acquisition**: GitHub API Client fetches PR metadata and diff
3. **Diff Parsing**: Diff Parser extracts structured change information
4. **Agent Orchestration**: Review Orchestrator distributes parsed data to analyzer agents
5. **Concurrent Analysis**: Each agent analyzes code changes in parallel
6. **Result Aggregation**: Orchestrator collects findings from all agents
7. **Comment Generation**: Comment Generator formats findings into structured output
8. **Persistence**: Review Repository stores results with metadata
9. **Response**: API returns formatted review comments to client

## Components and Interfaces

### 1. API Layer

**ReviewController**
```python
class ReviewController:
    async def create_review(request: ReviewRequest) -> ReviewResponse
    async def get_review_status(review_id: str) -> ReviewStatus
    async def get_review_history(filters: HistoryFilters) -> List[ReviewResponse]
```

**Models**
```python
class ReviewRequest:
    pr_url: Optional[str]
    repository: Optional[str]
    pr_number: Optional[int]
    diff_content: Optional[str]
    github_token: Optional[str]
    config: Optional[ReviewConfig]

class ReviewConfig:
    severity_threshold: str  # "low", "medium", "high"
    enabled_categories: List[str]  # ["logic", "readability", "performance", "security"]
    custom_rules: Optional[Dict[str, Any]]

class ReviewResponse:
    review_id: str
    pr_metadata: PRMetadata
    findings: List[Finding]
    summary: ReviewSummary
    timestamp: datetime
```

### 2. GitHub API Client

```python
class GitHubAPIClient:
    def __init__(self, token: Optional[str] = None)
    
    async def fetch_pr_data(repo: str, pr_number: int) -> PRData
    async def fetch_pr_diff(repo: str, pr_number: int) -> str
    def parse_pr_url(url: str) -> Tuple[str, int]
```

### 3. Diff Parser

```python
class DiffParser:
    def parse(diff_content: str) -> ParsedDiff
    def detect_language(file_path: str) -> str
    def extract_changes(patch: str) -> List[Change]

class ParsedDiff:
    files: List[FileChange]
    
class FileChange:
    file_path: str
    language: str
    is_binary: bool
    additions: List[LineChange]
    deletions: List[LineChange]
    modifications: List[LineChange]

class LineChange:
    line_number: int
    content: str
    change_type: str  # "add", "delete", "modify"
```

### 4. Review Orchestrator

```python
class ReviewOrchestrator:
    def __init__(self, config: ReviewConfig)
    
    async def orchestrate_review(parsed_diff: ParsedDiff) -> List[Finding]
    async def execute_agents_concurrently(
        agents: List[AnalyzerAgent], 
        context: ReviewContext
    ) -> List[Finding]
    def aggregate_findings(results: List[AgentResult]) -> List[Finding]
```

**LangGraph Workflow**
```python
# Define the agent workflow graph
workflow = StateGraph(ReviewState)

# Add nodes for each agent
workflow.add_node("logic_analyzer", logic_analyzer_node)
workflow.add_node("readability_analyzer", readability_analyzer_node)
workflow.add_node("performance_analyzer", performance_analyzer_node)
workflow.add_node("security_analyzer", security_analyzer_node)
workflow.add_node("aggregator", aggregator_node)

# Define parallel execution
workflow.add_edge(START, "logic_analyzer")
workflow.add_edge(START, "readability_analyzer")
workflow.add_edge(START, "performance_analyzer")
workflow.add_edge(START, "security_analyzer")

# All agents feed into aggregator
workflow.add_edge("logic_analyzer", "aggregator")
workflow.add_edge("readability_analyzer", "aggregator")
workflow.add_edge("performance_analyzer", "aggregator")
workflow.add_edge("security_analyzer", "aggregator")
workflow.add_edge("aggregator", END)
```

### 5. Analyzer Agents

**Base Agent Interface**
```python
class AnalyzerAgent(ABC):
    def __init__(self, llm: BaseLLM, config: AgentConfig)
    
    @abstractmethod
    async def analyze(context: ReviewContext) -> List[Finding]
    
    def create_prompt(context: ReviewContext) -> str
    def parse_llm_response(response: str) -> List[Finding]

class ReviewContext:
    file_changes: List[FileChange]
    language: str
    config: ReviewConfig
```

**Logic Analyzer Agent**
- Analyzes code for logical errors, null pointer issues, unreachable code
- Uses LLM with specialized prompts for bug detection
- Returns findings with severity and line-specific details

**Readability Analyzer Agent**
- Evaluates code complexity, naming conventions, documentation
- Calculates cyclomatic complexity for functions
- Suggests improvements for maintainability

**Performance Analyzer Agent**
- Identifies inefficient algorithms and data structures
- Detects redundant computations and N+1 queries
- Provides optimization recommendations

**Security Analyzer Agent**
- Scans for common vulnerabilities (SQL injection, XSS, etc.)
- Checks input validation and authentication patterns
- Assigns severity levels to security findings

### 6. Comment Generator

```python
class CommentGenerator:
    def generate_comments(findings: List[Finding]) -> FormattedReview
    def group_by_file_and_line(findings: List[Finding]) -> Dict[str, Dict[int, List[Finding]]]
    def format_as_markdown(grouped_findings: Dict) -> str

class Finding:
    file_path: str
    line_number: int
    severity: str  # "low", "medium", "high", "critical"
    category: str  # "logic", "readability", "performance", "security"
    description: str
    suggestion: Optional[str]
    agent_source: str

class FormattedReview:
    markdown_output: str
    structured_comments: List[Comment]
    summary: ReviewSummary
```

### 7. Review Repository

```python
class ReviewRepository:
    async def save_review(review: ReviewResult) -> str
    async def get_review(review_id: str) -> ReviewResult
    async def query_reviews(filters: HistoryFilters) -> List[ReviewResult]
    async def get_reviews_by_pr(repo: str, pr_number: int) -> List[ReviewResult]

class ReviewResult:
    review_id: str
    pr_metadata: PRMetadata
    commit_sha: str
    findings: List[Finding]
    timestamp: datetime
    config_used: ReviewConfig
```

## Data Models

### Database Schema

**reviews table**
```sql
CREATE TABLE reviews (
    review_id UUID PRIMARY KEY,
    repository VARCHAR(255) NOT NULL,
    pr_number INTEGER NOT NULL,
    commit_sha VARCHAR(40) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    config JSONB,
    summary JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_repo_pr (repository, pr_number),
    INDEX idx_timestamp (timestamp)
);
```

**findings table**
```sql
CREATE TABLE findings (
    finding_id UUID PRIMARY KEY,
    review_id UUID REFERENCES reviews(review_id),
    file_path VARCHAR(500) NOT NULL,
    line_number INTEGER NOT NULL,
    severity VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    suggestion TEXT,
    agent_source VARCHAR(50) NOT NULL,
    INDEX idx_review (review_id),
    INDEX idx_severity (severity)
);
```

### Core Data Structures

**PRMetadata**
```python
class PRMetadata:
    repository: str
    pr_number: int
    title: str
    author: str
    commit_sha: str
    base_branch: str
    head_branch: str
```

**ReviewSummary**
```python
class ReviewSummary:
    total_findings: int
    findings_by_severity: Dict[str, int]
    findings_by_category: Dict[str, int]
    files_analyzed: int
    lines_changed: int
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Data Acquisition Properties

Property 1: GitHub API fetch completeness
*For any* valid GitHub PR URL or repository/PR number combination, fetching PR data should return both metadata and diff content
**Validates: Requirements 1.1**

Property 2: File extraction completeness
*For any* GitHub API response containing PR data, extracting changes should identify all modified files with their additions and deletions
**Validates: Requirements 1.2**

Property 3: Token security
*For any* API request using a GitHub token, the token should not appear in logs, error messages, or response bodies
**Validates: Requirements 1.3**

Property 4: Error message clarity
*For any* GitHub API failure, the returned error message should contain the failure reason and be non-empty
**Validates: Requirements 1.4**

Property 5: Manual diff acceptance
*For any* valid git diff content provided as manual input, the system should process it successfully without requiring a PR URL
**Validates: Requirements 1.5**

### Diff Parsing Properties

Property 6: Diff parsing completeness
*For any* valid git diff content, parsing should extract all file paths, line numbers, and change types without loss
**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

Property 7: Language detection accuracy
*For any* file with a recognized extension, the detected language should match the extension's standard language mapping
**Validates: Requirements 11.1**

### Orchestration Properties

Property 8: Agent distribution completeness
*For any* parsed diff and set of enabled analyzer agents, all enabled agents should receive the diff data
**Validates: Requirements 3.1**

Property 9: Result aggregation completeness
*For any* set of agent results, the aggregated findings should contain all findings from all agents without loss
**Validates: Requirements 3.3**

Property 10: Fault tolerance
*For any* agent failure during review, the remaining agents should complete successfully and their findings should appear in results
**Validates: Requirements 3.4**

Property 11: Agent source preservation
*For any* finding in aggregated results, the agent_source field should correctly identify which agent produced the finding
**Validates: Requirements 3.5**

Property 12: Multi-language processing
*For any* PR containing files in multiple languages, each file should be analyzed with rules appropriate to its detected language
**Validates: Requirements 11.4**

### Agent Output Properties

Property 13: Finding structure completeness
*For any* issue identified by the Logic Analyzer Agent, the finding should include line number and non-empty explanation
**Validates: Requirements 4.5**

Property 14: Readability suggestion presence
*For any* issue identified by the Readability Analyzer Agent, the finding should include a specific improvement suggestion
**Validates: Requirements 5.5**

Property 15: Performance impact documentation
*For any* issue identified by the Performance Analyzer Agent, the finding should include performance impact explanation and optimization suggestion
**Validates: Requirements 6.5**

Property 16: Security severity assignment
*For any* vulnerability identified by the Security Analyzer Agent, the finding should include a severity level and remediation guidance
**Validates: Requirements 7.5**

### Comment Generation Properties

Property 17: Comment formatting completeness
*For any* finding, the formatted comment should contain file path, line number, severity, category, and description
**Validates: Requirements 8.1**

Property 18: Finding grouping by location
*For any* set of findings, those with identical file path and line number should be grouped together in the output
**Validates: Requirements 8.2, 8.3**

Property 19: Markdown validity
*For any* formatted review output, the content should be valid markdown syntax
**Validates: Requirements 8.4**

### API Properties

Property 20: Review request processing
*For any* valid review request with PR details, the API should return review results containing findings
**Validates: Requirements 9.1**

Property 21: Response structure conformance
*For any* completed review, the JSON response should contain findings structured by file and category
**Validates: Requirements 9.3**

Property 22: Error response correctness
*For any* processing error, the API response should have an HTTP status code >= 400 and include an error message
**Validates: Requirements 9.4**

Property 23: History retrieval completeness
*For any* PR with stored reviews, requesting history should return all past review results for that PR
**Validates: Requirements 9.5**

### Persistence Properties

Property 24: Review storage completeness
*For any* completed review, storing it should persist all findings, timestamp, and PR metadata
**Validates: Requirements 10.1**

Property 25: Finding association integrity
*For any* stored finding, it should maintain its association with the correct commit SHA and file version
**Validates: Requirements 10.2**

Property 26: Query filtering correctness
*For any* repository filter applied to historical queries, returned results should only include reviews from that repository
**Validates: Requirements 10.3**

Property 27: Review iteration separation
*For any* PR reviewed multiple times, each review should create a distinct record with unique review_id
**Validates: Requirements 10.4**

Property 28: Storage round-trip consistency
*For any* review result, storing then retrieving it should return equivalent data with all findings preserved
**Validates: Requirements 10.5**

### Configuration Properties

Property 29: Severity threshold filtering
*For any* configuration with severity threshold set to "high", returned findings should only include those with severity "high" or "critical"
**Validates: Requirements 12.1**

Property 30: Category disabling
*For any* configuration with a category disabled, the corresponding analyzer agent should not execute
**Validates: Requirements 12.2**

Property 31: Configuration validation
*For any* invalid configuration (e.g., unknown severity level), the system should reject it and return a validation error
**Validates: Requirements 12.5**

## Error Handling

### Error Categories

1. **GitHub API Errors**
   - Authentication failures (401)
   - Rate limiting (403)
   - Not found (404)
   - Network timeouts

2. **Parsing Errors**
   - Invalid diff format
   - Corrupted content
   - Unsupported encoding

3. **Agent Execution Errors**
   - LLM API failures
   - Timeout during analysis
   - Invalid agent responses

4. **Storage Errors**
   - Database connection failures
   - Constraint violations
   - Query timeouts

### Error Handling Strategy

**Graceful Degradation**
- Individual agent failures don't prevent review completion
- Partial results are returned when some agents succeed
- Failed agents are logged with error details

**Retry Logic**
- GitHub API calls: 3 retries with exponential backoff
- LLM API calls: 2 retries with 1-second delay
- Database operations: 2 retries for transient failures

**Error Response Format**
```python
class ErrorResponse:
    error_code: str
    message: str
    details: Optional[Dict[str, Any]]
    timestamp: datetime
```

**Logging**
- All errors logged with context (request ID, PR details, agent name)
- Structured logging for easy querying
- Sensitive data (tokens) excluded from logs

## Testing Strategy

### Unit Testing

**Framework**: pytest for Python components

**Coverage Areas**:
- Diff Parser: Test parsing of various diff formats, edge cases (empty diffs, binary files)
- GitHub API Client: Mock GitHub API responses, test error handling
- Comment Generator: Test formatting, grouping, markdown generation
- Review Repository: Test CRUD operations, query filtering

**Example Unit Tests**:
```python
def test_diff_parser_extracts_additions():
    diff = """
    diff --git a/file.py b/file.py
    +def new_function():
    +    return True
    """
    result = DiffParser().parse(diff)
    assert len(result.files[0].additions) == 2

def test_comment_generator_groups_by_line():
    findings = [
        Finding(file="test.py", line=10, category="logic"),
        Finding(file="test.py", line=10, category="security")
    ]
    result = CommentGenerator().generate_comments(findings)
    assert len(result.structured_comments) == 1  # Grouped into one comment
```

### Property-Based Testing

**Framework**: Hypothesis for Python

**Configuration**: Each property test should run minimum 100 iterations

**Test Tagging**: Each property-based test must include a comment with format:
`# Feature: pr-review-agent, Property {number}: {property_text}`

**Coverage Areas**:
- Diff parsing with randomly generated diffs
- Agent orchestration with various agent configurations
- Comment generation with random finding sets
- API request/response validation

### Integration Testing

**Test Scenarios**:
1. End-to-end review flow: Submit PR URL → Receive formatted comments
2. Multi-agent coordination: Verify all agents execute and contribute findings
3. Database persistence: Store and retrieve review results
4. Error recovery: Simulate agent failures and verify graceful degradation

**Test Environment**:
- Mock GitHub API server for consistent test data
- Test database with sample review data
- Mock LLM responses for deterministic agent behavior

### Agent Behavior Testing

**Approach**: Example-based testing with known code issues

**Test Data**:
- Code samples with known bugs (null pointers, infinite loops)
- Code with readability issues (high complexity, poor naming)
- Code with performance problems (N+1 queries, inefficient algorithms)
- Code with security vulnerabilities (SQL injection, XSS)

**Validation**:
- Verify agents detect known issues
- Check finding quality (line numbers, descriptions, suggestions)
- Ensure no false positives on clean code samples

## Implementation Notes

### LLM Integration

**Prompt Engineering**:
- Each agent has specialized system prompts for its analysis domain
- Prompts include examples of good findings
- Output format specified in prompts for consistent parsing

**Example Logic Analyzer Prompt**:
```
You are a code review expert specializing in logic errors and bugs.
Analyze the following code changes and identify:
- Null pointer dereferences
- Unreachable code
- Infinite loops or off-by-one errors
- Incorrect parameter usage

For each issue found, provide:
- Line number
- Issue description
- Severity (low/medium/high/critical)
- Suggested fix

Code changes:
{code_changes}

Return findings in JSON format:
[{"line": 10, "description": "...", "severity": "high", "suggestion": "..."}]
```

**Response Parsing**:
- Agents parse LLM JSON responses into Finding objects
- Validation ensures required fields are present
- Malformed responses trigger retry or fallback to empty findings

### Concurrency

**Agent Execution**:
- LangGraph manages parallel agent execution
- Each agent runs in separate async task
- Timeout of 30 seconds per agent to prevent hanging

**Database Access**:
- Connection pooling for concurrent queries
- Async database driver (asyncpg) for non-blocking operations
- Transaction isolation for review storage

### Performance Optimization

**Caching**:
- GitHub API responses cached for 5 minutes (same PR may be reviewed multiple times during development)
- Language detection results cached by file extension

**Batching**:
- Multiple file changes sent to agents in batches
- Database inserts batched for findings (bulk insert)

**Resource Limits**:
- Maximum 50 files per review (reject larger PRs with error message)
- Maximum 10,000 lines of diff content
- Agent timeout prevents runaway LLM calls

### Security Considerations

**Token Management**:
- GitHub tokens stored in environment variables or secure vault
- Tokens never logged or included in responses
- Token validation before use

**Input Validation**:
- PR URLs validated against GitHub URL format
- Diff content size limited to prevent DoS
- Configuration validated against schema

**API Security**:
- Rate limiting on review endpoint (10 requests per minute per IP)
- API key authentication for production use
- CORS configured for allowed origins

### Deployment

**Architecture**:
- Containerized FastAPI application (Docker)
- PostgreSQL database (managed service or container)
- Environment-based configuration (dev/staging/prod)

**Scaling**:
- Horizontal scaling of API instances behind load balancer
- Database connection pooling
- Async processing allows high concurrency per instance

**Monitoring**:
- Metrics: Request rate, review duration, agent success rate
- Logging: Structured logs to centralized logging service
- Alerts: Failed reviews, high error rates, slow response times
