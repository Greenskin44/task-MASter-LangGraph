# Project Inventory

## Overview

This document provides a comprehensive inventory of all directories, files, and their purposes within the LangGraph Python project. The project contains multiple LangGraph implementations across different directories, each serving different purposes from demonstration to production deployment.

## Root Directory Structure

```
langgraph-project/
├── .devcontainer/          # Development container configuration
├── .git/                   # Git version control
├── .kiro/                  # Kiro IDE specifications and workflows
├── .vscode/                # VS Code editor settings
├── deep-research-agent/    # Deep research agent with multi-agent supervisor
├── deep_agents/            # Additional agent implementations
├── deployment/             # Production-ready deployment graphs
├── email_assistant/        # Email processing and triage workflows
├── project-env/            # Python virtual environment
├── report-team-MAS-LangGraph/  # Report generation multi-agent system
├── studio/                 # LangGraph Studio demonstration graphs
├── .env                    # Environment variables (not committed)
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore patterns
├── demo-text.txt           # Demo examples and test inputs
├── README.md               # Project documentation
└── requirements.txt        # Root-level Python dependencies
```

## Detailed Directory Inventory

### 1. Studio Directory (`studio/`)

**Purpose**: Contains demonstration graphs for LangGraph Studio showcasing various LangGraph patterns and capabilities.

**Configuration Files**:
- `langgraph.json` - Defines 4 graph entry points (parallelization, sub_graphs, map_reduce, research_assistant)
- `requirements.txt` - Dependencies: langgraph, langchain-core, langchain-community, langchain-openai, tavily-python, wikipedia
- `.env` - Environment variables for API keys
- `.env.example` - Template for environment variables

**Graph Files**:
- `parallelization.py` - Demonstrates parallel execution with web and Wikipedia search
  - **State**: `State(question, answer, context)`
  - **Nodes**: search_web, search_wikipedia, generate_answer
  - **Pattern**: Parallel fan-out to multiple search sources, then converge to answer generation

- `sub_graphs.py` - Demonstrates nested graph composition with subgraphs
  - **State**: `EntryGraphState`, `FailureAnalysisState`, `QuestionSummarizationState`
  - **Nodes**: clean_logs, failure_analysis (subgraph), question_summarization (subgraph)
  - **Pattern**: Entry graph delegates to two parallel subgraphs for different analysis tasks

- `map_reduce.py` - Demonstrates map-reduce pattern using Send() API
  - **State**: `OverallState(topic, subjects, jokes, best_selected_joke)`
  - **Nodes**: generate_topics, generate_joke, best_joke
  - **Pattern**: Generate topics, map joke generation across topics, reduce to best joke

- `research_assistant.py` - Multi-agent research with analyst personas and human-in-the-loop
  - **State**: `ResearchGraphState(topic, max_analysts, analysts, sections, final_report)`
  - **Nodes**: create_analysts, human_feedback, conduct_interview (subgraph), write_report, write_introduction, write_conclusion, finalize_report
  - **Pattern**: Create analyst personas, conduct parallel interviews, synthesize final report
  - **Features**: Human-in-the-loop for analyst approval, parallel interview execution

**Support Files**:
- `__pycache__/` - Python bytecode cache
- `.langgraph_api/` - LangGraph API runtime files

### 2. Deployment Directory (`deployment/`)

**Purpose**: Contains production-ready graphs for deployment, specifically a personal task management assistant with memory.

**Configuration Files**:
- `langgraph.json` - Defines 1 graph entry point (task_maistro)
- `requirements.txt` - Dependencies: langgraph, langchain-core, langchain-community, langchain-openai, trustcall
- `docker-compose.yml` - Docker deployment configuration
- `docker-compose-example.yml` - Example Docker configuration

**Graph Files**:
- `task_maistro.py` - Personal task management assistant with multi-namespace memory
  - **State**: `MessagesState` with store integration
  - **Nodes**: task_mAIstro, update_profile, update_todos, update_instructions
  - **Pattern**: Chatbot with conditional routing to update different memory namespaces
  - **Features**: Trustcall integration for memory extraction, multi-namespace storage (profile, todo, instructions)
  - **Schemas**: Profile, ToDo, UpdateMemory

**Support Files**:
- `configuration.py` - Configuration schema for user_id, todo_category, task_maistro_role

### 3. Email Assistant Directory (`email_assistant/`)

**Purpose**: Automated email triage and response system with tool-based actions.

**Main Files**:
- `email_assistant.py` - Main email triage and response workflow
  - **State**: `State(email_input, classification_decision, messages)`
  - **Nodes**: triage_router, response_agent (subgraph with llm_call, environment)
  - **Pattern**: Triage emails into respond/notify/ignore, then route to response agent if needed
  - **Features**: Tool-based actions, structured output for classification

- `email_assistant_hitl.py` - Email assistant with human-in-the-loop
- `email_assistant_hitl_memory.py` - Email assistant with memory persistence
- `email_assistant_hitl_memory_gmail.py` - Gmail integration with memory
- `langgraph_101.py` - Basic LangGraph tutorial/example

**Support Files**:
- `configuration.py` - Configuration schema
- `prompts.py` - System prompts for triage and agent
- `schemas.py` - Pydantic schemas (State, RouterSchema, StateInput)
- `utils.py` - Utility functions (parse_email, format_email_markdown)
- `cron.py` - Scheduled execution support
- `__init__.py` - Package initialization

**Subdirectories**:
- `tools/` - Custom tools for email actions
- `eval/` - Evaluation scripts and test cases
- `__pycache__/` - Python bytecode cache

