"""Lightweight MBTI-style personality evaluator for characters."""

from __future__ import annotations

import re
from typing import Dict, Tuple
import json

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

    def evaluate(self, text: str) -> Dict[str, object]:
        """Return raw trait scores and a best-guess type."""
        words = re.findall(r"\w+", text.lower())
        scores: Dict[str, int] = {trait: 0 for pair in TRAITS for trait in pair[:2]}
        for a, b, set_a, set_b in TRAITS:
            scores[a] += sum(1 for w in words if w in set_a)
            scores[b] += sum(1 for w in words if w in set_b)
        mbti = "".join(a if scores[a] >= scores[b] else b for a, b, *_ in TRAITS)
        return {"type": mbti, "scores": scores}

    async def analyze(self, text: str) -> str:
        """Standardized analysis method for pipeline integration."""
        result = self.evaluate(text)
        return f"## MBTI Evaluation\n\n**Type:** {result['type']}\n\n```json\n{json.dumps(result['scores'], indent=2)}\n```"
