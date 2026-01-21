"""Agent for real-time poker analysis using OCR.

This agent scrapes the on-screen poker table, reads the cards with
``pytesseract`` and evaluates the resulting hand. The overall approach is
inspired by open-source projects like *gtopokerbot* which perform table
scraping for automated analysis.

The class is written so that it can be plugged into the existing Agent
infrastructure. The OCR and evaluation libraries are imported lazily so
that the module can be imported even when optional dependencies are not
present.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional

from .agent import Agent, AgentConfig, AgentContext


class PokerOcrAgent(Agent):
    """Agent that captures the poker table and evaluates the current hand."""

    def __init__(
        self,
        number: int,
        config: AgentConfig,
        region: Dict[str, int],
        context: AgentContext | None = None,
    ) -> None:
        """Initialise the agent.

        Args:
            number: Identifier of this agent instance.
            config: Standard :class:`AgentConfig` used by Aria Bot (formerly Agent Zero).
            region: ``mss``-style region dictionary describing the screen
                area containing the poker table.
            context: Optional pre-existing :class:`AgentContext`.
        """
        super().__init__(number, config, context)
        self.region = region
        self._sct = None
        self._evaluator = None

    def _grab_table(self):
        """Capture a screenshot of the configured table region."""
        import mss
        from PIL import Image

        if self._sct is None:
            self._sct = mss.mss()
        shot = self._sct.grab(self.region)
        return Image.frombytes("RGB", shot.size, shot.rgb)

    def _read_cards(self, img) -> List[str]:
        """Use OCR to extract card codes from an image."""
        import pytesseract
        from PIL import ImageOps

        grey = ImageOps.grayscale(img)
        text = pytesseract.image_to_string(grey, config="--psm 6")
        return re.findall(r"[2-9TJQKA][shdc]", text.replace(" ", ""))

    def _evaluate(self, cards: List[str]) -> Optional[int]:
        """Return the strength of a hand according to ``treys``.

        The first two cards are treated as the player's hole cards and the
        remaining cards as the board.
        """
        if len(cards) < 5:
            return None
        from treys import Card, Evaluator

        if self._evaluator is None:
            self._evaluator = Evaluator()
        hole = [Card.new(c) for c in cards[:2]]
        board = [Card.new(c) for c in cards[2:]]
        return self._evaluator.evaluate(board, hole)

    def analyze_table(self) -> Dict[str, Optional[int] | List[str]]:
        """Capture, read and evaluate the current poker table."""
        img = self._grab_table()
        cards = self._read_cards(img)
        rank = self._evaluate(cards)
        return {"cards": cards, "rank": rank}
