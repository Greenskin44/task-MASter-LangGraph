"""Pytest configuration and shared fixtures for LangGraph tests.

This module provides common test fixtures and configuration used across
all test modules in the test suite.
"""

import os
import pytest
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def api_keys() -> Dict[str, str]:
    """Provide API keys from environment variables.

    Returns:
        Dictionary containing API keys needed for testing.

    Raises:
        pytest.skip: If required API keys are not available.
    """
    keys = {
        "openai": os.getenv("OPENAI_API_KEY"),
        "tavily": os.getenv("TAVILY_API_KEY"),
        "langsmith": os.getenv("LANGSMITH_API_KEY"),
    }

    # Skip tests if OpenAI key is missing (required for most tests)
    if not keys["openai"] or keys["openai"].startswith("sk-test"):
        pytest.skip(
            "OPENAI_API_KEY not set or invalid - skipping tests requiring API access"
        )

    return keys


@pytest.fixture
def sample_question() -> str:
    """Provide a simple test question for search-based graphs.

    Returns:
        A simple question string suitable for testing.
    """
    return "What is LangGraph?"


@pytest.fixture
def sample_topic() -> str:
    """Provide a simple test topic for generation-based graphs.

    Returns:
        A simple topic string suitable for testing.
    """
    return "artificial intelligence"


@pytest.fixture
def sample_logs() -> List[Dict[str, Any]]:
    """Provide sample log data for sub-graphs testing.

    Returns:
        List of log dictionaries with various fields.
    """
    return [
        {
            "id": "1",
            "question": "How to use Chroma?",
            "docs": ["doc1", "doc2"],
            "answer": "Chroma is a vector store...",
            "grade": 3,
            "grader": "human",
            "feedback": "Could be more detailed",
        },
        {
            "id": "2",
            "question": "What is ChatOllama?",
            "docs": ["doc3"],
            "answer": "ChatOllama is a chat interface...",
        },
        {
            "id": "3",
            "question": "How to install LangChain?",
            "docs": [],
            "answer": "Use pip install langchain",
            "grade": 5,
            "grader": "auto",
            "feedback": "Good answer",
        },
    ]


@pytest.fixture
def sample_email_respond() -> str:
    """Provide a sample email that should trigger a response.

    Returns:
        Email text that requires a response action.
    """
    return """
    From: john@example.com
    Subject: Question about project timeline
    
    Hi team,
    
    I wanted to check in on the status of the Q4 project. Can you provide
    an update on the timeline and any blockers you're facing?
    
    Thanks,
    John
    """


@pytest.fixture
def sample_email_notify() -> str:
    """Provide a sample email that should trigger a notification.

    Returns:
        Email text that requires a notify action.
    """
    return """
    From: alerts@system.com
    Subject: System Alert: High CPU Usage
    
    Alert: Server prod-01 is experiencing high CPU usage (95%).
    
    Time: 2024-10-29 14:30:00
    Severity: Warning
    """


@pytest.fixture
def sample_email_ignore() -> str:
    """Provide a sample email that should be ignored.

    Returns:
        Email text that should be ignored (spam/promotional).
    """
    return """
    From: marketing@newsletter.com
    Subject: 50% OFF - Limited Time Offer!
    
    Don't miss out on our biggest sale of the year!
    Click here to shop now and save big.
    
    Unsubscribe | View in browser
    """


@pytest.fixture
def sample_research_topic() -> str:
    """Provide a sample research topic.

    Returns:
        A research topic suitable for testing research workflows.
    """
    return "LangGraph memory management"


@pytest.fixture
def sample_task_message() -> str:
    """Provide a sample task management message.

    Returns:
        A message for testing task management functionality.
    """
    return "I need to finish the project report by Friday"


@pytest.fixture
def sample_profile_update() -> str:
    """Provide a sample profile update message.

    Returns:
        A message for testing profile update functionality.
    """
    return "My name is Alex and I work as a software engineer"
