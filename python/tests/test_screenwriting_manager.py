
import unittest
import shutil
import os
import sys
import json
from datetime import datetime
from unittest.mock import MagicMock

# Mock dependencies to avoid importing the heavy Agent stack
sys.modules["nest_asyncio"] = MagicMock()
sys.modules["models"] = MagicMock()
sys.modules["litellm"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.language_models"] = MagicMock()
sys.modules["langchain_core.language_models.chat_models"] = MagicMock()
sys.modules["langchain_core.language_models.llms"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["cryptography"] = MagicMock()
sys.modules["cryptography.hazmat"] = MagicMock()
sys.modules["cryptography.hazmat.primitives"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.asymmetric"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.hashes"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.serialization"] = MagicMock()
sys.modules["aiohttp"] = MagicMock()
sys.modules["paramiko"] = MagicMock()
sys.modules["git"] = MagicMock()
sys.modules["psutil"] = MagicMock()
sys.modules["diskcache"] = MagicMock()
sys.modules["crontab"] = MagicMock()
sys.modules["webcolors"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["faiss"] = MagicMock()
sys.modules["numpy"] = MagicMock()

# Now import the manager
from agents.screenwriting.manager import ScreenwritingManager

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

    def test_add_quote(self):
        quote = "I'll be back."
        character = "Terminator"
        self.assertTrue(self.manager.add_quote(quote, character=character, category="Action"))

        quotes_data = self.manager.load_data('sick_quotes')
        self.assertEqual(len(quotes_data['quotes']), 1)
        self.assertEqual(quotes_data['quotes'][0]['quote'], quote)
        self.assertEqual(quotes_data['categories'], ["Action"])

    def test_search_quotes(self):
        self.manager.add_quote("I'll be back.", character="Terminator")
        self.manager.add_quote("Hasta la vista, baby.", character="Terminator")
        self.manager.add_quote("May the Force be with you.", character="Yoda")

        results = self.manager.search_quotes("back")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['quote'], "I'll be back.")

        results = self.manager.search_quotes("Terminator")
        self.assertEqual(len(results), 2)

    def test_add_scene(self):
        scene_data = {"title": "Opening Scene", "description": "Fade in..."}
        self.assertTrue(self.manager.add_scene(scene_data))

        outline = self.manager.load_data('book_outline')
        self.assertEqual(len(outline['scenes']), 1)
        self.assertEqual(outline['scenes'][0]['title'], "Opening Scene")
        self.assertTrue('id' in outline['scenes'][0])

    def test_add_sketch(self):
        sketch_data = {"title": "Hero Design", "type": "sketch"}
        self.assertTrue(self.manager.add_sketch(sketch_data))

        imagery = self.manager.load_data('sketches_imagery')
        self.assertEqual(len(imagery['sketches']), 1)

        mood_board_data = {"title": "Dark Mood", "type": "mood_board"}
        self.assertTrue(self.manager.add_sketch(mood_board_data))

        imagery = self.manager.load_data('sketches_imagery')
        self.assertEqual(len(imagery['mood_boards']), 1)

    def test_create_project(self):
        project_name = "New Sci-Fi"
        self.assertTrue(self.manager.create_project(project_name, "Sci-Fi", "In a world..."))

        projects = self.manager.load_data('projects')
        self.assertEqual(len(projects['projects']), 1)
        self.assertEqual(projects['active_project'], projects['projects'][0]['id'])

        # Verify it resets other data (since create_project initializes new empty structures)
        # Assuming load_data reads from the file system which create_project has just overwritten
        outline = self.manager.load_data('book_outline')
        self.assertEqual(len(outline['scenes']), 0)

    def test_ingest_story_document(self):
        content = "Chapter One\n\nIt was a dark and stormy night. Suddenly, a shot rang out.\n\nChapter Two\n\nThe detective arrived."
        doc = self.manager.ingest_story_document("My Novel", content)

        self.assertIsNotNone(doc)
        self.assertEqual(doc['name'], "My Novel")
        # Depending on how regex split works, check expectations.
        # "Chapter One\n\n..." should split into roughly 2 chunks if \n\n is the separator.
        self.assertTrue(len(doc['chapters']) >= 1)

        storybook = self.manager.load_data('storybook')
        self.assertEqual(len(storybook['documents']), 1)
        self.assertEqual(storybook['documents'][0]['id'], doc['id'])

    def test_delete_document(self):
        doc = self.manager.ingest_story_document("Doc to Delete", "Some content")
        doc_id = doc['id']

        self.assertTrue(self.manager.delete_document(doc_id))

        storybook = self.manager.load_data('storybook')
        self.assertEqual(len(storybook['documents']), 0)

    def test_ingest_story_document_edge_cases(self):
        # Empty content should return None
        self.assertIsNone(self.manager.ingest_story_document("Empty", ""))

        # Whitespace only content should return None (after we fix it)
        # Currently it might return a document with no chapters.
        # let's assert what we WANT: None
        self.assertIsNone(self.manager.ingest_story_document("Whitespace", "   "))

if __name__ == '__main__':
    unittest.main()
