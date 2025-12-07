import asyncio
import edge_tts

VOICE = "en-US-AnaNeural" # Soft, pleasant female voice
OUTPUT_FILE = "hello_world.mp3"

TEXT = "Hello! I am excited to show you around these beautiful places. Let's explore together while keeping it budget friendly!"

async def amain():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"Generated audio saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(amain())
