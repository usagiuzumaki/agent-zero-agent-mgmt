import unittest
import sqlite3
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock
from python.helpers.mvl_manager import MVLManager
import json

class TestPatternEcho(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_pattern_loom.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        # Mock Agent
        self.mock_agent = MagicMock()
        self.mock_agent.call_utility_model = AsyncMock()

        self.manager = MVLManager(db_path=self.db_path, agent=self.mock_agent)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_detect_pattern_found(self):
        # Setup mock response
        mock_response = json.dumps({
            "pattern_found": True,
            "type": "loop",
            "summary": "User keeps repeating the same question.",
            "strength": 0.8,
            "evidence_quotes": ["Why?", "Why not?"]
        })
        self.mock_agent.call_utility_model.return_value = mock_response

        async def run_test():
            user_id = "test_user_1"
            text = "Why is this happening?"

            # Run process_message
            await self.manager.process_message(user_id, text)

            # Check if LLM was called
            self.mock_agent.call_utility_model.assert_called_once()

            # Check pattern_echo table
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pattern_echo WHERE user_id = ?", (user_id,))
            pattern = cursor.fetchone()
            self.assertIsNotNone(pattern)
            self.assertEqual(pattern[2], "loop") # type
            self.assertEqual(pattern[3], "User keeps repeating the same question.") # summary

            # Check interaction_event table
            cursor.execute("SELECT pattern_ids FROM interaction_event WHERE user_id = ?", (user_id,))
            event = cursor.fetchone()
            self.assertIsNotNone(event)
            self.assertIn(pattern[0], event[0]) # pattern_id in pattern_ids

            conn.close()

        asyncio.run(run_test())

    def test_detect_pattern_not_found(self):
        # Setup mock response
        mock_response = json.dumps({
            "pattern_found": False
        })
        self.mock_agent.call_utility_model.return_value = mock_response

        async def run_test():
            user_id = "test_user_2"
            text = "Hello there."

            # Run process_message
            await self.manager.process_message(user_id, text)

            # Check pattern_echo table (should be empty)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pattern_echo WHERE user_id = ?", (user_id,))
            pattern = cursor.fetchone()
            self.assertIsNone(pattern)

            conn.close()

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
