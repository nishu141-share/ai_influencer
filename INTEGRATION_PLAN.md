# AI Influencer Integration Plan
## Hybrid Architecture Implementation

**Created**: 2025-12-10  
**Status**: Ready for Implementation  
**Deployment**: Google Colab (FREE)

---

## 🎯 Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    AUTOMATION LAYER                          │
│         (gemini-youtube-automation Framework)                │
│  - Scheduling & Orchestration                                │
│  - Gemini API Integration (FREE)                             │
│  - YouTube Upload & Publishing                               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    CONTENT LAYER                             │
│              (Your Existing Agents)                          │
│  - Orchestrator Agent (Main Controller)                      │
│  - Trend Watcher Agent (Content Ideas)                       │
│  - Content Agent (Script Generation)                         │
│  - Marketing Agent (SEO & Optimization)                      │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    VIDEO PRODUCTION LAYER                    │
│           (Text-To-Video-AI + Your Setup)                    │
│  - Script → Storyboard                                       │
│  - Text-to-Speech (gTTS/EdgeTTS - FREE)                      │
│  - Stock Footage (Pexels API - FREE)                         │
│  - Video Assembly (MoviePy)                                  │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                    AVATAR LAYER                              │
│              (Your SadTalker Setup)                          │
│  - AI Influencer Image + Audio → Talking Head Video         │
│  - Facial Animation & Lip Sync                               │
│  - Final Video Rendering                                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 New Project Structure

```
ai_influencer/
├── .env                          # API keys and configuration
├── .gitignore
├── README.md
│
├── config/                       # Configuration files
│   ├── influencer_config.json   # AI influencer persona settings
│   ├── content_plan.json        # Content calendar
│   └── api_keys.json            # API credentials (gitignored)
│
├── agents/                       # Your existing agents (KEEP)
│   ├── orchestrator.py          # Main controller
│   ├── content_agent.py         # Content generation
│   ├── trend_watcher.py         # Trend analysis
│   ├── marketing_agent.py       # SEO & optimization
│   ├── visual_agent.py          # Visual content
│   ├── voice_agent.py           # Voice generation
│   └── publishing_agent.py      # Publishing logic
│
├── core/                         # New integration layer
│   ├── __init__.py
│   ├── automation.py            # From gemini-youtube-automation
│   ├── video_pipeline.py        # From Text-To-Video-AI
│   ├── avatar_generator.py      # Your SadTalker integration
│   └── gemini_client.py         # Gemini API wrapper
│
├── utils/                        # Utility functions
│   ├── __init__.py
│   ├── text_to_speech.py        # TTS utilities
│   ├── video_editor.py          # Video editing utilities
│   └── youtube_uploader.py      # YouTube API wrapper
│
├── assets/                       # Static assets
│   ├── influencer_image.png     # Your AI influencer avatar
│   ├── fonts/                   # Custom fonts
│   └── templates/               # Video templates
│
├── output/                       # Generated content
│   ├── videos/
│   ├── audio/
│   ├── thumbnails/
│   └── logs/
│
├── notebooks/                    # Colab notebooks
│   ├── colab_setup.ipynb        # Google Colab setup
│   ├── test_pipeline.ipynb      # Testing notebook
│   └── manual_run.ipynb         # Manual execution
│
├── scripts/                      # Utility scripts
│   ├── setup_colab.sh           # Colab environment setup
│   └── download_models.py       # Download SadTalker models
│
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
└── requirements_colab.txt        # Colab-specific dependencies
```

---

## 🔧 Integration Steps

### **Phase 1: Setup & Preparation** (Day 1)

#### Step 1.1: Create New Project Structure
```bash
# Create new directories
mkdir -p config core utils notebooks scripts assets/fonts output/{videos,audio,thumbnails,logs}
```

#### Step 1.2: Merge Requirements
Create `requirements.txt` combining all dependencies:
```txt
# Gemini API
google-generativeai
google-api-python-client
google-auth-httplib2
google-auth-oauthlib

# Your existing dependencies
openai
anthropic
requests
python-dotenv

# Video generation
moviepy==1.0.3
Pillow==9.5.0
pydub
opencv-python

# Text-to-Speech
gTTS
edge-tts

# SadTalker dependencies (from your setup)
torch
torchvision
torchaudio
face-alignment
imageio
imageio-ffmpeg
librosa
numba
numpy
scipy
tqdm
yacs

# Utilities
pexels-api
youtube-upload
```

#### Step 1.3: Create Configuration Files

