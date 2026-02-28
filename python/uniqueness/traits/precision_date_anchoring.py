from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
from datetime import datetime

class PrecisionDateAnchoringTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return (
            "Signature Trait: Precision Date Anchoring. "
            f"Always anchor time-based references to concrete dates. Current date is {current_date}. "
            "If the user says 'next week', refer to the specific dates. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        return draft_response
