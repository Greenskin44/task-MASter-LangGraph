# Demo Strategy

## Overview

This document defines the strategy for creating and organizing demo assets that enable smooth, professional demonstrations of all LangGraph implementations. The goal is to provide copy-paste-ready examples that work flawlessly in LangGraph Studio without any modification.

## Demo Asset Structure

### Primary Demo File: `demo-text.txt`

A single, well-organized text file containing all demo examples with clear section headers and descriptions.

**Structure**:
```
# [Graph Collection Name]

## [Graph Name]: [Brief Description]
### Example 1: [Scenario Name]
[Copy-paste ready input]

### Example 2: [Scenario Name]
[Copy-paste ready input]

---
```

**Benefits**:
- Single source of truth for all demos
- Easy to navigate with clear headers
- Copy-paste ready format
- No need to switch between files during demos

## Demo Content Requirements

### For Each Graph

1. **Minimum 2 Examples**: Each graph must have at least two different scenarios
2. **Clear Descriptions**: Each example includes what it demonstrates
3. **Expected Outputs**: Document what the demo should produce
4. **Execution Time**: Estimate how long each demo takes
5. **Prerequisites**: Note any required setup or configuration

### Example Quality Standards

- **Simplicity**: Examples should be easy to understand
- **Relevance**: Examples should showcase key features
- **Reliability**: Examples must work consistently
- **Variety**: Examples should cover different use cases
- **Realism**: Examples should reflect real-world scenarios

## Studio Graphs Demo Content

### 1. Parallelization Graph

**Purpose**: Demonstrate parallel execution of web and Wikipedia search

**Example 1: Simple Question**
```
What is LangGraph?
```
- **Demonstrates**: Basic parallel search functionality
- **Expected Output**: Answer synthesized from web and Wikipedia sources
- **Execution Time**: ~5-8 seconds
- **Key Points**: Show parallel execution in Studio UI, highlight context sources

**Example 2: Technical Question**
```
How does parallel execution work in LangGraph?
```
- **Demonstrates**: Technical query handling
- **Expected Output**: Detailed explanation with code examples
- **Execution Time**: ~6-10 seconds
- **Key Points**: Emphasize quality of technical responses

**Example 3: Comparison Question**
```
What are the differences between LangGraph and LangChain?
```
- **Demonstrates**: Complex comparative analysis
- **Expected Output**: Structured comparison with multiple sources
- **Execution Time**: ~8-12 seconds
- **Key Points**: Show how parallel search improves answer quality

### 2. Sub-Graphs

**Purpose**: Demonstrate nested graph composition with failure analysis

**Example 1: Basic Logs**
```json
{
  "raw_logs": [
    {"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "message": "Database connection timeout after 30 seconds"},
    {"timestamp": "2024-01-01T10:00:30", "level": "WARNING", "message": "Retry attempt 1 of 3"},
    {"timestamp": "2024-01-01T10:01:00", "level": "ERROR", "message": "Database connection timeout after 30 seconds"},
    {"timestamp": "2024-01-01T10:01:30", "level": "WARNING", "message": "Retry attempt 2 of 3"},
    {"timestamp": "2024-01-01T10:02:00", "level": "INFO", "message": "Connection established successfully"}
  ]
}
```
- **Demonstrates**: Log analysis and failure pattern detection
- **Expected Output**: Failure analysis summary and comprehensive report
- **Execution Time**: ~3-5 seconds
- **Key Points**: Show subgraph execution in Studio UI

**Example 2: Mixed Severity Logs**
```json
{
  "raw_logs": [
    {"timestamp": "2024-01-01T09:00:00", "level": "INFO", "message": "Application started"},
    {"timestamp": "2024-01-01T09:30:00", "level": "WARNING", "message": "Memory usage at 75%"},
    {"timestamp": "2024-01-01T10:00:00", "level": "ERROR", "message": "Out of memory exception"},
    {"timestamp": "2024-01-01T10:00:05", "level": "CRITICAL", "message": "Application crashed"},
    {"timestamp": "2024-01-01T10:05:00", "level": "INFO", "message": "Application restarted"}
  ]
}
```
- **Demonstrates**: Handling multiple severity levels
- **Expected Output**: Prioritized failure analysis focusing on critical issues
- **Execution Time**: ~3-5 seconds
- **Key Points**: Highlight how subgraphs process different log types

### 3. Map-Reduce Graph

**Purpose**: Demonstrate map-reduce pattern for parallel generation and selection

**Example 1: Simple Topic**
```
artificial intelligence
```
- **Demonstrates**: Basic map-reduce workflow
- **Expected Output**: Best joke selected from multiple generated options
- **Execution Time**: ~8-12 seconds
- **Key Points**: Show map phase (parallel generation) and reduce phase (selection)

