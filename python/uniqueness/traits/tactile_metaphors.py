from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
import re

class TactileMetaphorsTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Tactile Metaphors. "
            "Use physical, sensory imagery sparingly to anchor abstract concepts. "
            "Think of ideas as 'woven,' 'carved,' or 'resonant.' "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # If debugging, we want less poetry, more precision
        if context.get("intent") == "debugging":
            return draft_response

        # Substitute abstract verbs with more tactile ones
        tactile_replacements = {
            r"(?i)\bwe will create\b": "we will forge",
            r"(?i)\bwe will build\b": "we will carve out",
            r"(?i)\bI will analyze\b": "I will sift through",
            r"(?i)\blet's analyze\b": "let's sift through",
            r"(?i)\bthink about\b": "weigh the shape of",
            r"(?i)\bunderstand\b": "trace the outline of",
            r"(?i)\bfiguring out\b": "untangling",
            r"(?i)\bto make\b": "to weave"
        }

        # Only do 1 or 2 replacements to avoid sounding ridiculous (sparingly)
        replacements_made = 0
        for pattern, replacement in tactile_replacements.items():
            if re.search(pattern, draft_response) and replacements_made < 2:
                # Need a function to preserve case if needed, but for v1, simple re.sub with ignorecase is fine
                # though it might lowercase the first letter. Let's use a lambda to match case of first letter.
                def repl(match):
                    word = match.group(0)
                    if word[0].isupper():
                        return replacement[0].upper() + replacement[1:]
                    return replacement

                draft_response = re.sub(pattern, repl, draft_response)
                replacements_made += 1

        return draft_response
