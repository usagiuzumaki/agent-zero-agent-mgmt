import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from python.uniqueness.engine import AriaUniquenessEngine
from python.uniqueness.score import UniquenessScorer
from python.uniqueness.memory_style import AriaMemoryStyle

class MockAgent:
    def __init__(self):
        self.config = type('Config', (), {'additional': {'UNIQUENESS_ENGINE': True}, 'uniqueness_engine': True})
    def get_data(self, key): return None
    def set_data(self, key, val): pass

async def test_engine_initialization():
    print("Testing Engine Initialization...")
    engine = AriaUniquenessEngine()
    assert engine.config["enabled"] is True
    assert len(engine.traits) > 0
    assert len(engine.rituals) > 0
    print("OK")

async def test_system_prompt_snippet():
    print("Testing System Prompt Snippet...")
    engine = AriaUniquenessEngine()
    snippet = await engine.get_system_prompt_snippet()
    assert "ARIA UNIQUENESS PROTOCOL" in snippet
    assert "SIGNATURE TRAITS" in snippet
    print("OK")

async def test_response_processing():
    print("Testing Response Processing...")
    engine = AriaUniquenessEngine()
    agent = MockAgent()
    raw_response = "Certainly! I can help. As an AI language model..."
    processed = await engine.process_response(agent, "test", raw_response)
    assert "Resonant." in processed
    assert "As an AI language model" not in processed
    print("OK")

async def test_uniqueness_scoring():
    print("Testing Uniqueness Scoring...")
    engine = AriaUniquenessEngine()
    scorer = UniquenessScorer(engine.config)
    response = "I hear the pattern. We shall weave a solution. Operation Labyrinth is a go."
    state = {"active_traits": ["trait1", "trait2"], "ritual_applied": True}
    score = scorer.calculate_score(response, {"user_input": "test"}, state)
    assert score > 0.5
    print(f"Score: {score} OK")

async def test_memory_style():
    print("Testing Memory Style...")
    engine = AriaUniquenessEngine()
    memory_style = AriaMemoryStyle(engine.config)
    assert await memory_style.should_store_memory("I love Python", {}) is True
    assert await memory_style.should_store_memory("What is 2+2", {}) is False
    print("OK")

async def run_all():
    try:
        await test_engine_initialization()
        await test_system_prompt_snippet()
        await test_response_processing()
        await test_uniqueness_scoring()
        await test_memory_style()
        print("\nALL TESTS PASSED!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_all())
