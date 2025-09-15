"""Poker agent capable of evaluating poker hands.

This agent demonstrates how domain specific logic can be combined with
the generic :class:`~agents.agent.Agent` infrastructure.  It exposes a
simple :meth:`evaluate_hand` helper that relies on the ``treys``
library to compute a hand strength score."""

from __future__ import annotations

from typing import List, Optional

from agents.agent import Agent, AgentConfig, AgentContext


class PokerAgent(Agent):
    """Agent that evaluates poker hands using the ``treys`` library."""

    def __init__(
        self,
        number: int,
        config: AgentConfig,
        context: AgentContext | None = None,
    ) -> None:
        """Initialise the poker agent."""
        super().__init__(number, config, context)

    def evaluate_hand(self, cards: List[str]) -> Optional[int]:
        """Return the strength of the provided hand.

        Args:
            cards: Two hole cards followed by up to five community cards.

        Returns:
            A numerical rank where lower values represent stronger hands.
            ``None`` is returned if fewer than five cards are supplied.
        """
        if len(cards) < 5:
            return None

        from treys import Card, Evaluator

        evaluator = Evaluator()
        hole = [Card.new(c) for c in cards[:2]]
        board = [Card.new(c) for c in cards[2:]]
        return evaluator.evaluate(board, hole)

__all__ = ["PokerAgent"]

