import pytest
import asyncio
from python.uniqueness.engine import AriaUniquenessEngine
from python.uniqueness.score import UniquenessScorer
from python.uniqueness.memory_style import AriaMemoryStyle

class MockAgent:
    def __init__(self):
        self.config = type('Config', (), {'additional': {'UNIQUENESS_ENGINE': True}, 'uniqueness_engine': True})
    def get_data(self, key): return None
    def set_data(self, key, val): pass

@pytest.mark.asyncio
async def test_engine_initialization():
    engine = AriaUniquenessEngine()
    assert engine.config["enabled"] is True
    assert len(engine.traits) > 0
    assert len(engine.rituals) > 0

@pytest.mark.asyncio
async def test_system_prompt_snippet():
    engine = AriaUniquenessEngine()
    snippet = await engine.get_system_prompt_snippet()
    assert "ARIA UNIQUENESS PROTOCOL" in snippet
    assert "SIGNATURE TRAITS" in snippet

@pytest.mark.asyncio
async def test_response_processing():
    engine = AriaUniquenessEngine()
    agent = MockAgent()
    raw_response = "Certainly! I can help. As an AI language model..."
    processed = await engine.process_response(agent, "test", raw_response)
    assert "Resonant." in processed
    assert "As an AI language model" not in processed

@pytest.mark.asyncio
async def test_uniqueness_scoring():
    engine = AriaUniquenessEngine()
    scorer = UniquenessScorer(engine.config)
    response = "I hear the pattern. We shall weave a solution. Operation Labyrinth is a go."
    state = {"active_traits": ["trait1", "trait2"], "ritual_applied": True}
    score = scorer.calculate_score(response, {"user_input": "test"}, state)
    assert score > 0.5

@pytest.mark.asyncio
async def test_memory_style():
    engine = AriaUniquenessEngine()
    memory_style = AriaMemoryStyle(engine.config)
    assert await memory_style.should_store_memory("I love Python", {}) is True
    assert await memory_style.should_store_memory("What is 2+2", {}) is False
