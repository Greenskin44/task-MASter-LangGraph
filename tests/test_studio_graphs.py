"""Tests for studio demonstration graphs.

This module contains tests for all studio graphs including:
- Parallelization (web + Wikipedia search)
- Sub-graphs (log analysis)
- Map-reduce (joke generation)
- Research assistant (multi-agent research)
"""

import pytest
from typing import Dict, Any


@pytest.mark.studio
@pytest.mark.integration
class TestParallelization:
    """Tests for the parallelization graph."""

    def test_simple_question(self, api_keys, sample_question):
        """Test parallelization with a simple question.

        Verifies that the graph can execute web and Wikipedia searches
        in parallel and generate an answer.
        """
        from graphs.studio.parallelization import graph

        # Execute graph
        result = graph.invoke({"question": sample_question})

        # Verify structure
        assert "answer" in result
        assert "context" in result
        assert "question" in result

        # Verify content
        assert result["question"] == sample_question
        assert len(result["context"]) > 0
        assert result["answer"] is not None

        # Verify answer is an AIMessage
        assert hasattr(result["answer"], "content")
        assert len(result["answer"].content) > 0

    def test_technical_question(self, api_keys):
        """Test parallelization with a technical question.

        Verifies that the graph handles more complex technical queries.
        """
        from graphs.studio.parallelization import graph

        question = "How does parallel execution work in LangGraph?"

        # Execute graph
        result = graph.invoke({"question": question})

        # Verify structure
        assert "answer" in result
        assert "context" in result

        # Verify we got context from both sources
        assert len(result["context"]) >= 2

        # Verify answer contains relevant content
        answer_text = result["answer"].content.lower()
        assert len(answer_text) > 50


@pytest.mark.studio
@pytest.mark.integration
class TestSubGraphs:
    """Tests for the sub-graphs demonstration."""

    def test_basic_logs(self, api_keys, sample_logs):
        """Test sub-graphs with basic log data.

        Verifies that the graph processes logs through both
        failure analysis and question summarization sub-graphs.
        """
        from graphs.studio.sub_graphs import graph

        # Execute graph
        result = graph.invoke({"raw_logs": sample_logs})

        # Verify structure
        assert "fa_summary" in result
        assert "report" in result
        assert "processed_logs" in result

        # Verify content
        assert result["fa_summary"] is not None
        assert len(result["fa_summary"]) > 0
        assert result["report"] is not None
        assert len(result["report"]) > 0

        # Verify processed logs from both sub-graphs
        assert len(result["processed_logs"]) > 0

    def test_logs_with_failures(self, api_keys):
        """Test sub-graphs with logs containing failures.

        Verifies that failure analysis correctly identifies and
        processes logs with grade information.
        """
        from graphs.studio.sub_graphs import graph

        logs_with_failures = [
            {
                "id": "1",
                "question": "Test question 1",
                "answer": "Test answer 1",
                "grade": 2,
                "grader": "human",
                "feedback": "Needs improvement",
            },
            {
                "id": "2",
                "question": "Test question 2",
                "answer": "Test answer 2",
                "grade": 4,
                "grader": "auto",
            },
        ]

        # Execute graph
        result = graph.invoke({"raw_logs": logs_with_failures})

        # Verify failure analysis ran
        assert "fa_summary" in result
        assert result["fa_summary"] is not None

        # Verify processed logs include failure analysis
        failure_logs = [
            log for log in result["processed_logs"] if "failure-analysis" in log
        ]
        assert len(failure_logs) > 0


@pytest.mark.studio
@pytest.mark.integration
class TestMapReduce:
    """Tests for the map-reduce pattern graph."""

    def test_simple_topic(self, api_keys, sample_topic):
        """Test map-reduce with a simple topic.

        Verifies that the graph generates sub-topics, creates jokes
        for each, and selects the best one.
        """
        from graphs.studio.map_reduce import graph

        # Execute graph
        result = graph.invoke({"topic": sample_topic})

        # Verify structure
        assert "best_selected_joke" in result
        assert "jokes" in result
        assert "subjects" in result

        # Verify content
        assert result["best_selected_joke"] is not None
        assert len(result["best_selected_joke"]) > 0
        assert len(result["jokes"]) > 0
        assert len(result["subjects"]) > 0

        # Verify best joke is one of the generated jokes
        assert result["best_selected_joke"] in result["jokes"]

    def test_technical_topic(self, api_keys):
        """Test map-reduce with a technical topic.

        Verifies that the graph handles technical topics appropriately.
        """
        from graphs.studio.map_reduce import graph

        topic = "quantum computing"

        # Execute graph
        result = graph.invoke({"topic": topic})

        # Verify structure
        assert "best_selected_joke" in result
        assert "jokes" in result

        # Verify we got multiple jokes
        assert len(result["jokes"]) >= 3

        # Verify best joke was selected
        assert result["best_selected_joke"] in result["jokes"]


@pytest.mark.studio
@pytest.mark.integration
class TestResearchAssistant:
    """Tests for the research assistant multi-agent graph."""

    def test_simple_research(self, api_keys):
        """Test research assistant with a simple topic.

        Verifies that the graph creates analysts, conducts interviews,
        and generates a final report.
        """
        from graphs.studio.research_assistant import graph

        # Execute graph with auto-approval
        result = graph.invoke(
            {
                "topic": "LangGraph basics",
                "max_analysts": 2,
                "human_analyst_feedback": "approve",
            },
            config={"recursion_limit": 100},
        )

        # Verify structure
        assert "analysts" in result
        assert "sections" in result
        assert "final_report" in result

        # Verify analysts were created
        assert len(result["analysts"]) == 2

        # Verify sections were written
        assert len(result["sections"]) > 0

        # Verify final report was generated
        assert result["final_report"] is not None
        assert len(result["final_report"]) > 100

    def test_research_with_max_analysts(self, api_keys):
        """Test research assistant with multiple analysts.

        Verifies that the graph correctly creates the specified
        number of analysts and coordinates their work.
        """
        from graphs.studio.research_assistant import graph

        # Execute graph with 3 analysts
        result = graph.invoke(
            {
                "topic": "AI safety",
                "max_analysts": 3,
                "human_analyst_feedback": "approve",
            },
            config={"recursion_limit": 100},
        )

        # Verify correct number of analysts
        assert len(result["analysts"]) == 3

        # Verify each analyst has required fields
        for analyst in result["analysts"]:
            assert hasattr(analyst, "name")
            assert hasattr(analyst, "role")
            assert hasattr(analyst, "affiliation")
            assert hasattr(analyst, "description")

        # Verify final report includes content from multiple perspectives
        assert "final_report" in result
        assert len(result["final_report"]) > 200
