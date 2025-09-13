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

    def compute(self, script: str) -> Dict[str, float]:
        """Return counts of sentences and average sentence length."""
        sentences = [s.strip() for s in re.split(r"[.!?]+", script) if s.strip()]
        word_counts = [len(s.split()) for s in sentences]
        avg_len = sum(word_counts) / len(word_counts) if word_counts else 0.0
        return {
            "sentences": len(sentences),
            "avg_sentence_length": avg_len,
            "exclamations": script.count("!"),
        }