**config/influencer_config.json**:
```json
{
  "influencer": {
    "name": "Your AI Influencer Name",
    "persona": "Attractive Asian woman tech influencer",
    "niche": "Technology & AI",
    "target_audience": "Tech enthusiasts, developers, AI learners",
    "content_style": "Educational, engaging, trendy",
    "posting_schedule": "daily",
    "platforms": ["youtube", "tiktok", "instagram"]
  },
  "video_settings": {
    "long_form": {
      "duration": "5-10 minutes",
      "format": "1920x1080",
      "fps": 30
    },
    "short_form": {
      "duration": "30-60 seconds",
      "format": "1080x1920",
      "fps": 30
    }
  },
  "avatar": {
    "image_path": "assets/influencer_image.png",
    "voice_style": "female, professional, friendly",
    "language": "en"
  }
}
```

---

### **Phase 2: Core Integration** (Days 2-3)

#### Step 2.1: Create Gemini Client Wrapper

**core/gemini_client.py**:
```python
import os
import google.generativeai as genai
from typing import Dict, List, Optional

class GeminiClient:
    """Wrapper for Google Gemini API - FREE tier"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini"""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_trend_analysis(self, niche: str) -> Dict:
        """Analyze trends for content ideas"""
        prompt = f"""
        As an AI influencer in the {niche} niche, analyze current trends.
        Provide:
        1. Top 5 trending topics
        2. Viral content formats
        3. Recommended content angles
        4. Hashtag suggestions
        
        Return as JSON format.
        """
        response = self.generate_content(prompt)
        return self._parse_json_response(response)
    
    def generate_script(self, topic: str, duration: str, style: str) -> Dict:
        """Generate video script"""
        prompt = f"""
        Create a {duration} video script about: {topic}
        Style: {style}
        
        Include:
        1. Hook (first 3 seconds)
        2. Main content (structured sections)
        3. Call-to-action
        4. Hashtags
        
        Return as JSON with sections.
        """
        response = self.generate_content(prompt)
        return self._parse_json_response(response)
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Gemini response"""
        import json
        import re
        
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to parse directly
        try:
            return json.loads(response)
        except:
            return {"raw_response": response}
```

#### Step 2.2: Create Avatar Generator Integration

**core/avatar_generator.py**:
```python
import os
import sys
from pathlib import Path
from typing import Optional

class AvatarGenerator:
    """Integrates SadTalker for AI influencer avatar animation"""
    
    def __init__(self, sadtalker_path: str, checkpoint_path: str):
        self.sadtalker_path = Path(sadtalker_path)
        self.checkpoint_path = Path(checkpoint_path)
        
        # Add SadTalker to path
        sys.path.insert(0, str(self.sadtalker_path))
        
    def generate_talking_video(
        self,
        image_path: str,
        audio_path: str,
        output_path: str,
        enhancer: str = 'gfpgan'
    ) -> str:
        """
        Generate talking head video using SadTalker
        
        Args:
            image_path: Path to influencer image
            audio_path: Path to audio file
            output_path: Where to save video
            enhancer: Face enhancement model
            
        Returns:
            Path to generated video
        """
        try:
            from inference import main as sadtalker_inference
            
            # SadTalker inference
            result = sadtalker_inference(
                source_image=image_path,
                driven_audio=audio_path,
                result_dir=str(Path(output_path).parent),
                enhancer=enhancer,
                preprocess='crop',
                still_mode=True,
                use_idle_mode=False,
                batch_size=1,
                size=512,
                pose_style=0,
                expression_scale=1.0
            )
            
            return result
            
        except Exception as e:
            print(f"Error generating avatar video: {e}")
            raise
    
    def batch_generate(
        self,
        image_path: str,
        audio_files: list,
        output_dir: str
    ) -> list:
        """Generate multiple videos from audio files"""
        results = []
        for i, audio_file in enumerate(audio_files):
            output_path = Path(output_dir) / f"segment_{i:03d}.mp4"
            result = self.generate_talking_video(
                image_path, audio_file, str(output_path)
            )
            results.append(result)
        return results
```

#### Step 2.3: Create Video Pipeline Integration

