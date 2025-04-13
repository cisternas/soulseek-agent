from langgraph.graph import StateGraph, END
from .nodes import artist_recognition_node, extract_artist_and_title_node
from .state import State

def create_workflow() -> StateGraph:
    workflow = StateGraph(State)

    # Add nodes to the workflow
    workflow.add_node("artist_recognition", artist_recognition_node)
    workflow.add_node("extract_artist_and_title", extract_artist_and_title_node)

    # Set the entry point of the graph
    workflow.set_entry_point("artist_recognition")

    # Add edges between nodes
    workflow.add_edge("artist_recognition", "extract_artist_and_title")
    workflow.add_edge("extract_artist_and_title", END)

    return workflow.compile()