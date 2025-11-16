# Contributing to LangGraph Production Project

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- OpenAI API key
- Tavily API key (for research graphs)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/greenskin44/task-MASter-LangGraph.git
cd task-MASter-LangGraph
```

2. **Create a virtual environment**

```bash
python -m venv project-env
source project-env/bin/activate  # Mac/Linux
.\project-env\Scripts\Activate.ps1  # Windows
```

3. **Install dependencies**

```bash
# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

4. **Set up pre-commit hooks**

```bash
pre-commit install
```

5. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation updates
- `refactor/` for code refactoring
- `test/` for test additions/updates

### 2. Make Your Changes

Follow the project's coding standards:

- **Code Style**: Follow PEP 8 (enforced by Black and Ruff)
- **Type Hints**: Add type annotations to all functions
- **Docstrings**: Document all modules, classes, and functions
- **Error Handling**: Add appropriate error handling
- **Tests**: Write tests for new functionality

### 3. Run Quality Checks

Before committing, ensure your code passes all checks:

```bash
# Format code
black .

# Lint code
ruff check . --fix

# Type check
mypy graphs/ --ignore-missing-imports

# Run tests
pytest tests/ -v
```

Pre-commit hooks will automatically run these checks, but it's good practice to run them manually first.

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/updates
- `refactor:` for code refactoring
- `chore:` for maintenance tasks
- `ci:` for CI/CD changes

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub. The PR template will guide you through providing necessary information.

## Code Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Use Ruff for linting
- Use Mypy for type checking

### Type Hints

All functions should have type hints:

```python
from typing import Dict, List, Optional

def process_data(
    input_data: Dict[str, str],
    options: Optional[List[str]] = None
) -> Dict[str, any]:
    """Process input data with optional configuration.
    
    Args:
        input_data: Dictionary containing input parameters
        options: Optional list of processing options
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If input_data is invalid
    """
    # Implementation
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed, explaining the function's
    purpose and behavior in detail.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string
        
    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

### Error Handling

Always handle errors gracefully:

```python
def safe_api_call(input_data: Dict) -> Dict:
    """Make API call with proper error handling."""
    try:
        # Validate input
        if not input_data.get("required_field"):
            raise ValueError("Missing required field")
            
        # Make API call
        result = external_api(input_data)
        return {"success": True, "data": result}
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"success": False, "error": str(e)}
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"success": False, "error": "An unexpected error occurred"}
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common test data

Example test structure:

```python
import pytest
from graphs.studio.parallelization import graph

def test_parallelization_basic_question():
    """Test parallelization with a basic question."""
    input_data = {"question": "What is LangGraph?"}
    result = graph.invoke(input_data)
    
    assert "answer" in result
    assert "context" in result
    assert len(result["context"]) > 0

def test_parallelization_invalid_input():
    """Test parallelization with invalid input."""
    with pytest.raises(ValueError):
        graph.invoke({})
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_studio_graphs.py -v

# Run specific test
pytest tests/test_studio_graphs.py::test_parallelization_basic_question -v

# Run with coverage
pytest --cov=graphs tests/
```

## Adding New Graphs

To add a new graph to the project:

1. **Create the graph file** in the appropriate directory:
   - `graphs/studio/` for demo graphs
   - `graphs/deployment/` for production graphs
   - Create a new category if needed

2. **Implement the graph** following existing patterns:
   - Define state schema using TypedDict
   - Implement node functions with type hints and docstrings
   - Add error handling
   - Export the compiled graph

3. **Register in langgraph.json**:

```json
{
  "graphs": {
    "your_graph_name": "./graphs/category/your_graph.py:graph"
  }
}
```

4. **Write tests** in `tests/test_category.py`

5. **Add demo examples** to `demo-text.txt`

6. **Update documentation**:
   - Add description to README.md
   - Add walkthrough to docs/DEMO_GUIDE.md
   - Update docs/MAINTENANCE_NOTES.md if needed

## Pull Request Process

1. **Ensure all checks pass**:
   - All tests pass
   - Code quality checks pass (black, ruff, mypy)
   - Pre-commit hooks pass
   - No merge conflicts

2. **Update documentation**:
   - Update README.md if needed
   - Add/update docstrings
   - Update relevant docs/ files

3. **Fill out PR template**:
   - Describe changes clearly
   - Link related issues
   - Add screenshots if applicable

4. **Request review**:
   - Tag relevant reviewers
   - Respond to feedback promptly
   - Make requested changes

5. **Merge**:
   - Squash commits if needed
   - Use descriptive merge commit message
   - Delete feature branch after merge

## CI/CD Pipeline

The project uses automated CI/CD workflows:

### GitHub Actions

- **CI Workflow**: Runs tests and code quality checks on every push/PR
- **Pre-commit Workflow**: Validates pre-commit hooks in CI
- **Dependency Review**: Reviews dependency changes in PRs

### Pre-commit Hooks

Local hooks run automatically before each commit:
- Trailing whitespace removal
- End of file fixing
- YAML/JSON/TOML validation
- Black formatting
- Ruff linting
- Mypy type checking

### Dependabot

Automated dependency updates:
- Weekly updates for Python packages
- Weekly updates for GitHub Actions
- Grouped updates for related packages

See [docs/CI_CD_SETUP.md](docs/CI_CD_SETUP.md) for complete CI/CD documentation.

## Code Review Guidelines

### For Contributors

- Keep PRs focused and reasonably sized
- Respond to feedback constructively
- Test your changes thoroughly
- Update documentation as needed

### For Reviewers

- Be constructive and respectful
- Focus on code quality and maintainability
- Check for test coverage
- Verify documentation is updated
- Test changes locally if needed

## Getting Help

- **Documentation**: Check the `docs/` directory
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.