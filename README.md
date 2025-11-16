# LangGraph Production Project

A comprehensive collection of production-ready LangGraph implementations demonstrating core patterns, multi-agent coordination, memory management, and real-world applications. This project showcases best practices for building, testing, and deploying LangGraph applications.

**🚀 Use as Template**: This repository is designed to serve as both a demonstration and a template for building your own LangGraph projects.

### Template Quick Links
- **[Quick Start Guide](QUICKSTART_TEMPLATE.md)** - Get started in 5 minutes
- **[Template Usage Guide](TEMPLATE_USAGE.md)** - Comprehensive template documentation
- **[Setup Checklist](SETUP_CHECKLIST.md)** - Step-by-step customization checklist
- **[Template Graph](graphs/TEMPLATE_GRAPH.py)** - Minimal graph template to copy

## Overview

This project contains 8 production-ready LangGraph implementations in a unified structure. **All graphs launch with a single command** from the project root.

### Graph Categories

- **Studio Graphs (4)**: Demonstration graphs showcasing core LangGraph patterns
  - Parallelization: Parallel web + Wikipedia search
  - Sub-Graphs: Nested graph composition for log analysis
  - Map-Reduce: Map-reduce pattern for joke generation
  - Research Assistant: Multi-agent research with analyst personas

- **Deployment Graphs (1)**: Production-ready implementations with memory persistence
  - Task Maistro: Personal assistant with multi-namespace memory

- **Email Assistant (1)**: Automated email triage and response generation
  - Email Assistant: Intelligent email classification and response

- **Research Agents (2)**: Deep research workflows with multi-agent coordination
  - Research Agent Full: Comprehensive research with user clarification
  - Multi-Agent Supervisor: Supervisor pattern for agent coordination

All graphs are designed to run seamlessly in LangGraph Studio for local development and testing.

## Features

- **Comprehensive Testing**: 26+ test scenarios covering all graph implementations
- **Memory Persistence**: Multi-namespace memory management with Trustcall integration
- **Multi-Agent Coordination**: Parallel agent execution with supervisor patterns
- **Copy-Paste Demos**: Ready-to-use examples in `demo-text.txt` for smooth demonstrations
- **LangSmith Integration**: Built-in tracing and monitoring support

## Prerequisites

- **Python 3.11+** (Python 3.11 or 3.12 recommended)
- **OpenAI API Key** (required for all graphs)
- **Tavily API Key** (required for research and search graphs)
- **LangSmith API Key** (optional but recommended for tracing)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/greenskin44/task-MASter-LangGraph.git
cd task-MASter-LangGraph
```

### 2. Create Virtual Environment

#### Mac/Linux/WSL
```bash
python3 -m venv project-env
source project-env/bin/activate
```

#### Windows PowerShell
```powershell
python -m venv project-env
.\project-env\Scripts\Activate.ps1
```

#### Windows Command Prompt
```cmd
python -m venv project-env
project-env\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including:
- LangGraph and LangChain core libraries
- OpenAI integration
- Tavily web search
- Testing frameworks (pytest)
- Development tools (black, ruff, mypy)

### 4. Configure Environment Variables

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here

# Optional but recommended
LANGSMITH_API_KEY=lsv2_pt_your-langsmith-key-here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=task-MASter-LangGraph
```

**Getting API Keys:**
- **OpenAI**: Sign up at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Tavily**: Sign up at [https://tavily.com](https://tavily.com) (generous free tier)
- **LangSmith**: Sign up at [https://smith.langchain.com](https://smith.langchain.com)

### 5. Run LangGraph Studio

**One command launches all 8 graphs:**

```bash
langgraph dev
```

You should see output like:

```
✓ Starting LangGraph API server...
✓ Loaded 8 graphs:
  - parallelization
  - sub_graphs
  - map_reduce
  - research_assistant
  - task_maistro
  - email_assistant
  - research_agent_full
  - multi_agent_supervisor
