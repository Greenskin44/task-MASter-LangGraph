"""Sub-graphs demonstration for LangGraph.

This module demonstrates nested graph composition using sub-graphs.
It processes logs through two parallel sub-graphs: failure analysis
and question summarization.

Example:
    >>> logs = [{"id": "1", "question": "How to use Chroma?", ...}]
    >>> result = graph.invoke({"raw_logs": logs})
    >>> print(result["fa_summary"], result["report"])
"""

from operator import add
from typing import List, Optional, Annotated, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# The structure of the logs
class Log(TypedDict):
    """Schema for log entries.

    Attributes:
        id: Unique identifier for the log entry.
        question: The question that was asked.
        docs: Optional list of documents retrieved.
        answer: The answer that was provided.
        grade: Optional quality grade for the answer.
        grader: Optional identifier of who graded the answer.
        feedback: Optional feedback on the answer quality.
    """

    id: str
    question: str
    docs: Optional[List]
    answer: str
    grade: Optional[int]
    grader: Optional[str]
    feedback: Optional[str]


# Failure Analysis Sub-graph
class FailureAnalysisState(TypedDict):
    """State schema for failure analysis sub-graph.

    Attributes:
        cleaned_logs: Preprocessed log entries.
        failures: Log entries that contain failures.
        fa_summary: Summary of failure analysis.
        processed_logs: List of processed log identifiers.
    """

    cleaned_logs: List[Log]
    failures: List[Log]
    fa_summary: str
    processed_logs: List[str]


class FailureAnalysisOutputState(TypedDict):
    """Output state schema for failure analysis sub-graph.

    Attributes:
        fa_summary: Summary of failure analysis.
        processed_logs: List of processed log identifiers.
    """

    fa_summary: str
    processed_logs: List[str]


def get_failures(state: FailureAnalysisState) -> Dict[str, Any]:
    """Extract logs that contain failures.

    Filters the cleaned logs to identify entries with grade information,
    indicating they were evaluated and potentially failed.

    Args:
        state: Current failure analysis state with cleaned logs.

    Returns:
        Dictionary with filtered failure logs.
    """
    cleaned_logs = state["cleaned_logs"]
    failures = [log for log in cleaned_logs if "grade" in log]
    return {"failures": failures}


def generate_summary(state: FailureAnalysisState) -> Dict[str, Any]:
    """Generate summary of failures"""
    failures = state["failures"]
    # Add fxn: fa_summary = summarize(failures)
    fa_summary = "Poor quality retrieval of Chroma documentation."
    return {
        "fa_summary": fa_summary,
        "processed_logs": [
            f"failure-analysis-on-log-{failure['id']}" for failure in failures
        ],
    }


fa_builder = StateGraph(FailureAnalysisState, output_schema=FailureAnalysisOutputState)
fa_builder.add_node("get_failures", get_failures)
fa_builder.add_node("generate_summary", generate_summary)
fa_builder.add_edge(START, "get_failures")
fa_builder.add_edge("get_failures", "generate_summary")
fa_builder.add_edge("generate_summary", END)


# Summarization subgraph
class QuestionSummarizationState(TypedDict):
    cleaned_logs: List[Log]
    qs_summary: str
    report: str
    processed_logs: List[str]


class QuestionSummarizationOutputState(TypedDict):
    report: str
    processed_logs: List[str]


def generate_summary(state):
    cleaned_logs = state["cleaned_logs"]
    # Add fxn: summary = summarize(generate_summary)
    summary = "Questions focused on usage of ChatOllama and Chroma vector store."
    return {
        "qs_summary": summary,
        "processed_logs": [f"summary-on-log-{log['id']}" for log in cleaned_logs],
    }


def send_to_slack(state):
    qs_summary = state["qs_summary"]
    # Add fxn: report = report_generation(qs_summary)
    report = "foo bar baz"
    return {"report": report}


qs_builder = StateGraph(
    QuestionSummarizationState, output_schema=QuestionSummarizationOutputState
)
qs_builder.add_node("generate_summary", generate_summary)
qs_builder.add_node("send_to_slack", send_to_slack)
qs_builder.add_edge(START, "generate_summary")
qs_builder.add_edge("generate_summary", "send_to_slack")
qs_builder.add_edge("send_to_slack", END)


# Entry Graph
class EntryGraphState(TypedDict):
    raw_logs: List[Log]
    cleaned_logs: List[Log]
    fa_summary: str  # This will only be generated in the FA sub-graph
    report: str  # This will only be generated in the QS sub-graph
    processed_logs: Annotated[
        List[int], add
    ]  # This will be generated in BOTH sub-graphs


def clean_logs(state):
    # Get logs
    raw_logs = state["raw_logs"]
    # Data cleaning raw_logs -> docs
    cleaned_logs = raw_logs
    return {"cleaned_logs": cleaned_logs}


entry_builder = StateGraph(EntryGraphState)
entry_builder.add_node("clean_logs", clean_logs)
entry_builder.add_node("question_summarization", qs_builder.compile())
entry_builder.add_node("failure_analysis", fa_builder.compile())

entry_builder.add_edge(START, "clean_logs")
entry_builder.add_edge("clean_logs", "failure_analysis")
entry_builder.add_edge("clean_logs", "question_summarization")
entry_builder.add_edge("failure_analysis", END)
entry_builder.add_edge("question_summarization", END)

graph = entry_builder.compile()
