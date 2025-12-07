import asyncio
import os
import edge_tts
from .base_agent import AgentBase

class VoiceAgent(AgentBase):
    def __init__(self, config_path=None):
        super().__init__("VoiceAgent", config_path)
        # Default voice: en-US-AnaNeural, en-US-AriaNeural, en-US-GuyNeural, etc.
        self.voice = "en-US-AriaNeural" 

    def run(self, input_data):
        """
        Input: {'text': str, 'emotion': str (optional), 'output_path': str (optional)}
        Output: {'audio_path': str}
        """
        text = input_data.get("text")
        if not text:
            self.log("Error: No text provided.")
            return None

        output_path = input_data.get("output_path", "output/voice_output.mp3")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self.log(f"Generating audio for: '{text[:20]}...' using voice {self.voice}")

        # Run async function synchronously
        try:
            asyncio.run(self._generate_audio(text, output_path))
            self.log(f"Audio saved to {output_path}")
            return {"audio_path": output_path}
        except Exception as e:
            self.log(f"Error generating audio: {e}")
            return None

    async def _generate_audio(self, text, output_file):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_file)

if __name__ == "__main__":
    # Test the agent
    agent = VoiceAgent()
    agent.run({"text": "Hello, this is a test of the AI Influencer Voice Agent.", "output_path": "scratch/ai_influencer/output/test_voice.mp3"})
