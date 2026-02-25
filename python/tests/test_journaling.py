import unittest
import os
import shutil
import asyncio
from datetime import datetime
from python.helpers.journal_manager import JournalManager
from python.helpers import files

class MockAgent:
    def __init__(self):
        self.number = 0
        self.context = type('obj', (object,), {'id': 'test_ctx', 'user_id': 'test_user'})

    async def call_utility_model(self, system, message):
        return "This is a mock reflection."

class TestJournaling(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_journal_loom.db"
        self.thoughts_dir = "TestAriasThoughts"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.thoughts_dir):
            shutil.rmtree(self.thoughts_dir)

        self.agent = MockAgent()
        # Patch JournalManager to use test dir and test db
        self.jm = JournalManager(agent=self.agent)
        self.jm.mvl.db_path = files.get_abs_path(self.db_path)
        self.jm.mvl._init_db()
        self.jm.thoughts_dir = files.get_abs_path(self.thoughts_dir)
        os.makedirs(self.jm.thoughts_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.thoughts_dir):
            shutil.rmtree(self.thoughts_dir)

    def test_journal_exists(self):
        date = datetime.now()
        self.assertFalse(self.jm.journal_exists(date))
        self.jm.save_journal("test", date)
        self.assertTrue(self.jm.journal_exists(date))

    def test_should_journal_now(self):
        # We can't easily mock time.now() without freezegun,
        # but we can check the logic.
        now = datetime.now()
        if now.hour >= 20:
            self.assertTrue(self.jm.should_journal_now())
        else:
            self.assertFalse(self.jm.should_journal_now())

    def test_generate_reflection(self):
        async def run_test():
            user_id = "test_user"
            # Insert mock interaction
            conn = self.jm.mvl.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO interaction_event (id, user_id, role, text, meaningfulness, mt_gate)
                VALUES ('test_id', 'test_user', 'user', 'hello', 0.5, 'reply')
            """)
            conn.commit()
            conn.close()

            reflection = await self.jm.generate_daily_reflection(user_id)
            self.assertEqual(reflection, "This is a mock reflection.")
            self.assertTrue(self.jm.journal_exists())

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
