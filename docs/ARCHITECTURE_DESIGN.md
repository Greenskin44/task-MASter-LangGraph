# Architecture Design

## Overview

This document proposes the production-ready architecture for the LangGraph project, organizing multiple graph implementations into a coherent, maintainable structure that supports seamless local development with LangGraph Studio.

## Current State

The project currently has graphs scattered across multiple directories:
- `studio/` - 4 demonstration graphs
- `deployment/` - 1 production graph (task_maistro)
- `email_assistant/` - Email processing workflow
- `deep-research-agent/` - Research agent with multi-agent supervisor
- `deep_agents/` - Additional agent implementations
- `report-team-MAS-LangGraph/` - Report generation agents

## Proposed Directory Structure

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
│   │   ├── task_maistro.py
│   │   └── configuration.py
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
│       ├── state_research.py
│       ├── state_multi_agent_supervisor.py
│       ├── state_scope.py
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
│       ├── langgraph.json
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
│   ├── REQUIREMENTS.md
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

## Design Rationale

### 1. Separation by Purpose

**Decision**: Organize graphs into `studio/`, `deployment/`, `email_assistant/`, and `research/` directories.

**Rationale**:
- **Studio graphs** are educational/demonstration focused, showcasing LangGraph patterns
- **Deployment graphs** are production-ready with memory persistence and robust error handling
- **Email assistant** is a specialized workflow with its own tools and schemas
- **Research agents** form a cohesive multi-agent system with shared state management

**Benefits**:
- Clear intent for each graph collection
- Easier to navigate and understand project structure
- Prevents mixing demo code with production code
- Supports different testing and deployment strategies

### 2. Configuration Isolation

**Decision**: Each graph collection has its own `config/` subdirectory with `langgraph.json`, `requirements.txt`, and `.env.example`.

**Rationale**:
- Different graphs have different dependency requirements
- Studio graphs need minimal dependencies for quick demos
- Deployment graphs need production dependencies (trustcall, checkpointing)
- Email assistant may need specialized packages
- Prevents dependency conflicts between graph collections

**Benefits**:
- Run `langgraph dev` in any config directory without conflicts
- Install only required dependencies for specific use cases
- Easy to maintain and update dependencies per collection
- Clear documentation of environment requirements

### 3. Shared Utilities Within Graph Collections

**Decision**: Keep prompts, schemas, utils, and tools within each graph's directory rather than creating a shared utilities folder.

**Rationale**:
- Each graph collection has specialized utilities not reusable elsewhere
- Avoids tight coupling between different graph types
- Makes each collection self-contained and portable
- Simplifies dependency management

**Benefits**:
- Can extract and deploy individual graph collections independently
- Reduces risk of breaking changes across collections
- Clearer ownership and maintenance boundaries
- Easier to understand what each graph needs

### 4. Testing Structure Mirrors Graph Structure

**Decision**: Create separate test files for each graph collection (`test_studio_graphs.py`, `test_deployment_graphs.py`, etc.).

**Rationale**:
- Tests are organized by the same logical groupings as the code
- Easy to locate tests for specific graphs
- Supports running tests for specific collections
- Matches mental model of project organization

**Benefits**:
- Fast test execution for specific areas
- Clear test coverage per graph collection
- Easy to add new tests alongside new graphs
- Supports parallel test execution

### 5. Centralized Documentation

**Decision**: All documentation lives in `docs/` directory.

**Rationale**:
- Single source of truth for project documentation
- Easy to find and navigate documentation
- Supports documentation versioning
- Keeps root directory clean

**Benefits**:
- Consistent documentation structure
- Easy to generate documentation site if needed
- Clear separation between code and documentation
- Supports documentation-driven development

### 6. Root-Level Dependency Management

**Decision**: Maintain `requirements.txt` at root level with core dependencies, plus config-specific requirements files.

**Rationale**:
- Core dependencies (langgraph, langchain-core) are shared across all graphs
- Config-specific files add only specialized dependencies
- Supports both full installation and minimal installation
- Provides clear dependency hierarchy

**Benefits**:
- Avoid duplicate dependency specifications
- Easy to update core dependencies across project
- Supports different installation scenarios
- Clear documentation of dependency relationships

### 7. Python Package Structure

**Decision**: Add `__init__.py` files to all graph directories to make them proper Python packages.

