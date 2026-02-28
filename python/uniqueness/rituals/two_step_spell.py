from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re

class TwoStepSpellRitual(Ritual):
    @property
    def name(self) -> str:
        return "Two-Step Spell"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") in ["asking", "building"]

    async def apply(self, response: str) -> str:
        # v1: Simple logic to ensure a quick plan + charm
        if "plan" in response.lower() or "step" in response.lower():
             return response

        # If no plan, we might wrap it (simplified for v1)
        return response
