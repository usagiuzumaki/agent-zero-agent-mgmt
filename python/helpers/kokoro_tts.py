"""
Lightweight stub for Kokoro TTS integration.
"""

from typing import Any, List, Optional
import os
from python.helpers.print_style import PrintStyle

# Track if model is "downloaded" (stub implementation)
_model_downloaded = False

async def is_downloaded() -> bool:
    """Return True if the Kokoro model is downloaded and ready."""
    return _model_downloaded

async def preload():
    """
    Preload the Kokoro TTS model.
    """
    global _model_downloaded
    try:
        PrintStyle().print("Preloading Kokoro TTS model (stub)...")
        # In a real implementation, this would download or load the model
        _model_downloaded = True
    except Exception as e:
        PrintStyle().error(f"Error preloading Kokoro TTS: {e}")

async def synthesize_sentences(sentences: List[str]) -> str:
    """
    Synthesize a list of sentences into audio.
    Returns a base64 encoded audio string or a path.
    """
    if not _model_downloaded:
        PrintStyle().warning("Kokoro TTS model not downloaded, attempting to preload...")
        await preload()

    PrintStyle().print(f"Synthesizing {len(sentences)} sentences with Kokoro TTS (stub)...")
    # Return an empty audio string or a placeholder to avoid breaking the frontend
    return ""

def is_available() -> bool:
    """Return True if the Kokoro TTS is available."""
    return True
