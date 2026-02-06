import sys
import asyncio
from unittest.mock import patch
from tests.screenwriting.mock_utils import get_sys_modules_mocks

def test_analyze_mbti():
    with patch.dict(sys.modules, get_sys_modules_mocks()):
        # Imports must happen inside the patch to use the mocks
        import models
        from agents import AgentConfig
        from agents.screenwriting.mbti_evaluator import MBTIEvaluator

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

        agent = MBTIEvaluator(0, dummy_config())
        # "Alone" -> I, "Analysis" -> T, "Plan" -> J
        result = asyncio.run(agent.analyze("I like being alone and doing analysis. I plan everything."))
        assert "MBTI Evaluation" in result
        assert "Type: ISTJ" in result
