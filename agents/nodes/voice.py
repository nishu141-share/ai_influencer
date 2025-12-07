import asyncio
import edge_tts
import os
from agents.state import AgentState

def voice_artist_node(state: AgentState) -> AgentState:
    """
    Converts the script to audio using edge-tts.
    """
    print(f"--> VoiceArtist synthesizing audio...")
    
    script = state.get("script")
    if not script:
        return {"error": "No script found in state."}
        
    output_file = os.path.abspath("output_audio.mp3")
    voice = "en-US-AnaNeural"
    
    async def _generate():
        communicate = edge_tts.Communicate(script, voice)
        await communicate.save(output_file)

    try:
        # Run the async generation synchronously
        asyncio.run(_generate())
        print(f"    Audio saved to: {output_file}")
        
        return {
            "audio_path": output_file,
            "current_step": "audio_generated"
        }
    except Exception as e:
        print(f"    Error generating voice: {e}")
        return {"error": str(e)}
