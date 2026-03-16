import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from python.tools.screenwriting import (
    SceneBreakdown,
    CharacterAnalyzer,
    WorldBuilder,
    DialoguePolisher,
    PacingMetrics,
    ScreenwritingPipeline,
    ScreenwritingSpecialist
)
from python.helpers.tool import Response

class MockSubordinate:
    DATA_NAME_SUBORDINATE = "subordinate"
    DATA_NAME_SUPERIOR = "superior"
    def __init__(self, *args, **kwargs):
        pass
    def set_data(self, name, val):
        pass
    def hist_add_user_message(self, msg):
        pass
    async def monologue(self):
        return "Mocked Subordinate Response"

class MockAgent:
    def __init__(self, *args, **kwargs):
        self.number = 0
        self.config = MagicMock()
        self.context = MagicMock()

        self._data = {}

        # Tools map
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
        return self._data.get(name)

    def set_data(self, name, val):
        self._data[name] = val

    def get_tool(self, name, method=None, args=None, message=None, loop_data=None):
        if name in self.tools:
            return self.tools[name](agent=self, args=args, message=message)
        from python.tools.unknown import Unknown
        return Unknown(agent=self, name="unknown")

    async def handle_intervention(self):
        pass

    def hist_add_user_message(self, msg):
        pass

    async def monologue(self):
        return "Mocked Subordinate Response"


@pytest.mark.asyncio
@patch("python.tools.screenwriting.scene_breakdown.Agent", new=MockSubordinate)
@patch("python.tools.screenwriting.character_analyzer.Agent", new=MockSubordinate)
@patch("python.tools.screenwriting.world_builder.Agent", new=MockSubordinate)
@patch("python.tools.screenwriting.dialogue_polisher.Agent", new=MockSubordinate)
@patch("python.tools.screenwriting.pacing_metrics.Agent", new=MockSubordinate)
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

    assert "=== FINAL PIPELINE DRAFT ===" in res.message
    assert "=== PIPELINE LOG ===" in res.message
    assert "scene_breakdown" in res.message
    assert "pacing_metrics" in res.message
    assert "dialogue_polisher" in res.message
    assert "world_builder" in res.message
    assert "character_analyzer" in res.message
