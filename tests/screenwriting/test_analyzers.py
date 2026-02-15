import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Define mocks immediately
def mock_module(name):
    m = MagicMock()
    sys.modules[name] = m
    return m

# DO NOT mock nest_asyncio
mock_module("litellm")
mock_module("regex")
mock_module("tiktoken")
mock_module("git")
mock_module("psutil")
mock_module("diskcache")
mock_module("crontab")
mock_module("yaml")
mock_module("pytz")
mock_module("paramiko")
mock_module("dotenv")
mock_module("aiohttp")
mock_module("webcolors")

# Cryptography
mock_module("cryptography")
mock_module("cryptography.hazmat")
mock_module("cryptography.hazmat.primitives")
mock_module("cryptography.hazmat.primitives.asymmetric")

# LangChain mocks
mock_module("langchain")
mock_module("langchain_community")

lc = mock_module("langchain_core")
mock_module("langchain_core.language_models")
mock_module("langchain_core.language_models.chat_models")
mock_module("langchain_core.language_models.llms")
mock_module("langchain_core.messages")
mock_module("langchain_core.prompts")
mock_module("langchain_core.runnables")
mock_module("langchain_core.output_parsers")
mock_module("langchain_core.outputs")
mock_module("langchain_core.outputs.chat_generation")
mock_module("langchain_core.callbacks")
mock_module("langchain_core.callbacks.manager")
mock_module("langchain.embeddings")
mock_module("langchain.embeddings.base")

import pytest
import models
from agents import AgentConfig
# We need to make sure nest_asyncio is not mocked when agents is imported
import agents.agent
from agents.screenwriting.components.emotional_tension import EmotionalTension
from agents.screenwriting.components.subtext_analyzer import SubtextAnalyzer
import asyncio

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
async def test_emotional_tension_analyze():
    with patch("agents.agent.call_extensions", new_callable=AsyncMock):
        agent = EmotionalTension(0, dummy_config())
        with patch.object(agent, 'monologue', new_callable=AsyncMock) as mock_monologue:
            mock_monologue.return_value = "High tension analysis"
            result = await agent.analyze("A scary scene.")
            assert result == "High tension analysis"
            mock_monologue.assert_called_once()

@pytest.mark.asyncio
async def test_subtext_analyzer_analyze():
    with patch("agents.agent.call_extensions", new_callable=AsyncMock):
        agent = SubtextAnalyzer(0, dummy_config())
        with patch.object(agent, 'monologue', new_callable=AsyncMock) as mock_monologue:
            with patch.object(agent, 'read_prompt', return_value="Subtext Whisperer Prompt"):
                mock_monologue.return_value = "Deep subtext analysis"
                result = await agent.analyze("A scene with secrets.")
                assert result == "Deep subtext analysis"
                mock_monologue.assert_called_once()
