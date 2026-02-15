import unittest
import sys
import os
import importlib
from unittest.mock import MagicMock, patch

# Ensure repo root is in path
sys.path.append(os.getcwd())

class TestScreenwritingToolsLoading(unittest.TestCase):
    def setUp(self):
        # Define modules to mock
        self.mock_modules = {
            "nest_asyncio": MagicMock(),
            "litellm": MagicMock(),
            "regex": MagicMock(),
            "tiktoken": MagicMock(),
            "git": MagicMock(),
            "psutil": MagicMock(),
            "diskcache": MagicMock(),
            "crontab": MagicMock(),
            "yaml": MagicMock(),
            "pytz": MagicMock(),
            "paramiko": MagicMock(),
            "dotenv": MagicMock(),
            "aiohttp": MagicMock(),
            "webcolors": MagicMock(),
            "sentence_transformers": MagicMock(),

            # Deep mocking for cryptography
            "cryptography": MagicMock(),
            "cryptography.hazmat": MagicMock(),
            "cryptography.hazmat.primitives": MagicMock(),
            "cryptography.hazmat.primitives.asymmetric": MagicMock(),
            "cryptography.hazmat.primitives.hashes": MagicMock(),
            "cryptography.hazmat.primitives.serialization": MagicMock(),
            "cryptography.hazmat.backends": MagicMock(),

            # Mock langchain and its submodules
            "langchain": MagicMock(),
            "langchain_community": MagicMock(),
            "langchain_core": MagicMock(),
            "langchain_core.language_models": MagicMock(),
            "langchain_core.language_models.chat_models": MagicMock(),
            "langchain_core.language_models.llms": MagicMock(),
            "langchain_core.prompts": MagicMock(),
            "langchain_core.messages": MagicMock(),
            "langchain_core.outputs": MagicMock(),
            "langchain_core.callbacks": MagicMock(),

            # Mock models
            "models": MagicMock(),

            # Mock mcp
            "mcp": MagicMock(),
            "mcp.client": MagicMock(),
            "mcp.client.stdio": MagicMock(),
            "mcp.client.sse": MagicMock(),
            "mcp.client.streamable_http": MagicMock(),
            "mcp.shared": MagicMock(),
            "mcp.shared.message": MagicMock(),
            "mcp.types": MagicMock(),

            # Mock anyio
            "anyio": MagicMock(),
            "anyio.streams": MagicMock(),
            "anyio.streams.memory": MagicMock(),

            # Mock pydantic
            "pydantic": MagicMock(),

            # Stop the chain reaction by mocking python.tools.unknown
            "python.tools": MagicMock(),
            "python.tools.unknown": MagicMock(),
        }

        # Start patching sys.modules
        self.patcher = patch.dict(sys.modules, self.mock_modules)
        self.patcher.start()

        # Clear modules that might have been loaded before with different dependencies
        # or that we want to load fresh with our mocks
        self.modules_to_unload = [
            "agents.agent",
            "agents.screenwriting.tools.screenwriting_pipeline",
            "agents.screenwriting.tools.screenwriting_specialist"
        ]
        for module in self.modules_to_unload:
            if module in sys.modules:
                del sys.modules[module]

        # Import modules under test
        from agents.agent import Agent, AgentConfig, AgentContext
        from agents.screenwriting.tools.screenwriting_pipeline import ScreenwritingPipeline
        from agents.screenwriting.tools.screenwriting_specialist import ScreenwritingSpecialist

        self.Agent = Agent
        self.AgentConfig = AgentConfig
        self.AgentContext = AgentContext
        self.ScreenwritingPipeline = ScreenwritingPipeline
        self.ScreenwritingSpecialist = ScreenwritingSpecialist

        # Setup mocks for Agent
        self.mock_config = MagicMock(spec=AgentConfig)
        self.mock_config.profile = "" # Default profile
        self.mock_config.chat_model = MagicMock()
        self.mock_config.utility_model = MagicMock()
        self.mock_config.embeddings_model = MagicMock()
        self.mock_config.browser_model = MagicMock()

        self.mock_context = MagicMock(spec=AgentContext)
        self.mock_context.log = MagicMock()

    def tearDown(self):
        self.patcher.stop()

        # Unload the modules we tested to avoid pollution
        # Although patch.dict handles restoration, cleaning up modules
        # that were loaded *during* the patch is good practice if we want to ensure
        # they are reloaded cleanly next time.
        # But if patch.dict restores sys.modules, it removes new entries.
        # So we don't strictly need this loop, but let's leave it out to rely on patch.dict.
        pass

    def test_get_tool_screenwriting_pipeline(self):
        # Patch dependencies of Agent.__init__
        with patch('agents.agent.asyncio.run'), \
             patch('agents.agent.Agent.call_extensions'):

            agent = self.Agent(0, self.mock_config, self.mock_context)

            # We need to make sure Unknown is returned if not found, but we mocked it.
            # However, we expect to find the tool, so Unknown shouldn't be used (except imported).

            tool = agent.get_tool(name="screenwriting_pipeline", method=None, args={}, message="", loop_data=None)

            self.assertEqual(tool.__class__.__name__, "ScreenwritingPipeline")

    def test_get_tool_screenwriting_specialist(self):
         with patch('agents.agent.asyncio.run'), \
             patch('agents.agent.Agent.call_extensions'):

            agent = self.Agent(0, self.mock_config, self.mock_context)
            tool = agent.get_tool(name="screenwriting_specialist", method=None, args={}, message="", loop_data=None)

            self.assertEqual(tool.__class__.__name__, "ScreenwritingSpecialist")

    def test_pipeline_has_version_tracker(self):
        import inspect
        sig = inspect.signature(self.ScreenwritingPipeline.execute)
        self.assertIn("include_version_history", sig.parameters)

if __name__ == '__main__':
    unittest.main()
