import unittest
import sqlite3
import os
import asyncio
from python.helpers.mvl_manager import MVLManager
from python.helpers import files

class TestMVLManager(unittest.TestCase):
    """
    Tests for the MVLManager class, ensuring database operations and
    MVL logic integration work as expected.
    """
    def setUp(self):
        self.db_path = "test_loom.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.manager = MVLManager(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='loom_state'")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_process_message(self):
        async def run_test():
            user_id = "test_user"
            text = "I want to test this feature."
            gate = await self.manager.process_message(user_id, text)
            self.assertIn(gate, ['silence', 'reply', 'refuse', 'delay', 'confront'])

            # Check interaction event
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM interaction_event WHERE user_id = ?", (user_id,))
            event = cursor.fetchone()
            self.assertIsNotNone(event)
            self.assertEqual(event[4], text) # text is 5th column (index 4)
            conn.close()

            # Check state update
            state = self.manager.get_state(user_id)
            self.assertIsNotNone(state)

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
