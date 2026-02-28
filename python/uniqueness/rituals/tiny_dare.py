from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict

class TinyDareRitual(Ritual):
    @property
    def name(self) -> str:
        return "Tiny Dare"

    async def when(self, context: Dict[str, Any]) -> bool:
        return True # Can be random or based on coaching relationship

    async def apply(self, response: str) -> str:
        # Placeholder: add one actionable challenge
        return response
