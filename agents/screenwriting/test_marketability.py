import pytest
from unittest.mock import AsyncMock, MagicMock
import models
from agents import AgentConfig
from .marketability import Marketability

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
async def test_analyze_marketability():
    # Setup
    config = dummy_config()
    agent = Marketability(0, config)

    # Mock monologue to avoid LLM call
    expected_output = "## Marketability Analysis\nHigh commercial potential."
    agent.monologue = AsyncMock(return_value=expected_output)

    # Execute
    synopsis = "A hero saves the world."
    result = await agent.analyze(synopsis)

    # Verify
    assert result == expected_output
    agent.monologue.assert_called_once()

    # Check if user message was added
    # (Accessing internal history might depend on implementation,
    # but we can trust the call happened if monologue was called after correct setup)

@pytest.mark.asyncio
async def test_assess_alias():
    # Setup
    config = dummy_config()
    agent = Marketability(0, config)
    agent.analyze = AsyncMock(return_value="Analysis Result")

    # Execute
    result = await agent.assess("text")

    # Verify
    assert result == "Analysis Result"
    agent.analyze.assert_called_with("text")
