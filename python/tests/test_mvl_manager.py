import unittest
import sqlite3
import os
import asyncio
import random
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

        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='loom_state'")
        self.assertIsNotNone(cursor.fetchone())

        # Check indexes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_interaction_event_user_ts'")
        self.assertIsNotNone(cursor.fetchone(), "idx_interaction_event_user_ts missing")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_pattern_echo_user'")
        self.assertIsNotNone(cursor.fetchone(), "idx_pattern_echo_user missing")

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
            # text is 5th column (index 4) - verify schema matches
            # id, user_id, ts, role, text
            self.assertEqual(event[4], text)
            conn.close()

            # Check state update
            state = self.manager.get_state(user_id)
            self.assertIsNotNone(state)

        asyncio.run(run_test())

    def test_concurrent_writes(self):
        """
        Simulate concurrent messages to ensure no locking issues.
        """
        async def worker(user_id, i):
            text = f"Message {i} from {user_id}"
            await self.manager.process_message(user_id, text)

        async def run_concurrent_test():
            tasks = []
            # Create 50 concurrent requests across 5 users
            for i in range(50):
                user_id = f"user_{i % 5}"
                tasks.append(worker(user_id, i))

            await asyncio.gather(*tasks)

            # Verify count
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM interaction_event")
            count = cursor.fetchone()[0]
            conn.close()
            self.assertEqual(count, 50)

        asyncio.run(run_concurrent_test())

if __name__ == '__main__':
    unittest.main()
