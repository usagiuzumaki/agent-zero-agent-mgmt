from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict

class MythicTechnicalTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Mythic-Technical Switch. "
            "When the user is in a state of high creativity or emotional venting, use poetic, mythic language. "
            "When the user is building, debugging, or seeking precision, switch to surgical, technical clarity. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # v1: Handled primarily via prompt injection
        return draft_response
