import os
import sys
import subprocess
from .base_agent import AgentBase

class VisualAgent(AgentBase):
    def __init__(self, config_path=None):
        super().__init__("VisualAgent", config_path)
        
        # Locate SadTalker
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # agents -> ai_influencer
        self.tools_dir = os.path.join(self.base_dir, "tools")
        self.sadtalker_dir = os.path.join(self.tools_dir, "SadTalker")
        self.inference_script = os.path.join(self.sadtalker_dir, "inference.py")
        
    def run(self, input_data):
        """
        Input: {'audio_path': str, 'image_path': str, 'output_dir': str (optional)}
        Output: {'video_path': str}
        """
        audio_path = input_data.get("audio_path")
        image_path = input_data.get("image_path")
        
        if not audio_path or not image_path:
            self.log("Error: Missing audio or image path.")
            return None

        # Default output dir
        output_dir = input_data.get("output_dir", os.path.join(self.base_dir, "output"))
        os.makedirs(output_dir, exist_ok=True)
        
        self.log(f"Generating video from {image_path} and {audio_path}...")
        
        # Determine device (simple check)
        # For now, default to CPU as established in verifying process
        # TODO: Add dynamic check if CUDA becomes available
        device_flag = "--cpu" 

        # Construct command
        # Using fixed arguments from our successful manual test: --still --preprocess crop
        cmd = [
            sys.executable, self.inference_script,
            "--driven_audio", os.path.abspath(audio_path),
            "--source_image", os.path.abspath(image_path),
            "--result_dir", os.path.abspath(output_dir),
            "--still", 
            "--preprocess", "crop", # Changed from full to crop due to checkpoint mismatch
            device_flag
        ]
        
        self.log(f"Running SadTalker command: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, cwd=self.sadtalker_dir, check=True)
            self.log(f"Video generation complete. Output in {output_dir}")
            
            # Find the generated file (latest mp4 in output_dir)
            # This is a bit hacky because SadTalker creates a timestamped folder
            # We'll return the output_dir for now, orchestration can look inside
            return {"output_dir": output_dir}
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error running SadTalker: {e}")
            return None
