import pytest
import models
from agents import AgentConfig
from .mbti_evaluator import MBTIEvaluator


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


@pytest.mark.asyncio
async def test_analyze_mbti():
    agent = MBTIEvaluator(0, dummy_config())
    # "Alone" -> I, "Analysis" -> T, "Plan" -> J
    result = await agent.analyze("I like being alone and doing analysis. I plan everything.")
    assert "MBTI Analysis" in result
    assert "Estimated Type" in result
    assert "Scores" in result
