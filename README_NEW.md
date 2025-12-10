# 🤖 AI Influencer Automation System

**Fully automated AI influencer content generation using FREE cloud services**

Generate professional talking-head videos daily using:
- ✅ **Google Gemini API** (FREE) - Content generation
- ✅ **Google Colab** (FREE) - GPU computing
- ✅ **SadTalker** (FREE) - Avatar animation
- ✅ **gTTS** (FREE) - Text-to-speech
- ✅ **Pexels API** (FREE) - Stock footage

**Total Cost: $0/month** 🎉

---

## 🎯 What This Does

This system automatically:
1. **Analyzes trends** in your niche using Gemini AI
2. **Generates scripts** for long-form and short-form videos
3. **Creates voiceovers** using text-to-speech
4. **Animates your AI avatar** using SadTalker
5. **Optimizes for SEO** with AI-generated titles and descriptions
6. **Publishes to YouTube/TikTok** (when configured)

All running on **FREE** cloud services!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Automation Layer (gemini-youtube-automation)               │
│  - Scheduling & Orchestration                               │
│  - Gemini API Integration                                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Content Layer (Your Agents + Gemini)                       │
│  - Trend Analysis                                           │
│  - Script Generation                                        │
│  - SEO Optimization                                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Video Production (Text-To-Video-AI + MoviePy)              │
│  - Text-to-Speech (gTTS)                                    │
│  - Stock Footage (Pexels)                                   │
│  - Video Assembly                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  Avatar Animation (SadTalker)                               │
│  - Facial Animation                                         │
│  - Lip Sync                                                 │
│  - Final Rendering                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### **Option 1: Local Setup** (Recommended for testing)

#### 1. Clone and Install
```bash
# Clone this repository
git clone <your-repo-url>
cd ai_influencer

# Install dependencies
pip install -r requirements.txt
```

#### 2. Setup API Keys
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# Get it FREE from: https://makersuite.google.com/app/apikey
```

#### 3. Configure Your Influencer
Edit `config/influencer_config.json`:
```json
{
  "influencer": {
    "name": "Your AI Influencer Name",
    "persona": "Your persona description",
    "niche": "Your niche (e.g., Technology & AI)"
  }
}
```

#### 4. Add Your Avatar Image
Place your AI influencer image as `test_character.png` in the root directory.

#### 5. Run!
```bash
# Generate both long-form and short-form content
python main.py

# Or generate specific type
python main.py --video-type long_form
python main.py --video-type short_form
```

---

### **Option 2: Google Colab** (Recommended for production)

#### 1. Open Colab Notebook
Click here: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/ai_influencer/blob/main/notebooks/colab_setup.ipynb)

#### 2. Set API Keys in Colab Secrets
- Click the key icon (🔑) in the left sidebar
- Add `GEMINI_API_KEY` with your API key
- Add `PEXELS_API_KEY` (optional)

#### 3. Run All Cells
The notebook will:
- Install all dependencies
- Clone SadTalker
- Download models
- Generate your first video!

---

## 📁 Project Structure

```
ai_influencer/
├── config/
│   └── influencer_config.json    # Your influencer settings
├── core/
│   ├── gemini_client.py          # Gemini API wrapper
│   ├── video_pipeline.py         # Video production
│   ├── avatar_generator.py       # SadTalker integration
│   └── automation.py             # Main orchestrator
├── agents/                        # Your existing agents
├── output/
│   ├── videos/                   # Generated videos
│   ├── audio/                    # Generated audio
│   ├── thumbnails/               # Thumbnails
│   └── logs/                     # Metadata logs
├── notebooks/
│   └── colab_setup.ipynb         # Google Colab notebook
├── main.py                        # Main entry point
├── requirements.txt               # Dependencies
└── .env.example                   # Environment template
```

---

## 🔧 Configuration

### **Influencer Settings** (`config/influencer_config.json`)

```json
{
  "influencer": {
    "name": "AI Tech Influencer",
    "persona": "Attractive Asian woman tech influencer",
    "niche": "Technology & AI",
    "content_style": "Educational, engaging, trendy"
  },
  "video_settings": {
    "long_form": {
      "duration": "5-10 minutes",
      "format": "1920x1080"
    },
    "short_form": {
      "duration": "30-60 seconds",
      "format": "1080x1920"
    }
  },
  "avatar": {
    "image_path": "test_character.png",
    "voice_style": "female, professional, friendly",
    "language": "en"
  }
}
```

### **Environment Variables** (`.env`)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
PEXELS_API_KEY=your_pexels_api_key_here
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_secret
```