**Example 2: Technical Topic**
```
quantum computing
```
- **Demonstrates**: Handling specialized topics
- **Expected Output**: Technical humor with topic relevance
- **Execution Time**: ~8-12 seconds
- **Key Points**: Emphasize quality of selection process

**Example 3: Abstract Topic**
```
philosophy of mind
```
- **Demonstrates**: Complex abstract concepts
- **Expected Output**: Thoughtful, relevant humor
- **Execution Time**: ~8-12 seconds
- **Key Points**: Show versatility of the pattern

### 4. Research Assistant

**Purpose**: Demonstrate multi-agent research with analyst personas

**Example 1: Technology Topic**
```json
{
  "topic": "LangGraph architecture and design patterns",
  "max_analysts": 2
}
```
- **Demonstrates**: Multi-agent coordination and research synthesis
- **Expected Output**: Comprehensive report from multiple analyst perspectives
- **Execution Time**: ~30-60 seconds
- **Key Points**: Show analyst creation, parallel interviews, report synthesis

**Example 2: Business Topic**
```json
{
  "topic": "Impact of AI on software development workflows",
  "max_analysts": 3
}
```
- **Demonstrates**: Broader research scope with more analysts
- **Expected Output**: Multi-perspective analysis with business insights
- **Execution Time**: ~45-90 seconds
- **Key Points**: Highlight how more analysts provide richer perspectives

## Deployment Graphs Demo Content

### 1. Task Maistro

**Purpose**: Demonstrate personal task management with memory persistence

**Example 1: Add Task**
```
I need to finish the project report by Friday and prepare slides for the Monday presentation.
```
- **Demonstrates**: Task extraction and todo list management
- **Expected Output**: Confirmation of tasks added with due dates
- **Execution Time**: ~3-5 seconds
- **Key Points**: Show memory persistence, highlight todo namespace

**Example 2: Update Profile**
```
My name is Alex, I work as a Senior Software Engineer at TechCorp, and I prefer concise communication.
```
- **Demonstrates**: Profile management and personalization
- **Expected Output**: Confirmation of profile update
- **Execution Time**: ~3-5 seconds
- **Key Points**: Show profile namespace, demonstrate personalization in subsequent interactions

**Example 3: Set Instructions**
```
Always prioritize urgent tasks and remind me of deadlines at the start of each conversation.
```
- **Demonstrates**: Custom instruction management
- **Expected Output**: Confirmation of instruction saved
- **Execution Time**: ~3-5 seconds
- **Key Points**: Show instructions namespace, demonstrate instruction following

**Example 4: Query Tasks**
```
What tasks do I have this week?
```
- **Demonstrates**: Memory retrieval and task querying
- **Expected Output**: List of tasks with due dates
- **Execution Time**: ~2-4 seconds
- **Key Points**: Show memory retrieval across namespaces

## Email Assistant Demo Content

### 1. Email Triage and Response

**Purpose**: Demonstrate automated email classification and response generation

**Example 1: Meeting Request**
```
Subject: Project Sync Meeting

Hi,

I'd like to schedule a meeting to discuss the Q4 project roadmap. Are you available next Tuesday at 2pm? We should cover the timeline, resource allocation, and key milestones.

Looking forward to hearing from you.

Best regards,
Sarah
```
- **Demonstrates**: Meeting request classification and response
- **Expected Output**: Classification as "respond" with meeting acknowledgment
- **Execution Time**: ~5-8 seconds
- **Key Points**: Show triage logic, response generation

**Example 2: Information Request**
```
Subject: Status Update Request

Hello,

Can you please send me the latest status report for the infrastructure migration project? I need it for tomorrow's executive meeting.

Thanks,
Michael
```
- **Demonstrates**: Information request handling
- **Expected Output**: Classification as "respond" or "notify" with appropriate action
- **Execution Time**: ~5-8 seconds
- **Key Points**: Show tool execution for information retrieval

**Example 3: Newsletter (Ignore)**
```
Subject: Weekly Tech Newsletter - Top 10 AI Trends

Discover the latest trends in artificial intelligence! This week's highlights include:
- New LLM releases
- AI regulation updates
- Industry insights

Click here to read more!

Unsubscribe | Manage Preferences
```
- **Demonstrates**: Spam/newsletter detection
- **Expected Output**: Classification as "ignore"
- **Execution Time**: ~3-5 seconds
- **Key Points**: Show classification accuracy, no response generated

## Research Agent Demo Content

### 1. Deep Research Workflow

**Purpose**: Demonstrate comprehensive research with clarification and multi-agent coordination