**core/video_pipeline.py**:
```python
import os
from pathlib import Path
from typing import List, Dict, Optional
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip,
    concatenate_videoclips, CompositeVideoClip
)
from gtts import gTTS
import requests

class VideoPipeline:
    """Combines Text-To-Video-AI logic with avatar generation"""
    
    def __init__(self, pexels_api_key: str):
        self.pexels_api_key = pexels_api_key
        
    def text_to_speech(self, text: str, output_path: str, lang: str = 'en') -> str:
        """Convert text to speech using gTTS (FREE)"""
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        return output_path
    
    def get_stock_footage(self, query: str, orientation: str = 'landscape') -> Optional[str]:
        """Get stock video from Pexels (FREE)"""
        headers = {'Authorization': self.pexels_api_key}
        params = {
            'query': query,
            'orientation': orientation,
            'size': 'medium',
            'per_page': 1
        }
        
        response = requests.get(
            'https://api.pexels.com/videos/search',
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['videos']:
                video_url = data['videos'][0]['video_files'][0]['link']
                return video_url
        return None
    
    def create_b_roll_video(
        self,
        script_sections: List[Dict],
        output_path: str,
        format: str = 'landscape'
    ) -> str:
        """Create B-roll video from script sections"""
        clips = []
        
        for section in script_sections:
            # Get stock footage
            footage_url = self.get_stock_footage(
                section['visual_query'],
                'landscape' if format == 'landscape' else 'portrait'
            )
            
            if footage_url:
                # Download and create clip
                clip = VideoFileClip(footage_url).subclip(0, section['duration'])
                clips.append(clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        return output_path
    
    def combine_avatar_and_broll(
        self,
        avatar_video: str,
        broll_video: Optional[str],
        output_path: str,
        layout: str = 'picture_in_picture'
    ) -> str:
        """Combine avatar video with B-roll footage"""
        avatar_clip = VideoFileClip(avatar_video)
        
        if broll_video:
            broll_clip = VideoFileClip(broll_video)
            
            if layout == 'picture_in_picture':
                # Avatar in corner, B-roll as background
                avatar_resized = avatar_clip.resize(height=avatar_clip.h // 3)
                avatar_positioned = avatar_resized.set_position(('right', 'bottom'))
                
                final = CompositeVideoClip([broll_clip, avatar_positioned])
            else:
                # Side by side or other layouts
                final = avatar_clip
        else:
            final = avatar_clip
        
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return output_path
```

---

### **Phase 3: Agent Integration** (Days 4-5)

#### Step 3.1: Update Orchestrator

**core/automation.py** (Main orchestrator combining everything):
```python
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import your existing agents
import sys
sys.path.append(str(Path(__file__).parent.parent / 'agents'))

from orchestrator import OrchestratorAgent
from content_agent import ContentAgent
from trend_watcher import TrendWatcherAgent
from marketing_agent import MarketingAgent

# Import new integrations
from .gemini_client import GeminiClient
from .avatar_generator import AvatarGenerator
from .video_pipeline import VideoPipeline

class AIInfluencerAutomation:
    """Main automation system combining all components"""
    
    def __init__(self, config_path: str):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize clients
        self.gemini = GeminiClient()
        self.avatar_gen = AvatarGenerator(
            sadtalker_path=os.getenv('SADTALKER_PATH'),
            checkpoint_path=os.getenv('SADTALKER_CHECKPOINT_PATH')
        )
        self.video_pipeline = VideoPipeline(
            pexels_api_key=os.getenv('PEXELS_API_KEY')
        )
        
        # Initialize your existing agents
        self.orchestrator = OrchestratorAgent()
        self.content_agent = ContentAgent()
        self.trend_watcher = TrendWatcherAgent()
        self.marketing_agent = MarketingAgent()
        
        # Output directory
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_daily_content(self) -> Dict:
        """Main workflow: Generate daily content"""
        print("🚀 Starting daily content generation...")
        
        # Step 1: Analyze trends
        print("📊 Analyzing trends...")
        trends = self.gemini.generate_trend_analysis(
            self.config['influencer']['niche']
        )
        
        # Step 2: Select topic
        print("🎯 Selecting topic...")
        topic = trends['trending_topics'][0]  # Pick top trend
        
        # Step 3: Generate script
        print("📝 Generating script...")
        script = self.gemini.generate_script(
            topic=topic,
            duration=self.config['video_settings']['long_form']['duration'],
            style=self.config['influencer']['content_style']
        )
        
        # Step 4: Generate audio
        print("🎤 Generating voiceover...")
        audio_path = self.output_dir / f"audio_{datetime.now().strftime('%Y%m%d')}.mp3"
        self.video_pipeline.text_to_speech(
            script['full_script'],
            str(audio_path)
        )
        
        # Step 5: Generate avatar video
        print("🎬 Generating avatar video...")
        avatar_video_path = self.output_dir / f"avatar_{datetime.now().strftime('%Y%m%d')}.mp4"
        self.avatar_gen.generate_talking_video(
            image_path=self.config['avatar']['image_path'],
            audio_path=str(audio_path),
            output_path=str(avatar_video_path)
        )
        
        # Step 6: Create B-roll (optional)
        print("🎥 Adding B-roll footage...")
        # ... B-roll generation logic
        
        # Step 7: Combine and finalize
        print("✨ Finalizing video...")
        final_video_path = self.output_dir / f"final_{datetime.now().strftime('%Y%m%d')}.mp4"
        # ... Combine avatar + B-roll
        
        # Step 8: Generate thumbnail
        print("🖼️ Creating thumbnail...")
        # ... Thumbnail generation
        
        return {
            'video_path': str(final_video_path),
            'topic': topic,
            'script': script,
            'metadata': {
                'title': script.get('title'),
                'description': script.get('description'),
                'tags': script.get('hashtags')
            }
        }
    
    def publish_content(self, content: Dict):
        """Publish to YouTube/TikTok/Instagram"""
        print("📤 Publishing content...")
        # Use your existing publishing agent
        # ... Publishing logic
        pass
    
    def run(self):
        """Main execution"""
        try:
            content = self.generate_daily_content()
            self.publish_content(content)
            print("✅ Daily content generation complete!")
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
```

