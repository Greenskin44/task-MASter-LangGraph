# LangGraph Demo Guide

## Overview

This guide provides step-by-step instructions for demonstrating all LangGraph implementations in this project. Each section includes setup instructions, demo flow, expected outputs, and presentation tips to ensure smooth, professional demonstrations.

## Table of Contents

1. [Pre-Demo Setup](#pre-demo-setup)
2. [Demo Environment](#demo-environment)
3. [Studio Graphs Demos](#studio-graphs-demos)
4. [Deployment Graphs Demos](#deployment-graphs-demos)
5. [Email Assistant Demo](#email-assistant-demo)
6. [Research Agent Demo](#research-agent-demo)
7. [Presentation Tips](#presentation-tips)
8. [Troubleshooting During Demos](#troubleshooting-during-demos)

---

## Pre-Demo Setup

### 1. Environment Verification (15 minutes before demo)

**Check Python Environment:**
```bash
# Verify Python version (should be 3.11+)
python --version

# Activate virtual environment
source project-env/bin/activate  # Mac/Linux
.\project-env\Scripts\Activate.ps1  # Windows
```

**Verify Dependencies:**
```bash
# Check that all packages are installed
pip list | grep langgraph
pip list | grep langchain
```

**Verify API Keys:**
```bash
# Check .env file exists
cat .env  # Mac/Linux
type .env  # Windows

# Verify keys are set (don't display actual keys!)
echo "OpenAI: ${OPENAI_API_KEY:0:7}..."
echo "Tavily: ${TAVILY_API_KEY:0:7}..."
```

### 2. Test LangGraph Studio (10 minutes before demo)

**Start Studio for Studio Graphs:**
```bash
cd studio
langgraph dev
```

**Expected Output:**
```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

**Verify Studio UI:**
1. Open browser to `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
2. Confirm all 4 studio graphs appear in dropdown:
   - parallelization
   - sub_graphs
   - map_reduce
   - research_assistant
3. Test one simple example (e.g., parallelization with "What is LangGraph?")

### 3. Prepare Demo Materials

**Open Required Files:**
- `demo-text.txt` in a text editor (for copy-paste examples)
- This `DEMO_GUIDE.md` in a separate window (for reference)
- LangGraph Studio in browser

**Backup Plan:**
- Have screenshots of successful runs ready
- Prepare to explain if API calls fail
- Have alternative examples ready

---

## Demo Environment

### Browser Setup

**Recommended Browser:** Chrome or Firefox (latest version)

**Window Layout:**
- **Left Half**: LangGraph Studio UI
- **Right Half**: Text editor with `demo-text.txt`

**Studio UI Components:**
- **Graph Selector**: Dropdown at top to switch between graphs
- **Input Panel**: Left side for entering inputs
- **Configuration Panel**: Below input for graph configuration
- **Output Panel**: Right side showing execution results
- **Graph Visualization**: Bottom showing node execution flow

### Presentation Mode

**Screen Sharing Tips:**
- Share entire screen or specific window
- Increase browser zoom to 125-150% for visibility
- Use full-screen mode for Studio UI
- Hide bookmarks bar and unnecessary browser elements

---

## Studio Graphs Demos

### Demo 1: Parallelization (5 minutes)

**Purpose**: Demonstrate parallel execution of web and Wikipedia search

**Setup:**
1. Select "parallelization" from graph dropdown
2. Open `demo-text.txt` to "Parallelization" section

**Demo Flow:**

**Step 1: Simple Question**
```json
{
  "question": "What is LangGraph?"
}
```

**What to Say:**
> "This graph demonstrates parallel execution. When I submit this question, LangGraph will simultaneously search the web using Tavily and query Wikipedia. Watch the graph visualization at the bottom - you'll see both search nodes execute in parallel."

**Expected Output:**
- Execution time: ~5-8 seconds
- Answer synthesizing web and Wikipedia results
- Context showing sources from both searches

**Key Points to Highlight:**
- ✅ Parallel node execution (show in graph visualization)
- ✅ Multiple information sources combined
- ✅ Faster than sequential execution

**Step 2: Technical Question**
```json
{
  "question": "How does parallel execution work in distributed systems?"
}
```

**What to Say:**
> "Let's try a more technical question. Notice how the graph handles complex queries by gathering information from multiple sources and synthesizing a comprehensive answer."

**Expected Output:**
- Execution time: ~6-10 seconds
- Detailed technical explanation
- Citations from multiple sources

**Key Points to Highlight:**
- ✅ Handles complex technical queries
- ✅ Quality of synthesized answers
- ✅ Source attribution

---

### Demo 2: Map-Reduce (5 minutes)

**Purpose**: Demonstrate map-reduce pattern for parallel generation and selection

**Setup:**
1. Select "map_reduce" from graph dropdown
2. Open `demo-text.txt` to "Map-Reduce" section

**Demo Flow:**

**Step 1: Simple Topic**
```json
{
  "topic": "artificial intelligence"
}
```

**What to Say:**
> "This graph demonstrates the map-reduce pattern. First, it generates 3 sub-topics related to AI. Then, in the map phase, it generates a joke for each sub-topic in parallel. Finally, in the reduce phase, it selects the best joke. Watch the graph visualization to see the dynamic Send() API in action."

**Expected Output:**
- Execution time: ~8-12 seconds
- Shows 3 generated sub-topics
- Shows 3 jokes (one per sub-topic)
- Final selection of best joke

**Key Points to Highlight:**
- ✅ Dynamic parallel execution with Send() API
- ✅ Map phase: parallel joke generation
- ✅ Reduce phase: best joke selection
- ✅ Structured output with Pydantic models

**Step 2: Technical Topic**
```json
{
  "topic": "quantum computing"
}
```

**What to Say:**
> "The pattern works with any topic. Notice how it adapts to technical subjects and generates relevant sub-topics and humor."

**Expected Output:**
- Execution time: ~8-12 seconds
- Technical sub-topics (qubits, superposition, entanglement, etc.)
- Relevant technical humor
- Best joke selected

---

### Demo 3: Sub-Graphs (5 minutes)

**Purpose**: Demonstrate nested graph composition

**Setup:**
1. Select "sub_graphs" from graph dropdown
2. Open `demo-text.txt` to "Sub-Graphs" section

**Demo Flow:**

**Step 1: Logs with Failures**
```json
{
  "raw_logs": [
    {
      "id": "1",
      "question": "How do I use Chroma vector store?",
      "docs": ["doc1", "doc2"],
      "answer": "Chroma is a vector database...",
      "grade": 2,
      "grader": "human",
      "feedback": "Poor retrieval quality"
    },
    {
      "id": "2",
      "question": "What is ChatOllama?",
      "docs": ["doc3"],
      "answer": "ChatOllama is a chat interface...",
      "grade": 1,
      "grader": "human",
      "feedback": "Incomplete answer"
    },
    {
      "id": "3",
      "question": "How to implement RAG?",
      "docs": ["doc4", "doc5"],
      "answer": "RAG combines retrieval with generation..."
    }
  ]
}
```

**What to Say:**
> "This graph demonstrates nested sub-graphs. The main graph splits into two parallel sub-graphs: one analyzes failures in graded logs, the other summarizes question themes. Watch how both sub-graphs execute simultaneously and then merge their results."

**Expected Output:**
- Execution time: ~3-5 seconds
- `fa_summary`: Analysis of failure patterns
- `report`: Summary of question themes
- `processed_logs`: List of processed log IDs

**Key Points to Highlight:**
- ✅ Nested graph composition
- ✅ Parallel sub-graph execution
- ✅ Independent processing paths
- ✅ Result merging

---

### Demo 4: Research Assistant (10 minutes)

**Purpose**: Demonstrate multi-agent research with analyst personas

**Setup:**
1. Select "research_assistant" from graph dropdown
2. Open `demo-text.txt` to "Research Assistant" section
3. **Warning**: This demo takes 30-90 seconds - prepare audience

**Demo Flow:**

**Step 1: Simple Research**
```json
{
  "topic": "LangGraph architecture patterns",
  "max_analysts": 2,
  "human_analyst_feedback": "approve"
}
```

**What to Say:**
> "This is our most sophisticated demo - a multi-agent research system. It will create 2 analyst personas with different perspectives, each conducting parallel interviews using web and Wikipedia searches. Then it synthesizes their findings into a comprehensive report. This takes about 30-60 seconds, so let's watch the graph visualization to see the multi-agent coordination."

**Expected Output:**
- Execution time: ~30-60 seconds
- 2 analyst personas created with distinct perspectives
- Parallel interview execution
- Comprehensive final report with:
  - Introduction
  - Insights from each analyst
  - Conclusion
  - Sources and citations

**Key Points to Highlight:**
- ✅ Multi-agent coordination
- ✅ Parallel agent execution
- ✅ Diverse perspectives from different analysts
- ✅ Comprehensive report synthesis
- ✅ Human-in-the-loop capability (analyst feedback)

**Step 2: Research with More Analysts (if time permits)**
```json
{
  "topic": "production deployment of LangGraph applications",
  "max_analysts": 3,
  "human_analyst_feedback": "Focus on DevOps and scalability"
}
```

**What to Say:**
> "We can scale this to more analysts for richer perspectives. With 3 analysts and specific feedback, we get even more comprehensive research. This will take about 45-90 seconds."

**Expected Output:**
- Execution time: ~45-90 seconds
- 3 analyst personas aligned with feedback
- More diverse perspectives
- Richer final report

---

## Deployment Graphs Demos

### Demo 5: Task Maistro (10 minutes)

**Purpose**: Demonstrate production-ready personal assistant with memory

**Setup:**
1. Stop studio server (Ctrl+C)
2. Navigate to deployment directory:
   ```bash
   cd ../deployment
   langgraph dev
   ```
3. Refresh browser (Studio UI should show "task_maistro" graph)
4. Open `demo-text.txt` to "Task Maistro" section

**Demo Flow:**

**Step 1: Profile Update**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hi! My name is Alex and I work as a software engineer in San Francisco. I'm interested in AI, rock climbing, and cooking."
    }
  ]
}
```

**Configuration:**
```json
{
  "configurable": {
    "user_id": "demo_user_001",
    "todo_category": "personal",
    "thread_id": "thread_001"
  }
}
```

**What to Say:**
> "Task Maistro is a production-ready personal assistant with long-term memory. It maintains three separate memory namespaces: profile, todos, and instructions. Let's start by updating the user profile. Notice the configuration - we specify a user_id for memory persistence."

**Expected Output:**
- Natural response acknowledging the information
- Profile memory updated (visible in memory panel if available)
- Friendly, personalized tone

**Key Points to Highlight:**
- ✅ Multi-namespace memory (profile, todos, instructions)
- ✅ Trustcall integration for intelligent memory updates
- ✅ Configuration-based user identification

**Step 2: Add Tasks**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need to finish the project documentation by Friday and review the pull requests by tomorrow afternoon."
    }
  ]
}
```

**Configuration:**
```json
{
  "configurable": {
    "user_id": "demo_user_001",
    "todo_category": "work",
    "thread_id": "thread_002"
  }
}
```

**What to Say:**
> "Now let's add some tasks. Notice I'm using a different thread_id and todo_category. The assistant will extract tasks, deadlines, and store them in the todo namespace."

**Expected Output:**
- Confirmation of 2 tasks added
- Task details with deadlines
- Organized by category (work)

**Key Points to Highlight:**
- ✅ Automatic task extraction
- ✅ Deadline recognition
- ✅ Category-based organization

**Step 3: Set Custom Instructions**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "When I add tasks, always estimate the time to complete and suggest at least 2 specific solutions or approaches for each task."
    }
  ]
}
```

**Configuration:**
```json
{
  "configurable": {
    "user_id": "demo_user_001",
    "todo_category": "personal",
    "thread_id": "thread_003"
  }
}
```

**What to Say:**
> "Users can set custom instructions that persist across conversations. Let's tell the assistant to always estimate time and suggest solutions when adding tasks."

**Expected Output:**
- Confirmation that preferences have been noted
- Instructions stored in instructions namespace

**Step 4: Demonstrate Memory Persistence**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Add a task to prepare the quarterly report"
    }
  ]
}
```

**Configuration:**
```json
{
  "configurable": {
    "user_id": "demo_user_001",
    "todo_category": "work",
    "thread_id": "thread_004"
  }
}
```

**What to Say:**
> "Now watch how the assistant follows the custom instructions we set earlier. It should estimate time and suggest solutions for this new task."

**Expected Output:**
- Task added with time estimate
- At least 2 specific solutions suggested
- Demonstrates instruction memory working

**Key Points to Highlight:**
- ✅ Memory persistence across conversations
- ✅ Instructions applied automatically
- ✅ Production-ready memory management

**Step 5: Query Tasks**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What tasks do I have coming up?"
    }
  ]
}
```

**Configuration:**
```json
{
  "configurable": {
    "user_id": "demo_user_001",
    "todo_category": "work",
    "thread_id": "thread_005"
  }
}
```

**What to Say:**
> "Finally, let's query the tasks. The assistant will retrieve all tasks from memory and present them organized by deadline."

**Expected Output:**
- List of all tasks added in previous steps
- Organized by deadline or priority
- Demonstrates memory retrieval

---

## Email Assistant Demo

### Demo 6: Email Triage (10 minutes)

**Purpose**: Demonstrate automated email classification and response

**Note**: Email assistant requires additional setup. Check `email_assistant/` directory for configuration.

**Demo Flow:**

**Step 1: Meeting Request (RESPOND)**

**Input:**
```json
{
  "email_input": {
    "id": "email_001",
    "from_email": "sarah.johnson@techcorp.com",
    "to_email": "demo@example.com",
    "subject": "Quick sync on API documentation",
    "page_content": "Hi,\n\nI hope this email finds you well. I wanted to reach out about the API documentation for the new LangChain endpoints. We're planning to integrate them into our product next week.\n\nCould we schedule a 30-minute call this week to discuss the authentication flow and rate limits? I'm available Tuesday afternoon or Thursday morning.\n\nLooking forward to hearing from you!\n\nBest regards,\nSarah Johnson"
  }
}
```

**What to Say:**
> "The email assistant automatically triages emails into three categories: respond, notify, or ignore. This meeting request should be classified as 'respond' and the assistant will draft a reply."

**Expected Output:**
- Classification: `respond`
- Draft response scheduling meeting
- Professional tone maintained

**Step 2: Company Announcement (NOTIFY)**

**Input:**
```json
{
  "email_input": {
    "id": "email_002",
    "from_email": "hr@company.com",
    "to_email": "demo@example.com",
    "subject": "Reminder: Q1 Performance Reviews Due January 31st",
    "page_content": "Hi Team,\n\nThis is a friendly reminder that Q1 performance reviews are due by January 31st. Please ensure you complete your self-assessments and peer feedback forms in the HR portal.\n\nKey deadlines:\n- Self-assessments: January 25th\n- Peer feedback: January 28th\n- Manager reviews: January 31st\n\nIf you have any questions, please reach out to the HR team.\n\nBest,\nHR Department"
  }
}
```

**What to Say:**
> "Company announcements are classified as 'notify' - important to know but don't require a response."

**Expected Output:**
- Classification: `notify`
- No response drafted
- Important information flagged

**Step 3: Marketing Email (IGNORE)**

**Input:**
```json
{
  "email_input": {
    "id": "email_003",
    "from_email": "newsletter@techconference.com",
    "to_email": "demo@example.com",
    "subject": "🎉 Early Bird Discount: AI Summit 2024",
    "page_content": "Don't miss out on the biggest AI conference of the year!\n\nAI Summit 2024 is coming to San Francisco on March 15-17. Register now and save 30% with our early bird discount.\n\nUse code EARLYBIRD2024 at checkout.\n\nRegister now: https://techconference.com/register"
  }
}
```

**What to Say:**
> "Marketing emails and newsletters are classified as 'ignore' - no action needed."

**Expected Output:**
- Classification: `ignore`
- No response drafted
- Email filtered out

**Key Points to Highlight:**
- ✅ Intelligent email classification
- ✅ Automated response generation
- ✅ Tool-based actions (calendar, email composition)
- ✅ Configurable classification rules

---

## Research Agent Demo

### Demo 7: Deep Research Workflow (15 minutes)

**Purpose**: Demonstrate comprehensive research with clarification and multi-agent coordination

**Note**: Research agent requires additional setup. Check `deep-research-agent/` directory.

**Demo Flow:**

**Step 1: Simple Research (No Clarification)**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I want to learn about LangGraph memory management and persistence strategies"
    }
  ]
}
```

