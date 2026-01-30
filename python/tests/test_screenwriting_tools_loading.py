import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Ensure repo root is in path
sys.path.append(os.getcwd())

# Mock dependencies to avoid import errors
sys.modules["nest_asyncio"] = MagicMock()
sys.modules["litellm"] = MagicMock()
sys.modules["regex"] = MagicMock()
sys.modules["tiktoken"] = MagicMock()
sys.modules["git"] = MagicMock()
sys.modules["psutil"] = MagicMock()
sys.modules["diskcache"] = MagicMock()
sys.modules["crontab"] = MagicMock()
sys.modules["yaml"] = MagicMock()
sys.modules["pytz"] = MagicMock()
sys.modules["paramiko"] = MagicMock()
sys.modules["dotenv"] = MagicMock()
sys.modules["aiohttp"] = MagicMock()
sys.modules["webcolors"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()

# Deep mocking for cryptography
sys.modules["cryptography"] = MagicMock()
sys.modules["cryptography.hazmat"] = MagicMock()
sys.modules["cryptography.hazmat.primitives"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.asymmetric"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.hashes"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.serialization"] = MagicMock()
sys.modules["cryptography.hazmat.backends"] = MagicMock()

# Mock langchain and its submodules
sys.modules["langchain"] = MagicMock()
sys.modules["langchain_community"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.language_models"] = MagicMock()
sys.modules["langchain_core.language_models.chat_models"] = MagicMock()
sys.modules["langchain_core.language_models.llms"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_core.outputs"] = MagicMock()
sys.modules["langchain_core.callbacks"] = MagicMock()

# Mock models
sys.modules["models"] = MagicMock()

# Mock mcp
sys.modules["mcp"] = MagicMock()
sys.modules["mcp.client"] = MagicMock()
sys.modules["mcp.client.stdio"] = MagicMock()
sys.modules["mcp.client.sse"] = MagicMock()
sys.modules["mcp.client.streamable_http"] = MagicMock()
sys.modules["mcp.shared"] = MagicMock()
sys.modules["mcp.shared.message"] = MagicMock()
sys.modules["mcp.types"] = MagicMock()

# Mock anyio
sys.modules["anyio"] = MagicMock()
sys.modules["anyio.streams"] = MagicMock()
sys.modules["anyio.streams.memory"] = MagicMock()

# Mock pydantic
sys.modules["pydantic"] = MagicMock()

# Stop the chain reaction by mocking python.tools.unknown
sys.modules["python.tools"] = MagicMock()
sys.modules["python.tools.unknown"] = MagicMock()

# Now import modules under test
from agents.agent import Agent, AgentConfig, AgentContext
from agents.screenwriting.tools.screenwriting_pipeline import ScreenwritingPipeline
from agents.screenwriting.tools.screenwriting_specialist import ScreenwritingSpecialist

class TestScreenwritingToolsLoading(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock(spec=AgentConfig)
        self.mock_config.profile = "" # Default profile
        self.mock_config.chat_model = MagicMock()
        self.mock_config.utility_model = MagicMock()
        self.mock_config.embeddings_model = MagicMock()
        self.mock_config.browser_model = MagicMock()

        self.mock_context = MagicMock(spec=AgentContext)
        self.mock_context.log = MagicMock()

    def test_get_tool_screenwriting_pipeline(self):
        # Patch dependencies of Agent.__init__
        with patch('agents.agent.asyncio.run'), \
             patch('agents.agent.Agent.call_extensions'):

            agent = Agent(0, self.mock_config, self.mock_context)

            # We need to make sure Unknown is returned if not found, but we mocked it.
            # However, we expect to find the tool, so Unknown shouldn't be used (except imported).

            tool = agent.get_tool(name="screenwriting_pipeline", method=None, args={}, message="", loop_data=None)

            self.assertEqual(tool.__class__.__name__, "ScreenwritingPipeline")

    def test_get_tool_screenwriting_specialist(self):
         with patch('agents.agent.asyncio.run'), \
             patch('agents.agent.Agent.call_extensions'):

            agent = Agent(0, self.mock_config, self.mock_context)
            tool = agent.get_tool(name="screenwriting_specialist", method=None, args={}, message="", loop_data=None)

            self.assertEqual(tool.__class__.__name__, "ScreenwritingSpecialist")

    def test_pipeline_has_version_tracker(self):
        import inspect
        sig = inspect.signature(ScreenwritingPipeline.execute)
        self.assertIn("include_version_history", sig.parameters)

if __name__ == '__main__':
    unittest.main()
