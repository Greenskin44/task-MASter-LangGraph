# Demo Testing Instructions

## Overview

This document provides step-by-step instructions for manually testing all 27 demo examples from `demo-text.txt` in LangGraph Studio. Each example must be tested to verify it executes without modification and produces expected outputs.

## Prerequisites

### 1. Environment Setup

Create a `.env` file in the root directory with the following API keys:

```bash
# Required for all graphs
OPENAI_API_KEY=your_openai_api_key_here

# Required for parallelization, research_assistant, and research agent
TAVILY_API_KEY=your_tavily_api_key_here

# Optional but recommended for tracing
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-productionalization
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install LangGraph CLI

```bash
pip install langgraph-cli
```

## Testing Workflow

### Studio Graphs (11 examples)

**Location:** `studio/` directory  
**Graphs:** parallelization, sub_graphs, map_reduce, research_assistant

#### Start LangGraph Studio

```bash
cd studio
langgraph dev
```

Expected output:
```
Ready!
- API: http://127.0.0.1:8123
- Docs: http://127.0.0.1:8123/docs
- LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

#### Test Each Example

1. Open LangGraph Studio in your browser (use the URL from console output)
2. Select the graph from the dropdown menu
3. Open `demo-text.txt` and locate the example
4. Copy the JSON input
5. Paste into Studio input field
6. Click "Run" or "Submit"
7. Observe execution and verify output
8. Document results in `docs/DEMO_EXAMPLES_VALIDATION.md`


#### Examples to Test

**Parallelization (3 examples):**
1. Simple Technology Question - "What is LangGraph?"
2. Technical Concept - "How does parallel execution work in distributed systems?"
3. Current Events - "What are the latest developments in large language models?"

**Sub-Graphs (2 examples):**
1. Basic Logs with Failures - JSON with graded logs
2. Logs Without Failures - JSON with ungraded logs

**Map-Reduce (3 examples):**
1. Technology Topic - "artificial intelligence"
2. Science Topic - "quantum computing"
3. Everyday Topic - "coffee"

**Research Assistant (3 examples):**
1. Technology Research (Minimal) - LangGraph architecture patterns, 2 analysts
2. Technology Research (With Feedback) - AI safety and alignment, 3 analysts
3. Practical Application Research - production deployment, 2 analysts

### Deployment Graphs (5 examples)

**Location:** `deployment/` directory  
**Graph:** task_maistro

#### Start LangGraph Studio

```bash
cd deployment
langgraph dev
```

#### Test Each Example

Follow the same process as studio graphs, but note that Task Maistro requires configuration:

**Configuration Format:**
```json
{
  "configurable": {
    "user_id": "user_123",
    "todo_category": "personal",
    "thread_id": "thread_001"
  }
}
```

In LangGraph Studio, you can set configuration in the "Config" tab or panel.

#### Examples to Test

**Task Maistro (5 examples):**
1. Profile Update - User introduces themselves
2. Todo List Management - Add tasks with deadlines
3. Custom Instructions Update - Set preferences for task handling
4. Multi-Turn Conversation - Add task, then query tasks
5. Complex Task with Solutions - Plan team offsite event

### Email Assistant (6 examples)

**Location:** `graphs/email_assistant/` directory  
**Graph:** email_assistant

#### Start LangGraph Studio

If there's a separate langgraph.json for email assistant:
```bash
cd config/email_assistant
langgraph dev
```

Otherwise, the email assistant may be included in the studio or deployment configurations.

#### Examples to Test

**Email Assistant (6 examples):**
1. Meeting Request (RESPOND) - Schedule meeting request
2. Technical Question (RESPOND) - LangGraph memory persistence question
3. Company Announcement (NOTIFY) - Performance review reminder
4. Marketing Email (IGNORE) - Conference promotion
5. Build Notification (NOTIFY) - GitHub deployment success
6. Spam/Suspicious Email (IGNORE) - Phishing attempt

