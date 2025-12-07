from .content_agent import ContentAgent
from .voice_agent import VoiceAgent
from .visual_agent import VisualAgent
from .marketing_agent import MarketingAgent
from .publishing_agent import PublishingAgent
from .trend_agent import TrendWatcherAgent
from .community_agent import CommunityManagerAgent

class Orchestrator:
    def __init__(self):
        self.trend_agent = TrendWatcherAgent()
        self.content_agent = ContentAgent()
        self.voice_agent = VoiceAgent()
        self.visual_agent = VisualAgent()
        self.marketing_agent = MarketingAgent()
        self.publishing_agent = PublishingAgent()
        self.community_agent = CommunityManagerAgent()

    def create_post(self, topic: str = None):
        print("=== Orchestrator: Starting Pipeline ===")
        
        # 1. Trend (or simple topic)
        if not topic:
            # For now, TrendAgent is a placeholder returning a list. We take the first one.
            trends = self.trend_agent.run({"category": "tech"})
            topic = trends["trends"][0]
            print(f"Orchestrator: Auto-selected trending topic: {topic}")

        # 2. Content
        print(f"Orchestrator: Requesting content for '{topic}'...")
        content = self.content_agent.run({"topic": topic})
        if not content:
            print("Orchestrator: Content generation failed.")
            return
        
        script = content["script"]
        print(f"Orchestrator: Generated Script: {script[:50]}...")
        
        # 3. Voice
        print("Orchestrator: Generating Voiceover...")
        audio = self.voice_agent.run({"text": script, "output_path": "output/generated_audio.mp3"})
        if not audio:
            print("Orchestrator: Voice generation failed.")
            return
            
        audio_path = audio["audio_path"]
        
        # 4. Visual
        # Use the newly generated avatar
        # TODO: Dynamic avatar selection based on availability
        image_path = "scratch/ai_influencer/output/indian_influencer_avatar.png" 
        import os
        if not os.path.exists(image_path):
             # Fallback if specific avatar not found
             print(f"Orchestrator: Warning, {image_path} not found. Checking assets...")
             # For test purposes, we might need to rely on the generate_image tool having run
             pass

        print(f"Orchestrator: Generating Video using {image_path}...")
        video = self.visual_agent.run({
            "audio_path": audio_path, 
            "image_path": image_path,
            "output_dir": "output/final_videos"
        })
        
        if not video:
             print("Orchestrator: Video generation failed.")
             return

        # 5. Marketing (Placeholder for now)
        metadata = self.marketing_agent.run({
            "video_path": video["output_dir"], 
            "platform": "instagram"
        })
        
        # 6. Publishing (Placeholder for now)
        self.publishing_agent.run({
            "video_path": video["output_dir"],
            "metadata": metadata
        })
        
        print("=== Orchestrator: Pipeline Complete ===")
        return video

    def engage_community(self):
        print("=== Orchestrator: Starting Community Engagement ===")
        self.community_agent.run({"platform": "instagram", "post_id": "latest"})

if __name__ == "__main__":
    orc = Orchestrator()
    # Test auto-trend mode
    orc.create_post()
    orc.engage_community()
