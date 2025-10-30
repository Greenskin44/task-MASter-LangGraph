# Testing Plan

## Overview

This document defines the comprehensive testing strategy for all LangGraph implementations in the project. Each graph will be tested with at least two scenarios to verify functionality, error handling, and expected outputs.

## Testing Approach

### Test Levels

1. **Unit Tests**: Test individual node functions in isolation
2. **Integration Tests**: Test complete graph execution end-to-end
3. **Validation Tests**: Verify configuration and dependencies

### Test Framework

- **Framework**: pytest
- **Mocking**: unittest.mock for external API calls (when needed)
- **Coverage**: pytest-cov for code coverage reporting
- **Assertions**: Standard pytest assertions

### Test Execution

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_studio_graphs.py

# Run specific test
pytest tests/test_studio_graphs.py::test_parallelization_simple

# Run with coverage
pytest --cov=graphs tests/

# Run with verbose output
pytest -v tests/
```

## Studio Graphs Test Scenarios

### 1. Parallelization Graph

**Purpose**: Verify parallel web and Wikipedia search with answer generation

**Test File**: `tests/test_studio_graphs.py`

#### Scenario 1: Simple Question
```python
def test_parallelization_simple():
    """Test parallelization with a simple question."""
    input_data = {"question": "What is LangGraph?"}
    
    # Expected behavior:
    # - Parallel search executes
    # - Context from web and Wikipedia
    # - Answer generated from context
    
    result = graph.invoke(input_data)
    
    assert "answer" in result
    assert "context" in result
    assert len(result["context"]) > 0
    assert "LangGraph" in result["answer"]
```

**Expected Output**:
- Answer contains information about LangGraph
- Context includes sources from web and Wikipedia
- Execution time < 10 seconds

#### Scenario 2: Technical Question
```python
def test_parallelization_technical():
    """Test parallelization with a technical question."""
    input_data = {"question": "How does parallel execution work in LangGraph?"}
    
    result = graph.invoke(input_data)
    
    assert "answer" in result
    assert "context" in result
    assert "parallel" in result["answer"].lower()