### Research Agent (5 examples)

**Location:** `graphs/research/` directory  
**Graph:** research_agent_full

#### Start LangGraph Studio

Check if there's a separate configuration for the research agent, or if it's included in studio/deployment configs.

#### Examples to Test

**Deep Research Agent (5 examples):**
1. Simple Research Topic - LangGraph memory management (no clarification)
2. Research Topic Requiring Clarification - AI safety (multi-turn)
3. Complex Multi-Faceted Research - Production LangGraph deployment
4. Research with Specific Source Preferences - LLM architectures (academic focus)
5. Iterative Research with Human Feedback - LangGraph in production (multi-turn)

## Validation Checklist

For each example, verify:

- [ ] Input can be copied from demo-text.txt without modification
- [ ] Example executes without errors
- [ ] Output matches expected format and content
- [ ] Execution completes in reasonable time (< 2 minutes for most)
- [ ] No warnings or errors in console output
- [ ] Graph visualization shows correct flow

## Common Issues and Solutions

### Issue: API Key Errors

**Symptom:** "Authentication failed" or "API key not found"

**Solution:**
- Verify `.env` file exists in the correct directory
- Check API keys are valid and not expired
- Ensure environment variables are loaded (restart langgraph dev)

### Issue: Module Import Errors

**Symptom:** "ModuleNotFoundError" or "ImportError"

**Solution:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.11+
- Ensure virtual environment is activated

### Issue: Graph Not Found

**Symptom:** Graph doesn't appear in Studio dropdown

**Solution:**
- Check langgraph.json configuration
- Verify graph file path is correct
- Restart langgraph dev server

### Issue: Memory Store Errors (Task Maistro)

**Symptom:** "Store not configured" or memory persistence failures

**Solution:**
- Check that InMemoryStore or SQLite store is properly configured
- Verify configuration includes user_id and thread_id
- Check deployment/langgraph.json for store configuration

### Issue: Tool Execution Failures (Email Assistant)

**Symptom:** "Tool not found" or tool execution errors

**Solution:**
- Verify all required tools are imported and registered
- Check tool configurations in the graph file
- Some tools may be mocked - verify mock implementations

## Recording Results

After testing each example, update `docs/DEMO_EXAMPLES_VALIDATION.md`:

1. Change status from ⚠️ NEEDS REVIEW to:
   - ✅ PASS if example works correctly
   - ❌ FAIL if example doesn't work
   - 🔧 FIXED if you had to fix something

2. Add notes about:
   - Execution time
   - Any warnings or issues
   - Actual output received
   - Any modifications needed

3. If an example fails:
   - Document the error message
   - Investigate the root cause
   - Fix the issue in the graph code or demo-text.txt
   - Retest and update status to 🔧 FIXED

## Final Validation

After testing all 27 examples:

1. Update the summary section in DEMO_EXAMPLES_VALIDATION.md
2. Confirm all examples have ✅ PASS or 🔧 FIXED status
3. Document any remaining issues or limitations
4. Mark task 8.6 as complete in tasks.md

## Tips for Efficient Testing

1. **Test in batches:** Test all examples for one graph before moving to the next
2. **Keep Studio running:** Don't restart langgraph dev unless necessary
3. **Use copy-paste:** Always copy directly from demo-text.txt to ensure accuracy
4. **Document as you go:** Update validation document immediately after each test
5. **Take screenshots:** Capture successful executions for documentation
6. **Note timing:** Record how long each example takes to execute
7. **Check logs:** Monitor console output for warnings or errors

## Estimated Testing Time

- Studio Graphs: ~30-45 minutes (11 examples)
- Deployment Graphs: ~20-30 minutes (5 examples)
- Email Assistant: ~20-30 minutes (6 examples)
- Research Agent: ~20-30 minutes (5 examples)
- **Total:** ~90-135 minutes (1.5-2.25 hours)

Note: Actual time may vary based on API response times and any issues encountered.
