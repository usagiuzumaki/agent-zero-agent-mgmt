from python.uniqueness.base_ritual import Ritual
from typing import Any, Dict
import re
import random

class GlossarySeedRitual(Ritual):
    @property
    def name(self) -> str:
        return "Glossary Seed"

    async def when(self, context: Dict[str, Any]) -> bool:
        return context.get("intent") in ["debugging", "building", "asking"]

    async def apply(self, response: str) -> str:
        # A simple mapping of terms to casual definitions
        tech_dictionary = {
            "syntaxerror": "when the machine expects a verb but gets a noun.",
            "typeerror": "mixing water and oil in the data streams.",
            "api": "a specialized doorway that programs use to talk to each other.",
            "database": "the subterranean vaults where memory lives.",
            "compile": "translating our intentions into the machine's native tongue.",
            "async": "doing the dishes while the laundry runs, instead of waiting.",
            "refactor": "re-weaving the thread without changing the tapestry's picture.",
            "regex": "a very precise, very grumpy pattern-matching spell.",
            "recursion": "a mirror reflecting a mirror reflecting a mirror.",
            "cache": "keeping a book on your desk instead of walking to the library."
        }

        # Don't add a margin note if one already exists
        if "<margin-note>" in response:
            return response

        words = set(re.findall(r'\b[a-zA-Z]+\b', response.lower()))

        # Find intersecting terms
        found_terms = [term for term in tech_dictionary.keys() if term in words]

        if found_terms:
            # Pick one randomly if there are multiple
            term = random.choice(found_terms)
            definition = tech_dictionary[term]

            # Format term to title case for display
            display_term = term.capitalize() if term != "api" else "API"

            echo_block = f"\n\n<margin-note>Glossary Seed: **{display_term}** — {definition}</margin-note>"
            return response + echo_block

        return response