---

## 📖 Usage Examples

### Generate Daily Content
```bash
# Generate both long and short videos
python main.py

# Generate only long-form
python main.py --video-type long_form

# Generate only shorts
python main.py --video-type short_form
```

### Use as Python Module
```python
from core.automation import AIInfluencerAutomation

# Initialize
automation = AIInfluencerAutomation()

# Generate content
result = automation.generate_daily_content(video_type='long_form')

print(f"Video: {result['video_path']}")
print(f"Topic: {result['topic']}")
```

### Test Individual Components
```python
# Test Gemini API
from core.gemini_client import GeminiClient

client = GeminiClient()
trends = client.generate_trend_analysis("Technology & AI")
print(trends)

# Test Video Pipeline
from core.video_pipeline import VideoPipeline

pipeline = VideoPipeline()
pipeline.text_to_speech("Hello world!", "test.mp3")
```

---

## 🎓 Detailed Guides

- **[Integration Plan](INTEGRATION_PLAN.md)** - Detailed implementation plan
- **[GitHub Projects Analysis](github_projects_analysis.md)** - Analysis of base projects
- **[Colab Guide](colab_guide.md)** - Google Colab setup guide

---

## 🆓 Free Services Used

| Service | Free Tier | Usage |
|---------|-----------|-------|
| **Google Gemini API** | 60 requests/min | Content generation |
| **Google Colab** | 12 hours/day | GPU computing |
| **Pexels API** | 200 requests/month | Stock footage |
| **gTTS** | Unlimited | Text-to-speech |
| **SadTalker** | Unlimited | Avatar animation |
| **YouTube API** | 10,000 units/day | Video upload |

**Total Monthly Cost: $0** 🎉

---

## 🔄 Workflow

1. **Morning (Automated)**
   - Analyze trending topics in your niche
   - Select best topic for today
   - Generate script using Gemini

2. **Midday (Automated)**
   - Convert script to speech (gTTS)
   - Generate avatar video (SadTalker)
   - Create thumbnail and optimize SEO

3. **Evening (Automated)**
   - Upload to YouTube
   - Post short to TikTok/Instagram
   - Log analytics

---

## 🎯 Roadmap

- [x] Gemini API integration
- [x] SadTalker integration
- [x] Video pipeline
- [x] Google Colab support
- [ ] YouTube auto-upload
- [ ] TikTok integration
- [ ] Instagram Reels
- [ ] Analytics dashboard
- [ ] A/B testing
- [ ] Multi-language support

---

## 🤝 Contributing

Based on these amazing open-source projects:
- [gemini-youtube-automation](https://github.com/ChaituRajSagar/gemini-youtube-automation)
- [Text-To-Video-AI](https://github.com/SamurAIGPT/Text-To-Video-AI)
- [SadTalker](https://github.com/OpenTalker/SadTalker)

---

## 📄 License

MIT License - See LICENSE file

---

## 🆘 Support

**Issues?**
1. Check the [Integration Plan](INTEGRATION_PLAN.md)
2. Review [GitHub Projects Analysis](github_projects_analysis.md)
3. Open an issue on GitHub

**Questions?**
- Email: your@email.com
- Discord: [Your Discord]

---

## 🌟 Show Your Support

If this project helps you, please:
- ⭐ Star this repository
- 🐦 Share on Twitter
- 📝 Write a blog post
- 💰 Sponsor the project

---

**Made with ❤️ using FREE AI tools**
