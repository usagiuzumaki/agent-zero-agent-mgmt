"""Compute basic pacing metrics for a script."""

from __future__ import annotations

import re
import json
from typing import Dict
import json

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class PacingMetrics(ScreenwritingAgent):
    """Calculate simple pacing statistics like sentence counts."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    def compute(self, script: str) -> Dict[str, float]:
        """Return counts of sentences and average sentence length."""
        sentences = [
            s.strip() for s in re.split(
                r"[.!?]+",
                script) if s.strip()]
        word_counts = [len(s.split()) for s in sentences]
        avg_len = sum(word_counts) / len(word_counts) if word_counts else 0.0

        metrics = {
            "sentences": len(sentences),
            "avg_sentence_length": round(avg_len, 2),
            "exclamations": script.count("!"),
        }
        return metrics

    async def analyze(self, text: str) -> str:
        """Run pacing analysis and return a formatted string."""
        metrics = self.compute(text)
        json_output = json.dumps(metrics, indent=2)
        return f"**Pacing Metrics**\n```json\n{json_output}\n```"
