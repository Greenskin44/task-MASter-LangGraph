"""Map-reduce pattern demonstration for LangGraph.

This module demonstrates the map-reduce pattern using LangGraph's Send() API.
It generates jokes about sub-topics and selects the best one using a
dynamic map-reduce workflow.

Example:
    >>> result = graph.invoke({"topic": "artificial intelligence"})
    >>> print(result["best_selected_joke"])
"""

import operator
from typing import Annotated, Dict, Any
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI

from langgraph.constants import Send
from langgraph.graph import END, StateGraph, START

# Prompts we will use
subjects_prompt = """Generate a list of 3 sub-topics that are all related to this overall topic: {topic}."""
joke_prompt = """Generate a joke about {subject}"""
best_joke_prompt = """Below are a bunch of jokes about {topic}. Select the best one! Return the ID of the best one, starting 0 as the ID for the first joke. Jokes: \n\n  {jokes}"""

# LLM
model = ChatOpenAI(model="gpt-4o", temperature=0)


# Define the state
class Subjects(BaseModel):
    """Schema for generated sub-topics.

    Attributes:
        subjects: List of sub-topic strings related to the main topic.
    """

    subjects: list[str]


class BestJoke(BaseModel):
    """Schema for best joke selection.

    Attributes:
        id: Index of the best joke in the jokes list.
    """

    id: int


class OverallState(TypedDict):
    topic: str
    subjects: list
    jokes: Annotated[list, operator.add]
    best_selected_joke: str


def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}


class JokeState(TypedDict):
    subject: str


class Joke(BaseModel):
    joke: str


def generate_joke(state: JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Joke).invoke(prompt)
    return {"jokes": [response.joke]}


def best_joke(state: OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"], jokes=jokes)
    response = model.with_structured_output(BestJoke).invoke(prompt)
    return {"best_selected_joke": state["jokes"][response.id]}


def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


# Construct the graph: here we put everything together to construct our graph
graph_builder = StateGraph(OverallState)
graph_builder.add_node("generate_topics", generate_topics)
graph_builder.add_node("generate_joke", generate_joke)
graph_builder.add_node("best_joke", best_joke)
graph_builder.add_edge(START, "generate_topics")
graph_builder.add_conditional_edges(
    "generate_topics", continue_to_jokes, ["generate_joke"]
)
graph_builder.add_edge("generate_joke", "best_joke")
graph_builder.add_edge("best_joke", END)

# Compile the graph
graph = graph_builder.compile()
