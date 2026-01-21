import pytest
import models
from agents import AgentConfig
from .pacing_metrics import PacingMetrics


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
async def test_analyze_basic():
    agent = PacingMetrics(0, dummy_config())
    metrics_str = await agent.analyze("Run! Jump. Stop?")
    assert "sentences" in metrics_str
    assert "3" in metrics_str
    assert "exclamations" in metrics_str
    assert "1" in metrics_str
