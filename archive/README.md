# Archived Files

This folder contains the original scattered project structure that was consolidated.

## Why These Files Are Archived

The LangGraph project was originally organized with separate folders for each graph category:
- studio/ - Demo graphs
- deployment/ - Production graphs  
- email_assistant/ - Email processing
- deep-research-agent/ - Research agents
- deep_agents/ - Experimental notebooks
- report-team-MAS-LangGraph/ - Learning materials

These have been consolidated into a unified `graphs/` structure with a single root-level
`langgraph.json` that registers all graphs.

## What's Preserved Here

### Duplicates (for reference)
- studio/ - Duplicate of graphs/studio/
- deployment/ - Duplicate of graphs/deployment/
- deep-research-agent/ - Duplicate of graphs/research/

### Unique Content (preserved for future use)
- email_assistant/email_assistant_hitl*.py - HITL and Gmail variants
- email_assistant/eval/ - Evaluation scripts and datasets
- deep_agents/ - Experimental notebooks and tools
- report-team-MAS-LangGraph/ - Learning materials with langmem

### Historical Value
- deep-research-agent/.git/ - Original repository history
- deployment/docker-compose*.yml - Deployment configurations

## Using Archived Content

If you need to reference or restore any archived content:
1. Check the archive/ folder for the original files
2. Compare with current graphs/ implementation
3. Extract specific features if needed

## Consolidation Date

Archived: 2025-10-30
