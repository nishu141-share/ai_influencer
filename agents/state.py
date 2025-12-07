from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    """
    Represents the state of the AI Influencer creation pipeline.
    """
    topic: str
    script: Optional[str]
    
    # Asset Paths
    audio_path: Optional[str]
    image_path: Optional[str]
    video_path: Optional[str]
    
    # Status / Errors
    current_step: str
    error: Optional[str]
