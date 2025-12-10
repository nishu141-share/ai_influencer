"""
Gemini API Client - FREE tier integration
Handles all content generation using Google's Gemini API
"""

import os
import json
import re
from typing import Dict, List, Optional
import google.generativeai as genai


class GeminiClient:
    """Wrapper for Google Gemini API - FREE tier"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key (or set GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it in .env or pass as parameter")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini API initialized (FREE tier)")
    
    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate content using Gemini
        
        Args:
            prompt: Input prompt
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            Generated text
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                )
            )
            return response.text
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            raise
    
    def generate_trend_analysis(self, niche: str) -> Dict:
        """
        Analyze trends for content ideas
        
        Args:
            niche: Content niche (e.g., "Technology & AI")
            
        Returns:
            Dictionary with trending topics and recommendations
        """
        prompt = f"""
You are a social media trend analyst for an AI influencer in the {niche} niche.

Analyze current trends and provide content recommendations.

Return ONLY valid JSON in this exact format:
{{
  "trending_topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3",
    "Topic 4",
    "Topic 5"
  ],
  "viral_formats": [
    "Format 1",
    "Format 2",
    "Format 3"
  ],
  "content_angles": [
    "Angle 1",
    "Angle 2",
    "Angle 3"
  ],
  "hashtags": [
    "#hashtag1",
    "#hashtag2",
    "#hashtag3",
    "#hashtag4",
    "#hashtag5"
  ],
  "recommended_topic": "Most recommended topic for today"
}}

Focus on trending, viral-worthy topics that will get views.
"""
        response = self.generate_content(prompt, temperature=0.8)
        return self._parse_json_response(response)
    
    def generate_script(
        self,
        topic: str,
        duration: str,
        style: str,
        video_type: str = "long_form"
    ) -> Dict:
        """
        Generate video script
        
        Args:
            topic: Video topic
            duration: Target duration (e.g., "5-10 minutes")
            style: Content style (e.g., "Educational, engaging")
            video_type: "long_form" or "short_form"
            
        Returns:
            Dictionary with script sections
        """
        if video_type == "short_form":
            prompt = f"""
Create a {duration} YouTube Shorts/TikTok script about: {topic}
Style: {style}

Return ONLY valid JSON in this exact format:
{{
  "title": "Catchy title (max 60 chars)",
  "hook": "First 3 seconds hook to grab attention",
  "main_content": "Main message (30-45 seconds)",
  "call_to_action": "CTA at the end",
  "full_script": "Complete script as one paragraph",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "description": "Video description for platform"
}}

Make it viral-worthy and engaging!
"""
        else:
            prompt = f"""
Create a {duration} YouTube video script about: {topic}
Style: {style}

Return ONLY valid JSON in this exact format:
{{
  "title": "Engaging video title",
  "hook": "First 10 seconds hook",
  "sections": [
    {{
      "heading": "Section 1 heading",
      "content": "Section 1 content",
      "duration": "estimated seconds"
    }},
    {{
      "heading": "Section 2 heading",
      "content": "Section 2 content",
      "duration": "estimated seconds"
    }}
  ],
  "call_to_action": "Subscribe and like message",
  "full_script": "Complete script as continuous narration",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "description": "SEO-optimized video description",
  "tags": ["tag1", "tag2", "tag3"]
}}

Make it educational, engaging, and optimized for YouTube algorithm.
"""
        
        response = self.generate_content(prompt, temperature=0.7)
        return self._parse_json_response(response)
    
    def generate_thumbnail_text(self, topic: str) -> Dict:
        """
        Generate thumbnail text and design suggestions
        
        Args:
            topic: Video topic
            
        Returns:
            Dictionary with thumbnail recommendations
        """
        prompt = f"""
Create thumbnail text and design for a video about: {topic}

Return ONLY valid JSON:
{{
  "main_text": "Big bold text for thumbnail (max 4 words)",
  "sub_text": "Optional smaller text",
  "color_scheme": "Recommended colors",
  "style": "Design style recommendation"
}}
"""
        response = self.generate_content(prompt, temperature=0.6)
        return self._parse_json_response(response)
    
    def optimize_for_seo(self, title: str, description: str) -> Dict:
        """
        Optimize title and description for SEO
        
        Args:
            title: Original title
            description: Original description
            
        Returns:
            Optimized title and description
        """
        prompt = f"""
Optimize this YouTube video for SEO:

Title: {title}
Description: {description}

Return ONLY valid JSON:
{{
  "optimized_title": "SEO-optimized title (max 60 chars)",
  "optimized_description": "SEO-optimized description with keywords",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "suggested_tags": ["tag1", "tag2", "tag3"]
}}
"""
        response = self.generate_content(prompt, temperature=0.5)
        return self._parse_json_response(response)
    
    def _parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON from Gemini response
        
        Args:
            response: Raw Gemini response
            
        Returns:
            Parsed JSON dictionary
        """
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response
        
        # Parse JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse JSON: {e}")
            print(f"Response: {response[:200]}...")
            return {"raw_response": response, "error": str(e)}


# Example usage
if __name__ == "__main__":
    # Test the client
    client = GeminiClient()
    
    # Test trend analysis
    print("\n📊 Testing trend analysis...")
    trends = client.generate_trend_analysis("Technology & AI")
    print(json.dumps(trends, indent=2))
    
    # Test script generation
    print("\n📝 Testing script generation...")
    script = client.generate_script(
        topic="Introduction to ChatGPT",
        duration="5 minutes",
        style="Educational, friendly",
        video_type="long_form"
    )
    print(json.dumps(script, indent=2))