✓ Server running at http://127.0.0.1:2024
```

**API Endpoints:**
- API: http://127.0.0.1:2024
- Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- API Docs: http://127.0.0.1:2024/docs

### 6. Open LangGraph Studio

Navigate to the Studio UI in your browser:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**All 8 graphs will appear in the dropdown menu.** Select any graph and use examples from `demo-text.txt` to test!

## Project Structure

```
task-MASter-LangGraph/
├── langgraph.json               # Unified config for ALL 8 graphs
├── requirements.txt             # All dependencies (pinned versions)
├── .env                         # Environment variables (API keys)
├── .env.example                 # Environment variable template
├── demo-text.txt                # Copy-paste ready examples
├── README.md                    # This file
│
├── graphs/                      # All graph implementations
│   ├── studio/                  # 4 demo graphs
│   │   ├── parallelization.py       # Parallel web + Wikipedia search
│   │   ├── sub_graphs.py            # Nested graph composition
│   │   ├── map_reduce.py            # Map-reduce joke generation
│   │   └── research_assistant.py    # Multi-agent research
│   │
│   ├── deployment/              # 1 production graph
│   │   ├── task_maistro.py          # Personal assistant with memory
│   │   └── configuration.py         # Configuration management
│   │
│   ├── email_assistant/         # 1 email processing graph
│   │   ├── email_assistant.py       # Email triage and response
│   │   ├── configuration.py         # Configuration management
│   │   ├── prompts.py               # Email processing prompts
│   │   ├── schemas.py               # Pydantic models
│   │   ├── utils.py                 # Utility functions
│   │   └── tools/                   # Email-related tools
│   │
│   └── research/                # 2 research agent graphs
│       ├── research_agent_full.py   # Full research workflow
│       ├── multi_agent_supervisor.py # Multi-agent coordination
│       ├── prompts.py               # Research prompts
│       ├── utils.py                 # Utility functions
│       └── state_*.py               # State definitions
│
├── tests/                       # Comprehensive test suite
│   ├── test_studio_graphs.py    # Studio graph tests
│   ├── test_deployment_graphs.py # Deployment tests
│   ├── test_email_assistant.py  # Email assistant tests
│   └── test_research_agent.py   # Research agent tests
│
├── docs/                        # Documentation
│   ├── DEMO_GUIDE.md            # Step-by-step demo walkthrough
│   ├── MAINTENANCE_NOTES.md     # Known limitations and improvements
│   ├── TESTING_RESULTS.md       # Test execution results
│   ├── ARCHITECTURE_DESIGN.md   # Architecture and design decisions
│   └── [other docs]             # Additional documentation
```

### Key Structure Features

- **Unified Configuration:** Single `langgraph.json` at root registers all 8 graphs
- **One Command:** `langgraph dev` launches everything
- **Clear Organization:** Graphs organized by category in `graphs/` folder
- **Production Ready:** All graphs tested and working

## Running Tests

The project includes a comprehensive test suite with 26+ test scenarios.

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Studio graphs only
pytest tests/test_studio_graphs.py -v

# Deployment graphs only
pytest tests/test_deployment_graphs.py -v

# Email assistant only
pytest tests/test_email_assistant.py -v

# Research agent only
pytest tests/test_research_agent.py -v
```

### Run Tests by Marker

```bash
# Integration tests (use real APIs)
pytest -m integration -v

# Unit tests (mocked dependencies)
pytest -m unit -v

# Specific graph category
pytest -m studio -v
pytest -m deployment -v
```

### Test with Coverage

```bash
pytest --cov=graphs tests/
```

**Note**: Tests require `OPENAI_API_KEY` to be set. Tests will automatically skip if API keys are missing.

## Performance Benchmarking

The project includes a performance benchmarking suite to measure execution times and detect performance regressions.

### Run Benchmarks

```bash
# Run all benchmarks
pytest tests/test_benchmarks.py --benchmark-only

# Run with convenience script
python scripts/run_benchmarks.py
```

### Save Baseline Metrics

```bash
# Save results as baseline
pytest tests/test_benchmarks.py --benchmark-only --benchmark-save=baseline

# Or use the script
python scripts/run_benchmarks.py --save baseline
```

### Compare Performance

```bash
# Compare with baseline
pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline

# Or use the script
python scripts/run_benchmarks.py --compare baseline
```

### Generate Performance Reports

```bash
# Generate histogram
python scripts/run_benchmarks.py --histogram

# Fail if performance degrades by >10%
pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline --benchmark-compare-fail=mean:10%
```

See **[docs/PERFORMANCE_BENCHMARKS.md](docs/PERFORMANCE_BENCHMARKS.md)** for detailed benchmarking documentation, baseline metrics, and optimization strategies.

## Using Demo Examples

The `demo-text.txt` file contains copy-paste ready examples for all graphs. To use them:

