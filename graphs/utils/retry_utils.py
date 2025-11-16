"""Retry utilities with exponential backoff for API calls.

This module provides decorators and utilities for retrying failed operations,
particularly useful for external API calls that may experience transient failures.

Example:
    >>> from graphs.utils import retry_with_backoff
    >>> 
    >>> @retry_with_backoff(max_retries=3)
    >>> def call_external_api():
    ...     return api.search("query")
"""

import time
import functools
from typing import Callable, Type, Tuple, Any
from graphs.utils.logging_config import get_logger

logger = get_logger(__name__)


class APIError(Exception):
    """Base exception for API-related errors.
    
    This exception should be raised when an API call fails in a way that
    might be recoverable with a retry (e.g., rate limits, temporary outages).
    
    Attributes:
        message: Description of the error.
        original_error: The underlying exception that caused this error.
        troubleshooting_hint: Helpful hint for resolving the issue.
    """

    def __init__(
        self,
        message: str,
        original_error: Exception = None,
        troubleshooting_hint: str = None,
    ):
        """Initialize the API error with context.
        
        Args:
            message: Description of what went wrong.
            original_error: The original exception that was caught.
            troubleshooting_hint: Suggestion for how to fix the issue.
        """
        self.message = message
        self.original_error = original_error
        self.troubleshooting_hint = troubleshooting_hint
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format the error message with troubleshooting hints.
        
        Returns:
            Formatted error message with hints if available.
        """
        error_str = self.message
        if self.original_error:
            error_str += f"\nOriginal error: {str(self.original_error)}"
        if self.troubleshooting_hint:
            error_str += f"\n💡 Troubleshooting hint: {self.troubleshooting_hint}"
        return error_str


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """Decorator that retries a function with exponential backoff.
    
    This decorator will retry the wrapped function if it raises one of the
    specified exceptions. The delay between retries increases exponentially.
    
    Args:
        max_retries: Maximum number of retry attempts. Defaults to 3.
        initial_delay: Initial delay in seconds before first retry. Defaults to 1.0.
        backoff_factor: Multiplier for delay after each retry. Defaults to 2.0.
        exceptions: Tuple of exception types to catch and retry. Defaults to (Exception,).
    
    Returns:
        Decorated function with retry logic.
    
    Example:
        >>> @retry_with_backoff(max_retries=3, initial_delay=1.0)
        >>> def unstable_api_call():
        ...     return external_api.fetch_data()
        
        >>> # With custom exceptions
        >>> @retry_with_backoff(exceptions=(ConnectionError, TimeoutError))
        >>> def network_call():
        ...     return requests.get("https://api.example.com")
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.info(
                            f"Retry attempt {attempt}/{max_retries} for {func.__name__}",
                            extra={"function": func.__name__, "attempt": attempt},
                        )
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}",
                            extra={
                                "function": func.__name__,
                                "attempt": attempt + 1,
                                "error": str(e),
                            },
                        )
                        logger.info(f"Retrying in {delay:.1f} seconds...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_retries + 1} attempts",
                            extra={
                                "function": func.__name__,
                                "total_attempts": max_retries + 1,
                                "final_error": str(e),
                            },
                        )

            # If we've exhausted all retries, raise the last exception
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def create_api_error(
    operation: str, error: Exception, api_name: str = "API"
) -> APIError:
    """Create a detailed API error with troubleshooting hints.
    
    This helper function creates an APIError with context-specific
    troubleshooting hints based on the type of error encountered.
    
    Args:
        operation: Description of what operation was being performed.
        error: The original exception that occurred.
        api_name: Name of the API service (e.g., "OpenAI", "Tavily").
    
    Returns:
        APIError with appropriate troubleshooting hints.
    
    Example:
        >>> try:
        ...     result = openai_client.chat.completions.create(...)
        ... except Exception as e:
        ...     raise create_api_error("generate completion", e, "OpenAI")
    """
    error_str = str(error).lower()
    
    # Determine appropriate troubleshooting hint
    if "api key" in error_str or "authentication" in error_str or "401" in error_str:
        hint = (
            f"Check that your {api_name} API key is set correctly in your .env file. "
            f"Verify the key is valid and has not expired."
        )
    elif "rate limit" in error_str or "429" in error_str:
        hint = (
            f"{api_name} rate limit exceeded. Wait a moment and try again. "
            f"Consider implementing request throttling or upgrading your API plan."
        )
    elif "timeout" in error_str or "timed out" in error_str:
        hint = (
            f"Request to {api_name} timed out. Check your internet connection. "
            f"The service may be experiencing high load - try again in a moment."
        )
    elif "connection" in error_str or "network" in error_str:
        hint = (
            f"Network connection to {api_name} failed. Check your internet connection. "
            f"Verify that {api_name} services are accessible from your network."
        )
    elif "not found" in error_str or "404" in error_str:
        hint = (
            f"The requested {api_name} resource was not found. "
            f"Verify the endpoint URL and resource identifiers are correct."
        )
    elif "invalid" in error_str or "400" in error_str:
        hint = (
            f"Invalid request to {api_name}. Check that all required parameters "
            f"are provided and formatted correctly."
        )
    else:
        hint = (
            f"An unexpected error occurred with {api_name}. "
            f"Check the error details above and verify your configuration."
        )
    
    return APIError(
        message=f"Failed to {operation} using {api_name}",
        original_error=error,
        troubleshooting_hint=hint,
    )
