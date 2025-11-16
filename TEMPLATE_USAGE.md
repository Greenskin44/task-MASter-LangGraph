# Using This Project as a Template

This repository serves as both a **demonstration of LangGraph capabilities** and a **template for building new LangGraph projects**. Follow this guide to use it as a starting point for your own LangGraph applications.

## Why Use This as a Template?

This project provides:

- **Production-ready structure** with best practices for organizing LangGraph applications
- **Comprehensive testing setup** with pytest, benchmarking, and CI/CD integration
- **Pre-configured development environment** with code quality tools (Black, Ruff, Mypy)
- **Working examples** of 8 different graph patterns you can learn from and modify
- **Complete documentation** templates for architecture, testing, and maintenance
- **GitHub Actions workflows** for automated testing and dependency management
- **Unified configuration** that makes it easy to add new graphs

## Quick Start: Creating a New Project from This Template

### Option 1: Use GitHub's Template Feature (Recommended)

1. Click "Use this template" button on GitHub (green button at top of repository)
2. Choose "Create a new repository"
3. Name your new repository
4. Clone your new repository and follow the setup below

### Option 2: Manual Clone and Customize

1. **Clone this repository**
   ```bash
   git clone https://github.com/greenskin44/task-MASter-LangGraph.git my-langgraph-project
   cd my-langgraph-project
   ```

2. **Remove existing git history** (start fresh)
   ```bash
   # Windows PowerShell
   Remove-Item -Recurse -Force .git
   git init
   
   # Mac/Linux
   rm -rf .git
   git init
   ```

3. **Customize the project**
   - Update `pyproject.toml` with your project name and details
   - Update `README.md` with your project description
   - Update `.env.example` with your required API keys
   - Modify `langgraph.json` to include only the graphs you need

4. **Create your first commit**
   ```bash
   git add .
   git commit -m "Initial commit from template"
   ```

## Customizing for Your Project

### 1. Update Project Metadata

Edit `pyproject.toml`:

```toml
[project]
name = "your-project-name"
version = "0.1.0"
description = "Your project description"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]

[project.urls]
Homepage = "https://github.com/yourusername/your-project"
Repository = "https://github.com/yourusername/your-project"
```

### 2. Clean Up Example Graphs (Optional)

If you want to start fresh without the example graphs:

```bash
# Remove all example graphs
rm -r graphs/studio graphs/deployment graphs/email_assistant graphs/research

# Create your own graph directory
mkdir graphs/my_graph
```

Or keep the examples as references and add your own alongside them.

### 3. Update Configuration Files

**langgraph.json**: Define which graphs to load

```json
{
  "graphs": {
    "my_custom_graph": "./graphs/my_graph/my_graph.py:graph"
  },
  "env": "./.env",
  "python_version": "3.11",
  "dependencies": ["./requirements.txt"]
}
```

**.env.example**: List required API keys

```bash
# Your Custom API Keys
YOUR_API_KEY=xxx
ANOTHER_SERVICE_KEY=yyy
```

### 4. Update Documentation

