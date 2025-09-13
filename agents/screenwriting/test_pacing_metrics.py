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


def test_compute_basic():
    agent = PacingMetrics(0, dummy_config())
    metrics = agent.compute("Run! Jump. Stop?")
    assert metrics["sentences"] == 3
    assert metrics["exclamations"] == 1
    assert metrics["avg_sentence_length"] > 0
