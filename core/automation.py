"""
Main Automation System
Combines all components: Gemini, Video Pipeline, Avatar Generator, and your existing agents
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import core components
from .gemini_client import GeminiClient
from .avatar_generator import AvatarGenerator
from .video_pipeline import VideoPipeline


class AIInfluencerAutomation:
    """Main automation system combining all components"""
    
    def __init__(self, config_path: str = "config/influencer_config.json"):
        """
        Initialize automation system
        
        Args:
            config_path: Path to configuration file
        """
        print("🚀 Initializing AI Influencer Automation System...")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        print(f"✅ Loaded config for: {self.config['influencer']['name']}")
        
        # Initialize core components
        self.gemini = GeminiClient()
        self.video_pipeline = VideoPipeline()
        self.avatar_gen = AvatarGenerator()
        
        # Setup output directories
        self.output_dir = Path('output')
        self.video_dir = self.output_dir / 'videos'
        self.audio_dir = self.output_dir / 'audio'
        self.thumbnail_dir = self.output_dir / 'thumbnails'
        self.log_dir = self.output_dir / 'logs'
        
        for dir_path in [self.video_dir, self.audio_dir, self.thumbnail_dir, self.log_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print("✅ AI Influencer Automation System ready!")
    
    def generate_daily_content(self, video_type: str = "long_form") -> Dict:
        """
        Main workflow: Generate daily content
        
        Args:
            video_type: "long_form" or "short_form"
            
        Returns:
            Dictionary with video path and metadata
        """
        print("\n" + "="*60)
        print(f"🎬 Starting {video_type} content generation...")
        print("="*60)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Step 1: Analyze trends
            print("\n📊 Step 1: Analyzing trends...")
            trends = self.gemini.generate_trend_analysis(
                self.config['influencer']['niche']
            )
            topic = trends.get('recommended_topic', trends['trending_topics'][0])
            print(f"✅ Selected topic: {topic}")
            
            # Step 2: Generate script
            print("\n📝 Step 2: Generating script...")
            duration = self.config['video_settings'][video_type]['duration']
            style = self.config['influencer']['content_style']
            
            script = self.gemini.generate_script(
                topic=topic,
                duration=duration,
                style=style,
                video_type=video_type
            )
            print(f"✅ Script generated: {script.get('title', 'Untitled')}")
            
            # Step 3: Generate audio (TTS)
            print("\n🎤 Step 3: Generating voiceover...")
            audio_filename = f"audio_{video_type}_{timestamp}.mp3"
            audio_path = self.audio_dir / audio_filename
            
            full_script = script.get('full_script', '')
            if not full_script:
                # Combine sections if no full_script
                if 'sections' in script:
                    full_script = ' '.join([s['content'] for s in script['sections']])
                else:
                    full_script = script.get('main_content', topic)
            
            self.video_pipeline.text_to_speech(
                text=full_script,
                output_path=str(audio_path),
                lang=self.config['avatar']['language']
            )
            print(f"✅ Audio generated: {audio_path}")
            
            # Step 4: Generate avatar video
            print("\n🎭 Step 4: Generating avatar video...")
            
            if self.avatar_gen.is_available():
                avatar_video_filename = f"avatar_{video_type}_{timestamp}.mp4"
                avatar_video_path = self.video_dir / avatar_video_filename
                
                self.avatar_gen.generate_talking_video(
                    image_path=self.config['avatar']['image_path'],
                    audio_path=str(audio_path),
                    output_path=str(avatar_video_path),
                    still_mode=True,
                    expression_scale=1.0
                )
                print(f"✅ Avatar video generated: {avatar_video_path}")
                final_video_path = avatar_video_path
            else:
                print("⚠️ SadTalker not available, creating simple video...")
                simple_video_filename = f"simple_{video_type}_{timestamp}.mp4"
                simple_video_path = self.video_dir / simple_video_filename
                
                self.video_pipeline.create_simple_video(
                    image_path=self.config['avatar']['image_path'],
                    audio_path=str(audio_path),
                    output_path=str(simple_video_path),
                    add_text=script.get('title', topic)
                )
                print(f"✅ Simple video generated: {simple_video_path}")
                final_video_path = simple_video_path
            
            # Step 5: Generate thumbnail (placeholder for now)
            print("\n🖼️ Step 5: Generating thumbnail...")
            thumbnail_data = self.gemini.generate_thumbnail_text(topic)
            print(f"✅ Thumbnail text: {thumbnail_data.get('main_text', topic)}")
            
            # Step 6: Optimize for SEO
            print("\n🔍 Step 6: Optimizing for SEO...")
            seo_data = self.gemini.optimize_for_seo(
                title=script.get('title', topic),
                description=script.get('description', '')
            )
            print(f"✅ SEO optimized title: {seo_data.get('optimized_title', '')}")
            
            # Compile results
            result = {
                'video_path': str(final_video_path),
                'audio_path': str(audio_path),
                'topic': topic,
                'script': script,
                'trends': trends,
                'thumbnail': thumbnail_data,
                'seo': seo_data,
                'metadata': {
                    'title': seo_data.get('optimized_title', script.get('title', topic)),
                    'description': seo_data.get('optimized_description', script.get('description', '')),
                    'tags': seo_data.get('suggested_tags', script.get('hashtags', [])),
                    'hashtags': script.get('hashtags', [])
                },
                'timestamp': timestamp,
                'video_type': video_type
            }
            
            # Save metadata
            metadata_path = self.log_dir / f"metadata_{video_type}_{timestamp}.json"
            with open(metadata_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print("\n" + "="*60)
            print("✅ Content generation complete!")
            print(f"📹 Video: {final_video_path}")
            print(f"📄 Metadata: {metadata_path}")
            print("="*60)
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error during content generation: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_short_from_long(self, long_video_metadata: Dict) -> Dict:
        """
        Generate a short-form video from long-form content
        
        Args:
            long_video_metadata: Metadata from long-form video
            
        Returns:
            Dictionary with short video path and metadata
        """
        print("\n🎬 Generating short-form video from long-form content...")
        
        # Extract best moment for short
        topic = long_video_metadata['topic']
        
        # Generate short script
        short_script = self.gemini.generate_script(
            topic=f"Quick tip: {topic}",
            duration="30-60 seconds",
            style="Fast-paced, engaging",
            video_type="short_form"
        )
        
        # Generate short video
        return self.generate_daily_content(video_type="short_form")
    
    def publish_content(self, content: Dict):
        """
        Publish to YouTube/TikTok/Instagram
        (Placeholder - implement with your publishing agent)
        
        Args:
            content: Content metadata dictionary
        """
        print("\n📤 Publishing content...")
        print(f"   Platforms: {self.config['influencer']['platforms']}")
        
        # TODO: Integrate with your publishing agent
        # from agents.publishing_agent import PublishingAgent
        # publisher = PublishingAgent()
        # publisher.publish(content)
        
        print("⚠️ Publishing not yet implemented. Add your publishing agent integration here.")
    
    def run_daily_automation(self):
        """Run complete daily automation workflow"""
        print("\n" + "="*60)
        print("🤖 AI INFLUENCER DAILY AUTOMATION")
        print("="*60)
        
        try:
            # Generate long-form content
            long_content = self.generate_daily_content(video_type="long_form")
            
            # Generate short-form content
            short_content = self.generate_daily_content(video_type="short_form")
            
            # Publish (when implemented)
            # self.publish_content(long_content)
            # self.publish_content(short_content)
            
            print("\n✅ Daily automation complete!")
            return {
                'long_form': long_content,
                'short_form': short_content
            }
            
        except Exception as e:
            print(f"\n❌ Daily automation failed: {e}")
            raise


# Example usage
if __name__ == "__main__":
    # Initialize automation
    automation = AIInfluencerAutomation()
    
    # Run daily automation
    automation.run_daily_automation()