**What to Say:**
> "The research agent has a multi-stage workflow: clarification, research brief generation, multi-agent research, and report synthesis. For clear requests like this, it skips clarification and proceeds directly to research."

**Expected Output:**
- Execution time: ~60-120 seconds
- Research brief generated
- Multi-agent coordination
- Comprehensive final report with:
  - Overview of LangGraph memory
  - Checkpoint persistence strategies
  - Best practices
  - Code examples
  - Sources and citations

**Step 2: Research Requiring Clarification**

**Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need information about AI safety"
    }
  ]
}
```

**What to Say:**
> "For vague requests, the agent asks clarifying questions to ensure relevant research."

**Expected Output (First Interaction):**
- Clarifying questions about:
  - Specific aspects of AI safety
  - Background or use case
  - Time periods or developments

**Follow-up Input:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need information about AI safety"
    },
    {
      "role": "assistant",
      "content": "To provide you with the most relevant research, I need to clarify a few things:\n\n- What specific aspects of AI safety are you interested in?\n- What is your background or use case?\n- Are there specific developments you want to focus on?"
    },
    {
      "role": "user",
      "content": "I'm a software engineer interested in technical approaches to AI alignment, particularly RLHF and constitutional AI. Focus on recent developments from 2023-2024."
    }
  ]
}
```

