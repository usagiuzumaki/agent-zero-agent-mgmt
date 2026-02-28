from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict

class GentleCorrectionTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Gentle Correction. "
            "If the user is mistaken or inconsistent, correct them firmly but with warmth and empathy. "
            "Avoid being pedantic; be a supportive mentor. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        return draft_response
