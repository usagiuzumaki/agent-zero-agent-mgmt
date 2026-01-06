
import unittest
import shutil
import os
import json
from datetime import datetime
from python.helpers.screenwriting_manager import ScreenwritingManager

class TestScreenwritingManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_screenwriting_data"
        self.manager = ScreenwritingManager(storage_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_character(self):
        char_data = {"name": "Test Char", "role": "Protagonist"}
        self.assertTrue(self.manager.add_character(char_data))

        profiles = self.manager.load_data('character_profiles')
        self.assertEqual(len(profiles['characters']), 1)
        self.assertEqual(profiles['characters'][0]['name'], "Test Char")
        self.assertTrue('id' in profiles['characters'][0])

    def test_update_character(self):
        # Add initial character
        char_data = {"name": "Original Name", "role": "Protagonist"}
        self.manager.add_character(char_data)

        profiles = self.manager.load_data('character_profiles')
        char_id = profiles['characters'][0]['id']
        created_at = profiles['characters'][0]['created']

        # Update character
        update_data = {"name": "Updated Name", "role": "Antagonist"}
        self.assertTrue(self.manager.update_character(char_id, update_data))

        # Verify update
        profiles = self.manager.load_data('character_profiles')
        updated_char = profiles['characters'][0]
        self.assertEqual(updated_char['name'], "Updated Name")
        self.assertEqual(updated_char['role'], "Antagonist")
        self.assertEqual(updated_char['id'], char_id)
        self.assertEqual(updated_char['created'], created_at)
        self.assertTrue('last_updated' in updated_char)

    def test_delete_character(self):
        # Add two characters
        self.manager.add_character({"name": "Char 1"})
        self.manager.add_character({"name": "Char 2"})

        profiles = self.manager.load_data('character_profiles')
        self.assertEqual(len(profiles['characters']), 2)
        char1_id = profiles['characters'][0]['id']

        # Delete first character
        self.assertTrue(self.manager.delete_character(char1_id))

        # Verify deletion
        profiles = self.manager.load_data('character_profiles')
        self.assertEqual(len(profiles['characters']), 1)
        self.assertEqual(profiles['characters'][0]['name'], "Char 2")

    def test_update_nonexistent_character(self):
        self.assertFalse(self.manager.update_character("fake_id", {}))

    def test_delete_nonexistent_character(self):
        self.assertFalse(self.manager.delete_character("fake_id"))

if __name__ == '__main__':
    unittest.main()
