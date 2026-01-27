import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Mock dependencies to prevent ImportError when importing ScreenwritingPipeline
sys.modules['langchain'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.language_models'] = MagicMock()
sys.modules['langchain_core.language_models.chat_models'] = MagicMock()
sys.modules['langchain_core.language_models.llms'] = MagicMock()
sys.modules['langchain_core.messages'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.output_parsers'] = MagicMock()
sys.modules['langchain_core.outputs'] = MagicMock()
sys.modules['langchain_core.outputs.chat_generation'] = MagicMock()
sys.modules['langchain_core.callbacks'] = MagicMock()
sys.modules['langchain_core.callbacks.manager'] = MagicMock()
sys.modules['langchain_core.runnables'] = MagicMock()
sys.modules['langchain.embeddings'] = MagicMock()
sys.modules['langchain.embeddings.base'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['langchain_community'] = MagicMock()
sys.modules['langchain_community.chat_models'] = MagicMock()
sys.modules['nest_asyncio'] = MagicMock()
sys.modules['litellm'] = MagicMock()
sys.modules['regex'] = MagicMock()
sys.modules['tiktoken'] = MagicMock()
sys.modules['git'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['diskcache'] = MagicMock()
sys.modules['crontab'] = MagicMock()
sys.modules['yaml'] = MagicMock()
sys.modules['pytz'] = MagicMock()
sys.modules['paramiko'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['aiohttp'] = MagicMock()
sys.modules['webcolors'] = MagicMock()
sys.modules['cryptography'] = MagicMock()
sys.modules['cryptography.hazmat'] = MagicMock()
sys.modules['cryptography.hazmat.primitives'] = MagicMock()
sys.modules['cryptography.hazmat.primitives.asymmetric'] = MagicMock()
sys.modules['cryptography.hazmat.primitives.asymmetric.rsa'] = MagicMock()
sys.modules['cryptography.hazmat.primitives.asymmetric.padding'] = MagicMock()
sys.modules['cryptography.hazmat.primitives.hashes'] = MagicMock()
sys.modules['cryptography.hazmat.primitives.serialization'] = MagicMock()
sys.modules['browser_use'] = MagicMock()
sys.modules['simpleeval'] = MagicMock()
sys.modules['flaredantic'] = MagicMock()
sys.modules['pathspec'] = MagicMock()
sys.modules['flask_login'] = MagicMock()
sys.modules['flask_cors'] = MagicMock()
sys.modules['faiss'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['elevenlabs'] = MagicMock()
sys.modules['diffusers'] = MagicMock()
sys.modules['torch'] = MagicMock()

# Add repo root to path
sys.path.append(os.getcwd())

# Need to mock specific agent modules before importing pipeline if they fail to import
# But let's try importing pipeline first.
# If pipeline imports real agents, and real agents import base agent, and base agent imports...
# We might need to mock agents.screenwriting.* in sys.modules if they have side effects on import.

from python.tools.screenwriting.screenwriting_pipeline import ScreenwritingPipeline
from python.helpers.tool import Response

class TestScreenwritingPipeline(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_agent = MagicMock()
        self.mock_agent.agent_name = "TestAgent"
        self.mock_agent.number = 0
        self.mock_agent.config = MagicMock()
        self.mock_agent.context = MagicMock()

    @patch('python.tools.screenwriting.screenwriting_pipeline.VersionTracker')
    @patch('python.tools.screenwriting.screenwriting_pipeline.ScriptFormatter')
    @patch('python.tools.screenwriting.screenwriting_pipeline.DialogueEvaluator')
    @patch('python.tools.screenwriting.screenwriting_pipeline.CoWriter')
    @patch('python.tools.screenwriting.screenwriting_pipeline.CreativeIdeas')
    @patch('python.tools.screenwriting.screenwriting_pipeline.PlotAnalyzer')
    async def test_execute_with_version_history(self, MockPlot, MockCreative, MockCoWriter, MockDialogue, MockFormatter, MockVersionTracker):
        # Setup mocks
        for MockClass in [MockPlot, MockCreative, MockCoWriter, MockDialogue, MockFormatter, MockVersionTracker]:
            instance = MockClass.return_value
            # All methods are async
            instance.analyze = AsyncMock(return_value="Analysis Result")
            instance.brainstorm = AsyncMock(return_value="Ideas Result")
            instance.draft = AsyncMock(return_value="Draft Result")
            instance.evaluate = AsyncMock(return_value="Evaluation Result")
            instance.format = AsyncMock(return_value="Formatted Script")
            instance.record = AsyncMock(return_value="Version Recorded")

        pipeline = ScreenwritingPipeline(
            agent=self.mock_agent,
            name="screenwriting_pipeline",
            method="execute",
            args={},
            message="msg",
            loop_data={}
        )

        # Execute
        response = await pipeline.execute(
            task="Write a test script",
            project_name="TestProject",
            include_version_history=True
        )

        # Verify VersionTracker was called
        MockVersionTracker.assert_called_once()
        MockVersionTracker.return_value.record.assert_called_once()
        args = MockVersionTracker.return_value.record.call_args[0]
        self.assertIn("TestProject", args[0])

        # Verify response
        self.assertIsInstance(response, Response)
        self.assertIn("Formatted Script", response.message)

if __name__ == '__main__':
    unittest.main()
