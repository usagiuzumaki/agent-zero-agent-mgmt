"""
Kokoro TTS integration.
"""

import io
import base64
import numpy as np
import soundfile as sf
import torch
from python.helpers.print_style import PrintStyle

# Global pipeline instance
_pipeline = None

async def is_downloaded() -> bool:
    """Return True if the Kokoro model is loaded."""
    return _pipeline is not None

async def preload():
    """
    Preload the Kokoro TTS model.
    """
    global _pipeline
    if _pipeline is not None:
        return

    try:
        from kokoro import KPipeline
        PrintStyle().print("Initializing Kokoro TTS pipeline...")
        # 'a' for American English, use 'b' for British English
        # We might want to make this configurable in the future
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Check if we can specify map_location to cpu to be safe if cuda is detected but fails?
        # But torch.cuda.is_available() should be reliable.

        # Initialize pipeline. This might download weights.
        _pipeline = KPipeline(lang_code='a', device=device)
        PrintStyle().print(f"Kokoro TTS pipeline initialized on {device}.")
    except Exception as e:
        PrintStyle().error(f"Error initializing Kokoro TTS: {e}")
        # Ensure _pipeline is None on failure
        _pipeline = None
        raise e

async def synthesize_sentences(sentences: list[str]) -> str:
    """
    Synthesize a list of sentences into audio.
    Returns a base64 encoded audio string (WAV format).
    """
    global _pipeline

    if _pipeline is None:
        PrintStyle().warning("Kokoro TTS model not loaded, attempting to preload...")
        await preload()

    if _pipeline is None:
        raise Exception("Failed to load Kokoro TTS model.")

    PrintStyle().print(f"Synthesizing {len(sentences)} sentences with Kokoro TTS...")

    # KPipeline handles text processing.
    text = " ".join(sentences)

    if not text.strip():
        return ""

    try:
        # Generate audio
        # voice='af_heart' is a good default for 'a' lang_code
        # speed=1 is default
        generator = _pipeline(text, voice='af_heart', speed=1, split_pattern=r'\n+')

        audio_parts = []

        for i, (gs, ps, audio) in enumerate(generator):
            # audio is a numpy array (float32)
            if audio is not None and len(audio) > 0:
                audio_parts.append(audio)

        if not audio_parts:
            return ""

        # Concatenate all audio parts
        full_audio = np.concatenate(audio_parts)

        # Convert to WAV in memory
        buffer = io.BytesIO()
        # Kokoro uses 24000 Hz sample rate
        sf.write(buffer, full_audio, 24000, format='WAV')
        buffer.seek(0)

        # Encode to base64
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return audio_base64
    except Exception as e:
        PrintStyle().error(f"Error during synthesis: {e}")
        raise e

def is_available() -> bool:
    """Return True if the Kokoro TTS is available (dependencies installed)."""
    try:
        import kokoro
        import soundfile
        return True
    except ImportError:
        return False
