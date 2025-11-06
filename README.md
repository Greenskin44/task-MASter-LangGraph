# LangGraph Production Project

A comprehensive collection of production-ready LangGraph implementations demonstrating core patterns, multi-agent coordination, memory management, and real-world applications. This project showcases best practices for building, testing, and deploying LangGraph applications.

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

- ✅ **Production-Ready Code**: Follows Python best practices with type hints, docstrings, and error handling
- ✅ **Comprehensive Testing**: 26+ test scenarios covering all graph implementations
- ✅ **Memory Persistence**: Multi-namespace memory management with Trustcall integration
- ✅ **Multi-Agent Coordination**: Parallel agent execution with supervisor patterns
- ✅ **Copy-Paste Demos**: Ready-to-use examples in `demo-text.txt` for smooth demonstrations
- ✅ **LangSmith Integration**: Built-in tracing and monitoring support

## Prerequisites

- **Python 3.11+** (Python 3.11 or 3.12 recommended)
- **OpenAI API Key** (required for all graphs)
- **Tavily API Key** (required for research and search graphs)
- **LangSmith API Key** (optional but recommended for tracing)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd langgraph-project
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
LANGSMITH_PROJECT=langgraph-project
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
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

### 6. Open LangGraph Studio

Navigate to the Studio UI in your browser:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

**All 8 graphs will appear in the dropdown menu.** Select any graph and use examples from `demo-text.txt` to test!

## Project Structure

```
langgraph-project/
├── langgraph.json               # ✨ Unified config for ALL 8 graphs
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
│
├── archive/                     # Archived old structure (reference only)
│   ├── README.md                # Explains what's archived and why
│   ├── studio/                  # Old studio folder
│   ├── deployment/              # Old deployment folder
│   ├── email_assistant/         # Old email assistant (with variants)
│   ├── deep-research-agent/     # Old research agent
│   ├── deep_agents/             # Experimental notebooks
│   └── report-team-MAS-LangGraph/ # Learning materials
│
└── MIGRATION_LOG.md             # Consolidation documentation
```

### Key Structure Features

✨ **Unified Configuration:** Single `langgraph.json` at root registers all 8 graphs  
✨ **One Command:** `langgraph dev` launches everything  
✨ **Clear Organization:** Graphs organized by category in `graphs/` folder  
✨ **No Duplication:** Old scattered folders archived for reference  
✨ **Production Ready:** All graphs tested and working

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
cd /path/to/langgraph-project
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

## Archive Folder

The `archive/` folder contains the original scattered project structure that was consolidated on November 5, 2025. These folders are preserved for reference but are **not used** by the active project:

- **archive/studio/** - Old demo graphs (duplicate of graphs/studio/)
- **archive/deployment/** - Old production graphs (duplicate of graphs/deployment/)
- **archive/email_assistant/** - Old email assistant with unique HITL variants and evaluation tools
- **archive/deep-research-agent/** - Old research agents (duplicate of graphs/research/)
- **archive/deep_agents/** - Experimental notebooks and tools
- **archive/report-team-MAS-LangGraph/** - Learning materials with langmem

**Why archived?** The project was consolidated to use a single `langgraph.json` configuration at the root, eliminating the need for separate folder structures. The archive preserves:
- Historical code for reference
- Unique variants (HITL email assistants, Gmail integration)
- Evaluation tools and datasets
- Learning materials and notebooks
- Original repository history

See `archive/README.md` and `MIGRATION_LOG.md` for complete consolidation details.

## Development

### Code Quality

The project follows Python best practices:

- **Type Hints**: All functions have type annotations
- **Docstrings**: Comprehensive documentation for all modules, classes, and functions
- **Error Handling**: Graceful error handling with meaningful messages
- **PEP 8**: Code formatted with Black and linted with Ruff

### Running Code Quality Checks

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy graphs/
```

### Adding New Graphs

See `docs/MAINTENANCE_NOTES.md` for guidance on:
- Adding new graph implementations
- Updating dependencies
- Extending the test suite
- Contributing to the project

## Documentation

- **[DEMO_GUIDE.md](docs/DEMO_GUIDE.md)**: Step-by-step walkthrough for demonstrating each graph
- **[MAINTENANCE_NOTES.md](docs/MAINTENANCE_NOTES.md)**: Known limitations, technical debt, and future improvements
- **[TESTING_RESULTS.md](docs/TESTING_RESULTS.md)**: Comprehensive test execution results
- **[ARCHITECTURE_DESIGN.md](docs/ARCHITECTURE_DESIGN.md)**: Detailed architecture and design decisions
- **[TESTING_PLAN.md](docs/TESTING_PLAN.md)**: Testing strategy and scenarios

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Acknowledgments

Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain).
