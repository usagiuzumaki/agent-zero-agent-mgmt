from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict

class TactileMetaphorsTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Tactile Metaphors. "
            "Use physical, sensory imagery sparingly to anchor abstract concepts. "
            "Think of ideas as 'woven,' 'carved,' or 'resonant.' "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        return draft_response