---

### **Phase 4: Google Colab Setup** (Day 6)

#### Step 4.1: Create Colab Notebook

**notebooks/colab_setup.ipynb**:
```python
# Cell 1: Install dependencies
!pip install -q google-generativeai moviepy gTTS pydub Pillow requests

# Cell 2: Clone your repository
!git clone https://github.com/YOUR_USERNAME/ai_influencer.git
%cd ai_influencer

# Cell 3: Setup SadTalker
!git clone https://github.com/OpenTalker/SadTalker.git
%cd SadTalker
!pip install -r requirements.txt

# Download models (optimized)
!bash scripts/download_models.sh

# Cell 4: Configure API keys
import os
from google.colab import userdata

os.environ['GEMINI_API_KEY'] = userdata.get('GEMINI_API_KEY')
os.environ['PEXELS_API_KEY'] = userdata.get('PEXELS_API_KEY')
os.environ['YOUTUBE_CLIENT_SECRET'] = userdata.get('YOUTUBE_CLIENT_SECRET')

# Cell 5: Run automation
%cd /content/ai_influencer
!python main.py
```

---

## 📋 Implementation Checklist

### Week 1: Foundation
- [ ] Create new project structure
- [ ] Merge requirements.txt
- [ ] Create configuration files
- [ ] Set up Gemini API client
- [ ] Test Gemini API connection

### Week 2: Integration
- [ ] Integrate avatar generator
- [ ] Integrate video pipeline
- [ ] Update orchestrator
- [ ] Connect existing agents
- [ ] Test end-to-end flow locally

### Week 3: Colab Deployment
- [ ] Create Colab notebook
- [ ] Optimize for Colab environment
- [ ] Set up Google Drive integration
- [ ] Test on Colab
- [ ] Set up scheduling

### Week 4: Launch
- [ ] Final testing
- [ ] Create first video
- [ ] Publish to YouTube
- [ ] Monitor performance
- [ ] Iterate and improve

---

## 💰 Cost Breakdown (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| **Google Colab** | $0 | Free tier (12hrs/day) |
| **Gemini API** | $0 | Free tier (60 requests/min) |
| **Pexels API** | $0 | Free (200 requests/month) |
| **gTTS** | $0 | Free unlimited |
| **SadTalker** | $0 | Open-source |
| **YouTube API** | $0 | Free (10,000 units/day) |
| **Total** | **$0/month** | 🎉 |

**Upgrade Options** (if needed later):
- Colab Pro: $9.99/month (better GPU, longer sessions)
- Gemini Pro API: Pay-as-you-go (very cheap)
- ElevenLabs TTS: $5/month (better voice quality)

---

## 🚀 Next Steps

1. **Review this plan** - Make sure you understand the architecture
2. **Set up API keys** - Get Gemini API key (free)
3. **Start Phase 1** - Create project structure
4. **Test components** - Test each piece individually
5. **Deploy to Colab** - Move to cloud when ready

---

**Questions? Let me know which phase you'd like to start with!**
