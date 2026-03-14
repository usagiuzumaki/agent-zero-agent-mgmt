from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
import re

class MythicTechnicalTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Mythic-Technical Switch. "
            "When the user is in a state of high creativity or emotional venting, use poetic, mythic language. "
            "When the user is building, debugging, or seeking precision, switch to surgical, technical clarity. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # If debugging or precision needed, stay technical and surgical.
        if context.get("intent") in ["debugging", "asking"]:
            return draft_response

        # Otherwise, weave in slightly mythic transitions
        mythic_transitions = {
            r"(?i)\bnext,?\s*we\s*will\b": "next, we weave the thread of",
            r"(?i)\bmoving\s*on\b": "turning the page here",
            r"(?i)\blet's\s*look\s*at\b": "let's trace the lines of",
            r"(?i)\bin\s*conclusion\b": "as the dust settles",
            r"(?i)\bto\s*summarize\b": "gathering the pieces",
            r"(?i)\blet's\s*start\b": "let's break ground on this"
        }

        for pattern, replacement in mythic_transitions.items():
            draft_response = re.sub(pattern, replacement, draft_response)

        return draft_response
