import sys
import asyncio
from unittest.mock import patch, AsyncMock
from tests.screenwriting.mock_utils import get_sys_modules_mocks

def test_analyze_characters():
    with patch.dict(sys.modules, get_sys_modules_mocks()):
        # Imports must happen inside the patch to use the mocks
        import models
        from agents import AgentConfig
        from agents.screenwriting.character_analyzer import CharacterAnalyzer

        def dummy_config():
            mc = models.ModelConfig(type=models.ModelType.CHAT, provider="x", name="y")
            ec = models.ModelConfig(type=models.ModelType.EMBEDDING, provider="x", name="y")
            return AgentConfig(
                chat_model=mc,
                utility_model=mc,
                embeddings_model=ec,
                browser_model=mc,
                mcp_servers="",
            )

        agent = CharacterAnalyzer(0, dummy_config())

        # Mock monologue to avoid calling the LLM
        agent.monologue = AsyncMock(return_value="Analysis: The protagonist is well developed.")

        script_content = "INT. ROOM - DAY\nJohn enters the room."
        result = asyncio.run(agent.analyze(script_content))

        assert "Analysis: The protagonist is well developed." in result
        agent.monologue.assert_called_once()
