"""Parallelization demonstration graph for LangGraph.

This module demonstrates parallel execution of search operations using LangGraph.
It performs simultaneous web and Wikipedia searches, then generates an answer
based on the combined context.

Example:
    >>> result = graph.invoke({"question": "What is LangGraph?"})
    >>> print(result["answer"])
"""

import operator
from typing import Annotated, Dict, Any
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from langchain_community.document_loaders import WikipediaLoader
from langchain_community.tools import TavilySearchResults

from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="gpt-4o", temperature=0)


class State(TypedDict):
    """State schema for the parallelization graph.

    Attributes:
        question: The user's question to be answered.
        answer: The generated answer based on search results.
        context: Accumulated search results from multiple sources.
    """

    question: str
    answer: str
    context: Annotated[list, operator.add]


def search_web(state: State) -> Dict[str, Any]:
    """Retrieve documents from web search using Tavily.

    Performs a web search for the question and formats the results
    as structured documents with URLs and content.

    Args:
        state: Current graph state containing the question.

    Returns:
        Dictionary with formatted search results added to context.

    Raises:
        ValueError: If question is missing from state.
    """
    try:
        # Validate required state fields
        if not state.get("question"):
            raise ValueError("Question is required in state")

        # Search
        tavily_search = TavilySearchResults(max_results=3)
        search_docs = tavily_search.invoke(state["question"])

        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                for doc in search_docs
            ]
        )

        return {"context": [formatted_search_docs]}

    except Exception as e:
        # Return error context instead of failing
        error_msg = f"Web search failed: {str(e)}"
        return {"context": [f"<Error>{error_msg}</Error>"]}


def search_wikipedia(state: State) -> Dict[str, Any]:
    """Retrieve documents from Wikipedia.

    Searches Wikipedia for articles related to the question and formats
    the results with source metadata.

    Args:
        state: Current graph state containing the question.

    Returns:
        Dictionary with formatted Wikipedia results added to context.

    Raises:
        ValueError: If question is missing from state.
    """
    try:
        # Validate required state fields
        if not state.get("question"):
            raise ValueError("Question is required in state")

        # Search
        search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()

        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ]
        )

        return {"context": [formatted_search_docs]}

    except Exception as e:
        # Return error context instead of failing
        error_msg = f"Wikipedia search failed: {str(e)}"
        return {"context": [f"<Error>{error_msg}</Error>"]}


def generate_answer(state: State) -> Dict[str, Any]:
    """Generate an answer based on accumulated search context.

    Uses the LLM to synthesize information from web and Wikipedia searches
    into a coherent answer to the user's question.

    Args:
        state: Current graph state with question and accumulated context.

    Returns:
        Dictionary with the generated answer.

    Raises:
        ValueError: If required state fields are missing.
    """
    try:
        # Validate required state fields
        if not state.get("question"):
            raise ValueError("Question is required in state")
        if not state.get("context"):
            raise ValueError("Context is required in state")

        # Get state
        context = state["context"]
        question = state["question"]

        # Template
        answer_template = (
            """Answer the question {question} using this context: {context}"""
        )
        answer_instructions = answer_template.format(question=question, context=context)

        # Answer
        answer = llm.invoke(
            [SystemMessage(content=answer_instructions)]
            + [HumanMessage(content=f"Answer the question.")]
        )

        # Append it to state
        return {"answer": answer}

    except Exception as e:
        # Return error message as answer
        error_msg = f"Failed to generate answer: {str(e)}"
        return {"answer": AIMessage(content=error_msg)}


# Add nodes
builder = StateGraph(State)

# Initialize each node with node_secret
builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

# Flow
builder.add_edge(START, "search_wikipedia")
builder.add_edge(START, "search_web")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("generate_answer", END)
graph = builder.compile()
