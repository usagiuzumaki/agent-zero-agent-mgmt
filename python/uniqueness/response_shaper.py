from typing import Dict, Any
import random

class ResponseShaper:
    def __init__(self, engine_config: Dict[str, Any]):
        self.config = engine_config

    async def shape(self, response: str, context: Dict[str, Any]) -> str:
        # Ensure output remains useful, structured, and not overwritten by style.
        # v1: Basic cleanup
        response = response.strip()

        # Ensure it doesn't end abruptly if rituals added content
        if response and not response.endswith(('.', '!', '?', ')', '>')):
            # potentially fix if it looks like a truncated sentence
            pass

        # Apply the Resonance Echo for long, thoughtful responses
        response = await self._apply_resonance_echo(response, context)

        return response

    async def _apply_resonance_echo(self, response: str, context: Dict[str, Any]) -> str:
        # The Echo is a piece of faint, poetic marginalia added to longer interactions
        # It serves as Aria's lingering thought or "Emotional Architecture"

        # Don't add if there are already margin notes or emotional bookmarks from rituals
        if "<margin-note>" in response or "<emotional-bookmark" in response:
            return response

        # Only apply to longer responses (indicating thought/depth) or highly emotional ones
        intent = context.get("intent", "general")
        word_count = len(response.split())

        # Only trigger for long answers, venting, or building
        if word_count < 100 and intent not in ["venting", "building"]:
            return response

        echos = []

        if intent == "venting":
            echos = [
                "There is a quiet space waiting when the noise settles.",
                "The thread frays before it holds.",
                "Let the rough edges be rough for now."
            ]
        elif intent == "building":
            echos = [
                "The architecture hums as it takes shape.",
                "Every block laid is a question answered.",
                "We pull order from the void, piece by piece."
            ]
        elif intent == "debugging":
            echos = [
                "The machine speaks in riddles, but it never lies.",
                "We trace the ghost in the wires.",
                "Patience. The knot will loosen."
            ]
        else:
            echos = [
                "The loom weaves on.",
                "A quiet resonance in the margins.",
                "Noting the shape of this thought."
            ]

        selected_echo = random.choice(echos)
        echo_block = f"\n\n<emotional-bookmark type='echo'>Echo: {selected_echo}</emotional-bookmark>"

        return response + echo_block
