# Error Handling and Logging Guide

This document describes the enhanced error handling and logging capabilities implemented across all LangGraph graphs in this project.

## Overview

All graphs now include:
- **Structured logging** with consistent formatting and contextual information
- **Retry logic** with exponential backoff for transient API failures
- **Detailed error messages** with troubleshooting hints
- **Graceful degradation** to prevent complete graph failures

## Logging

### Setup

Logging is configured centrally using the `graphs.utils.logging_config` module:

```python
from graphs.utils import setup_logging, get_logger

# Configure logging at application startup (optional)
setup_logging("INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Get a logger for your module
logger = get_logger(__name__)
```

### Log Levels

- **DEBUG**: Detailed diagnostic information (e.g., number of context items, memory operations)
- **INFO**: General informational messages (e.g., operation started/completed, classification results)
- **WARNING**: Warning messages for recoverable issues (e.g., retry attempts)
- **ERROR**: Error messages for failures (e.g., API errors, validation failures)
- **CRITICAL**: Critical errors that may cause system failure

### Log Format

All logs follow a consistent structured format:

```
2025-01-15 10:30:45 | INFO     | graphs.studio.parallelization | Starting web search | Context: {"question": "What is LangGraph?"}
```

Format: `timestamp | level | module | message | context`

### Usage Examples

```python
from graphs.utils import get_logger

logger = get_logger(__name__)

# Basic logging
logger.info("Processing started")
logger.debug("Processing 5 items")
logger.warning("Rate limit approaching")
logger.error("API call failed")

# Logging with context
logger.info(
    "User request processed",
    extra={"user_id": "123", "category": "work"}
)

# Logging in exception handlers
try:
    result = api_call()
except Exception as e:
    logger.error(f"Operation failed: {e}")
```

## Error Handling

### Retry Logic

The `retry_with_backoff` decorator automatically retries failed operations with exponential backoff:

```python
from graphs.utils import retry_with_backoff

@retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
def search_web(state):
    # This function will be retried up to 3 times
    # Delays: 1.0s, 2.0s, 4.0s
    return tavily_search.invoke(state["question"])
```

**Parameters:**
- `max_retries`: Maximum number of retry attempts (default: 3)
- `initial_delay`: Initial delay in seconds before first retry (default: 1.0)
- `backoff_factor`: Multiplier for delay after each retry (default: 2.0)
- `exceptions`: Tuple of exception types to catch (default: (Exception,))

**Behavior:**
- Logs each retry attempt with attempt number
- Increases delay exponentially between retries
- Logs final failure after all retries exhausted
- Re-raises the last exception if all retries fail

### API Errors with Troubleshooting Hints

The `create_api_error` function creates detailed error messages with context-specific troubleshooting hints:

```python
from graphs.utils import create_api_error

try:
    result = openai_client.chat.completions.create(...)
except Exception as e:
    raise create_api_error("generate completion", e, "OpenAI")
```

**Automatic Hint Detection:**

The function analyzes the error and provides appropriate hints:

| Error Type | Troubleshooting Hint |
|------------|---------------------|
| API Key / Authentication | Check that your API key is set correctly in .env file |
| Rate Limit (429) | Wait a moment and try again. Consider request throttling |
| Timeout | Check internet connection. Service may be experiencing high load |
| Connection / Network | Check internet connection. Verify service is accessible |
| Not Found (404) | Verify endpoint URL and resource identifiers |
| Invalid Request (400) | Check that all required parameters are provided correctly |
| Other | Check error details and verify configuration |

### Error Message Format

```
Failed to generate completion using OpenAI
Original error: RateLimitError: Rate limit exceeded
💡 Troubleshooting hint: OpenAI rate limit exceeded. Wait a moment and try again. 
Consider implementing request throttling or upgrading your API plan.
```

### Graceful Degradation

Graphs are designed to degrade gracefully rather than fail completely:

