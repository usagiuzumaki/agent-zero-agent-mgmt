import os, logging
from dotenv import load_dotenv
load_dotenv()

import openai
try:
    from elevenlabs.client import ElevenLabs
except Exception as e:  # pragma: no cover - optional dependency
    logging.warning("ElevenLabs library not available: %s", e)
    ElevenLabs = None

openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

eleven_client = None
voice_id = None
if ELEVEN_API_KEY and ElevenLabs:
    try:
        eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)
        voice_id = os.getenv("PERSONA_VOICE_ID")
        if not voice_id:
            voices = eleven_client.voices.get_all().voices
            if voices:
                voice_id = voices[0].voice_id
    except Exception as e:
        logging.error(f"ElevenLabs init failed: {e}")
        eleven_client = None

class PersonaEngine:
    def __init__(self, name: str, personality: str = "playful, flirty, supportive"):
        self.name = name
        self.personality = personality
        self.system_prompt = (
            f"You are {name}, an AI egirl with a {personality} personality. "
            f"Keep replies warm, clever, a little chaotic, with emojis when fitting."
        )
        self.history = []

    def generate_response(self, user_message: str):
        self.history.append({ "role": "user", "content": user_message })
        messages = [{ "role": "system", "content": self.system_prompt }] + self.history
        try:
            resp = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
            text = resp.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            raise
        self.history.append({ "role": "assistant", "content": text })

        audio_path = None
        if eleven_client and voice_id:
            try:
                audio = eleven_client.text_to_speech.convert(
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    text=text,
                    output_format="mp3_44100_128"
                )
                os.makedirs("outputs", exist_ok=True)
                audio_path = f"outputs/{self.name}_response.mp3"
                with open(audio_path, "wb") as f:
                    for chunk in audio:
                        if chunk: f.write(chunk)
            except Exception as e:
                logging.error(f"ElevenLabs TTS failed: {e}")
        return { "text": text, "audio_path": audio_path }
