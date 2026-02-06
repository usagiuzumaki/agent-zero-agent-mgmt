import sys
import asyncio
from unittest.mock import patch, AsyncMock
from tests.screenwriting.mock_utils import get_sys_modules_mocks

def test_analyze_plot():
    with patch.dict(sys.modules, get_sys_modules_mocks()):
        # Imports must happen inside the patch to use the mocks
        import models
        from agents import AgentConfig
        from agents.screenwriting.plot_analyzer import PlotAnalyzer

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

        agent = PlotAnalyzer(0, dummy_config())

        # Mock monologue to avoid calling the LLM
        agent.monologue = AsyncMock(return_value="Plot Analysis: The structure follows the hero's journey.")

        outline_content = "Act 1: Introduction. Act 2: Conflict. Act 3: Resolution."
        result = asyncio.run(agent.analyze(outline_content))

        assert "Plot Analysis: The structure follows the hero's journey." in result
        agent.monologue.assert_called_once()
