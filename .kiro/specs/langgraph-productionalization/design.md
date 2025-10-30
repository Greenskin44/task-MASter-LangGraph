# Design Document

## Overview

This design document outlines the architecture and approach for productionalizing a LangGraph Python project containing multiple graph implementations across different directories. The project includes:

- **studio/**: 4 demonstration graphs (parallelization, sub_graphs, map_reduce, research_assistant)
- **deployment/**: 1 production graph (task_maistro)
- **email_assistant/**: Email processing workflow
- **deep-research-agent/**: Research agent with multi-agent supervisor
- **deep_agents/**: Additional agent implementations
- **report-team-MAS-LangGraph/**: Report generation agents

The productionalization effort will focus on creating a unified, well-documented structure that enables seamless local development with LangGraph Studio, comprehensive testing, and production-ready code quality.

## Architecture

### Directory Structure

The refactored project will follow Python best practices with clear separation of concerns:

```
langgraph-project/
├── .kiro/
│   └── specs/
│       └── langgraph-productionalization/
├── graphs/
│   ├── studio/                    # Demo graphs for LangGraph Studio
│   │   ├── __init__.py
│   │   ├── parallelization.py
│   │   ├── sub_graphs.py
│   │   ├── map_reduce.py
│   │   └── research_assistant.py
│   ├── deployment/                # Production-ready graphs
│   │   ├── __init__.py
│   │   └── task_maistro.py
│   ├── email_assistant/           # Email processing workflows
│   │   ├── __init__.py
│   │   ├── email_assistant.py
│   │   ├── configuration.py
│   │   ├── prompts.py
│   │   ├── schemas.py
│   │   ├── utils.py
│   │   └── tools/
│   └── research/                  # Research agent workflows
│       ├── __init__.py
│       ├── research_agent_full.py
│       ├── multi_agent_supervisor.py
│       ├── prompts.py
│       ├── state_*.py
│       └── utils.py
├── config/
│   ├── studio/
│   │   ├── langgraph.json
│   │   ├── requirements.txt
│   │   └── .env.example
│   ├── deployment/
│   │   ├── langgraph.json
│   │   ├── requirements.txt
│   │   └── .env.example
│   └── email_assistant/
│       ├── langgraph.json (if needed)
│       └── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── test_studio_graphs.py
│   ├── test_deployment_graphs.py
│   ├── test_email_assistant.py
│   └── test_research_agent.py
├── docs/
│   ├── PROJECT_INVENTORY.md
│   ├── CURRENT_STATE_ANALYSIS.md
│   ├── ARCHITECTURE_DESIGN.md
│   ├── TESTING_PLAN.md
│   ├── DEMO_STRATEGY.md
│   ├── TESTING_RESULTS.md
│   ├── DEMO_GUIDE.md
│   └── MAINTENANCE_NOTES.md
├── demo-text.txt                  # Copy-paste ready examples
├── README.md                      # Main documentation
├── requirements.txt               # Root dependencies
├── pyproject.toml                 # Project metadata
└── .env.example                   # Environment variable template
```

### Design Rationale

1. **Separation by Purpose**: Graphs are organized by their intended use (studio demos, deployment, specialized workflows)
2. **Configuration Isolation**: Each graph collection has its own langgraph.json and requirements.txt to prevent conflicts
3. **Shared Utilities**: Common code (prompts, schemas, utils) stays within each graph's directory
4. **Testing Structure**: Tests mirror the graph structure for easy navigation
5. **Documentation Centralization**: All documentation lives in docs/ for easy access

## Components and Interfaces

### Graph Components

#### Studio Graphs (Demo/Learning)

**1. Parallelization Graph**
- **Purpose**: Demonstrates parallel execution of search operations
- **Input**: `{"question": str}`
- **Output**: `{"answer": str, "context": list}`
- **Key Features**: Parallel web and Wikipedia search, answer generation
- **Dependencies**: tavily-python, wikipedia, langchain-openai

**2. Sub-Graphs**
- **Purpose**: Demonstrates nested graph composition
- **Input**: `{"raw_logs": List[Log]}`
- **Output**: `{"fa_summary": str, "report": str, "processed_logs": list}`
- **Key Features**: Failure analysis and question summarization subgraphs
- **Dependencies**: langchain-core

**3. Map-Reduce**
- **Purpose**: Demonstrates map-reduce pattern for joke generation
- **Input**: `{"topic": str}`
- **Output**: `{"best_selected_joke": str}`
- **Key Features**: Dynamic Send() API, structured output
- **Dependencies**: langchain-openai

**4. Research Assistant**
- **Purpose**: Multi-agent research with analyst personas
- **Input**: `{"topic": str, "max_analysts": int}`
- **Output**: `{"final_report": str}`
- **Key Features**: Human-in-the-loop, parallel interviews, report synthesis
- **Dependencies**: tavily-python, wikipedia, langchain-openai

#### Deployment Graphs (Production)

**1. Task Maistro**
- **Purpose**: Personal task management with memory
- **Input**: `MessagesState`
- **Output**: `MessagesState` with updated memories
- **Key Features**: Trustcall integration, multi-namespace memory, profile/todo/instructions management
- **Dependencies**: trustcall, langgraph-checkpoint-sqlite, langchain-openai

#### Email Assistant

**1. Email Assistant**
- **Purpose**: Automated email triage and response
- **Input**: `{"email_input": str}`
- **Output**: `{"classification_decision": str, "messages": list}`
- **Key Features**: Triage routing, tool-based actions, response generation
- **Dependencies**: langchain-community, custom tools

#### Research Agent

**1. Deep Research Agent**
- **Purpose**: Comprehensive research workflow with clarification
- **Input**: `{"user_input": str}`
- **Output**: `{"final_report": str}`
- **Key Features**: User clarification, research brief, multi-agent coordination
- **Dependencies**: langchain-openai, custom state management

### Configuration Management

Each graph collection will have:

1. **langgraph.json**: Defines graph entry points, Python version, dependencies
2. **requirements.txt**: Pinned dependency versions
3. **.env.example**: Template for required environment variables

### Environment Variables

Required across all graphs:
- `OPENAI_API_KEY`: OpenAI API access
- `LANGSMITH_API_KEY`: LangSmith tracing (optional but recommended)
- `TAVILY_API_KEY`: Web search for research graphs

Graph-specific:
- Task Maistro: May require additional configuration keys
- Email Assistant: Email service credentials (if integrated)

## Data Models

### State Schemas

Each graph defines its own state schema using TypedDict:

**Studio Graphs**:
- Parallelization: `State(question, answer, context)`
- Sub-Graphs: `EntryGraphState`, `FailureAnalysisState`, `QuestionSummarizationState`
- Map-Reduce: `OverallState(topic, subjects, jokes, best_selected_joke)`
- Research Assistant: `ResearchGraphState(topic, max_analysts, analysts, sections, final_report)`

**Deployment**:
- Task Maistro: `MessagesState` with store integration

**Email Assistant**:
- `State(email_input, classification_decision, messages)`

**Research Agent**:
- `AgentState(user_input, research_brief, notes, final_report, messages)`

### Pydantic Models

Structured outputs use Pydantic for validation:
- `Analyst`, `Perspectives` (research_assistant)
- `Profile`, `ToDo`, `UpdateMemory` (task_maistro)
- `RouterSchema` (email_assistant)
- `Subjects`, `Joke`, `BestJoke` (map_reduce)

## Error Handling

### Strategy

1. **Dependency Validation**: Check for required environment variables at graph initialization
2. **API Error Handling**: Wrap external API calls (OpenAI, Tavily) with try-except blocks
3. **State Validation**: Use Pydantic models to validate state transitions
4. **Graceful Degradation**: Provide meaningful error messages when operations fail
5. **Logging**: Add structured logging for debugging and monitoring

### Implementation Approach

```python
# Example error handling pattern
def node_with_error_handling(state: State) -> dict:
    """Node with proper error handling."""
    try:
        # Validate required state fields
        if not state.get("required_field"):
            raise ValueError("Missing required field")
        
        # Perform operation
        result = external_api_call(state["input"])
        
        return {"output": result}
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"error": str(e)}
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": "An unexpected error occurred"}
```

### Error Categories

1. **Configuration Errors**: Missing API keys, invalid langgraph.json
2. **Runtime Errors**: API failures, network issues, rate limits
3. **State Errors**: Invalid state transitions, missing required fields
4. **Dependency Errors**: Missing packages, version conflicts

## Testing Strategy

### Test Levels

**1. Unit Tests**
- Test individual node functions in isolation
- Mock external API calls
- Validate state transformations
- Test error handling paths

**2. Integration Tests**
- Test complete graph execution
- Use real API calls with test data
- Validate end-to-end workflows
- Test conditional edges and routing

**3. Validation Tests**
- Verify langgraph.json configuration
- Check dependency compatibility
- Validate environment variable requirements

### Test Data

Each graph will have:
- **Minimal Input**: Simplest valid input
- **Complex Input**: Realistic scenario with edge cases
- **Invalid Input**: Test error handling

### Test Execution

```bash
# Run all tests
pytest tests/

# Run specific graph tests
pytest tests/test_studio_graphs.py::test_parallelization

# Run with coverage
pytest --cov=graphs tests/
```

### Continuous Validation

- Pre-commit hooks for code quality (black, ruff, mypy)
- CI/CD pipeline for automated testing
- LangSmith integration for tracing and debugging

## Demo Strategy

### Demo Asset Structure

The `demo-text.txt` file will contain copy-paste ready examples organized by graph:

```markdown
# Studio Graphs

## Parallelization: Web + Wikipedia Search
### Example 1: Simple Question
What is LangGraph?

### Example 2: Technical Question
How does parallel execution work in LangGraph?

---

## Sub-Graphs: Log Analysis
### Example 1: Basic Logs
[JSON with sample logs]

---

## Map-Reduce: Joke Generation
### Example 1: Simple Topic
artificial intelligence

### Example 2: Technical Topic
quantum computing

---

## Research Assistant: Multi-Agent Research
### Example 1: Technology Topic
{"topic": "LangGraph architecture", "max_analysts": 2}

### Example 2: With Human Feedback
{"topic": "AI safety", "max_analysts": 3, "human_analyst_feedback": "Focus on technical approaches"}

---

# Deployment Graphs

## Task Maistro: Personal Assistant
### Example 1: Add Task
I need to finish the project report by Friday

### Example 2: Update Profile
My name is Alex and I work as a software engineer

---

# Email Assistant

## Email Triage and Response
### Example 1: Meeting Request
[Sample email text]

### Example 2: Information Request
[Sample email text]

---

# Research Agent

## Deep Research
### Example 1: Research Topic
{"user_input": "I want to learn about LangGraph memory management"}
```

### Demo Execution Flow

1. Start LangGraph Studio: `langgraph dev` in appropriate directory
2. Open Studio UI in browser
3. Select graph from dropdown
4. Copy example from demo-text.txt
5. Paste into Studio input
6. Execute and observe results
7. Verify expected outputs

### Expected Outputs

Each demo example will document:
- Expected execution time
- Key intermediate states
- Final output format
- Success indicators

## Implementation Phases

### Phase 1: Discovery (Requirements 1)
- Create PROJECT_INVENTORY.md
- Create CURRENT_STATE_ANALYSIS.md
- Create REQUIREMENTS.md
- Identify all dependencies and conflicts

### Phase 2: Design (Requirements 2)
- Create ARCHITECTURE_DESIGN.md
- Create TESTING_PLAN.md
- Create DEMO_STRATEGY.md
- Get stakeholder approval

### Phase 3: Refactoring (Requirements 3, 4)
- Reorganize directory structure
- Pin all dependencies
- Add docstrings and type hints
- Implement error handling
- Follow PEP 8 guidelines

### Phase 4: Testing (Requirements 5)
- Write unit tests
- Write integration tests
- Execute test suite
- Document results in TESTING_RESULTS.md

### Phase 5: Demo Assets (Requirements 6)
- Create demo-text.txt
- Test all examples
- Verify copy-paste functionality
- Document expected outputs

### Phase 6: Documentation (Requirements 7)
- Write comprehensive README.md
- Create DEMO_GUIDE.md
- Create MAINTENANCE_NOTES.md
- Add inline code documentation

### Phase 7: Validation (Requirements 8)
- Run `langgraph dev` for each configuration
- Execute all demo examples
- Verify zero errors/warnings
- Confirm all success criteria

## Technology Stack

### Core Dependencies
- **langgraph**: Graph orchestration framework
- **langchain-core**: Core LangChain abstractions
- **langchain-openai**: OpenAI integration
- **langchain-community**: Community tools and integrations

### Specialized Dependencies
- **tavily-python**: Web search API
- **wikipedia**: Wikipedia API wrapper
- **trustcall**: Memory management for task_maistro
- **langgraph-checkpoint-sqlite**: Persistence layer

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Type checking
- **python-dotenv**: Environment variable management

### Version Strategy
- Pin major and minor versions (e.g., `langgraph==0.2.45`)
- Allow patch updates where safe
- Document known compatibility issues
- Test with specified Python version (3.11)

## Security Considerations

1. **API Key Management**: Never commit .env files, use .env.example templates
2. **Input Validation**: Validate all user inputs before processing
3. **Rate Limiting**: Implement rate limiting for external API calls
4. **Error Messages**: Avoid exposing sensitive information in error messages
5. **Dependency Scanning**: Regular security audits of dependencies

## Performance Considerations

1. **Parallel Execution**: Leverage LangGraph's parallel execution where appropriate
2. **Caching**: Implement caching for expensive operations
3. **Streaming**: Use streaming for long-running operations
4. **Resource Limits**: Set appropriate timeouts and resource limits
5. **Monitoring**: Integrate LangSmith for performance monitoring

## Maintenance and Extensibility

### Adding New Graphs
1. Create graph file in appropriate directory
2. Add entry to langgraph.json
3. Write tests in tests/
4. Add examples to demo-text.txt
5. Update documentation

### Updating Dependencies
1. Test in isolated environment
2. Update requirements.txt
3. Run full test suite
4. Update documentation if needed
5. Document breaking changes

### Troubleshooting Guide
- Common error patterns and solutions
- Dependency conflict resolution
- API key configuration issues
- LangGraph Studio connection problems
