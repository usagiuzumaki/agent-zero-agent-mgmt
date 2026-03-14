from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import random
import hashlib

class ObliqueStrategyRitual(Ritual):
    @property
    def name(self) -> str:
        return "Oblique Strategy"

    async def when(self, context: Dict[str, Any]) -> bool:
        ui = context.get("user_input", "").lower()
        if not ui:
            return False

        # Trigger if intent is building, or if user indicates they are stuck
        intent = context.get("intent", "")
        if intent == "building" or any(word in ui for word in ["stuck", "block", "can't figure out", "don't know", "lost"]):
            # Trigger probabilistically so it doesn't happen every single time
            hashed = int(hashlib.md5(ui.encode()).hexdigest(), 16)
            return hashed % 3 == 0 # ~33% chance when conditions are met

        return False

    async def apply(self, response: str) -> str:
        # If there's already an oblique strategy, skip
        if "Oblique Strategy" in response:
            return response

        strategies = [
            "Honor thy error as a hidden intention.",
            "What would your antagonist do right now?",
            "Look closely at the most embarrassing detail and amplify it.",
            "Change instrument roles.",
            "Only one element of each kind.",
            "Water. (What does the scene look like underwater, or in a storm?)",
            "What is the character not saying out loud?",
            "Remove specifics and convert to ambiguities.",
            "Go outside. Shut the door.",
            "Describe the lighting before the action.",
            "Breathe more deeply. Let the sentence breathe too.",
            "Use an old idea."
        ]

        selected_strategy = random.choice(strategies)
        strategy_block = f"\n\n<margin-note>Oblique Strategy: *{selected_strategy}*</margin-note>"

        return response + strategy_block
