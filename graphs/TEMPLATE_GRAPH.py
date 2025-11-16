"""
Minimal LangGraph Template

Use this as a starting point for creating new graphs.
Copy this file and customize for your specific use case.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


# =============================================================================
# STATE DEFINITION
# =============================================================================

class GraphState(TypedDict):
    """
    Define the state structure for your graph.
    
    The state is passed between nodes and can be updated by each node.
    Use TypedDict for clear structure and type hints.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    # Add your custom state fields here
    # example_field: str
    # counter: int


# =============================================================================
# NODE FUNCTIONS
# =============================================================================

def process_input(state: GraphState) -> GraphState:
    """
    Example node that processes user input.
    
    Nodes receive the current state and return updates to merge into state.
    Return only the fields you want to update.
    """
    # Get the last user message
    user_message = state["messages"][-1].content
    
    # Process with LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke([HumanMessage(content=user_message)])
    
    # Return state updates
    return {
        "messages": [response]
    }


def example_conditional_node(state: GraphState) -> GraphState:
    """
    Example of a node that could be used in conditional routing.
    """
    # Your logic here
    return state


# =============================================================================
# CONDITIONAL EDGES (ROUTING LOGIC)
# =============================================================================

def route_based_on_state(state: GraphState) -> str:
    """
    Example conditional edge function.
    
    Returns the name of the next node to execute.
    Enables dynamic routing based on state.
    """
    # Example: Route based on message content
    last_message = state["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        content = last_message.content
        if isinstance(content, str) and "urgent" in content.lower():
            return "urgent_path"
    
    return "normal_path"


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def create_graph():
    """
    Construct the graph by defining nodes and edges.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize graph with state schema
    builder = StateGraph(GraphState)
    
    # Add nodes
    builder.add_node("process", process_input)
    # Add more nodes as needed
    # builder.add_node("another_node", another_function)
    
    # Add edges
    builder.add_edge(START, "process")
    builder.add_edge("process", END)
    
    # Example conditional edge (commented out)
    # builder.add_conditional_edges(
    #     "process",
    #     route_based_on_state,
    #     {
    #         "urgent_path": "urgent_handler",
    #         "normal_path": "normal_handler"
    #     }
    # )
    
    # Compile with optional memory checkpointer
    # memory = MemorySaver()
    # return builder.compile(checkpointer=memory)
    
    return builder.compile()


# =============================================================================
# GRAPH EXPORT
# =============================================================================

# Create and export the graph
# This is what langgraph.json references
graph = create_graph()


# =============================================================================
# TESTING (Optional - for quick local testing)
# =============================================================================

if __name__ == "__main__":
    """
    Quick test of the graph.
    Run: python -m graphs.your_graph.graph_name
    """
    from langchain_core.messages import HumanMessage
    
    # Test input
    test_state = {
        "messages": [HumanMessage(content="Hello, test the graph!")]
    }
    
    # Run graph
    result = graph.invoke(test_state)
    
    # Print result
    print("Graph output:")
    print(result["messages"][-1].content)
