"""Centralized logging configuration for all LangGraph graphs.

This module provides structured logging with consistent formatting across
all graph implementations. It supports different log levels and includes
contextual information for debugging.

Example:
    >>> from graphs.utils import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("Processing started", extra={"user_id": "123"})
"""

import logging
import sys
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """Custom formatter that adds structured information to log records.
    
    This formatter ensures consistent log output with timestamps, log levels,
    module names, and optional context information.
    """

    def __init__(self):
        """Initialize the structured formatter with a standard format."""
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with additional context if available.
        
        Args:
            record: The log record to format.
            
        Returns:
            Formatted log string with context information.
        """
        # Add any extra context to the message
        if hasattr(record, "context"):
            record.msg = f"{record.msg} | Context: {record.context}"
        return super().format(record)


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the entire application.
    
    Sets up a console handler with structured formatting and the specified
    log level. This should be called once at application startup.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            Defaults to INFO.
    
    Example:
        >>> setup_logging("DEBUG")
    """
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Set the log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Set the formatter
    console_handler.setFormatter(StructuredFormatter())
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a logger instance for a specific module.
    
    Creates or retrieves a logger with the specified name. If a level is
    provided, it overrides the root logger level for this specific logger.
    
    Args:
        name: Name of the logger, typically __name__ of the calling module.
        level: Optional log level override for this specific logger.
    
    Returns:
        Configured logger instance.
    
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
        >>> 
        >>> debug_logger = get_logger(__name__, "DEBUG")
        >>> debug_logger.debug("Detailed information")
    """
    logger = logging.getLogger(name)
    
    if level:
        log_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(log_level)
    
    return logger
