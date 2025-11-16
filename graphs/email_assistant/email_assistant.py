"""Email assistant graph for automated email triage and response.

This module implements an email assistant that:
1. Triages incoming emails (respond, notify, or ignore)
2. Generates appropriate responses using tools
3. Manages calendar and meeting scheduling

Example:
    >>> email = {"author": "john@example.com", "to": "me@example.com", ...}
    >>> result = email_assistant.invoke({"email_input": email})
"""

from typing import Literal, Dict, Any

from langchain.chat_models import init_chat_model

from graphs.email_assistant.tools import get_tools, get_tools_by_name
from graphs.email_assistant.tools.default.prompt_templates import AGENT_TOOLS_PROMPT
from graphs.email_assistant.prompts import (
    triage_system_prompt,
    triage_user_prompt,
    agent_system_prompt,
    default_background,
    default_triage_instructions,
    default_response_preferences,
    default_cal_preferences,
)
from graphs.email_assistant.schemas import State, RouterSchema, StateInput
from graphs.email_assistant.utils import parse_email, format_email_markdown

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from dotenv import load_dotenv

from graphs.utils import get_logger, retry_with_backoff, create_api_error

load_dotenv(".env")

# Initialize logger for this module
logger = get_logger(__name__)

# Get tools
tools = get_tools()
tools_by_name = get_tools_by_name(tools)

# Initialize the LLM for use with router / structured output
llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
llm_router = llm.with_structured_output(RouterSchema)

# Initialize the LLM, enforcing tool use (of any available tools) for agent
llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
llm_with_tools = llm.bind_tools(tools, tool_choice="any")


# Nodes
@retry_with_backoff(max_retries=2, initial_delay=1.0)
def llm_call(state: State) -> Dict[str, Any]:
    """LLM decides whether to call a tool or not.

    Args:
        state: Current email assistant state.

    Returns:
        Dictionary with updated messages including tool calls.

    Raises:
        ValueError: If messages are missing from state.
    """
    logger.info("Processing LLM call for email assistant")
    
    try:
        # Validate required state fields
        if not state.get("messages"):
            logger.error("LLM call failed: missing messages in state")
            raise ValueError("Messages are required in state")
        
        logger.debug(f"Processing {len(state['messages'])} messages")

        response = llm_with_tools.invoke(
            [
                {
                    "role": "system",
                    "content": agent_system_prompt.format(
                        tools_prompt=AGENT_TOOLS_PROMPT,
                        background=default_background,
                        response_preferences=default_response_preferences,
                        cal_preferences=default_cal_preferences,
                    ),
                },
            ]
            + state["messages"]
        )
        
        logger.info("LLM call completed successfully")
        
        return {"messages": [response]}
        
    except ValueError as e:
        # Re-raise validation errors
        raise
    except Exception as e:
        # Create detailed error
        api_error = create_api_error("process email with LLM", e, "OpenAI")
        logger.error(f"LLM call failed: {api_error}")
        return {"messages": [{"role": "assistant", "content": str(api_error)}]}


def tool_node(state: State) -> Dict[str, Any]:
    """Execute tool calls from the LLM.

    Args:
        state: Current email assistant state with tool calls.

    Returns:
        Dictionary with tool execution results.
    """
    result = []
    logger.info("Executing tool calls")
    
    try:
        # Validate that we have messages with tool calls
        if not state.get("messages") or not state["messages"][-1].tool_calls:
            logger.error("Tool node failed: no tool calls found in messages")
            raise ValueError("No tool calls found in messages")
        
        tool_calls = state["messages"][-1].tool_calls
        logger.debug(f"Processing {len(tool_calls)} tool calls")

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            logger.info(f"Executing tool: {tool_name}")
            
            try:
                tool = tools_by_name[tool_name]
                observation = tool.invoke(tool_call["args"])
                result.append(
                    {
                        "role": "tool",
                        "content": observation,
                        "tool_call_id": tool_call["id"],
                    }
                )
                logger.info(f"Tool {tool_name} executed successfully")
                
            except KeyError:
                error_msg = f"Tool '{tool_name}' not found. Available tools: {', '.join(tools_by_name.keys())}"
                logger.error(error_msg)
                result.append(
                    {
                        "role": "tool",
                        "content": error_msg,
                        "tool_call_id": tool_call["id"],
                    }
                )
            except Exception as e:
                error_msg = f"Tool '{tool_name}' execution failed: {str(e)}"
                logger.error(error_msg)
                result.append(
                    {
                        "role": "tool",
                        "content": error_msg,
                        "tool_call_id": tool_call["id"],
                    }
                )

        return {"messages": result}

    except Exception as e:
        # Return error message
        error_msg = f"Tool node failed: {str(e)}"
        logger.error(error_msg)
        return {"messages": [{"role": "assistant", "content": error_msg}]}


# Conditional edge function
def should_continue(state: State) -> Literal["Action", "__end__"]:
    """Route to Action node or end if Done tool was called.

    Args:
        state: Current email assistant state.

    Returns:
        Next node name or END.
    """
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            if tool_call["name"] == "Done":
                return END
            else:
                return "Action"


# Build workflow
agent_builder = StateGraph(State)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("environment", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        # Name returned by should_continue : Name of next node to visit
        "Action": "environment",
        END: END,
    },
)
agent_builder.add_edge("environment", "llm_call")

# Compile the agent
agent = agent_builder.compile()


@retry_with_backoff(max_retries=2, initial_delay=1.0)
def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:
    """Analyze email content to decide if we should respond, notify, or ignore.

    The triage step prevents the assistant from wasting time on:
    - Marketing emails and spam
    - Company-wide announcements
    - Messages meant for other teams
    """
    try:
        logger.info("Starting email triage")
        
        author, to, subject, email_thread = parse_email(state["email_input"])
        subject_preview = subject[:50] if subject else "No subject"
        logger.debug(f"Triaging email from {author} with subject: {subject_preview}")
        
        system_prompt = triage_system_prompt.format(
            background=default_background, triage_instructions=default_triage_instructions
        )

        user_prompt = triage_user_prompt.format(
            author=author, to=to, subject=subject, email_thread=email_thread
        )

        # Create email markdown for Agent Inbox in case of notification
        email_markdown = format_email_markdown(subject, author, to, email_thread)

        # Run the router LLM
        result = llm_router.invoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        # Decision
        classification = result.classification
        logger.info(f"Email classified as: {classification}")

        if classification == "respond":
            print("📧 Classification: RESPOND - This email requires a response")
            goto = "response_agent"
            # Add the email to the messages
            update = {
                "classification_decision": result.classification,
                "messages": [
                    {"role": "user", "content": f"Respond to the email: {email_markdown}"}
                ],
            }
        elif result.classification == "ignore":
            print("🚫 Classification: IGNORE - This email can be safely ignored")
            update = {
                "classification_decision": result.classification,
            }
            goto = END
        elif result.classification == "notify":
            # If real life, this would do something else
            print("🔔 Classification: NOTIFY - This email contains important information")
            update = {
                "classification_decision": result.classification,
            }
            goto = END
        else:
            error_msg = f"Invalid classification: {result.classification}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        return Command(goto=goto, update=update)
        
    except Exception as e:
        api_error = create_api_error("triage email", e, "OpenAI")
        logger.error(f"Email triage failed: {api_error}")
        raise


# Build workflow
overall_workflow = (
    StateGraph(State, input_schema=StateInput)
    .add_node(triage_router)
    .add_node("response_agent", agent)
    .add_edge(START, "triage_router")
)

graph = overall_workflow.compile()

# Backward compatibility alias
email_assistant = graph
