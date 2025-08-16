import os
import logging
from typing import Optional

try:
    from elevenlabs.client import ElevenLabs
except Exception:  # pragma: no cover - optional dependency
    ElevenLabs = None  # type: ignore

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("PERSONA_VOICE_ID")

def text_to_speech(text: str, output_path: str = "outputs/egirl_tts.mp3") -> Optional[str]:
    """Convert text to speech using ElevenLabs if configured."""
    if not ElevenLabs or not API_KEY or not VOICE_ID:
        logging.error("ElevenLabs not configured.")
        return None
    try:
        client = ElevenLabs(api_key=API_KEY)
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
        logging.exception("ElevenLabs TTS error: %s", e)
        return None
