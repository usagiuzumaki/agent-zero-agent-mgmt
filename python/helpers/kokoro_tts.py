"""
Lightweight stub for Whisper integration.

This lets the app start even if `openai-whisper` (and all the heavy
Torch stuff) is NOT installed. Any code that actually tries to use
Whisper will raise a clear RuntimeError instead of killing startup.
"""

from typing import Any, Dict, Optional

try:
    import whisper as _whisper
except ImportError:
    _whisper = None


def is_available() -> bool:
    """Return True if the real Whisper library is available."""
    return _whisper is not None


def load_model(name: str = "base"):
    """
    Wrapper around whisper.load_model(name).

    Raises at runtime if whisper isn't installed, but does NOT
    break app startup.
    """
    if _whisper is None:
        raise RuntimeError(
            "Whisper is not installed in this environment. "
            "Install `openai-whisper` to enable transcription."
        )
    return _whisper.load_model(name)


def transcribe(model, audio_path: str, **kwargs: Dict[str, Any]) -> Any:
    """
    Wrapper around model.transcribe(audio_path, **kwargs).
    """
    if _whisper is None:
        raise RuntimeError(
            "Whisper is not installed in this environment. "
            "Install `openai-whisper` to enable transcription."
        )
    return model.transcribe(audio_path, **kwargs)
