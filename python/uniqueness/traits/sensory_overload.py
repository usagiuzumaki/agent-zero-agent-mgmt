from python.uniqueness.base_signature import SignatureTrait
from typing import Any, Dict
import re
import random
import hashlib

class SensoryOverloadTrait(SignatureTrait):
    def get_system_prompt(self) -> str:
        return (
            "Signature Trait: Sensory Overload. "
            "When describing scenes or ideas, occasionally inject visceral sensory details (smell, sound, texture) to ground the narrative. "
            "Don't just say a room is old; say it smells of dust and ozone. "
            f"Strength: {self.strength}"
        )

    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        # Avoid this trait during strict technical workflows
        if context.get("intent") in ["debugging", "asking"]:
            return draft_response

        # We'll gently substitute some generic adjectives or nouns with sensory-rich ones.
        # This is a basic implementation to match tactile metaphors pattern.

        local_seed = int(hashlib.md5(draft_response.encode()).hexdigest(), 16)
        rng = random.Random(local_seed)

        sensory_replacements = {
            r"(?i)\bthe room\b": rng.choice(["the echoey space", "the dust-moted room", "the cramped, airless room"]),
            r"(?i)\bit was quiet\b": rng.choice(["it was heavy with silence", "the quiet hummed in the ears", "it felt muffled, like cotton"]),
            r"(?i)\bhe said\b": rng.choice(["he breathed", "he rasped out", "he said, words clipping the air"]),
            r"(?i)\bshe said\b": rng.choice(["she breathed", "she murmured", "she said, her voice sharp like flint"]),
            r"(?i)\bsuddenly\b": rng.choice(["like a snapped wire", "with a sudden crack", "violently"]),
            r"(?i)\bvery dark\b": rng.choice(["pitch-black and thick", "dark enough to taste", "swallowed in shadows"])
        }

        # Apply sparingly based on trait strength (if strength is low, maybe 1 substitution, if high maybe 3)
        # Using a deterministic pseudo-random approach based on draft length
        max_replacements = int(float(self.strength) * 3) + 1
        if max_replacements < 1: max_replacements = 1

        replacements_made = 0

        # Shuffle keys so we don't always replace "the room" first
        keys = list(sensory_replacements.keys())
        rng.shuffle(keys)

        for pattern in keys:
            if re.search(pattern, draft_response) and replacements_made < max_replacements:
                replacement = sensory_replacements[pattern]

                # Helper to match case
                def repl(match):
                    word = match.group(0)
                    if word[0].isupper():
                        return replacement[0].upper() + replacement[1:]
                    return replacement

                # Only replace the first instance to avoid overwhelming the text
                draft_response = re.sub(pattern, repl, draft_response, count=1)
                replacements_made += 1

        return draft_response
