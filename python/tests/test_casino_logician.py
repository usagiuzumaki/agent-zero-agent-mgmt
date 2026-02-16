import unittest
import asyncio
import os
import sys

# Ensure repo root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import AgentConfig, AgentContext, LoopData
from agents.poker import PokerAgent
import models

class TestCasinoLogician(unittest.TestCase):
    def setUp(self):
        # Set dummy API key for models initialization
        os.environ["OPENAI_API_KEY"] = "dummy"

    def test_casino_logician_injection(self):
        # Setup configuration
        chat_conf = models.ModelConfig(type=models.ModelType.CHAT, provider="openai", name="gpt-4o")
        embed_conf = models.ModelConfig(type=models.ModelType.EMBEDDING, provider="openai", name="text-embedding-3-small")
        config = AgentConfig(
            chat_model=chat_conf,
            utility_model=chat_conf,
            embeddings_model=embed_conf,
            browser_model=chat_conf,
            mcp_servers="",
            profile="poker"
        )

        agent = PokerAgent(1, config)
        loop_data = LoopData()
        agent.loop_data = loop_data

        # Build prompt
        prompt = asyncio.run(agent.prepare_prompt(loop_data))
        system_content = prompt[0].content

        self.assertIn("THE CASINO LOGICIAN", system_content)
        self.assertIn("Theatre of the Gamble", system_content)

    def test_casino_analysis_tool_resolution(self):
        chat_conf = models.ModelConfig(type=models.ModelType.CHAT, provider="openai", name="gpt-4o")
        embed_conf = models.ModelConfig(type=models.ModelType.EMBEDDING, provider="openai", name="text-embedding-3-small")
        config = AgentConfig(
            chat_model=chat_conf,
            utility_model=chat_conf,
            embeddings_model=embed_conf,
            browser_model=chat_conf,
            mcp_servers="",
            profile="poker"
        )
        agent = PokerAgent(1, config)
        loop_data = LoopData()

        tool = agent.get_tool("casino_analysis", None, {}, "", loop_data)
        self.assertEqual(tool.__class__.__name__, "CasinoAnalysis")

if __name__ == "__main__":
    unittest.main()
