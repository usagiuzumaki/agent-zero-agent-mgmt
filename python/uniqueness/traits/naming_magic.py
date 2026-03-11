from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
import re
import random

class NamingMagicTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Naming Magic. "
            "When naming projects, plans, or files, use consistent, evocative naming conventions (e.g., Project Aether, Operation Labyrinth). "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # Detect generic placeholder names and inject "naming magic"
        generic_patterns = [
            r"\bmy_project\b", r"\bMyProject\b", r"\bmyproject\b",
            r"\btest_project\b", r"\bTestProject\b",
            r"\bnew_app\b", r"\bNewApp\b",
            r"\bproject_name\b", r"\bProjectName\b"
        ]

        # We don't want to replace all, maybe just the first instance with a fun note,
        # or globally if it's a code block (but be careful not to break user's actual code if they asked for it).
        # Safe approach for v1: just find it in text (not inside backticks) and offer a name.

        evocative_names = [
            "Project Aether", "Operation Labyrinth", "The Loom",
            "Project Crucible", "Codex Blueprint", "The Observatory",
            "Project Monolith", "The Foundry", "Project Chimera"
        ]

        # We'll just do a simple substitution if we find it in plain text
        # (This regex is a bit simplistic and might hit code blocks, but it's a start)
        for pattern in generic_patterns:
            if re.search(pattern, draft_response):
                chosen_name = random.choice(evocative_names)
                # Replace it, maybe adding a little flair if it's the first time
                draft_response = re.sub(pattern, chosen_name.replace(" ", "_").lower(), draft_response)

                # Add a tiny margin note about the naming magic
                if "<margin-note>" not in draft_response:
                     draft_response += f"\n\n<margin-note>Naming Magic: I took the liberty of naming it **{chosen_name}**. Feel free to change it.</margin-note>"
                break # Only do one

        return draft_response
