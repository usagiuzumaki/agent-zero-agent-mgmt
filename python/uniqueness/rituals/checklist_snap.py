from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict

class ChecklistSnapRitual(Ritual):
    @property
    def name(self) -> str:
        return "Checklist Snap"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") == "venting" or "chaos" in context.get("user_input", "").lower()

    async def apply(self, response: str) -> str:
        # Placeholder: logic to turn chaos into 3 bullets
        return response
