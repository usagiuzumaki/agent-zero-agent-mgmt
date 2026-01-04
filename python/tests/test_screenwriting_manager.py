import unittest
import json
import shutil
import os
import tempfile
from python.helpers.screenwriting_manager import ScreenwritingManager

class TestScreenwritingManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.manager = ScreenwritingManager(storage_dir=self.test_dir)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_add_character(self):
        char_data = {"name": "Test Char", "role": "Protagonist"}
        self.assertTrue(self.manager.add_character(char_data))

        profiles = self.manager.load_data('character_profiles')
        self.assertEqual(len(profiles['characters']), 1)
        self.assertEqual(profiles['characters'][0]['name'], "Test Char")
        self.assertTrue('id' in profiles['characters'][0])

    def test_update_character(self):
        # Add first
        char_data = {"name": "Original Name", "role": "Protagonist"}
        self.manager.add_character(char_data)
        profiles = self.manager.load_data('character_profiles')
        char_id = profiles['characters'][0]['id']

        # Update
        update_data = {"id": char_id, "name": "Updated Name", "role": "Antagonist"}
        self.assertTrue(self.manager.update_character(update_data))

        # Verify
        profiles_updated = self.manager.load_data('character_profiles')
        updated_char = profiles_updated['characters'][0]
        self.assertEqual(updated_char['name'], "Updated Name")
        self.assertEqual(updated_char['role'], "Antagonist")
        self.assertEqual(updated_char['id'], char_id)

    def test_delete_character(self):
        # Add first
        char_data = {"name": "To Delete", "role": "Extra"}
        self.manager.add_character(char_data)
        profiles = self.manager.load_data('character_profiles')
        char_id = profiles['characters'][0]['id']

        # Delete
        self.assertTrue(self.manager.delete_character(char_id))

        # Verify
        profiles_after = self.manager.load_data('character_profiles')
        self.assertEqual(len(profiles_after['characters']), 0)

    def test_delete_nonexistent_character(self):
        self.assertFalse(self.manager.delete_character("fake_id"))

    def test_update_nonexistent_character(self):
        update_data = {"id": "fake_id", "name": "Nobody"}
        self.assertFalse(self.manager.update_character(update_data))

if __name__ == '__main__':
    unittest.main()