1. Start LangGraph Studio (see "Run LangGraph Studio" above)
2. Open `demo-text.txt` in a text editor
3. Find the graph you want to test
4. Copy the example input
5. Paste into the Studio UI input field
6. Click "Run" and observe the results

All examples are designed to work without modification!

## Graph Descriptions

### Studio Graphs

#### 1. Parallelization
Demonstrates parallel execution by simultaneously searching the web (Tavily) and Wikipedia, then synthesizing results.

**Use Case**: Answering questions that benefit from multiple information sources

**Example Input**:
```json
{
  "question": "What is LangGraph?"
}
```

#### 2. Sub-Graphs
Demonstrates nested graph composition with two parallel sub-graphs for log analysis.

**Use Case**: Processing data through multiple specialized workflows

**Example Input**:
```json
{
  "raw_logs": [
    {"id": "1", "question": "How do I use Chroma?", "grade": 2, "feedback": "Poor quality"}
  ]
}
```

#### 3. Map-Reduce
Demonstrates the map-reduce pattern using Send() API for parallel joke generation and selection.

**Use Case**: Generating multiple options and selecting the best one

**Example Input**:
```json
{
  "topic": "artificial intelligence"
}
```

#### 4. Research Assistant
Demonstrates multi-agent research with analyst personas conducting parallel interviews.

**Use Case**: Comprehensive research from multiple perspectives

**Example Input**:
```json
{
  "topic": "LangGraph architecture patterns",
  "max_analysts": 2,
  "human_analyst_feedback": "approve"
}
```

### Deployment Graphs

#### Task Maistro
Production-ready personal assistant with multi-namespace memory (profile, todos, instructions).

**Use Case**: Personal task management with long-term memory

**Example Input**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need to finish the project report by Friday"
    }
  ]
}
```

**Configuration**:
```json
{
  "configurable": {
    "user_id": "user_123",
    "todo_category": "work",
    "thread_id": "thread_001"
  }
}
```

### Email Assistant Graphs

#### Email Assistant
Automated email triage and response generation with intelligent classification into three categories: respond, notify, or ignore.

**Use Case**: Processing incoming emails and drafting appropriate responses

**Example Input**:
```json
{
  "email_input": {
    "id": "email_001",
    "thread_id": "thread_001",
    "from_email": "sarah.johnson@techcorp.com",
    "to_email": "greenskin44@email.com",
    "subject": "Quick sync on API documentation",
    "page_content": "Hi Lance,\n\nI hope this email finds you well. I wanted to reach out about the API documentation for the new LangChain endpoints. We're planning to integrate them into our product next week.\n\nCould we schedule a 30-minute call this week to discuss the authentication flow and rate limits? I'm available Tuesday afternoon or Thursday morning.\n\nLooking forward to hearing from you!\n\nBest regards,\nSarah Johnson\nSenior Engineer, TechCorp",
    "send_time": "2024-01-15T09:30:00Z"
  }
}
```

### Research Agent Graphs

#### Research Agent Full
Comprehensive research workflow with user clarification, research brief generation, multi-agent coordination, and report synthesis.

**Use Case**: Deep research on complex topics requiring multiple perspectives

**Example Input**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I'm building a production LangGraph application and need to understand deployment options, monitoring strategies, and scaling patterns."
    }
  ]
}
```

**Configuration**:
```json
{
  "configurable": {
    "thread_id": "research_thread_001"
  }
}
```

#### Multi-Agent Supervisor
Supervisor pattern for coordinating multiple research agents working in parallel on different aspects of a research topic.

**Use Case**: Complex research tasks requiring parallel investigation and synthesis

**Example Input**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Research the latest developments in large language model architectures"
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### Issue: `langgraph: command not found`

**Solution**: Make sure you've installed dependencies and activated your virtual environment:

```bash
# Activate virtual environment
source project-env/bin/activate  # Mac/Linux
.\project-env\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Issue: `Error: Missing API key`

**Solution**: Verify your `.env` file exists and contains valid API keys:

```bash
# Check if .env exists
ls -la .env  # Mac/Linux
dir .env     # Windows

# Verify contents (don't commit this file!)
cat .env     # Mac/Linux
type .env    # Windows
```

Make sure there are no quotes around the API keys in the `.env` file:

```bash
# Correct
OPENAI_API_KEY=sk-abc123

