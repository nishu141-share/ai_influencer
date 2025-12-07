# AI Influencer Project

Multi-agent system for automated AI influencer content creation.

## Features
- **Content Agent**: Generates viral scripts using Gemini AI
- **Voice Agent**: Text-to-speech using Edge TTS
- **Visual Agent**: Animated talking head videos using SadTalker
- **Trend Watcher**: Identifies viral topics
- **Marketing Agent**: Optimizes content for platforms
- **Publishing Agent**: Distributes to social media
- **Community Manager**: Engages with audience

## Setup

### Prerequisites
- Python 3.13+
- Git

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Add your `GEMINI_API_KEY`
3. Add social media credentials (optional)

## Usage

### Run Full Pipeline
```bash
python -m agents.orchestrator
```

### Individual Agents
```bash
# Generate content
python -m agents.content_agent

# Generate voice
python -m agents.voice_agent

# Generate video (requires SadTalker setup)
python -m agents.visual_agent
```

## Project Structure
```
ai_influencer/
├── agents/           # Agent implementations
├── tools/            # External tools (SadTalker)
├── output/           # Generated content
├── .env              # Configuration (not in git)
└── README.md         # This file
```

## GPU Acceleration
For faster video generation, use Google Colab (free GPU). See `colab_guide.md`.

## License
MIT
