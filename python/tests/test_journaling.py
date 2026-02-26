import pytest
import os
import shutil
from datetime import datetime
from python.helpers.journal_manager import JournalManager
from unittest.mock import MagicMock

def test_journal_manager_basic():
    test_dir = "test_thoughts"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    jm = JournalManager(thoughts_dir=test_dir)
    jm.save_thought("Test reflection", user_id="user123")

    thoughts = jm.get_todays_thoughts()
    assert "Test reflection" in thoughts
    assert "user123" in thoughts

    shutil.rmtree(test_dir)

def test_comfort_level_gating():
    mvl_mock = MagicMock()
    # Mocking the context manager _get_db
    conn_mock = mvl_mock._get_db.return_value.__enter__.return_value
    cursor_mock = conn_mock.cursor.return_value

    # Low comfort
    cursor_mock.fetchone.return_value = [0.5]
    jm = JournalManager(thoughts_dir="test_thoughts_2")
    assert jm.can_share_thoughts(mvl_mock, "user1") == False

    # High comfort
    cursor_mock.fetchone.return_value = [0.8]
    assert jm.can_share_thoughts(mvl_mock, "user1") == True

    if os.path.exists("test_thoughts_2"):
        shutil.rmtree("test_thoughts_2")