**What to Say:**
> "After clarification, the agent generates a detailed research brief and coordinates multiple research agents to gather comprehensive information."

**Expected Output:**
- Detailed research brief
- Multi-agent research on RLHF and constitutional AI
- Final report with recent developments
- Academic sources and citations

**Key Points to Highlight:**
- ✅ Adaptive clarification (skips when not needed)
- ✅ Research brief generation
- ✅ Multi-agent supervisor coordination
- ✅ Comprehensive report synthesis
- ✅ Source attribution

---

## Presentation Tips

### General Tips

**Pacing:**
- Allow time for graphs to execute (don't rush)
- Explain what's happening during execution
- Use graph visualization to show progress

**Engagement:**
- Ask audience what topics they'd like to see
- Invite questions throughout
- Adapt examples to audience interests

**Technical Depth:**
- Adjust complexity based on audience
- For technical audiences: show graph code, discuss architecture
- For business audiences: focus on use cases and outcomes

### Time Management

**30-Minute Demo:**
- Introduction (2 min)
- Parallelization (3 min)
- Map-Reduce (3 min)
- Research Assistant (8 min)
- Task Maistro (8 min)
- Q&A (6 min)

**60-Minute Demo:**
- Introduction (5 min)
- All Studio Graphs (20 min)
- Task Maistro (10 min)
- Email Assistant (10 min)
- Research Agent (10 min)
- Q&A (5 min)

**15-Minute Quick Demo:**
- Introduction (2 min)
- Parallelization (3 min)
- Research Assistant (7 min)
- Q&A (3 min)

### Handling Questions

**Common Questions:**

**Q: "How does this compare to other frameworks?"**
A: "LangGraph provides explicit control over agent workflows with graph-based orchestration. Unlike black-box solutions, you can see and control every step."

**Q: "Can this run in production?"**
A: "Yes! Task Maistro demonstrates production-ready patterns with memory persistence, error handling, and configuration management."

**Q: "How do you handle errors?"**
A: "Each graph has error handling for API failures, invalid inputs, and edge cases. We use try-except blocks and graceful degradation."

**Q: "What about costs?"**
A: "Costs depend on API usage. Research Assistant makes more calls than Parallelization. You can monitor costs through LangSmith and set rate limits."

**Q: "Can I customize these graphs?"**
A: "Absolutely! All code is available and well-documented. You can modify prompts, add nodes, change routing logic, or integrate different tools."

---

## Troubleshooting During Demos

### If a Graph Fails

**Stay Calm:**
> "Looks like we hit an API rate limit / network issue. Let me show you a screenshot of the expected output while we wait."

**Have Backup:**
- Screenshots of successful runs
- Alternative examples ready
- Explanation of what should happen

### If Studio Disconnects

**Quick Fix:**
```bash
# Restart langgraph dev
Ctrl+C
langgraph dev
```

**While Restarting:**
> "Let me take this opportunity to explain the architecture while the server restarts..."

### If Output is Unexpected

**Explain Variability:**
> "LLM outputs can vary between runs. The key pattern we're looking for is [describe pattern]. Let's run it again to see the consistency."

### If Execution is Slow

**Manage Expectations:**
> "This graph makes multiple API calls in parallel, so it takes 30-60 seconds. Let's watch the graph visualization to see the multi-agent coordination happening in real-time."

---

## Post-Demo Actions

### Immediate Follow-up

1. **Share Resources:**
   - Repository link
   - Documentation links
   - `demo-text.txt` file

2. **Collect Feedback:**
   - What resonated most?
   - What was confusing?
   - What additional examples would help?

3. **Answer Follow-up Questions:**
   - Provide email for questions
   - Share LangGraph documentation
   - Offer to schedule technical deep-dive

### Demo Improvement

1. **Document Issues:**
   - Note any failures or unexpected behavior
   - Record questions you couldn't answer
   - Identify confusing aspects

2. **Update Examples:**
   - Refine based on feedback
   - Add examples for common questions
   - Remove examples that don't work well

3. **Refine Timing:**
   - Adjust time estimates
   - Reorder demos for better flow
   - Identify skippable sections

---

## Success Metrics

### Demo Quality Indicators

- ✅ All examples execute without errors
- ✅ Outputs match expected patterns
- ✅ Execution times are reasonable
- ✅ Audience engagement is high
- ✅ Questions indicate understanding
- ✅ No technical difficulties

### Audience Engagement

- Questions throughout demo
- Requests for specific examples
- Discussion of use cases
- Interest in customization
- Follow-up meeting requests

---

## Conclusion

This demo guide provides everything you need to deliver professional, engaging demonstrations of all LangGraph implementations. Remember:

- **Prepare thoroughly**: Test everything before the demo
- **Stay flexible**: Adapt to audience interests and time constraints
- **Handle issues gracefully**: Have backups and explanations ready
- **Engage the audience**: Make it interactive and relevant
- **Follow up**: Share resources and collect feedback

With proper preparation and these guidelines, you'll deliver impressive demonstrations that showcase the power and flexibility of LangGraph!
