import asyncio
import sys

from python.tools.screenwriting import (
    SceneBreakdown,
    CharacterAnalyzer,
    WorldBuilder,
    DialoguePolisher,
    PacingMetrics,
    ScreenwritingPipeline,
    ScreenwritingSpecialist
)

class MockAgentConfig:
    def __init__(self):
        self.profile = ""

class MockAgent:
    def __init__(self):
        self.name = "MockAgent"
        self.number = 0
        self.config = MockAgentConfig()
        self.context = None
        self.tools = {
            "scene_breakdown": SceneBreakdown,
            "character_analyzer": CharacterAnalyzer,
            "world_builder": WorldBuilder,
            "dialogue_polisher": DialoguePolisher,
            "pacing_metrics": PacingMetrics,
            "screenwriting_pipeline": ScreenwritingPipeline,
            "screenwriting_specialist": ScreenwritingSpecialist
        }

    def get_data(self, name):
        return getattr(self, name, None)

    def set_data(self, name, val):
        setattr(self, name, val)

    def get_tool(self, name, method, args, message, loop_data):
        if name in self.tools:
            return self.tools[name](agent=self, args=args, message=message)
        from python.tools.unknown import Unknown
        return Unknown(agent=self, name="unknown")

    async def handle_intervention(self):
        pass

    def hist_add_user_message(self, msg):
        pass

    async def monologue(self):
        # Return a mocked response for the subordinate
        return "Mocked Subordinate Response"

async def test_tools_exist():
    agent = MockAgent()

    # Test Individual Tools
    scene = SceneBreakdown(agent=agent, args={"context": "A test scene"})
    res = await scene.execute()
    assert "Mocked Subordinate Response" in res.message

    char = CharacterAnalyzer(agent=agent, args={"context": "A test scene"})
    res = await char.execute()
    assert "Mocked Subordinate Response" in res.message

    world = WorldBuilder(agent=agent, args={"context": "A test scene"})
    res = await world.execute()
    assert "Mocked Subordinate Response" in res.message

    dialogue = DialoguePolisher(agent=agent, args={"context": "A test scene"})
    res = await dialogue.execute()
    assert "Mocked Subordinate Response" in res.message

    pacing = PacingMetrics(agent=agent, args={"context": "A test scene"})
    res = await pacing.execute()
    assert "Mocked Subordinate Response" in res.message

    # Test Specialist
    spec = ScreenwritingSpecialist(agent=agent, args={"mode": "direct", "tool_name": "CharacterAnalyzer", "prompt": "A test prompt"})
    res = await spec.execute()
    assert "Mocked Subordinate Response" in res.message

    # Test Pipeline
    pipe = ScreenwritingPipeline(agent=agent, args={"prompt": "Write a 1-scene short film about a robot learning to cook"})
    res = await pipe.execute()

    print("\n--- Pipeline Output ---")
    print(res.message)
    print("-----------------------\n")

    assert "=== FINAL PIPELINE DRAFT ===" in res.message
    assert "=== PIPELINE LOG ===" in res.message
    assert "scene_breakdown" in res.message
    assert "pacing_metrics" in res.message
    assert "dialogue_polisher" in res.message
    assert "world_builder" in res.message
    assert "character_analyzer" in res.message

    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    try:
        asyncio.run(test_tools_exist())
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
