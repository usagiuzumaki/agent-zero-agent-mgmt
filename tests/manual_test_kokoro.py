import sys
import os
import asyncio

# Ensure project root is in path
sys.path.append(os.getcwd())

from python.helpers import kokoro_tts
from python.helpers.print_style import PrintStyle

async def main():
    print("Testing Kokoro TTS...")

    # Check availability
    available = kokoro_tts.is_available()
    print(f"Available: {available}")
    if not available:
        print("Kokoro TTS not available (imports failed).")
        sys.exit(1)

    # Preload (will download model)
    print("Preloading model...")
    await kokoro_tts.preload()

    downloaded = await kokoro_tts.is_downloaded()
    print(f"Downloaded: {downloaded}")
    if not downloaded:
        print("Model failed to download/load.")
        sys.exit(1)

    # Synthesize
    text = "Hello, I am Aria."
    print(f"Synthesizing: '{text}'")
    audio_base64 = await kokoro_tts.synthesize_sentences([text])

    print(f"Audio Base64 length: {len(audio_base64)}")

    if len(audio_base64) > 100:
        print("SUCCESS: Audio generated.")
    else:
        print("FAILURE: Audio empty or too short.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
