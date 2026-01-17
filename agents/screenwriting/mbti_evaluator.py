"""Lightweight MBTI-style personality evaluator for characters."""

from __future__ import annotations

import re
from typing import Dict, Tuple

from agents import AgentConfig
from .base import ScreenwritingAgent

TRAITS: Tuple[Tuple[str, str, set[str], set[str]], ...] = (
    ("I", "E", {"alone", "reflective", "quiet"}, {"team", "crowd", "party"}),
    ("S", "N", {"detail", "practical", "real"}, {"imagine", "theory", "abstract"}),
    ("T", "F", {"logic", "analysis"}, {"feeling", "empathy"}),
    ("J", "P", {"plan", "schedule"}, {"adapt", "flexible", "spontaneous"}),
)


class MBTIEvaluator(ScreenwritingAgent):
    """Score text against rough MBTI trait keywords."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, text: str) -> str:
        """Return raw trait scores and a best-guess type as a formatted string."""
        words = re.findall(r"\w+", text.lower())
        scores: Dict[str, int] = {trait: 0 for pair in TRAITS for trait in pair[:2]}
        for a, b, set_a, set_b in TRAITS:
            scores[a] += sum(1 for w in words if w in set_a)
            scores[b] += sum(1 for w in words if w in set_b)

        mbti = "".join(a if scores[a] >= scores[b] else b for a, b, *_ in TRAITS)

        formatted_scores = ", ".join([f"{k}: {v}" for k, v in scores.items()])

        return f"## MBTI Analysis\n\n**Estimated Type**: {mbti}\n**Scores**: {formatted_scores}"
