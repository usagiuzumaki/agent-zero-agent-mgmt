import unittest
import sqlite3
import os
from python.helpers.mvl_manager import MVLManager

class TestMigration(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_migration.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        # Create OLD schema manually (without pattern_echo and pattern_ids)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create loom_state so _init_db thinks DB exists
        cursor.execute('''
        CREATE TABLE loom_state (
            user_id TEXT PRIMARY KEY,
            entropy REAL,
            dormancy BOOLEAN,
            last_active_ts DATETIME,
            silence_streak INTEGER,
            dependency_risk REAL,
            mask_weights TEXT,
            last_archetype_state_id TEXT
        )
        ''')

        # OLD interaction_event (no pattern_ids)
        cursor.execute('''
        CREATE TABLE interaction_event (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT,
            text TEXT,
            tokens INTEGER,
            channel TEXT,
            intent_tag TEXT,
            utility_flag BOOLEAN,
            novelty REAL,
            narrative_weight REAL,
            entropy_delta REAL,
            meaningfulness REAL,
            mt_gate TEXT,
            embedding_id TEXT
        )
        ''')

        # Missing pattern_echo table

        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_migration_adds_missing_elements(self):
        # Initialize MVLManager, which should trigger migration
        manager = MVLManager(db_path=self.db_path)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if pattern_echo exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pattern_echo'")
        self.assertIsNotNone(cursor.fetchone(), "pattern_echo table should have been created")

        # Check if interaction_event has pattern_ids
        cursor.execute("PRAGMA table_info(interaction_event)")
        columns = [info[1] for info in cursor.fetchall()]
        self.assertIn("pattern_ids", columns, "pattern_ids column should have been added")

        conn.close()

if __name__ == '__main__':
    unittest.main()
