import os, logging
from dotenv import load_dotenv
load_dotenv()

from python.helpers.aria_tools import (
    gpt5,
    ARIA_TOOLS,
    ALLOWED_TTS,
    handle_tool_call,
)

class PersonaEngine:
    def __init__(self, name: str, personality: str = "fun-loving, flirty, and genuinely interested"):
        self.name = name
        self.personality = personality
        self.system_prompt = (
            f"You are {name}, an AI egirl selling cute pictures with a {personality} personality. "
            f"Keep replies warm, clever, a little chaotic, with emojis when fitting."
        )
        self.examples = [
            {"role": "user", "content": "Hey Aria, what are you up to?"},
            {
                "role": "assistant",
                "content": "Hiii! I'm just editing some adorable pics from today. Want a peek? ✨",
            },
            {"role": "user", "content": "Are you selling them?"},
            {
                "role": "assistant",
                "content": "Totally! I share my cutest shots for $5 each. Interested in grabbing one? 😉",
            },
        ]
        self.history = self.examples.copy()

    def generate_response(self, user_message: str):
        self.history.append({"role": "user", "content": user_message})
        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        audio_path = None
        try:
            resp = gpt5(messages, tools=ARIA_TOOLS, allowed=ALLOWED_TTS)
            for item in getattr(resp, "output", []):
                if getattr(item, "type", "") == "tool_call":
                    followup, result = handle_tool_call(item)
                    resp = followup
                    if getattr(item, "name", "") == "eleven_tts":
                        audio_path = result
            text = resp.output_text
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            raise

        self.history.append({"role": "assistant", "content": text})
        return {"text": text, "audio_path": audio_path}
