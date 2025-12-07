import os
from agents.state import AgentState

def visual_artist_node(state: AgentState) -> AgentState:
    """
    Generates or retrieves the character image.
    Currently returns the pre-generated test character.
    """
    print(f"--> VisualArtist retrieving character...")
    
    # In a real scenario, this would call Fooocus API
    # For now, we use the static asset
    image_path = os.path.abspath("test_character.png")
    
    if not os.path.exists(image_path):
        return {"error": "Test character image not found."}
        
    return {
        "image_path": image_path,
        "current_step": "image_ready"
    }
