import subprocess
import sys
import os
from agents.state import AgentState

def animator_node(state: AgentState) -> AgentState:
    """
    Combines Image and Audio into a Video using SadTalker.
    """
    print(f"--> Animator generating video...")
    
    image_path = state.get("image_path")
    audio_path = state.get("audio_path")
    
    if not image_path or not audio_path:
        return {"error": "Missing image or audio path."}
        
    output_dir = os.path.abspath("output_agent_video")
    
    # Path to our existing video generation script
    # We use the script we already verified which handles hardware detection
    base_dir = os.getcwd() # Assumption: running from root
    script_path = os.path.join(base_dir, "video_gen", "generate_video.py")
    
    cmd = [
        sys.executable, script_path,
        "--image", image_path,
        "--audio", audio_path,
        "--output_dir", output_dir
    ]
    
    try:
        print(f"    Running SadTalker wrapper...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"    Animation failed: {result.stderr}")
            return {"error": f"Video generation failed: {result.stderr}"}
            
        print("    Video generated successfully.")
        # Find the output file (SadTalker names them randomly/timestamped)
        # We take the most recent file in the output dir
        files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".mp4")]
        if not files:
             return {"error": "Video generated but file not found in output."}
             
        latest_video = max(files, key=os.path.getctime)
        
        return {
            "video_path": latest_video,
            "current_step": "video_completed"
        }
        
    except Exception as e:
        print(f"    Error in Animator: {e}")
        return {"error": str(e)}
