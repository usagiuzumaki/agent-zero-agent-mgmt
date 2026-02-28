from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict

class GlossarySeedRitual(Ritual):
    @property
    def name(self) -> str:
        return "Glossary Seed"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") == "debugging"

    async def apply(self, response: str) -> str:
        # Placeholder: define one term casually
        return response