```

**Expected Output**:
- Answer explains parallel execution concepts
- Context includes technical documentation
- Multiple sources in context list

### 2. Sub-Graphs

**Purpose**: Verify nested graph composition with failure analysis and question summarization

**Test File**: `tests/test_studio_graphs.py`

#### Scenario 1: Basic Logs
```python
def test_sub_graphs_basic():
    """Test sub-graphs with basic log data."""
    input_data = {
        "raw_logs": [
            {"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "message": "Connection failed"},
            {"timestamp": "2024-01-01T10:01:00", "level": "INFO", "message": "Retry attempt 1"}
        ]
    }
    
    result = graph.invoke(input_data)
    
    assert "fa_summary" in result
    assert "report" in result
    assert "processed_logs" in result
    assert len(result["processed_logs"]) == 2
```

**Expected Output**:
- Failure analysis summary identifies connection issues
- Report synthesizes findings
- Processed logs maintain structure

#### Scenario 2: Mixed Log Levels
```python
def test_sub_graphs_mixed_levels():
    """Test sub-graphs with various log levels."""
    input_data = {
        "raw_logs": [
            {"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "message": "Database timeout"},
            {"timestamp": "2024-01-01T10:00:30", "level": "WARNING", "message": "High memory usage"},
            {"timestamp": "2024-01-01T10:01:00", "level": "INFO", "message": "System recovered"}
        ]
    }
    
    result = graph.invoke(input_data)
    
    assert "ERROR" in result["fa_summary"] or "error" in result["fa_summary"].lower()
    assert len(result["processed_logs"]) == 3
```

**Expected Output**:
- Failure analysis prioritizes errors
- Report includes warnings
- All log levels processed correctly

### 3. Map-Reduce Graph

**Purpose**: Verify map-reduce pattern for joke generation and selection

**Test File**: `tests/test_studio_graphs.py`

#### Scenario 1: Simple Topic
```python
def test_map_reduce_simple():
    """Test map-reduce with a simple topic."""
    input_data = {"topic": "artificial intelligence"}
    
    result = graph.invoke(input_data)
    
    assert "best_selected_joke" in result
    assert len(result["best_selected_joke"]) > 0
    assert "artificial intelligence" in result["best_selected_joke"].lower() or "AI" in result["best_selected_joke"]
```

**Expected Output**:
- Best joke selected from generated options
- Joke relates to the topic
- Structured output format

#### Scenario 2: Technical Topic
```python
def test_map_reduce_technical():
    """Test map-reduce with a technical topic."""
    input_data = {"topic": "quantum computing"}
    
    result = graph.invoke(input_data)
    
    assert "best_selected_joke" in result
    assert len(result["best_selected_joke"]) > 20  # Reasonable joke length
```

**Expected Output**:
- Multiple jokes generated (map phase)
- Best joke selected (reduce phase)
- Topic-relevant humor

### 4. Research Assistant

**Purpose**: Verify multi-agent research with analyst personas and report synthesis

**Test File**: `tests/test_studio_graphs.py`

#### Scenario 1: Technology Topic
```python
def test_research_assistant_technology():
    """Test research assistant with a technology topic."""
    input_data = {
        "topic": "LangGraph architecture",
        "max_analysts": 2
    }
    
    result = graph.invoke(input_data)
    
    assert "final_report" in result
    assert len(result["final_report"]) > 100
    assert "LangGraph" in result["final_report"]
```

**Expected Output**:
- Final report synthesizes multiple perspectives
- Report length indicates comprehensive research
- Topic covered in depth

#### Scenario 2: With Human Feedback
```python
def test_research_assistant_with_feedback():
    """Test research assistant with human feedback."""
    input_data = {
        "topic": "AI safety",
        "max_analysts": 2,
        "human_analyst_feedback": "Focus on technical approaches"
    }
    
    # Note: This test may require mocking human input
    result = graph.invoke(input_data)
    
    assert "final_report" in result
    assert "technical" in result["final_report"].lower() or "approach" in result["final_report"].lower()
```

**Expected Output**:
- Report incorporates human feedback
- Multiple analyst perspectives included
- Comprehensive synthesis

## Deployment Graphs Test Scenarios

### 1. Task Maistro

**Purpose**: Verify personal task management with memory persistence

**Test File**: `tests/test_deployment_graphs.py`

#### Scenario 1: Add Task
```python
def test_task_maistro_add_task():
    """Test adding a task to the todo list."""
    input_data = {
        "messages": [{"role": "user", "content": "I need to finish the project report by Friday"}]
    }
    
    result = graph.invoke(input_data, config={"configurable": {"thread_id": "test-1"}})
    
    assert "messages" in result
    assert len(result["messages"]) > 1
    # Verify task was added to memory
```

**Expected Output**:
- Task added to todo namespace
- Confirmation message generated
- Memory persisted with thread_id

#### Scenario 2: Update Profile
```python
def test_task_maistro_update_profile():
    """Test updating user profile."""
    input_data = {
        "messages": [{"role": "user", "content": "My name is Alex and I work as a software engineer"}]
    }
    
    result = graph.invoke(input_data, config={"configurable": {"thread_id": "test-2"}})
    
    assert "messages" in result
    # Verify profile updated in memory
```

**Expected Output**:
- Profile updated in profile namespace
- Personalized response
- Memory persisted correctly

#### Scenario 3: Retrieve Instructions
```python
def test_task_maistro_instructions():
    """Test retrieving and following instructions."""
    # First, set an instruction
    setup_data = {
        "messages": [{"role": "user", "content": "Always be concise in your responses"}]
    }
    graph.invoke(setup_data, config={"configurable": {"thread_id": "test-3"}})
    
    # Then test if instruction is followed
    test_data = {
        "messages": [{"role": "user", "content": "Tell me about task management"}]
    }
    result = graph.invoke(test_data, config={"configurable": {"thread_id": "test-3"}})
    
    assert "messages" in result
    # Verify response is concise
```

**Expected Output**:
- Instructions stored in instructions namespace
- Subsequent responses follow instructions
- Memory retrieval works correctly

## Email Assistant Test Scenarios

### 1. Email Triage and Response

**Purpose**: Verify email classification and appropriate action routing

**Test File**: `tests/test_email_assistant.py`

#### Scenario 1: Meeting Request (Respond)
```python
def test_email_triage_meeting_request():
    """Test email triage with a meeting request."""
    input_data = {
        "email_input": "Hi, I'd like to schedule a meeting to discuss the project. Are you available next Tuesday at 2pm?"
    }
    
    result = graph.invoke(input_data)
    
    assert "classification_decision" in result
    assert result["classification_decision"] == "respond"
    assert "messages" in result
```

**Expected Output**:
- Classification: "respond"
- Response generated with meeting acknowledgment
- Tool execution logged

#### Scenario 2: Information Request (Respond)
```python
def test_email_triage_information_request():
    """Test email triage with an information request."""
    input_data = {
        "email_input": "Can you send me the latest project status report?"
    }
    
    result = graph.invoke(input_data)
    
    assert "classification_decision" in result
    assert result["classification_decision"] in ["respond", "notify"]
```

**Expected Output**:
- Appropriate classification
- Response or notification generated
- Context-aware handling

#### Scenario 3: Spam/Ignore
```python
def test_email_triage_spam():
    """Test email triage with spam."""
    input_data = {
        "email_input": "Congratulations! You've won a million dollars! Click here now!"
    }
    
    result = graph.invoke(input_data)
    
    assert "classification_decision" in result
    assert result["classification_decision"] == "ignore"
```

**Expected Output**:
- Classification: "ignore"
- No response generated
- Spam detected correctly

## Research Agent Test Scenarios

### 1. Deep Research Workflow

**Purpose**: Verify comprehensive research with clarification and multi-agent coordination

**Test File**: `tests/test_research_agent.py`

#### Scenario 1: Research Topic
```python
def test_research_agent_basic():
    """Test research agent with a basic topic."""
    input_data = {
        "user_input": "I want to learn about LangGraph memory management"
    }
    
    result = graph.invoke(input_data)
    
    assert "final_report" in result
    assert "memory" in result["final_report"].lower()
    assert len(result["final_report"]) > 200
```

**Expected Output**:
- Clarification phase completes
- Research brief generated
- Final report synthesized
- Comprehensive coverage of topic

#### Scenario 2: Complex Research
```python
def test_research_agent_complex():
    """Test research agent with a complex topic."""
    input_data = {
        "user_input": "Compare different approaches to agent memory in LangGraph"
    }
    
    result = graph.invoke(input_data)
    
    assert "final_report" in result
    assert "compare" in result["final_report"].lower() or "comparison" in result["final_report"].lower()
```

**Expected Output**:
- Multiple research angles explored
- Comparative analysis in report
- Multi-agent coordination successful

## Configuration and Dependency Tests

### 1. LangGraph Configuration Validation

```python
def test_langgraph_json_studio():
    """Validate studio langgraph.json configuration."""
    import json
    
    with open("config/studio/langgraph.json") as f:
        config = json.load(f)
    
    assert "graphs" in config
    assert "parallelization" in config["graphs"]
    assert "sub_graphs" in config["graphs"]
    assert "map_reduce" in config["graphs"]
    assert "research_assistant" in config["graphs"]

def test_langgraph_json_deployment():
    """Validate deployment langgraph.json configuration."""
    import json
    
    with open("config/deployment/langgraph.json") as f:
        config = json.load(f)
    
    assert "graphs" in config
    assert "task_maistro" in config["graphs"]
    assert "store" in config
```

### 2. Dependency Compatibility

```python
def test_dependencies_no_conflicts():
    """Verify no dependency conflicts in requirements files."""
    # This test would parse requirements files and check for conflicts
    # Implementation depends on dependency resolution strategy
    pass

def test_environment_variables():
    """Verify required environment variables are documented."""
    import os
    from pathlib import Path
    
    env_example = Path(".env.example")
    assert env_example.exists()
    
    content = env_example.read_text()
    assert "OPENAI_API_KEY" in content
    assert "LANGSMITH_API_KEY" in content
```

## Test Data Management

### Mock Data

For tests that require external API calls, use mock data:

```python
# Mock OpenAI responses
MOCK_OPENAI_RESPONSE = {
    "choices": [{"message": {"content": "Mock response"}}]
}

# Mock Tavily search results
MOCK_TAVILY_RESULTS = [
    {"url": "https://example.com", "content": "Mock content"}
]

# Mock Wikipedia results
MOCK_WIKIPEDIA_CONTENT = "Mock Wikipedia article content"
```

### Test Fixtures

```python
@pytest.fixture
def sample_logs():
    """Provide sample log data for testing."""
    return [
        {"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "message": "Test error"},
        {"timestamp": "2024-01-01T10:01:00", "level": "INFO", "message": "Test info"}
    ]

@pytest.fixture
def test_config():
    """Provide test configuration."""
    return {"configurable": {"thread_id": "test-thread"}}
```

## Success Criteria

### Test Coverage Goals

- **Unit Test Coverage**: > 80% for core node functions
- **Integration Test Coverage**: 100% of graphs tested
- **Configuration Tests**: All langgraph.json files validated

### Test Execution Requirements

- All tests must pass before deployment
- No skipped tests in CI/CD pipeline
- Test execution time < 5 minutes for full suite

### Quality Metrics

- Zero test failures
- Zero flaky tests
- Clear, descriptive test names
- Comprehensive assertions
- Proper error messages

## Continuous Testing

### Pre-commit Hooks

```bash
# Run tests before commit
pytest tests/ --maxfail=1

# Run linting
black graphs/ tests/
ruff check graphs/ tests/

# Run type checking
mypy graphs/
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ --cov=graphs
```

## Test Maintenance

### Adding New Tests

1. Create test function with descriptive name
2. Add docstring explaining test purpose
3. Use appropriate fixtures
4. Include clear assertions
5. Document expected outputs

### Updating Tests

1. Update tests when graph logic changes
2. Maintain backward compatibility where possible
3. Document breaking changes
4. Update test data as needed

### Debugging Failed Tests

1. Run test in isolation: `pytest tests/test_file.py::test_name -v`
2. Add print statements or use debugger
3. Check test data and mocks
4. Verify environment variables
5. Review recent code changes

## Conclusion

This testing plan provides comprehensive coverage of all graphs in the project. By following these test scenarios and maintaining high test quality, we ensure that the LangGraph project is production-ready and reliable for demonstrations and deployment.