```python
@retry_with_backoff(max_retries=3)
def search_web(state):
    try:
        # Attempt search
        results = tavily_search.invoke(state["question"])
        return {"context": [format_results(results)]}
    except Exception as e:
        # Log error and return error context instead of failing
        api_error = create_api_error("perform web search", e, "Tavily")
        logger.error(f"Web search failed: {api_error}")
        return {"context": [f"<Error>{str(api_error)}</Error>"]}
```

**Benefits:**
- Partial results can still be used by downstream nodes
- Graph execution continues even if one component fails
- Users receive informative error messages instead of crashes

## Implementation Examples

### Parallelization Graph

The parallelization graph demonstrates all error handling features:

```python
from graphs.utils import get_logger, retry_with_backoff, create_api_error

logger = get_logger(__name__)

@retry_with_backoff(max_retries=3, initial_delay=1.0)
def search_web(state):
    logger.info("Starting web search", extra={"question": state.get("question", "")[:50]})
    
    try:
        if not state.get("question"):
            logger.error("Web search failed: missing question in state")
            raise ValueError("Question is required in state")

        tavily_search = TavilySearch(max_results=3)
        search_docs = tavily_search.invoke(state["question"])
        
        logger.info(f"Web search completed successfully, found {len(search_docs)} results")
        return {"context": [format_docs(search_docs)]}

    except ValueError as e:
        raise  # Re-raise validation errors without retry
    except Exception as e:
        api_error = create_api_error("perform web search", e, "Tavily")
        logger.error(f"Web search failed: {api_error}")
        return {"context": [f"<Error>{str(api_error)}</Error>"]}
```

### Task Maistro Graph

The task maistro graph includes logging for memory operations:

```python
@retry_with_backoff(max_retries=2, initial_delay=1.0)
def task_mAIstro(state, config, store):
    try:
        user_id = config.user_id
        logger.info(f"Processing request for user: {user_id}")

        # Load memories with logging
        memories = store.search(namespace)
        logger.debug(f"Loaded {len(memories)} todo items for {user_id}")

        # Generate response
        response = model.invoke(messages)
        logger.info("Successfully generated response")
        
        return {"messages": [response]}
        
    except Exception as e:
        api_error = create_api_error("process task maistro request", e, "OpenAI")
        logger.error(f"Task maistro failed: {api_error}")
        raise
```

### Email Assistant Graph

The email assistant includes detailed tool execution logging:

```python
def tool_node(state):
    logger.info("Executing tool calls")
    
    tool_calls = state["messages"][-1].tool_calls
    logger.debug(f"Processing {len(tool_calls)} tool calls")

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        logger.info(f"Executing tool: {tool_name}")
        
        try:
            tool = tools_by_name[tool_name]
            observation = tool.invoke(tool_call["args"])
            logger.info(f"Tool {tool_name} executed successfully")
            # ... return result
            
        except KeyError:
            error_msg = f"Tool '{tool_name}' not found. Available tools: {', '.join(tools_by_name.keys())}"
            logger.error(error_msg)
            # ... return error
```

## Best Practices

### 1. Log at Appropriate Levels

```python
# ✅ Good
logger.debug(f"Processing {len(items)} items")  # Detailed info
logger.info("Operation completed successfully")  # Key milestones
logger.warning("Retry attempt 2/3")  # Recoverable issues
logger.error("API call failed after retries")  # Failures

# ❌ Avoid
logger.info(f"Variable x = {x}")  # Too detailed for INFO
logger.error("Processing started")  # Not an error
```

### 2. Include Context in Logs

```python
# ✅ Good
logger.info(
    "User request processed",
    extra={"user_id": user_id, "operation": "update_profile"}
)

# ❌ Avoid
logger.info("Request processed")  # No context
```

### 3. Use Retry for Transient Failures Only

