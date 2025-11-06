# Task 11.6 - Graph Testing Fixes

**Date:** November 3, 2025
**Task:** Fix issues discovered during individual graph testing in Studio

## Issues Identified and Fixed

### Issue #1: Email Assistant - KeyError('author')

**Symptom:**
```
KeyError('author')
```
Occurred in `triage_router` node when testing with demo example.

**Root Cause:**
The `parse_email()` function expected field name `author`, but demo examples used `from_email` (following Gmail-style schema).

**Files Modified:**
- `graphs/email_assistant/utils.py`

**Fix:**
Modified `parse_email()` to support multiple field name conventions:
```python
# Support both 'author' and 'from_email' field names
author = email_input.get("author") or email_input.get("from_email")
# Support both 'to' and 'to_email' field names
to = email_input.get("to") or email_input.get("to_email")
# Support both 'email_thread' and 'page_content' field names
email_thread = email_input.get("email_thread") or email_input.get("page_content")
```

**Impact:**
Email assistant now works with both schema formats:
- Original: `author`, `to`, `email_thread`
- Gmail-style: `from_email`, `to_email`, `page_content`

---

### Issue #2: Research Agent Full - ValueError('Invalid format string')

**Symptom:**
```
ValueError('Invalid format string')
```
Occurred in `clarify_with_user` node when processing user messages.

**Root Cause:**
The function used Python's `.format()` method to insert message content into prompt templates. When message content contained curly braces `{}` (common in JSON), Python interpreted them as format placeholders, causing errors.

**Files Modified:**
- `graphs/research/research_agent_scope.py`

**Fix:**
Replaced `.format()` with `.replace()` in both functions:

**Before:**
```python
prompt = clarify_with_user_instructions.format(
    messages="\n".join([f"{msg.type}: {msg.content}" for msg in messages]),
    date=get_today_str(),
)
```

**After:**
```python
messages_str = "\n".join([f"{msg.type}: {msg.content}" for msg in messages])
prompt = clarify_with_user_instructions.replace("{messages}", messages_str).replace("{date}", get_today_str())
```

**Impact:**
Research agent can now handle messages containing JSON, code snippets, or any content with curly braces without errors.

---

### Issue #3: Multi-Agent Supervisor - ValueError('Invalid format string')

**Symptom:**
```
ValueError('Invalid format string')
```
Occurred in `supervisor` node during research coordination.

**Root Cause:**
Same as Issue #2 - `.format()` method conflicts with curly braces in content.

**Files Modified:**
- `graphs/research/multi_agent_supervisor.py`

**Fix:**
Replaced `.format()` with `.replace()` in supervisor function:

**Before:**
```python
system_message = lead_researcher_prompt.format(
    date=get_today_str(),
    max_concurrent_research_units=max_concurrent_researchers,
    max_researcher_iterations=max_researcher_iterations,
)
```

**After:**
```python
system_message = (
    lead_researcher_prompt
    .replace("{date}", get_today_str())
    .replace("{max_concurrent_research_units}", str(max_concurrent_researchers))
    .replace("{max_researcher_iterations}", str(max_researcher_iterations))
)
```

**Impact:**
Multi-agent supervisor can now handle research briefs and messages with any content without format string errors.

---

## Testing Status

### Server Status
- ✅ LangGraph dev restarted successfully
- ✅ All 8 graphs registered without errors
- ✅ Server running at http://127.0.0.1:2024
- ✅ Studio UI accessible

### Graphs Ready for Re-testing
1. ✅ parallelization (no issues)
2. ✅ sub_graphs (no issues)
3. ✅ map_reduce (no issues)
4. ✅ research_assistant (no issues)
5. ✅ task_maistro (no issues)
6. ✅ email_assistant (FIXED - ready for re-test)
7. ✅ research_agent_full (FIXED - ready for re-test)
8. ✅ multi_agent_supervisor (FIXED - ready for re-test)

### Next Steps
1. Re-test email_assistant with the same demo example
2. Re-test research_agent_full with the same demo example
3. Re-test multi_agent_supervisor with the same demo example
4. Verify all three graphs now work correctly
5. Complete testing of remaining graphs (if not already done)

---

## Technical Notes

### Why .replace() Instead of .format()?

Python's `.format()` method treats curly braces `{}` as special characters for placeholder substitution. When user input or message content contains curly braces (common in JSON, code, or structured data), `.format()` tries to interpret them, causing errors.

**Example of the problem:**
```python
template = "User said: {message}"
message = "Here's JSON: {\"key\": \"value\"}"
template.format(message=message)  # ❌ ValueError: Invalid format string
```

**Solution with .replace():**
```python
template = "User said: {message}"
message = "Here's JSON: {\"key\": \"value\"}"
template.replace("{message}", message)  # ✅ Works correctly
```

The `.replace()` method treats the template as a plain string and performs simple text substitution without interpreting special characters.

### Alternative Solutions Considered

1. **Double curly braces:** Could escape `{{` and `}}` in templates, but requires modifying all prompt templates
2. **Template engines:** Could use Jinja2 or similar, but adds dependency and complexity
3. **String concatenation:** Could build strings manually, but less readable
4. **f-strings:** Can't use with dynamic templates

**Chosen solution:** `.replace()` is simple, requires minimal code changes, and has no dependencies.

---

## Files Changed Summary

1. `graphs/email_assistant/utils.py` - Made email parsing flexible
2. `graphs/research/research_agent_scope.py` - Fixed format string issues in 2 functions
3. `graphs/research/multi_agent_supervisor.py` - Fixed format string issue in supervisor
4. `GRAPH_TESTING_RESULTS.md` - Documented issues and fixes
5. `TASK_11.6_FIXES.md` - This file

---

## Verification

All fixes have been applied and the server has been restarted. The graphs are ready for re-testing with the original demo examples that caused the errors.

**Server Process ID:** 11
**Server Status:** Running
**All Graphs Registered:** ✅ Yes (8/8)

