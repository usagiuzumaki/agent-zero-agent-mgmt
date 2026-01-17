"""Compute basic pacing metrics for a script."""

from __future__ import annotations

import re
from typing import Dict

from agents import AgentConfig
from .base import ScreenwritingAgent


class PacingMetrics(ScreenwritingAgent):
    """Calculate simple pacing statistics like sentence counts."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, script: str) -> str:
        """Return counts of sentences and average sentence length as a formatted string."""
        sentences = [s.strip() for s in re.split(r"[.!?]+", script) if s.strip()]
        word_counts = [len(s.split()) for s in sentences]
        avg_len = sum(word_counts) / len(word_counts) if word_counts else 0.0

        metrics = {
            "sentences": len(sentences),
            "avg_sentence_length": round(avg_len, 2),
            "exclamations": script.count("!"),
        }

        return f"## Pacing Metrics\n\n- **Sentences**: {metrics['sentences']}\n- **Avg Sentence Length**: {metrics['avg_sentence_length']} words\n- **Exclamations**: {metrics['exclamations']}"
