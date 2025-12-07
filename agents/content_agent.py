import os
import time
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core import exceptions
from .base_agent import AgentBase

class ContentAgent(AgentBase):
    def __init__(self, config_path=None):
        super().__init__("ContentAgent", config_path)
        
        # Load environment variables
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        load_dotenv(env_path)
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or "your_gemini_api_key" in self.api_key:
            print("[ContentAgent] WARNING: GEMINI_API_KEY not set in .env")
            self.model = None
        else:
            genai.configure(api_key=self.api_key)
            # gemini-flash-latest is generally the most cost-effective / free-tier friendly
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def run(self, input_data):
        """
        Input: {'topic': str}
        Output: {'script': str, 'caption': str, 'image_prompt': str}
        """
        topic = input_data.get("topic")
        if not topic:
            self.log("Error: No topic provided.")
            return None

        self.log(f"Brainstorming content for topic: {topic}")
        
        if not self.model:
            self.log("Error: Gemini model not initialized (missing API key). Using fallback.")
            return self._fallback_content(topic)

        # Retry logic for rate limits
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Generate content using Gemini
                response = self.model.generate_content(f"""
                You are a creative AI Influencer Content Director.
                Topic: {topic}
                
                1. Write a short, engaging, viral-style script (max 30 seconds spoken) for a video.
                   Tone: Flirty, mischievous, confident.
                   Format: Just the spoken text.
                
                2. Write a catchy Instagram caption with hashtags.
                
                3. Write a standard Stable Diffusion prompt for a background image relevant to this topic.
                
                Output format (strictly):
                SCRIPT: [Script text]
                CAPTION: [Caption text]
                IMAGE_PROMPT: [Prompt text]
                """)
                
                return self._parse_response(response.text)
                
            except exceptions.ResourceExhausted:
                wait_time = (2 ** attempt) * 2 # 2, 4, 8 seconds
                self.log(f"Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            except Exception as e:
                self.log(f"Error generating content: {e}")
                return self._fallback_content(topic)
        
        self.log("Max retries reached. Using fallback.")
        return self._fallback_content(topic)

    def _parse_response(self, text):
        script = ""
        caption = ""
        image_prompt = ""
        
        current_section = None
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith("SCRIPT:"):
                current_section = "SCRIPT"
                script = line.replace("SCRIPT:", "").strip()
            elif line.startswith("CAPTION:"):
                current_section = "CAPTION"
                caption = line.replace("CAPTION:", "").strip()
            elif line.startswith("IMAGE_PROMPT:"):
                current_section = "IMAGE_PROMPT"
                image_prompt = line.replace("IMAGE_PROMPT:", "").strip()
            elif current_section == "SCRIPT":
                script += " " + line
            elif current_section == "CAPTION":
                caption += " " + line
            elif current_section == "IMAGE_PROMPT":
                image_prompt += " " + line
                
        return {
            "script": script.strip(),
            "caption": caption.strip(),
            "image_prompt": image_prompt.strip()
        }

    def _fallback_content(self, topic):
        return {
            "script": f"Hey guys! Did you know about {topic}? It's absolutely wild. Follow for more!",
            "caption": f"Checking out {topic} today! #AI #{topic}",
            "image_prompt": f"futuristic representation of {topic}, 8k, bokeh"
        }
