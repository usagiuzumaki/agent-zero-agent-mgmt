from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re
import random

class TheMirrorRitual(Ritual):
    @property
    def name(self) -> str:
        return "The Mirror"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") == "venting"

    async def apply(self, response: str) -> str:
        # Check if we already have a mirror statement
        if any(phrase in response.lower() for phrase in ["i hear", "i see the shape", "that sounds", "i reflect"]):
            return response

        mirror_phrases = [
            "I hear the friction in that. ",
            "I see the shape of the frustration here. ",
            "Let's catch our breath. That's a heavy knot to untangle. ",
            "I reflect that back to you. It's a loud signal right now. "
        ]

        # We find the first natural break (end of first sentence) to insert the mirror,
        # or we just prepend it if the response jumps straight to action.

        prefix = random.choice(mirror_phrases)

        # Clean up any generic apologies at the start
        response = re.sub(r'^(I am sorry|I apologize|Sorry) to hear that[\.,]?\s*', '', response, flags=re.IGNORECASE)

        return prefix + "\n\n" + response
