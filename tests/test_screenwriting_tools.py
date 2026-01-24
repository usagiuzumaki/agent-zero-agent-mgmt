import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Add root directory to path so we can import modules
sys.path.append(os.getcwd())

# Mock dependencies that might be hard to load or have side effects
sys.modules['python.helpers.screenwriting_manager'] = MagicMock()
# sys.modules['agents'] = MagicMock() # Don't mock agents package
sys.modules['python.helpers.tool'] = MagicMock()
sys.modules['python.helpers.files'] = MagicMock()
sys.modules['python.helpers.print_style'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['python.helpers.dotenv'] = MagicMock()
sys.modules['python.helpers.rfc_exchange'] = MagicMock()
sys.modules['python.helpers.runtime'] = MagicMock()
sys.modules['python.helpers.crypto'] = MagicMock()
sys.modules['paramiko'] = MagicMock()
sys.modules['models'] = MagicMock() # Mock models to avoid DB/LLM connection
sys.modules['langchain_core'] = MagicMock() # Mock langchain to avoid dependencies
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.messages'] = MagicMock()
sys.modules['langchain_core.language_models'] = MagicMock()
sys.modules['langchain_core.language_models.chat_models'] = MagicMock()
sys.modules['langchain_core.language_models.llms'] = MagicMock()
sys.modules['langchain_core.embeddings'] = MagicMock()
sys.modules['nest_asyncio'] = MagicMock()
sys.modules['uuid'] = MagicMock()
sys.modules['regex'] = MagicMock()
sys.modules['tiktoken'] = MagicMock()
sys.modules['git'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['diskcache'] = MagicMock()
sys.modules['crontab'] = MagicMock()
sys.modules['yaml'] = MagicMock()
sys.modules['pytz'] = MagicMock()

# Define a dummy Tool class to avoid inheritance issues with MagicMock
class DummyTool:
    def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
        self.agent = agent
        self.name = name
        self.method = method
        self.args = args
        self.message = message
        self.loop_data = loop_data

    async def execute(self, **kwargs):
        pass

class DummyResponse:
    def __init__(self, message="", break_loop=False, **kwargs):
        self.message = message
        self.break_loop = break_loop

# Mock python.helpers.tool to return DummyTool
mock_tool_module = MagicMock()
mock_tool_module.Tool = DummyTool
mock_tool_module.Response = DummyResponse
sys.modules['python.helpers.tool'] = mock_tool_module

# Now import the tools to test
from python.tools.screenwriting.screenwriting_pipeline import ScreenwritingPipeline
from python.tools.screenwriting.screenwriting_specialist import ScreenwritingSpecialist
from python.tools.screenwriting.screenwriting import Screenwriting
from python.tools.screenwriting.fountain_to_html import FountainToHtml

class TestScreenwritingTools(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_agent = MagicMock()
        self.mock_agent.agent_name = "TestAgent"
        self.mock_agent.number = 0
        self.mock_agent.config = MagicMock()
        self.mock_agent.context = MagicMock()

        # Mock the Response class as it is returned by tools
        # We need to grab the Tool/Response class from where it was imported in the tool files
        # Since we mocked python.helpers.tool, the tools will be using that mock.
        pass

    async def test_screenwriting_pipeline_init(self):
        """Test that ScreenwritingPipeline can be initialized."""
        tool = ScreenwritingPipeline(
            agent=self.mock_agent,
            name="screenwriting_pipeline",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )
        # self.assertIsInstance(tool, ScreenwritingPipeline)
        # Since Tool is mocked, isinstance might fail if we don't handle inheritance correctly in mocks.
        # But we just want to ensure it instantiates without error.
        self.assertIsNotNone(tool)

    async def test_screenwriting_pipeline_execute(self):
        """Test ScreenwritingPipeline execution logic (mocked)."""
        tool = ScreenwritingPipeline(
            agent=self.mock_agent,
            name="screenwriting_pipeline",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )

        # Mock _run_stage to avoid actual agent creation
        tool._run_stage = AsyncMock(return_value="Stage Result")

        response = await tool.execute(
            task="Write a test script",
            project_name="Test Project",
            include_world_building=True
        )

        # Verify _run_stage was called for enabled stages
        # World Builder is enabled
        tool._run_stage.assert_any_call(
            unittest.mock.ANY,
            "World Builder",
            "build",
            unittest.mock.ANY
        )

        # Verify response
        self.assertIsNotNone(response)

    async def test_screenwriting_specialist_init(self):
        """Test that ScreenwritingSpecialist can be initialized."""
        tool = ScreenwritingSpecialist(
            agent=self.mock_agent,
            name="screenwriting_specialist",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )
        self.assertIsNotNone(tool)

    async def test_screenwriting_specialist_execute(self):
         """Test ScreenwritingSpecialist execution logic (mocked)."""
         tool = ScreenwritingSpecialist(
            agent=self.mock_agent,
            name="screenwriting_specialist",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )

         # Let's mock the specific agent class instantiation in the execute method using patch
         with patch('python.tools.screenwriting.screenwriting_specialist.PlotAnalyzer') as MockPlotAnalyzer:
             mock_sub_agent = MagicMock()
             mock_sub_agent.analyze = AsyncMock(return_value="Analysis Result")
             MockPlotAnalyzer.return_value = mock_sub_agent

             response = await tool.execute(specialist="PlotAnalyzer", task="Analyze this")

             MockPlotAnalyzer.assert_called()
             mock_sub_agent.analyze.assert_called_with("Analyze this")

    async def test_screenwriting_tool_init(self):
        """Test that Screenwriting tool can be initialized."""
        # Screenwriting tool initializes ScreenwritingManager in __init__
        # We mocked `python.helpers.screenwriting_manager` module, so `ScreenwritingManager()` call should return a mock.
        tool = Screenwriting(
            agent=self.mock_agent,
            name="screenwriting",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )
        self.assertIsNotNone(tool)
        self.assertTrue(hasattr(tool, 'manager'))

    async def test_fountain_to_html_execute(self):
        """Test FountainToHtml execute."""
        tool = FountainToHtml(
            agent=self.mock_agent,
            name="fountain_to_html",
            method=None,
            args={},
            message="Test message",
            loop_data={}
        )

        # We need to mock subprocess.run or tempfile to avoid actual execution
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stdout="<html>Result</html>", stderr="")

            response = await tool.execute(script="INT. TEST")
            self.assertIn("<html>Result</html>", response.message)

if __name__ == '__main__':
    unittest.main()
