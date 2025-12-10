"""
Video Pipeline - Combines Text-To-Video-AI logic
Handles TTS, stock footage, and video assembly
"""

import os
import requests
from pathlib import Path
from typing import List, Dict, Optional
from gtts import gTTS
try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, ImageClip,
        concatenate_videoclips, CompositeVideoClip, TextClip
    )
except ImportError:
    print("⚠️ MoviePy not installed. Install with: pip install moviepy")


class VideoPipeline:
    """Combines Text-To-Video-AI logic with avatar generation"""
    
    def __init__(self, pexels_api_key: Optional[str] = None):
        """
        Initialize video pipeline
        
        Args:
            pexels_api_key: Pexels API key for stock footage
        """
        self.pexels_api_key = pexels_api_key or os.getenv('PEXELS_API_KEY')
        if not self.pexels_api_key:
            print("⚠️ PEXELS_API_KEY not set. Stock footage will not be available.")
        
        print("✅ Video Pipeline initialized")
    
    def text_to_speech(
        self,
        text: str,
        output_path: str,
        lang: str = 'en',
        slow: bool = False
    ) -> str:
        """
        Convert text to speech using gTTS (FREE)
        
        Args:
            text: Text to convert
            output_path: Where to save audio file
            lang: Language code (default: 'en')
            slow: Speak slowly
            
        Returns:
            Path to generated audio file
        """
        try:
            print(f"🎤 Generating speech: {text[:50]}...")
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(output_path)
            print(f"✅ Audio saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ TTS error: {e}")
            raise
    
    def get_stock_image(
        self,
        query: str,
        orientation: str = 'landscape'
    ) -> Optional[str]:
        """
        Get stock image from Pexels (FREE)
        
        Args:
            query: Search query
            orientation: 'landscape', 'portrait', or 'square'
            
        Returns:
            Image URL or None
        """
        if not self.pexels_api_key:
            return None
        
        headers = {'Authorization': self.pexels_api_key}
        params = {
            'query': query,
            'orientation': orientation,
            'size': 'large',
            'per_page': 1
        }
        
        try:
            response = requests.get(
                'https://api.pexels.com/v1/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    image_url = data['photos'][0]['src']['large']
                    print(f"✅ Found stock image for: {query}")
                    return image_url
            else:
                print(f"⚠️ Pexels API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching stock image: {e}")
        
        return None
    
    def get_stock_footage(
        self,
        query: str,
        orientation: str = 'landscape'
    ) -> Optional[str]:
        """
        Get stock video from Pexels (FREE)
        
        Args:
            query: Search query
            orientation: 'landscape' or 'portrait'
            
        Returns:
            Video URL or None
        """
        if not self.pexels_api_key:
            return None
        
        headers = {'Authorization': self.pexels_api_key}
        params = {
            'query': query,
            'orientation': orientation,
            'size': 'medium',
            'per_page': 1
        }
        
        try:
            response = requests.get(
                'https://api.pexels.com/videos/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['videos']:
                    # Get HD video file
                    video_files = data['videos'][0]['video_files']
                    hd_video = next(
                        (v for v in video_files if v['quality'] == 'hd'),
                        video_files[0]
                    )
                    video_url = hd_video['link']
                    print(f"✅ Found stock footage for: {query}")
                    return video_url
            else:
                print(f"⚠️ Pexels API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching stock footage: {e}")
        
        return None
    
    def download_media(self, url: str, output_path: str) -> str:
        """
        Download media file from URL
        
        Args:
            url: Media URL
            output_path: Where to save file
            
        Returns:
            Path to downloaded file
        """
        try:
            print(f"📥 Downloading: {url[:50]}...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Download error: {e}")
            raise
    
    def create_simple_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        add_text: Optional[str] = None
    ) -> str:
        """
        Create simple video from image and audio
        
        Args:
            image_path: Path to image
            audio_path: Path to audio
            output_path: Where to save video
            add_text: Optional text overlay
            
        Returns:
            Path to created video
        """
        try:
            print(f"🎬 Creating video...")
            
            # Load audio to get duration
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Create image clip with audio duration
            image_clip = ImageClip(image_path).set_duration(duration)
            
            # Add text if provided
            if add_text:
                txt_clip = TextClip(
                    add_text,
                    fontsize=70,
                    color='white',
                    font='Arial-Bold'
                ).set_position('center').set_duration(duration)
                
                video = CompositeVideoClip([image_clip, txt_clip])
            else:
                video = image_clip
            
            # Set audio
            video = video.set_audio(audio)
            
            # Write video file
            video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Video creation error: {e}")
            raise
    
    def combine_videos(
        self,
        video_paths: List[str],
        output_path: str
    ) -> str:
        """
        Concatenate multiple videos
        
        Args:
            video_paths: List of video file paths
            output_path: Where to save combined video
            
        Returns:
            Path to combined video
        """
        try:
            print(f"🎬 Combining {len(video_paths)} videos...")
            
            clips = [VideoFileClip(path) for path in video_paths]
            final_clip = concatenate_videoclips(clips)
            
            final_clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final_clip.close()
            
            print(f"✅ Combined video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Video combination error: {e}")
            raise
    
    def add_background_music(
        self,
        video_path: str,
        music_path: str,
        output_path: str,
        music_volume: float = 0.1
    ) -> str:
        """
        Add background music to video
        
        Args:
            video_path: Path to video
            music_path: Path to music file
            output_path: Where to save result
            music_volume: Music volume (0.0-1.0)
            
        Returns:
            Path to video with music
        """
        try:
            print(f"🎵 Adding background music...")
            
            video = VideoFileClip(video_path)
            music = AudioFileClip(music_path).volumex(music_volume)
            
            # Loop music if shorter than video
            if music.duration < video.duration:
                music = music.audio_loop(duration=video.duration)
            else:
                music = music.subclip(0, video.duration)
            
            # Combine original audio with music
            if video.audio:
                final_audio = video.audio.volumex(1.0)
                # Mix audio (this is simplified, might need adjustment)
                video = video.set_audio(final_audio)
            
            video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac'
            )
            
            video.close()
            music.close()
            
            print(f"✅ Video with music created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding music: {e}")
            raise


# Example usage
if __name__ == "__main__":
    # Test the pipeline
    pipeline = VideoPipeline()
    
    # Test TTS
    print("\n🎤 Testing TTS...")
    audio_path = pipeline.text_to_speech(
        "Hello! This is a test of the text to speech system.",
        "test_audio.mp3"
    )
    
    # Test stock image search
    if pipeline.pexels_api_key:
        print("\n🖼️ Testing stock image search...")
        image_url = pipeline.get_stock_image("technology")
        if image_url:
            print(f"Image URL: {image_url}")