### 4. Deep Research Agent Directory (`deep-research-agent/`)

**Purpose**: Comprehensive research workflow with user clarification, research brief generation, and multi-agent coordination.

**Main Files**:
- `research_agent_full.py` - Full multi-agent research system
  - **State**: `AgentState(user_input, research_brief, notes, final_report, messages)`
  - **Nodes**: clarify_with_user, write_research_brief, supervisor_subgraph, final_report_generation
  - **Pattern**: User clarification → research brief → multi-agent research → final report
  - **Features**: Async execution, comprehensive research workflow

- `multi_agent_supervisor.py` - Supervisor pattern for coordinating multiple research agents
  - **State**: `SupervisorState`
  - **Nodes**: supervisor, supervisor_tools
  - **Pattern**: Supervisor delegates research topics to parallel researcher agents, aggregates results
  - **Features**: Parallel research execution, compressed research findings, think_tool for reflection

**Support Files**:
- `prompts.py` - System prompts for research agents
- `state_research.py` - State definitions for research workflow
- `state_scope.py` - State definitions for scoping workflow
- `state_multi_agent_supervisor.py` - State definitions for supervisor
- `utils.py` - Utility functions
- `pyproject.toml` - Project metadata and dependencies
- `__init__.py` - Package initialization

**Subdirectories**:
- `.git/` - Separate git repository
- `.github/` - GitHub workflows and configurations
- `.langgraph_api/` - LangGraph API runtime files
- `.venv/` - Python virtual environment
- `deep_research_from_scratch.egg-info/` - Package metadata
- `__pycache__/` - Python bytecode cache

### 5. Deep Agents Directory (`deep_agents/`)

**Purpose**: Additional agent implementations with file operations, research tools, and task management.

**Files**:
- `4_full_agent.ipynb` - Jupyter notebook with full agent implementation
- `file_tools.py` - File operation tools
- `research_tools.py` - Research and search tools
- `task_tool.py` - Task management tools
- `todo_tools.py` - Todo list management tools
- `prompts.py` - Agent prompts
- `state.py` - State definitions
- `utils.py` - Utility functions

**Subdirectories**:
- `deep_agents.egg-info/` - Package metadata

### 6. Report Team MAS LangGraph Directory (`report-team-MAS-LangGraph/`)

**Purpose**: Report generation using multi-agent system with long-term memory.

**Files**:
- `examples.py` - Example usage and demonstrations
- `long-term-mem-agent.ipynb` - Jupyter notebook with long-term memory agent
- `prompts.py` - System prompts
- `schemas.py` - Pydantic schemas
- `utils.py` - Utility functions
- `requirements.txt` - Pinned dependencies (langchain==0.3.18, langgraph==0.2.72, etc.)

### 7. Kiro Specs Directory (`.kiro/specs/`)

**Purpose**: Contains specifications for the productionalization workflow.

**Files**:
- `langgraph-productionalization/requirements.md` - Requirements document
- `langgraph-productionalization/design.md` - Design document
- `langgraph-productionalization/tasks.md` - Implementation task list

### 8. Development Configuration

**DevContainer** (`.devcontainer/`):
- `devcontainer.json` - VS Code development container configuration

**VS Code** (`.vscode/`):
- `settings.json` - Editor settings and preferences

## Root-Level Files

### Configuration Files

- **`.env`** - Environment variables (API keys, configuration)
  - Not committed to version control
  - Contains: OPENAI_API_KEY, LANGSMITH_API_KEY, TAVILY_API_KEY

- **`.env.example`** - Template for environment variables
  - Committed to version control
  - Documents required environment variables

- **`.gitignore`** - Git ignore patterns
  - Excludes: .env, __pycache__, .venv, etc.

### Dependency Files

- **`requirements.txt`** - Root-level Python dependencies
  - langgraph, langgraph-prebuilt, langgraph-sdk
  - langgraph-checkpoint-sqlite, langsmith
  - langchain-community, langchain-core, langchain-openai
  - notebook, tavily-python, wikipedia, trustcall
  - langgraph-cli[inmem]
  - **Note**: No version pinning, which may cause conflicts

### Documentation Files

- **`README.md`** - Project documentation
  - Setup instructions
  - Usage examples
  - Project overview

- **`demo-text.txt`** - Demo examples and test inputs
  - Copy-paste ready examples for testing graphs
  - Organized by graph type

## Python Virtual Environment

**`project-env/`** - Python virtual environment
- Contains installed packages and Python interpreter
- Should not be committed to version control
- Subdirectories: Scripts/, Lib/, Include/, etc.

## Summary Statistics

- **Total Graph Implementations**: 10+ graphs across 5 directories
- **Configuration Files**: 3 langgraph.json files (studio, deployment, email_assistant potential)
- **Requirements Files**: 4 requirements.txt files (root, studio, deployment, report-team-MAS-LangGraph)
- **Python Packages**: 6 directories with Python code
- **Documentation**: 1 README.md, 3 spec documents in .kiro/specs/

## Key Observations

1. **Multiple Dependency Files**: Different directories have their own requirements.txt with varying dependency specifications
2. **No Version Pinning**: Root requirements.txt lacks version pins, which may cause conflicts
3. **Duplicate Functionality**: Some overlap between deep-research-agent and deep_agents
4. **Mixed Patterns**: Graphs demonstrate various LangGraph patterns (parallel, subgraphs, map-reduce, supervisor)
5. **Production vs Demo**: Clear separation between studio (demo) and deployment (production) graphs
6. **Nested Git Repositories**: deep-research-agent has its own .git directory