**Rationale**:
- Enables proper import statements
- Supports relative imports within packages
- Makes code more testable
- Follows Python best practices

**Benefits**:
- Can import graphs as modules
- Supports better IDE integration
- Enables package distribution if needed
- Clearer code organization

## Migration Strategy

### Phase 1: Create New Structure
1. Create `graphs/` directory with subdirectories
2. Create `config/` directory with subdirectories
3. Create `tests/` directory
4. Ensure all directories have `__init__.py` files

### Phase 2: Move Graph Files
1. Move studio graphs to `graphs/studio/`
2. Move deployment graphs to `graphs/deployment/`
3. Move email assistant to `graphs/email_assistant/`
4. Move research agents to `graphs/research/`
5. Update import statements in all moved files

### Phase 3: Create Configuration Files
1. Create `config/studio/langgraph.json` with studio graph entry points
2. Create `config/deployment/langgraph.json` with deployment graph entry points
3. Create requirements files for each configuration
4. Create `.env.example` files documenting required variables

### Phase 4: Update Tests
1. Create test files in `tests/` directory
2. Update test imports to match new structure
3. Verify all tests pass with new structure

### Phase 5: Update Documentation
1. Update README.md with new structure
2. Update all documentation references
3. Create migration notes for existing users

## Configuration Details

### Studio Configuration (`config/studio/langgraph.json`)

```json
{
  "dependencies": ["./requirements.txt"],
  "graphs": {
    "parallelization": "./graphs/studio/parallelization.py:graph",
    "sub_graphs": "./graphs/studio/sub_graphs.py:graph",
    "map_reduce": "./graphs/studio/map_reduce.py:graph",
    "research_assistant": "./graphs/studio/research_assistant.py:graph"
  },
  "env": ".env"
}
```

### Deployment Configuration (`config/deployment/langgraph.json`)

```json
{
  "dependencies": ["./requirements.txt"],
  "graphs": {
    "task_maistro": "./graphs/deployment/task_maistro.py:graph"
  },
  "env": ".env",
  "store": {
    "type": "sqlite",
    "path": "./data/task_maistro.db"
  }
}
```

### Email Assistant Configuration (`config/email_assistant/langgraph.json`)

```json
{
  "dependencies": ["./requirements.txt"],
  "graphs": {
    "email_assistant": "./graphs/email_assistant/email_assistant.py:graph"
  },
  "env": ".env"
}
```

## Dependency Management Strategy

### Root `requirements.txt` (Core Dependencies)
```
langgraph>=0.2.45
langchain-core>=0.3.0
langchain-openai>=0.2.0
python-dotenv>=1.0.0
```

### Studio `requirements.txt` (Demo Dependencies)
```
-r ../../requirements.txt
tavily-python>=0.5.0
wikipedia>=1.4.0
```

### Deployment `requirements.txt` (Production Dependencies)
```
-r ../../requirements.txt
trustcall>=0.1.0
langgraph-checkpoint-sqlite>=1.0.0
```

### Email Assistant `requirements.txt` (Specialized Dependencies)
```
-r ../../requirements.txt
langchain-community>=0.3.0
```

## Benefits of This Architecture

1. **Clarity**: Clear separation of concerns and purpose
2. **Maintainability**: Easy to locate and update specific components
3. **Scalability**: Simple to add new graphs or collections
4. **Testability**: Structure supports comprehensive testing
5. **Portability**: Each collection can be extracted independently
6. **Documentation**: Self-documenting structure
7. **Development Experience**: Works seamlessly with LangGraph Studio
8. **Production Readiness**: Follows Python and LangGraph best practices

## Future Considerations

### Potential Enhancements
1. **Shared Utilities Package**: If common patterns emerge, create `graphs/common/`
2. **Plugin System**: Support dynamic graph loading
3. **Configuration Management**: Centralized configuration management system
4. **Monitoring**: Add observability and monitoring infrastructure
5. **CI/CD**: Automated testing and deployment pipelines

### Scalability
- Structure supports adding new graph collections
- Can scale to dozens of graphs without restructuring
- Supports team collaboration with clear ownership boundaries
- Enables microservices architecture if needed

## Conclusion

This architecture provides a solid foundation for productionalizing the LangGraph project. It balances simplicity with scalability, follows Python best practices, and supports seamless development with LangGraph Studio. The structure is designed to grow with the project while maintaining clarity and maintainability.
