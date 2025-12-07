from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes.writer import script_writer_node
from agents.nodes.voice import voice_artist_node
from agents.nodes.artist import visual_artist_node
from agents.nodes.video import animator_node

def create_agent_graph():
    """
    Constructs the LangGraph for the AI Influencer pipeline.
    """
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("script_writer", script_writer_node)
    workflow.add_node("voice_artist", voice_artist_node)
    workflow.add_node("visual_artist", visual_artist_node)
    workflow.add_node("animator", animator_node)
    
    # Add Edges (Linear flow)
    # Start -> ScriptWriter
    workflow.set_entry_point("script_writer")
    
    # ScriptWriter -> VoiceArtist
    workflow.add_edge("script_writer", "voice_artist")
    
    # VoiceArtist -> VisualArtist (Can be parallel actually, but linear for safety)
    workflow.add_edge("voice_artist", "visual_artist")
    
    # VisualArtist -> Animator
    workflow.add_edge("visual_artist", "animator")
    
    # Animator -> End
    workflow.add_edge("animator", END)
    
    return workflow.compile()

if __name__ == "__main__":
    # Test the graph construction
    app = create_agent_graph()
    print("Graph compiled successfully.")
    try:
        print(app.get_graph().draw_ascii())
    except ImportError:
        print("Install langgraph[plotting] or langchain-core to see ascii graph")