# Incorrect
OPENAI_API_KEY="sk-abc123"
```

#### Issue: `ModuleNotFoundError: No module named 'langgraph'`

**Solution**: Install dependencies in your virtual environment:

```bash
pip install -r requirements.txt
```

#### Issue: Studio UI shows "Connection Error"

**Solution**: 
1. Verify `langgraph dev` is running without errors
2. Check that port 2024 is not in use by another application
3. Try restarting the dev server
4. Check firewall settings

#### Issue: Tests fail with "API key not set"

**Solution**: Set the API key as an environment variable before running tests:

```bash
# Mac/Linux
export OPENAI_API_KEY="your-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY = "your-key-here"

# Windows Command Prompt
set OPENAI_API_KEY=your-key-here
```

#### Issue: Slow graph execution

**Solution**: 
- This is normal for graphs making multiple API calls
- Research Assistant can take 30-90 seconds due to parallel agent coordination
- Check your internet connection
- Verify API rate limits haven't been exceeded

#### Issue: Python version mismatch

**Solution**: This project requires Python 3.11+. Check your version:

```bash
python --version
```

If you have multiple Python versions, specify the correct one:

```bash
python3.11 -m venv project-env
```

#### Issue: Import errors in tests

**Solution**: Make sure you're running tests from the project root:

```bash
cd /path/to/task-MASter-LangGraph
pytest tests/ -v
```

#### Issue: Graph not appearing in Studio dropdown

**Solution**: 
1. Check `langgraph.json` configuration in the directory where you ran `langgraph dev`
2. Verify the graph file path is correct
3. Ensure the graph is properly exported (e.g., `graph = builder.compile()`)
4. Restart `langgraph dev`

### Getting Help

If you encounter issues not covered here:

1. Check the [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
2. Review the `docs/MAINTENANCE_NOTES.md` for known limitations
3. Check the `docs/TESTING_RESULTS.md` for test-specific issues
4. Open an issue in the project repository

### Running Code Quality Checks

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy graphs/
```

### CI/CD Pipeline

The project includes automated CI/CD workflows:

- **GitHub Actions**: Automated testing and code quality checks on every push/PR
- **Pre-commit Hooks**: Local code quality enforcement before commits
- **Dependabot**: Automated weekly dependency updates

#### Setting Up Pre-commit Hooks

Install pre-commit hooks for local development:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

Pre-commit will automatically run Black, Ruff, and Mypy before each commit.

#### Development Dependencies

Install all development tools:

```bash
pip install -r requirements-dev.txt
```

This includes:
- Code quality tools (black, ruff, mypy)
- Pre-commit hooks
- Type stubs

See **[docs/CI_CD_SETUP.md](docs/CI_CD_SETUP.md)** for complete CI/CD documentation.

### Adding New Graphs

See `docs/MAINTENANCE_NOTES.md` for guidance on:
- Adding new graph implementations
- Updating dependencies
- Extending the test suite
- Contributing to the project

## Documentation

- **[ARCHITECTURE_DESIGN.md](docs/ARCHITECTURE_DESIGN.md)**: Detailed architecture and design decisions
- **[DEMO_GUIDE.md](docs/DEMO_GUIDE.md)**: Step-by-step walkthrough for demonstrating each graph
- **[MAINTENANCE_NOTES.md](docs/MAINTENANCE_NOTES.md)**: Known limitations, technical debt, and future improvements
- **[TESTING_RESULTS.md](docs/TESTING_RESULTS.md)**: Comprehensive test execution results
- **[PERFORMANCE_BENCHMARKS.md](docs/PERFORMANCE_BENCHMARKS.md)**: Performance benchmarking guide and baseline metrics

- **[TESTING_PLAN.md](docs/TESTING_PLAN.md)**: Testing strategy and scenarios

## License

This project is licensed under the MIT License. See the project metadata in `pyproject.toml` for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Development setup
- Code quality standards
- Testing requirements
- Pull request process
- Code of conduct

## Acknowledgments

This project was inspired by and built upon concepts from the [LangChain Academy](https://academy.langchain.com/) courses, which provide excellent educational resources for learning LangGraph and multi-agent systems.

Special thanks to:
- **Lance Martin** for the Task Maistro graph implementation, which demonstrates production-ready memory management patterns with Trustcall integration
- The **LangChain team** for developing and maintaining [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
- The **LangChain Academy** for providing comprehensive courses on LangGraph patterns and best practices
