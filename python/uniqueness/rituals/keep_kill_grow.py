from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re
import random

class KeepKillGrowRitual(Ritual):
    @property
    def name(self) -> str:
        return "Keep / Kill / Grow"

    async def when(self, context: Dict[str, Any]) -> bool:
        ui_lower = context.get("user_input", "").lower()
        return "idea" in ui_lower or "brainstorm" in ui_lower or "concept" in ui_lower

    async def apply(self, response: str) -> str:
        if "Keep:" in response and "Kill:" in response:
            return response

        # Try to identify bullet points that look like ideas
        # Look for a list of items
        list_items = re.findall(r'(?m)^[-*]\s+(.+?)(?:\.|\n|$)', response)

        if len(list_items) >= 3:
            # Pick 3 items for the ritual
            selected = random.sample(list_items, min(3, len(list_items)))

            # Create the block
            triage_block = "\n\n**The Triage (Keep / Kill / Grow):**\n"
            triage_block += f"- **Keep:** *{selected[0].strip()}* — Solid foundation.\n"
            triage_block += f"- **Kill:** *{selected[1].strip()}* — Too much noise for now.\n"
            triage_block += f"- **Grow:** *{selected[2].strip()}* — This thread has the most potential, let's pull it.\n"

            # We append it as a fun, opinionated add-on to the brainstorm
            return response + triage_block

        return response
