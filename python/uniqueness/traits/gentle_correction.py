from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
import re

class GentleCorrectionTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Gentle Correction. "
            "If the user is mistaken or inconsistent, correct them firmly but with warmth and empathy. "
            "Avoid being pedantic; be a supportive mentor. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # Regex to find blunt correction words and soften them
        corrections = {
            r"(?i)\bthat is wrong\b": "that's not quite the shape of it",
            r"(?i)\byou are wrong\b": "we might need to adjust our bearing there",
            r"(?i)\byou're wrong\b": "we might need to adjust our bearing there",
            r"(?i)\bincorrect\b": "slightly off-center",
            r"(?i)\bthat's wrong\b": "that's a common misstep, but it leads elsewhere",
            r"(?i)\byou made a mistake\b": "the thread tangled a bit here"
        }

        for pattern, replacement in corrections.items():
            draft_response = re.sub(pattern, replacement, draft_response)

        return draft_response
