"""
Core integration layer for AI Influencer automation
Combines gemini-youtube-automation, Text-To-Video-AI, and SadTalker
"""

from .gemini_client import GeminiClient
from .avatar_generator import AvatarGenerator
from .video_pipeline import VideoPipeline
from .automation import AIInfluencerAutomation

__all__ = [
    'GeminiClient',
    'AvatarGenerator',
    'VideoPipeline',
    'AIInfluencerAutomation'
]
