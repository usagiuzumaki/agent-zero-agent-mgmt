
import sys
import os
import unittest
import inspect
from unittest.mock import MagicMock, patch

# Add repo root to path
sys.path.append(os.getcwd())

# Mock dependencies to allow importing Agent
modules_to_mock = [
    'nest_asyncio', 'litellm', 'regex', 'tiktoken', 'git', 'psutil', 'diskcache',
    'crontab', 'yaml', 'pytz', 'paramiko', 'dotenv', 'aiohttp', 'webcolors',
    'sentence_transformers', 'anyio', 'anyio.streams', 'anyio.streams.memory', 'pydantic',
    'cryptography', 'cryptography.hazmat', 'cryptography.hazmat.primitives', 'cryptography.hazmat.primitives.asymmetric',
    'cryptography.hazmat.primitives.asymmetric.padding', 'langchain', 'langchain.community',
    'langchain.core', 'langchain_core', 'langchain_core.prompts', 'langchain_core.messages', 'langchain_core.language_models',
    'langchain_core.language_models.chat_models', 'langchain_core.language_models.llms', 'langchain_core.language_models.base',
    'langchain_core.outputs', 'langchain_core.outputs.chat_generation',
    'langchain_core.callbacks', 'langchain_core.callbacks.manager', 'langchain.embeddings', 'langchain.embeddings.base',
    'mcp', 'mcp.client', 'mcp.shared', 'mcp.shared.message', 'mcp.client.session', 'mcp.types',
    'mcp.client.stdio', 'mcp.client.sse', 'mcp.client.streamable_http', 'elevenlabs', 'elevenlabs.client', 'openai',
    'python.helpers.mcp_handler'
]

for module in modules_to_mock:
    if module not in sys.modules:
        sys.modules[module] = MagicMock()

# Setup explicit mocks for things imported with 'from ... import ...'
sys.modules['langchain_core.prompts'].ChatPromptTemplate = MagicMock()
sys.modules['langchain_core.messages'].HumanMessage = MagicMock()
sys.modules['langchain_core.messages'].SystemMessage = MagicMock()
sys.modules['langchain_core.messages'].BaseMessage = MagicMock()

# Now import Agent
# We need to ensure we can import agents.agent without crashing
try:
    from agents.agent import Agent, AgentConfig, LoopData
    from python.helpers.tool import Tool
except ImportError as e:
    print(f"Failed to import Agent: {e}")
    sys.exit(1)

class TestScreenwritingToolsLoading(unittest.TestCase):
    def setUp(self):
        self.config = MagicMock(spec=AgentConfig)
        self.config.profile = "" # Default profile

        # Mock the agent instance
        self.agent = MagicMock(spec=Agent)
        self.agent.config = self.config

        # Bind the real get_tool method to our mock agent
        self.agent.get_tool = Agent.get_tool.__get__(self.agent, Agent)

    def test_get_tool_screenwriting_pipeline(self):
        """Test that get_tool can find ScreenwritingPipeline in the new location."""
        tool_name = "screenwriting_pipeline"

        # Attempt to load the tool
        tool = self.agent.get_tool(
            name=tool_name,
            method=None,
            args={},
            message="test",
            loop_data=None
        )

        # Verifications
        self.assertIsNotNone(tool, "Tool should not be None")
        self.assertEqual(tool.name, "screenwriting_pipeline", "Tool name mismatch")
        self.assertEqual(tool.__class__.__name__, "ScreenwritingPipeline", "Tool class mismatch")

        # Verify that it is indeed an instance of the class defined in the new location
        # Since the old directory is deleted, if it loads, it must be from the new location
        self.assertEqual(tool.__class__.__name__, "ScreenwritingPipeline")

    def test_get_tool_screenwriting_specialist(self):
        """Test that get_tool can find ScreenwritingSpecialist in the new location."""
        tool_name = "screenwriting_specialist"

        tool = self.agent.get_tool(
            name=tool_name,
            method=None,
            args={},
            message="test",
            loop_data=None
        )

        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "screenwriting_specialist")
        self.assertEqual(tool.__class__.__name__, "ScreenwritingSpecialist")

    def test_get_tool_script_analyzer(self):
        """Test that get_tool can find ScriptAnalyzer in the new location."""
        tool_name = "script_analyzer"

        tool = self.agent.get_tool(
            name=tool_name,
            method=None,
            args={},
            message="test",
            loop_data=None
        )

        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "script_analyzer")
        self.assertEqual(tool.__class__.__name__, "ScriptAnalyzer")

if __name__ == '__main__':
    unittest.main()
