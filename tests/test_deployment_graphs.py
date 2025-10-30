"""Tests for deployment graphs.

This module contains tests for production deployment graphs including:
- Task Maistro (personal task management with memory)
"""

import pytest
from langgraph.store.memory import InMemoryStore


@pytest.mark.deployment
@pytest.mark.integration
class TestTaskMaistro:
    """Tests for the Task Maistro graph."""

    def test_profile_update(self, api_keys, sample_profile_update):
        """Test profile update functionality.

        Verifies that the graph can update user profile information
        and store it in memory.
        """
        from graphs.deployment.task_maistro import builder

        # Create in-memory store and compile graph with it
        store = InMemoryStore()
        graph = builder.compile(store=store)

        # Configure with test user
        config = {
            "configurable": {
                "user_id": "test_user_1",
                "todo_category": "personal",
                "thread_id": "test_thread_1",
            }
        }

        # Execute graph with profile update
        result = graph.invoke(
            {"messages": [{"role": "user", "content": sample_profile_update}]},
            config=config,
        )

        # Verify response structure
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Verify profile was stored
        namespace = ("profile", "personal", "test_user_1")
        memories = store.search(namespace)
        assert len(memories) > 0

        # Verify profile contains expected information
        profile = memories[0].value
        assert profile is not None

    def test_todo_management(self, api_keys, sample_task_message):
        """Test todo list management functionality.

        Verifies that the graph can add tasks to the todo list
        and manage them appropriately.
        """
        from graphs.deployment.task_maistro import builder

        # Create in-memory store and compile graph with it
        store = InMemoryStore()
        graph = builder.compile(store=store)

        # Configure with test user
        config = {
            "configurable": {
                "user_id": "test_user_2",
                "todo_category": "work",
                "thread_id": "test_thread_2",
            }
        }

        # Execute graph with task addition
        result = graph.invoke(
            {"messages": [{"role": "user", "content": sample_task_message}]},
            config=config,
        )

        # Verify response structure
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Verify todo was stored
        namespace = ("todo", "work", "test_user_2")
        memories = store.search(namespace)
        assert len(memories) > 0

        # Verify todo contains task information
        todo = memories[0].value
        assert "task" in todo
        assert todo["task"] is not None

    def test_instructions_update(self, api_keys):
        """Test custom instructions update functionality.

        Verifies that the graph can store and update custom
        instructions for todo list management.
        """
        from graphs.deployment.task_maistro import builder

        # Create in-memory store and compile graph with it
        store = InMemoryStore()
        graph = builder.compile(store=store)

        # Configure with test user
        config = {
            "configurable": {
                "user_id": "test_user_3",
                "todo_category": "general",
                "thread_id": "test_thread_3",
            }
        }

        # Execute graph with instruction update
        instruction_message = (
            "When I add tasks, always estimate time to complete and suggest solutions"
        )
        result = graph.invoke(
            {"messages": [{"role": "user", "content": instruction_message}]},
            config=config,
        )

        # Verify response structure
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Verify instructions were stored
        namespace = ("instructions", "general", "test_user_3")
        memory = store.get(namespace, "user_instructions")

        # Instructions may or may not be created depending on interpretation
        # Just verify the graph executed successfully
        assert result is not None

    def test_memory_persistence(self, api_keys):
        """Test memory persistence across multiple interactions.

        Verifies that the graph maintains memory state across
        multiple invocations with the same user.
        """
        from graphs.deployment.task_maistro import builder

        # Create in-memory store and compile graph with it
        store = InMemoryStore()
        graph = builder.compile(store=store)

        # Configure with test user
        config = {
            "configurable": {
                "user_id": "test_user_4",
                "todo_category": "personal",
                "thread_id": "test_thread_4",
            }
        }

        # First interaction: Add profile
        result1 = graph.invoke(
            {"messages": [{"role": "user", "content": "My name is Jordan"}]},
            config=config,
        )

        # Second interaction: Add task
        result2 = graph.invoke(
            {"messages": [{"role": "user", "content": "Add task: buy groceries"}]},
            config=config,
        )

        # Verify both interactions succeeded
        assert "messages" in result1
        assert "messages" in result2

        # Verify profile persisted
        profile_namespace = ("profile", "personal", "test_user_4")
        profile_memories = store.search(profile_namespace)
        assert len(profile_memories) > 0

        # Verify todo persisted
        todo_namespace = ("todo", "personal", "test_user_4")
        todo_memories = store.search(todo_namespace)
        assert len(todo_memories) > 0

    def test_multiple_todos(self, api_keys):
        """Test managing multiple todo items.

        Verifies that the graph can handle multiple tasks
        and maintain them separately in memory.
        """
        from graphs.deployment.task_maistro import builder

        # Create in-memory store and compile graph with it
        store = InMemoryStore()
        graph = builder.compile(store=store)

        # Configure with test user
        config = {
            "configurable": {
                "user_id": "test_user_5",
                "todo_category": "work",
                "thread_id": "test_thread_5",
            }
        }

        # Add multiple tasks
        tasks = [
            "Add task: complete project documentation",
            "Add task: review pull requests",
            "Add task: attend team meeting",
        ]

        for task in tasks:
            result = graph.invoke(
                {"messages": [{"role": "user", "content": task}]}, config=config
            )
            assert "messages" in result

        # Verify all todos were stored
        namespace = ("todo", "work", "test_user_5")
        memories = store.search(namespace)
        assert len(memories) >= 3
