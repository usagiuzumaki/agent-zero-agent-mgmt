import unittest
from unittest.mock import MagicMock, patch
import asyncio
import sys
import os

# Mock complex dependencies
sys.modules['python.helpers.mcp_handler'] = MagicMock()
sys.modules['nest_asyncio'] = MagicMock()

# Import the necessary parts
from agents.agent import Agent, AgentConfig

class TestAgentBudget(unittest.TestCase):
    def setUp(self):
        # Manually create a minimal config
        model_mock = MagicMock()
        self.config = AgentConfig(
            chat_model=model_mock,
            utility_model=model_mock,
            embeddings_model=model_mock,
            browser_model=model_mock,
            mcp_servers="",
            profile="researcher"
        )
        self.agent = Agent(number=1, config=self.config)

    def test_tool_budget_enforcement(self):
        self.agent.tool_call_count = 15
        # 16th call should trigger budget exceeded
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.agent.process_tools('{"tool_name": "search", "tool_args": {}}'))
        self.assertIn("Budget exceeded", result)

if __name__ == "__main__":
    unittest.main()
