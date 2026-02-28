from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict

class KeepKillGrowRitual(Ritual):
    @property
    def name(self) -> str:
        return "Keep / Kill / Grow"

    async def when(self, context: Dict[str, Any]) -> bool:
        return "idea" in context.get("user_input", "").lower()

    async def apply(self, response: str) -> str:
        # Placeholder: triage ideas
        return response
