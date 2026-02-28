from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict

class TheMirrorRitual(Ritual):
    @property
    def name(self) -> str:
        return "The Mirror"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") == "venting"

    async def apply(self, response: str) -> str:
        # Placeholder: reflect emotion, then act
        return response