**Example 1: Research Topic**
```
I want to learn about LangGraph memory management and persistence strategies.
```
- **Demonstrates**: Full research workflow from clarification to final report
- **Expected Output**: Comprehensive research report with multiple sources
- **Execution Time**: ~60-120 seconds
- **Key Points**: Show clarification phase, research brief generation, multi-agent coordination

**Example 2: Complex Research**
```
Compare different approaches to building production-ready AI agents, focusing on reliability, scalability, and maintainability.
```
- **Demonstrates**: Complex comparative research
- **Expected Output**: Detailed comparison with pros/cons analysis
- **Execution Time**: ~90-150 seconds
- **Key Points**: Highlight multi-agent collaboration, synthesis quality

## Demo Execution Guidelines

### Pre-Demo Setup

1. **Environment Check**:
   - Verify all API keys are set in `.env`
   - Confirm `langgraph dev` runs without errors
   - Test one example from each graph collection

2. **Studio Preparation**:
   - Open LangGraph Studio in browser
   - Verify all graphs appear in dropdown
   - Have `demo-text.txt` open in a separate window

3. **Backup Plan**:
   - Have screenshots of expected outputs
   - Prepare to explain if API calls fail
   - Have alternative examples ready

### During Demo

1. **Introduction** (2 minutes):
   - Explain LangGraph Studio interface
   - Show graph dropdown and input area
   - Mention that all examples are copy-paste ready

2. **Studio Graphs** (10-15 minutes):
   - Start with Parallelization (simplest)
   - Show Map-Reduce (visual map-reduce pattern)
   - Demonstrate Research Assistant (most impressive)
   - Skip Sub-Graphs unless time permits

3. **Deployment Graphs** (5-10 minutes):
   - Focus on Task Maistro
   - Show memory persistence across interactions
   - Demonstrate all three namespaces (profile, todo, instructions)

4. **Specialized Graphs** (5-10 minutes):
   - Show Email Assistant triage
   - Demonstrate Research Agent if time permits

5. **Q&A** (5-10 minutes):
   - Answer questions
   - Show additional examples if requested
   - Discuss customization possibilities

### Demo Tips

- **Start Simple**: Begin with straightforward examples
- **Build Complexity**: Gradually show more advanced features
- **Highlight Key Features**: Point out parallel execution, memory, multi-agent coordination
- **Manage Time**: Have a priority order for graphs
- **Handle Errors Gracefully**: Explain if something fails, have backup examples
- **Engage Audience**: Ask if they want to see specific scenarios

## Demo Validation Checklist

Before any demo, verify:

- [ ] All API keys are configured
- [ ] `langgraph dev` runs without errors in all config directories
- [ ] All examples in `demo-text.txt` have been tested
- [ ] Expected outputs are documented
- [ ] Backup examples are prepared
- [ ] Screenshots of successful runs are available
- [ ] Demo environment is clean (no old test data)
- [ ] Internet connection is stable
- [ ] Browser is configured correctly for Studio

## Demo Troubleshooting

### Common Issues

**Issue**: Graph doesn't appear in Studio dropdown
- **Solution**: Check `langgraph.json` configuration, verify graph path

**Issue**: API key error
- **Solution**: Verify `.env` file exists and contains valid keys

**Issue**: Slow execution
- **Solution**: Warn audience about API latency, have faster examples ready

**Issue**: Unexpected output
- **Solution**: Explain variability in LLM responses, show expected pattern

**Issue**: Studio connection error
- **Solution**: Restart `langgraph dev`, check port availability

## Success Metrics

### Demo Quality Indicators

- All examples execute without errors
- Outputs match expected patterns
- Execution times are reasonable
- Audience engagement is high
- Questions indicate understanding

### Post-Demo Actions

1. Document any issues encountered
2. Update examples if needed
3. Add new examples based on audience questions
4. Refine demo timing and flow
5. Update troubleshooting guide

## Continuous Improvement

### Feedback Collection

- Note which examples resonate most with audiences
- Track common questions and concerns
- Identify confusing aspects
- Gather suggestions for new examples

### Example Refinement

- Update examples based on feedback
- Add examples for frequently requested scenarios
- Remove examples that don't work well
- Improve descriptions and documentation

### Demo Evolution

- Adapt to new LangGraph features
- Incorporate best practices as they emerge
- Update for new use cases
- Refine based on demo experience

## Conclusion

This demo strategy ensures that all LangGraph implementations can be demonstrated professionally and reliably. By following these guidelines and using the prepared examples in `demo-text.txt`, presenters can deliver smooth, impressive demonstrations that showcase the power and flexibility of LangGraph.