```python
# ✅ Good - Retry network/API failures
@retry_with_backoff(max_retries=3)
def call_external_api():
    return api.fetch_data()

# ❌ Avoid - Don't retry validation errors
@retry_with_backoff(max_retries=3)
def validate_input(data):
    if not data:
        raise ValueError("Data required")  # Will retry unnecessarily
```

### 4. Re-raise Validation Errors

```python
# ✅ Good
try:
    if not state.get("question"):
        raise ValueError("Question required")
    result = api_call()
except ValueError as e:
    raise  # Don't retry validation errors
except Exception as e:
    # Handle API errors with retry
    pass
```

### 5. Provide Actionable Error Messages

```python
# ✅ Good
raise ValueError(
    "Question is required in state. "
    "Ensure the input includes a 'question' field."
)

# ❌ Avoid
raise ValueError("Invalid input")  # Not actionable
```

## Monitoring and Debugging

### Enable Debug Logging

For detailed debugging, set the log level to DEBUG:

```python
from graphs.utils import setup_logging

setup_logging("DEBUG")
```

Or for a specific module:

```python
logger = get_logger(__name__, "DEBUG")
```

### Log Output Example

```
2025-01-15 10:30:45 | INFO     | graphs.studio.parallelization | Starting web search | Context: {"question": "What is LangGraph?"}
2025-01-15 10:30:46 | INFO     | graphs.studio.parallelization | Web search completed successfully, found 3 results
2025-01-15 10:30:46 | INFO     | graphs.studio.parallelization | Starting Wikipedia search | Context: {"question": "What is LangGraph?"}
2025-01-15 10:30:47 | INFO     | graphs.studio.parallelization | Wikipedia search completed successfully, found 2 documents
2025-01-15 10:30:47 | INFO     | graphs.studio.parallelization | Starting answer generation
2025-01-15 10:30:47 | DEBUG    | graphs.studio.parallelization | Generating answer with 2 context items
2025-01-15 10:30:49 | INFO     | graphs.studio.parallelization | Answer generated successfully
```

### Common Issues and Solutions

#### Issue: Too Many Logs

**Solution:** Adjust log level to WARNING or ERROR:
```python
setup_logging("WARNING")
```

#### Issue: Missing Context in Errors

**Solution:** Add extra context to log calls:
```python
logger.error(
    "Operation failed",
    extra={"user_id": user_id, "operation": operation_name}
)
```

#### Issue: Retries Not Working

**Solution:** Check exception types:
```python
# Specify which exceptions to retry
@retry_with_backoff(exceptions=(ConnectionError, TimeoutError))
def network_call():
    pass
```

## Configuration

### Environment Variables

No environment variables are required for logging. However, you can control third-party library logging:

```python
import logging

# Reduce noise from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
```

### Custom Formatters

To customize log formatting, modify `graphs/utils/logging_config.py`:

```python
class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
```

## Testing

### Testing with Logging

```python
import logging
from graphs.utils import get_logger

def test_with_logging(caplog):
    logger = get_logger(__name__)
    
    with caplog.at_level(logging.INFO):
        # Your test code
        logger.info("Test message")
    
    assert "Test message" in caplog.text
```

### Testing Retry Logic

```python
from unittest.mock import Mock, patch
from graphs.utils import retry_with_backoff

def test_retry_logic():
    mock_func = Mock(side_effect=[Exception("Fail"), Exception("Fail"), "Success"])
    
    @retry_with_backoff(max_retries=3)
    def test_func():
        return mock_func()
    
    result = test_func()
    assert result == "Success"
    assert mock_func.call_count == 3
```

## Summary

The enhanced error handling and logging system provides:

✅ **Visibility**: Structured logs show exactly what's happening in your graphs  
✅ **Reliability**: Automatic retries handle transient failures  
✅ **Debuggability**: Detailed error messages with troubleshooting hints  
✅ **Resilience**: Graceful degradation prevents complete failures  
✅ **Maintainability**: Consistent patterns across all graphs  

For questions or issues, refer to the troubleshooting hints in error messages or check the logs for detailed diagnostic information.
