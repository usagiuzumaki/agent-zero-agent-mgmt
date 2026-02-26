"""
Kokoro TTS integration.
Uses the 'kokoro' pip package for high-quality, lightweight TTS.
"""

import io
import base64
import torch
import soundfile as sf
import numpy as np
from typing import List, Optional
from python.helpers.print_style import PrintStyle

# Global pipeline instance
_pipeline = None
_model_downloaded = False

def is_available() -> bool:
    """Return True if the Kokoro TTS is available (dependencies installed)."""
    try:
        import kokoro
        import soundfile
        import misaki
        return True
    except ImportError:
        return False
    except Exception as e:
        PrintStyle().error(f"Kokoro TTS availability check failed: {e}")
        return False

async def is_downloaded() -> bool:
    """Return True if the Kokoro model is loaded and ready."""
    return _pipeline is not None

async def preload():
    """
    Preload the Kokoro TTS model.
    This initializes the KPipeline, which triggers model download if needed.
    """
    global _pipeline, _model_downloaded

    if _pipeline is not None:
        return

    try:
        from kokoro import KPipeline
        PrintStyle().print("Initializing Kokoro TTS pipeline (this may download the model)...")

        # Initialize pipeline for American English
        # This will download the model to the huggingface cache if not present
        # Set device to cpu or cuda if available
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        _pipeline = KPipeline(lang_code='a', device=device)

        _model_downloaded = True
        PrintStyle().print(f"Kokoro TTS initialized on {device}.")

    except Exception as e:
        PrintStyle().error(f"Error initializing Kokoro TTS: {e}")
        _pipeline = None
        _model_downloaded = False
        raise e

async def synthesize_sentences(sentences: List[str], voice: str = 'af_heart', speed: float = 1.0) -> str:
    """
    Synthesize a list of sentences into audio.
    Returns a base64 encoded WAV string.
    """
    global _pipeline

    if _pipeline is None:
        PrintStyle().warning("Kokoro TTS model not initialized, attempting to preload...")
        await preload()
        if _pipeline is None:
            raise RuntimeError("Failed to initialize Kokoro TTS pipeline.")

    text = " ".join(sentences)
    if not text.strip():
        return ""

    try:
        # Generate audio
        # The pipeline returns a generator of (graphemes, phonemes, audio)
        generator = _pipeline(text, voice=voice, speed=speed, split_pattern=r'\n+')

        all_audio = []

        for _, _, audio in generator:
            if audio is not None:
                all_audio.append(audio)

        if not all_audio:
            return ""

        # Concatenate all audio chunks
        final_audio = np.concatenate(all_audio)

        # Convert to WAV in-memory
        buffer = io.BytesIO()
        # Kokoro output is 24khz
        sf.write(buffer, final_audio, 24000, format='WAV')
        buffer.seek(0)

        # Encode to base64
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return audio_base64

    except Exception as e:
        PrintStyle().error(f"Error synthesizing with Kokoro TTS: {e}")
        raise e
