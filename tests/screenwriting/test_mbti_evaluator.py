import sys
from unittest.mock import MagicMock

# Define mocks immediately
def mock_module(name):
    m = MagicMock()
    sys.modules[name] = m
    return m

mock_module("nest_asyncio")
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
from agents.screenwriting.components.mbti_evaluator import MBTIEvaluator
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

def test_analyze_mbti():
    agent = MBTIEvaluator(0, dummy_config())
    # "Alone" -> I, "Analysis" -> T, "Plan" -> J
    result = asyncio.run(agent.analyze("I like being alone and doing analysis. I plan everything."))
    assert "MBTI Evaluation" in result
    assert "Type: ISTJ" in result