- **README.md**: Describe your specific graphs and use cases
- **CONTRIBUTING.md**: Customize contribution guidelines for your project
- **docs/**: Update or remove documentation files as needed

## Building Your First Graph

### Step 1: Create Graph Structure

```bash
mkdir -p graphs/my_graph
touch graphs/my_graph/__init__.py
touch graphs/my_graph/my_graph.py
```

### Step 2: Implement Your Graph

Use the example graphs as references. Here's a minimal template:

```python
# graphs/my_graph/my_graph.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# Define your state
class MyState(TypedDict):
    input: str
    output: str

# Define your nodes
def process_node(state: MyState) -> MyState:
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    result = llm.invoke(state["input"])
    return {"output": result.content}

# Build the graph
builder = StateGraph(MyState)
builder.add_node("process", process_node)
builder.add_edge(START, "process")
builder.add_edge("process", END)

# Compile and export
graph = builder.compile()
```

### Step 3: Add to Configuration

Update `langgraph.json`:

```json
{
  "graphs": {
    "my_graph": "./graphs/my_graph/my_graph.py:graph"
  }
}
```

### Step 4: Test Your Graph

```bash
# Start LangGraph Studio
langgraph dev

# Or run tests
pytest tests/ -v
```

## Project Structure Patterns

### Recommended Structure for New Graphs

```
graphs/
├── your_graph/
│   ├── __init__.py
│   ├── your_graph.py          # Main graph implementation
│   ├── configuration.py        # Graph configuration (optional)
│   ├── prompts.py             # LLM prompts (optional)
│   ├── schemas.py             # Pydantic models (optional)
│   ├── utils.py               # Helper functions (optional)
│   └── tools/                 # Custom tools (optional)
│       ├── __init__.py
│       └── custom_tool.py
```

### Testing Structure

```
tests/
├── test_your_graph.py         # Unit tests for your graph
├── conftest.py                # Shared test fixtures
└── test_benchmarks.py         # Performance benchmarks
```

## Available Patterns and Examples

This template includes working examples of these LangGraph patterns:

### 1. **Parallelization** (`graphs/studio/parallelization.py`)
- Parallel node execution
- Combining results from multiple sources
- **Use for**: Gathering data from multiple APIs simultaneously

### 2. **Sub-Graphs** (`graphs/studio/sub_graphs.py`)
- Nested graph composition
- Reusable graph components
- **Use for**: Complex workflows with modular components

### 3. **Map-Reduce** (`graphs/studio/map_reduce.py`)
- Send() API for dynamic parallelization
- Aggregating parallel results
- **Use for**: Processing collections of items

### 4. **Research Assistant** (`graphs/studio/research_assistant.py`)
- Multi-agent coordination
- Parallel agent execution
- **Use for**: Tasks requiring multiple perspectives

### 5. **Task Maistro** (`graphs/deployment/task_maistro.py`)
- Multi-namespace memory
- Trustcall integration
- **Use for**: Production applications with persistent state

### 6. **Email Assistant** (`graphs/email_assistant/`)
- Classification workflows
- Conditional routing
- **Use for**: Triage and categorization tasks

### 7. **Research Agents** (`graphs/research/`)
- Deep research workflows
- Supervisor patterns
- **Use for**: Complex research and analysis tasks

## Development Workflow

### 1. Local Development

```bash
# Activate virtual environment
source project-env/bin/activate  # Mac/Linux
.\project-env\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run LangGraph Studio
langgraph dev
```

### 2. Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy graphs/

# Run all pre-commit checks
pre-commit run --all-files
```

### 3. Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_your_graph.py -v

# Run with coverage
pytest --cov=graphs tests/

# Run benchmarks
pytest tests/test_benchmarks.py --benchmark-only
```

### 4. Documentation

Update these files as you develop:

- `README.md`: Main project documentation
- `docs/ARCHITECTURE_DESIGN.md`: Architecture decisions
- `docs/DEMO_GUIDE.md`: Demo walkthrough
- `docs/MAINTENANCE_NOTES.md`: Known issues and improvements
- `demo-text.txt`: Copy-paste ready examples

## Adding Dependencies

### Application Dependencies

```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt
pip install -r requirements.txt
```

### Development Dependencies

```bash
# Add to requirements-dev.txt
echo "new-dev-tool==2.0.0" >> requirements-dev.txt
pip install -r requirements-dev.txt
```

## CI/CD Integration

The template includes GitHub Actions workflows:

- **CI Pipeline** (`.github/workflows/ci.yml`): Runs tests on every push/PR
- **Pre-commit Checks** (`.github/workflows/pre-commit.yml`): Code quality checks
- **Dependency Review** (`.github/workflows/dependency-review.yml`): Security scanning

Customize these workflows in `.github/workflows/` as needed.

## Best Practices from This Template

### 1. **Unified Configuration**
- Single `langgraph.json` at project root
- All graphs registered in one place
- Consistent environment management

### 2. **Comprehensive Testing**
- Unit tests for all graphs
- Integration tests with real APIs
- Performance benchmarking
- Test fixtures in `conftest.py`

### 3. **Code Quality**
- Black for formatting
- Ruff for linting
- Mypy for type checking
- Pre-commit hooks for automation

### 4. **Documentation**
- Clear README with examples
- Separate documentation files for different concerns
- Copy-paste ready demo examples
- Inline code comments

### 5. **Development Tools**
- Virtual environment management
- Requirements pinning
- CI/CD automation
- GitHub templates for issues and PRs

## Common Customizations

### Remove Example Graphs

```bash
# Keep only the graph utilities
find graphs -type f ! -path "*/utils/*" ! -name "__init__.py" -delete
find graphs -type d -empty -delete
```

### Add New API Integration

1. Add API key to `.env.example`
2. Create tool in `graphs/your_graph/tools/`
3. Import and use in your graph
4. Update documentation

### Change Python Version

1. Update `langgraph.json`: `"python_version": "3.12"`
2. Update `pyproject.toml`: `requires-python = ">=3.12"`
3. Update `.github/workflows/ci.yml`: Python version matrix
4. Recreate virtual environment with new Python version

## Troubleshooting Template Issues

### Issue: Import errors after customization

**Solution**: Update Python path and re-install:
```bash
pip install -e .
```

### Issue: Pre-commit hooks failing

**Solution**: Update `.pre-commit-config.yaml` or skip temporarily:
```bash
git commit --no-verify -m "message"
```

### Issue: Tests failing after removing example graphs

**Solution**: Remove corresponding test files:
```bash
rm tests/test_studio_graphs.py
rm tests/test_deployment_graphs.py
# etc.
```

## Resources

- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **LangChain Academy**: https://academy.langchain.com/
- **LangSmith**: https://smith.langchain.com/
- **Template Repository**: https://github.com/greenskin44/task-MASter-LangGraph

## Getting Help

- Review the example graphs in this template
- Check `docs/` for detailed documentation
- Refer to `demo-text.txt` for working examples
- Open an issue in the original template repository

## Contributing Back to Template

If you develop useful patterns or improvements, consider contributing back to the template repository to help other developers!

---

**Happy Building!** This template gives you everything you need to create production-ready LangGraph applications. Start with the examples, customize to your needs, and build amazing AI workflows.
