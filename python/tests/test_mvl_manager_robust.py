import unittest
import asyncio
import os
import sys
import sqlite3
import json
from unittest.mock import MagicMock, AsyncMock, patch

from python.helpers.mvl_manager import MVLManager

class MockAgent:
    def __init__(self):
        self.context = MagicMock()
        self.context.id = "test_user"
        self.call_utility_model = AsyncMock()

class TestMVLManagerRobust(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_loom_robust.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.agent = MockAgent()
        self.manager = MVLManager(db_path=self.db_path, agent=self.agent)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db_schema(self):
        """Test that the database is initialized with correct tables and columns."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check interaction_event table
        cursor.execute("PRAGMA table_info(interaction_event)")
        columns = [info[1] for info in cursor.fetchall()]
        self.assertIn("pattern_ids", columns)
        self.assertIn("embedding_id", columns)
        self.assertIn("mt_gate", columns)

        # Check pattern_echo table
        cursor.execute("PRAGMA table_info(pattern_echo)")
        columns = [info[1] for info in cursor.fetchall()]
        self.assertIn("type", columns)
        self.assertIn("status", columns)

        conn.close()

    def test_detect_pattern_valid_json(self):
        """Test detect_pattern with a valid JSON response from the agent."""
        valid_json = json.dumps({
            "mask": "The Tester",
            "claims": [],
            "signals": {},
            "pattern_candidates": [{"type": "trigger", "summary": "Test trigger", "lore_weight": 0.8}],
            "recommend_mt_gate": "reply"
        })
        self.agent.call_utility_model.return_value = valid_json

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis, new_ids = loop.run_until_complete(self.manager.detect_pattern("test_user", "Hello"))

        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["mask"], "The Tester")
        self.assertEqual(len(new_ids), 1)

        # Verify it was saved to DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT type FROM pattern_echo WHERE id=?", (new_ids[0],))
        row = cursor.fetchone()
        self.assertEqual(row[0], "trigger")
        conn.close()

    def test_detect_pattern_invalid_json(self):
        """Test detect_pattern with a non-JSON response."""
        self.agent.call_utility_model.return_value = "This is not JSON."

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Patch PrintStyle to avoid cluttering output
        with patch('python.helpers.mvl_manager.PrintStyle') as mock_print:
            analysis, new_ids = loop.run_until_complete(self.manager.detect_pattern("test_user", "Hello"))

        self.assertIsNone(analysis)
        self.assertEqual(new_ids, [])

    def test_detect_pattern_agent_exception(self):
        """Test detect_pattern when agent raises an exception."""
        self.agent.call_utility_model.side_effect = Exception("Agent error")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with patch('python.helpers.mvl_manager.PrintStyle') as mock_print:
            analysis, new_ids = loop.run_until_complete(self.manager.detect_pattern("test_user", "Hello"))

        self.assertIsNone(analysis)
        self.assertEqual(new_ids, [])

    def test_detect_pattern_no_agent(self):
        """Test detect_pattern with no agent attached."""
        manager_no_agent = MVLManager(db_path="test_loom_no_agent.db")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with patch('python.helpers.mvl_manager.PrintStyle') as mock_print:
            analysis, new_ids = loop.run_until_complete(manager_no_agent.detect_pattern("test_user", "Hello"))

        self.assertIsNone(analysis)
        self.assertEqual(new_ids, [])

        if os.path.exists("test_loom_no_agent.db"):
            os.remove("test_loom_no_agent.db")

    def test_process_message_integration(self):
        """Test the full process_message flow."""
        valid_json = json.dumps({
            "mask": "The Tester",
            "claims": [],
            "signals": {},
            "pattern_candidates": [],
            "recommend_mt_gate": "reply"
        })
        self.agent.call_utility_model.return_value = valid_json

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        gate = loop.run_until_complete(self.manager.process_message("test_user", "Hello world"))

        self.assertIn(gate, ["silence", "reply", "refuse", "delay", "confront"])

        # Verify interaction event saved
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT text, mt_gate FROM interaction_event WHERE user_id=?", ("test_user",))
        row = cursor.fetchone()
        self.assertEqual(row[0], "Hello world")
        self.assertEqual(row[1], gate)
        conn.close()

if __name__ == "__main__":
    unittest.main()
