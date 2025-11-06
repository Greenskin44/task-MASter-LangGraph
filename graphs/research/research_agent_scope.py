"""Research Agent Scoping Functions

This module contains the functions for user clarification and research brief generation
that are used in the full research agent workflow.
"""

from langchain_core.messages import HumanMessage, AIMessage
from langchain.chat_models import init_chat_model

from graphs.research.state_scope import AgentState, ClarifyWithUser, ResearchQuestion
from graphs.research.prompts import (
    clarify_with_user_instructions,
    transform_messages_into_research_topic_prompt,
)
from graphs.research.utils import get_today_str

# Initialize the model for scoping tasks
scoping_model = init_chat_model(model="openai:gpt-4o", max_tokens=4000)


async def clarify_with_user(state: AgentState):
    """
    Clarify with user node.
    
    Determines if clarification is needed from the user before proceeding with research.
    If clarification is needed, asks a question. Otherwise, proceeds to research brief generation.
    """
    messages = state.get("messages", [])
    
    # Format the prompt with current messages
    # Use replace() instead of format() to avoid issues with curly braces in message content
    messages_str = "\n".join([f"{msg.type}: {msg.content}" for msg in messages])
    prompt = clarify_with_user_instructions.replace("{messages}", messages_str).replace("{date}", get_today_str())
    
    # Get structured output from the model
    structured_model = scoping_model.with_structured_output(ClarifyWithUser)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])
    
    # If clarification is needed, add the question to messages and wait for user response
    if response.need_clarification:
        return {
            "messages": [AIMessage(content=response.question)],
        }
    else:
        # No clarification needed, add verification message and proceed
        return {
            "messages": [AIMessage(content=response.verification)],
        }


async def write_research_brief(state: AgentState):
    """
    Write research brief node.
    
    Transforms the conversation history into a detailed research question/brief
    that will guide the research process.
    """
    messages = state.get("messages", [])
    
    # Format the prompt with current messages
    # Use replace() instead of format() to avoid issues with curly braces in message content
    messages_str = "\n".join([f"{msg.type}: {msg.content}" for msg in messages])
    prompt = transform_messages_into_research_topic_prompt.replace("{messages}", messages_str).replace("{date}", get_today_str())
    
    # Get structured output from the model
    structured_model = scoping_model.with_structured_output(ResearchQuestion)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])
    
    return {
        "research_brief": response.research_brief,
        "messages": [AIMessage(content=f"Research brief created: {response.research_brief}")],
    }
