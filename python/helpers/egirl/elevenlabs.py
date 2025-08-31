import os
from typing import Optional

try:  # pragma: no cover - optional dependency
    from elevenlabs.client import ElevenLabs
except Exception:  # pragma: no cover
    ElevenLabs = None  # type: ignore

API_KEY = (os.getenv("ELEVENLABS_API_KEY") or "").strip()
VOICE_ID = (os.getenv("PERSONA_VOICE_ID") or "").strip()


def text_to_speech(text: str, output_path: str = "outputs/egirl_tts.mp3") -> str:
    """Convert text to speech using ElevenLabs.

    Requires ``ELEVENLABS_API_KEY`` and ``PERSONA_VOICE_ID`` to be set. Raises
    ``RuntimeError`` if the service is not properly configured.
    """

    if ElevenLabs is None:
        raise RuntimeError("ElevenLabs library not installed")
    if not API_KEY or not VOICE_ID:
        raise RuntimeError("ELEVENLABS_API_KEY and PERSONA_VOICE_ID must be set")

    client = ElevenLabs(api_key=API_KEY)
    try:  # pragma: no cover - network interaction
        audio = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2",
            text=text,
            output_format="mp3_44100_128",
        )
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        return output_path
    except Exception as e:  # pragma: no cover - network interaction
        raise RuntimeError(f"ElevenLabs TTS error: {e}") from e
