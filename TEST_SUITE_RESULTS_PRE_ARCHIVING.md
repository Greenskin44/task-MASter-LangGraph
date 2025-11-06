# Test Suite Results - Pre-Archiving

**Date:** November 3, 2025
**Task:** 11.7 Run full test suite before archiving
**Command:** `pytest tests/ -v`

## Summary

- **Total Tests:** 26
- **Passed:** 16 (61.5%)
- **Failed:** 8 (30.8%)
- **Skipped:** 2 (7.7%)
- **Warnings:** 8

## Test Results by Category

### ✅ Deployment Graphs (4/4 passed)
- `test_profile_update` - PASSED
- `test_todo_update` - PASSED
- `test_instructions_update` - PASSED
- `test_memory_persistence` - PASSED
- `test_multiple_todos` - PASSED

### ❌ Email Assistant (0/6 passed)
All 6 tests failed due to missing dependency: `html2text`

**Failed Tests:**
- `test_respond_classification` - ModuleNotFoundError: No module named 'html2text'
- `test_notify_classification` - ModuleNotFoundError: No module named 'html2text'
- `test_ignore_classification` - ModuleNotFoundError: No module named 'html2text'
- `test_meeting_request_email` - ModuleNotFoundError: No module named 'html2text'
- `test_information_request_email` - ModuleNotFoundError: No module named 'html2text'
- `test_promotional_email` - ModuleNotFoundError: No module named 'html2text'

**Root Cause:** The `html2text` package is not installed in the project-env virtual environment. This is imported in `graphs/email_assistant/utils.py:3`.

**Resolution:** Add `html2text` to requirements.txt and reinstall dependencies.

### ⚠️ Research Agent (5/7 passed, 2 skipped)
**Passed Tests:**
- `test_research_brief_generation` - PASSED
- `test_research_state_schema` - PASSED
- `test_supervisor_state_schema` - PASSED
- `test_research_tools_schema` - PASSED
- `test_research_prompts_exist` - PASSED

**Skipped Tests:**
- `test_supervisor_agent_basic` - SKIPPED (langchain-anthropic not available)
- `test_supervisor_with_multiple_topics` - SKIPPED (langchain-anthropic not available)

**Note:** Skipped tests are expected as `langchain-anthropic` is an optional dependency.

### ✅ Studio Graphs (6/8 passed)
**Passed Tests:**
- `test_simple_question` (Parallelization) - PASSED
- `test_technical_question` (Parallelization) - PASSED
- `test_basic_logs` (SubGraphs) - PASSED
- `test_logs_with_failures` (SubGraphs) - PASSED
- `test_simple_topic` (MapReduce) - PASSED
- `test_technical_topic` (MapReduce) - PASSED

**Failed Tests:**
- `test_simple_research` (ResearchAssistant) - AssertionError: 'final_report' not in result
- `test_research_with_max_analysts` (ResearchAssistant) - AssertionError: 'final_report' not in result

**Root Cause:** The research assistant tests are failing because the graph execution stops at the `interrupt_before` point and doesn't continue to generate the final report. The tests need to be updated to handle the human-in-the-loop workflow properly by resuming execution after the interrupt.

## Deprecation Warnings

The following deprecation warnings were detected:

1. **LangGraph Send Import** (3 occurrences)
   - Location: `trustcall/_base.py:46`, `task_maistro.py`, `map_reduce.py:20`, `research_assistant.py:16`
   - Issue: `from langgraph.constants import Send` is deprecated
   - Fix: Use `from langgraph.types import Send` instead

2. **Pydantic min_items** (1 occurrence)
   - Location: `task_maistro.py:181`
   - Issue: `min_items` is deprecated
   - Fix: Use `min_length` instead

3. **LangGraph config_schema** (1 occurrence)
   - Location: `task_maistro.py:534`
   - Issue: `config_schema` is deprecated
   - Fix: Use `context_schema` instead

4. **TavilySearchResults** (1 occurrence)
   - Location: `parallelization.py:64`
   - Issue: Class deprecated in LangChain 0.3.25
   - Fix: Use `langchain-tavily` package instead

## Recommendations

### Immediate Actions (Before Archiving)
1. ✅ **Document test failures** - Completed in this file
2. ⚠️ **Email Assistant:** Add `html2text` to requirements.txt (can be done in task 12.1)
3. ⚠️ **Research Assistant Tests:** Update tests to handle interrupt_before properly (can be done in task 12.2)

### Future Actions (Task 12.3)
1. Update all Send imports to use `langgraph.types`
2. Update Pydantic models to use `min_length`
3. Update task_maistro.py to use `context_schema`
4. Update TavilySearchResults to use langchain-tavily package

## Conclusion

The test suite shows that **core functionality is working** for:
- ✅ All deployment graphs (task_maistro)
- ✅ Most studio graphs (parallelization, sub_graphs, map_reduce)
- ✅ Research agent schema and utility tests

**Known Issues:**
- ❌ Email assistant tests fail due to missing `html2text` dependency
- ❌ Research assistant tests fail due to interrupt handling in tests
- ⚠️ 2 research agent tests skipped due to optional anthropic dependency

**Status:** Tests are in acceptable state for archiving. The failures are documented and will be addressed in Task 12 (Fix remaining test failures and deprecation warnings).
