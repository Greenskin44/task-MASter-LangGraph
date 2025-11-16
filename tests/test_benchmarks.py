"""Performance benchmarks for LangGraph graphs.

This module contains performance benchmarks for all graphs to establish
baseline metrics and detect performance regressions.

Benchmarks measure:
- Graph execution time
- Memory usage patterns
- API call efficiency

Run benchmarks with: pytest tests/test_benchmarks.py --benchmark-only
Compare results with: pytest tests/test_benchmarks.py --benchmark-compare
"""

import pytest
from typing import Dict, Any


@pytest.mark.benchmark
@pytest.mark.integration
class TestStudioGraphBenchmarks:
    """Performance benchmarks for studio demonstration graphs."""

    def test_parallelization_performance(self, api_keys, sample_question, benchmark):
        """Benchmark parallelization graph execution time.

        Measures the time to execute web and Wikipedia searches in parallel
        and generate an answer.
        """
        from graphs.studio.parallelization import graph

        def run_graph():
            return graph.invoke({"question": sample_question})

        result = benchmark(run_graph)

        # Verify result is valid
        assert "answer" in result
        assert "context" in result

    def test_sub_graphs_performance(self, api_keys, sample_logs, benchmark):
        """Benchmark sub-graphs execution time.

        Measures the time to process logs through failure analysis
        and question summarization sub-graphs.
        """
        from graphs.studio.sub_graphs import graph

        def run_graph():
            return graph.invoke({"raw_logs": sample_logs})

        result = benchmark(run_graph)

        # Verify result is valid
        assert "fa_summary" in result
        assert "report" in result

    def test_map_reduce_performance(self, api_keys, sample_topic, benchmark):
        """Benchmark map-reduce graph execution time.

        Measures the time to generate sub-topics, create jokes,
        and select the best one.
        """
        from graphs.studio.map_reduce import graph

        def run_graph():
            return graph.invoke({"topic": sample_topic})

        result = benchmark(run_graph)

        # Verify result is valid
        assert "best_selected_joke" in result
        assert "jokes" in result

    def test_research_assistant_performance(self, api_keys, benchmark):
        """Benchmark research assistant graph execution time.

        Measures the time to create analysts, conduct interviews,
        and generate a final report.
        
        Note: This graph uses interrupt_before, so we only benchmark
        the analyst creation phase for consistent timing.
        """
        from graphs.studio.research_assistant import graph

        def run_graph():
            return graph.invoke(
                {
                    "topic": "LangGraph basics",
                    "max_analysts": 2,
                    "human_analyst_feedback": "approve",
                },
                config={"recursion_limit": 100},
            )

        result = benchmark(run_graph)

        # Verify result is valid (analysts created)
        assert "analysts" in result
        assert len(result["analysts"]) == 2


@pytest.mark.benchmark
@pytest.mark.integration
class TestDeploymentGraphBenchmarks:
    """Performance benchmarks for deployment graphs."""

    def test_task_maistro_performance(self, api_keys, sample_task_message, benchmark):
        """Benchmark task_maistro graph execution time.

        Measures the time to process a task management message
        and update memories.
        """
        from graphs.deployment.task_maistro import builder
        from langgraph.store.memory import InMemoryStore

        def run_graph():
            store = InMemoryStore()
            graph = builder.compile(store=store)
            config = {
                "configurable": {
                    "thread_id": "benchmark_thread",
                    "user_id": "benchmark_user",
                    "todo_category": "personal",
                }
            }
            return graph.invoke(
                {"messages": [{"role": "user", "content": sample_task_message}]},
                config=config,
            )

        result = benchmark(run_graph)

        # Verify result is valid
        assert "messages" in result


@pytest.mark.benchmark
@pytest.mark.integration
class TestEmailAssistantBenchmarks:
    """Performance benchmarks for email assistant workflows."""

    def test_email_triage_respond_performance(
        self, api_keys, sample_email_respond, benchmark
    ):
        """Benchmark email triage for respond classification.

        Measures the time to classify and process an email
        that requires a response.
        """
        from graphs.email_assistant.email_assistant import graph

        def run_graph():
            return graph.invoke({"email_input": sample_email_respond})

        result = benchmark(run_graph)

        # Verify result is valid
        assert "classification_decision" in result

    def test_email_triage_notify_performance(
        self, api_keys, sample_email_notify, benchmark
    ):
        """Benchmark email triage for notify classification.

        Measures the time to classify and process an email
        that requires notification.
        """
        from graphs.email_assistant.email_assistant import graph

        def run_graph():
            return graph.invoke({"email_input": sample_email_notify})

        result = benchmark(run_graph)

        # Verify result is valid
        assert "classification_decision" in result


@pytest.mark.benchmark
@pytest.mark.integration
class TestResearchAgentBenchmarks:
    """Performance benchmarks for research agent workflows."""

    def test_research_workflow_performance(
        self, api_keys, sample_research_topic, benchmark
    ):
        """Benchmark research workflow execution time.

        Measures the time to process a research request through
        clarification, brief generation, and report synthesis.
        
        Note: This graph uses async nodes, so we skip this benchmark
        for synchronous testing. Use async benchmarks instead.
        """
        pytest.skip("Research agent requires async execution - use async benchmarks")
        
        # This test is skipped because the research_agent_full graph
        # uses async nodes that cannot be invoked synchronously
