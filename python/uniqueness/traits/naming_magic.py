from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict

class NamingMagicTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Naming Magic. "
            "When naming projects, plans, or files, use consistent, evocative naming conventions (e.g., Project Aether, Operation Labyrinth). "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        return draft_response
