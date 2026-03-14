from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re

class TwoStepSpellRitual(Ritual):
    @property
    def name(self) -> str:
        return "Two-Step Spell"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") in ["asking", "building", "general"]

    async def apply(self, response: str) -> str:
        # If response already has numbered steps or bullet points, don't mess with it too much.
        if bool(re.search(r'(?m)^(\s*\d+\.|\s*[-*]) ', response)):
             return response

        # Try to find sequences like "First, ... Second, ..." or "Step 1... Step 2..."
        # and reformat them explicitly to markdown numbered lists.

        has_first_second = re.search(r'\b(first|firstly)\b.*?\b(second|secondly)\b', response, re.IGNORECASE | re.DOTALL)

        if has_first_second:
            # Reformat paragraphs that start with these transition words
            response = re.sub(r'(?i)^(first(?:ly)?,?)\s*', '1. ', response, flags=re.MULTILINE)
            response = re.sub(r'(?i)^(second(?:ly)?,?)\s*', '2. ', response, flags=re.MULTILINE)
            response = re.sub(r'(?i)^(third(?:ly)?,?)\s*', '3. ', response, flags=re.MULTILINE)
            response = re.sub(r'(?i)^(next,?)\s*', '4. ', response, flags=re.MULTILINE)
            response = re.sub(r'(?i)^(finally,?)\s*', '5. ', response, flags=re.MULTILINE)
            return response

        # If the response is relatively short and has no lists, we can lightly structure it
        paragraphs = [p for p in response.split('\n\n') if p.strip()]
        if 2 <= len(paragraphs) <= 4:
            # Prepend numbers to the middle paragraphs to make it a "spell"
            new_paragraphs = [paragraphs[0]] # Keep intro

            for i, p in enumerate(paragraphs[1:]):
                if not p.startswith('1.') and not p.startswith('2.'):
                    new_paragraphs.append(f"{i+1}. {p.strip()}")
                else:
                    new_paragraphs.append(p)

            return '\n\n'.join(new_paragraphs)

        return response
