"""
Avatar Generator - Integrates SadTalker for talking head videos
"""

import os
import sys
from pathlib import Path
from typing import Optional, List


class AvatarGenerator:
    """Integrates SadTalker for AI influencer avatar animation"""
    
    def __init__(
        self,
        sadtalker_path: Optional[str] = None,
        checkpoint_path: Optional[str] = None
    ):
        """
        Initialize Avatar Generator
        
        Args:
            sadtalker_path: Path to SadTalker repository
            checkpoint_path: Path to SadTalker checkpoints
        """
        self.sadtalker_path = Path(sadtalker_path or os.getenv('SADTALKER_PATH', './tools/SadTalker'))
        self.checkpoint_path = Path(checkpoint_path or os.getenv('SADTALKER_CHECKPOINT_PATH', './tools/SadTalker/checkpoints'))
        
        # Check if SadTalker exists
        if not self.sadtalker_path.exists():
            print(f"⚠️ SadTalker not found at: {self.sadtalker_path}")
            print("   Please clone SadTalker or set SADTALKER_PATH")
            self.available = False
        else:
            # Add SadTalker to path
            sys.path.insert(0, str(self.sadtalker_path))
            self.available = True
            print(f"✅ SadTalker found at: {self.sadtalker_path}")
    
    def generate_talking_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        enhancer: str = 'gfpgan',
        preprocess: str = 'crop',
        still_mode: bool = True,
        expression_scale: float = 1.0,
        pose_style: int = 0
    ) -> str:
        """
        Generate talking head video using SadTalker
        
        Args:
            image_path: Path to influencer image
            audio_path: Path to audio file
            output_path: Where to save video
            enhancer: Face enhancement ('gfpgan' or 'RestoreFormer')
            preprocess: Preprocessing mode ('crop', 'resize', 'full')
            still_mode: Minimize head movement
            expression_scale: Expression intensity (0.0-2.0)
            pose_style: Pose style (0-45)
            
        Returns:
            Path to generated video
        """
        if not self.available:
            raise RuntimeError("SadTalker not available. Please set it up first.")
        
        try:
            print(f"🎭 Generating avatar video...")
            print(f"   Image: {image_path}")
            print(f"   Audio: {audio_path}")
            
            # Import SadTalker inference
            try:
                from inference import main as sadtalker_inference
            except ImportError:
                print("❌ Could not import SadTalker. Make sure it's properly installed.")
                raise
            
            # Prepare output directory
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Run SadTalker inference
            result = sadtalker_inference(
                source_image=str(image_path),
                driven_audio=str(audio_path),
                result_dir=str(output_dir),
                enhancer=enhancer,
                preprocess=preprocess,
                still_mode=still_mode,
                use_idle_mode=False,
                batch_size=1,
                size=512,
                pose_style=pose_style,
                expression_scale=expression_scale,
                checkpoint_dir=str(self.checkpoint_path)
            )
            
            print(f"✅ Avatar video generated: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Error generating avatar video: {e}")
            raise
    
    def batch_generate(
        self,
        image_path: str,
        audio_files: List[str],
        output_dir: str,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple videos from audio files
        
        Args:
            image_path: Path to influencer image
            audio_files: List of audio file paths
            output_dir: Directory to save videos
            **kwargs: Additional arguments for generate_talking_video
            
        Returns:
            List of generated video paths
        """
        results = []
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, audio_file in enumerate(audio_files):
            print(f"\n🎬 Generating video {i+1}/{len(audio_files)}...")
            
            video_path = output_path / f"segment_{i:03d}.mp4"
            
            try:
                result = self.generate_talking_video(
                    image_path=image_path,
                    audio_path=audio_file,
                    output_path=str(video_path),
                    **kwargs
                )
                results.append(result)
            except Exception as e:
                print(f"⚠️ Failed to generate video {i+1}: {e}")
                continue
        
        print(f"\n✅ Generated {len(results)}/{len(audio_files)} videos")
        return results
    
    def is_available(self) -> bool:
        """Check if SadTalker is available"""
        return self.available
    
    @staticmethod
    def setup_instructions():
        """Print setup instructions for SadTalker"""
        instructions = """
╔════════════════════════════════════════════════════════════════╗
║                  SadTalker Setup Instructions                  ║
╚════════════════════════════════════════════════════════════════╝

1. Clone SadTalker repository:
   git clone https://github.com/OpenTalker/SadTalker.git tools/SadTalker

2. Install dependencies:
   cd tools/SadTalker
   pip install -r requirements.txt

3. Download checkpoints:
   bash scripts/download_models.sh

4. Set environment variable (optional):
   export SADTALKER_PATH=/path/to/SadTalker
   export SADTALKER_CHECKPOINT_PATH=/path/to/checkpoints

5. Test installation:
   python inference.py --driven_audio test.mp3 --source_image test.png

For Google Colab setup, see: notebooks/colab_setup.ipynb
"""
        print(instructions)


# Example usage
if __name__ == "__main__":
    # Check if SadTalker is available
    avatar_gen = AvatarGenerator()
    
    if not avatar_gen.is_available():
        print("\n❌ SadTalker not available!")
        AvatarGenerator.setup_instructions()
    else:
        print("\n✅ SadTalker is ready to use!")
        
        # Example: Generate video
        # avatar_gen.generate_talking_video(
        #     image_path="test_character.png",
        #     audio_path="output_audio.mp3",
        #     output_path="output/test_avatar.mp4"
        # )
