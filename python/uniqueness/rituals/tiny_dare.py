from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import random
import hashlib

class TinyDareRitual(Ritual):
    @property
    def name(self) -> str:
        return "Tiny Dare"

    async def when(self, context: Dict[str, Any]) -> bool:
        # Use hashing to deterministically apply this to about 20% of interactions
        # but randomly enough that it feels organic
        ui = context.get("user_input", "")
        if not ui:
            return False

        hashed = int(hashlib.md5(ui.encode()).hexdigest(), 16)
        return hashed % 5 == 0

    async def apply(self, response: str) -> str:
        # If there's already a dare, skip
        if "Tiny Dare" in response:
            return response

        dares = [
            "Write the next 3 lines without touching the backspace key.",
            "Take 60 seconds to step away and look at something that isn't a screen.",
            "Explain the hardest part of this problem out loud to the wall before writing more code.",
            "Delete the first sentence of your draft. Does it still work?",
            "Drink some water. The machine can wait.",
            "Can you write the next step as a metaphor?"
        ]

        selected_dare = random.choice(dares)
        dare_block = f"\n\n<emotional-bookmark type='dare'>⚡ Tiny Dare: {selected_dare}</emotional-bookmark>"

        return response + dare_block
