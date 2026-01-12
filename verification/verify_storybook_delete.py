
"""Verification script for Storybook deletion functionality"""
import os
import json
import shutil
import unittest
from datetime import datetime
from python.helpers.screenwriting_manager import ScreenwritingManager

# Test data
TEST_DIR = "verification/test_data"
TEST_STORYBOOK_FILE = os.path.join(TEST_DIR, "storybook.json")

class TestStorybookDeletion(unittest.TestCase):
    def setUp(self):
        # Create test directory
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.makedirs(TEST_DIR)

        # Initialize manager with test directory
        self.manager = ScreenwritingManager(storage_dir=TEST_DIR)

        # Add a dummy document
        self.dummy_doc = {
            "id": "test_doc_1",
            "name": "Test Document",
            "description": "A test document",
            "tags": ["test"],
            "chapters": [],
            "suggestions": [],
            "uploaded_at": datetime.now().isoformat()
        }

        # Manually save it to ensure state
        storybook_data = {
            "documents": [self.dummy_doc],
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

        with open(TEST_STORYBOOK_FILE, 'w') as f:
            json.dump(storybook_data, f)

    def tearDown(self):
        # Cleanup
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def test_delete_document_success(self):
        # Verify document exists
        data = self.manager.load_data('storybook')
        self.assertEqual(len(data['documents']), 1)
        self.assertEqual(data['documents'][0]['id'], "test_doc_1")

        # Delete document
        result = self.manager.delete_document("test_doc_1")
        self.assertTrue(result)

        # Verify document is gone
        data = self.manager.load_data('storybook')
        self.assertEqual(len(data['documents']), 0)

    def test_delete_document_not_found(self):
        # Try to delete non-existent document
        result = self.manager.delete_document("non_existent_id")
        self.assertFalse(result)

        # Verify original document still exists
        data = self.manager.load_data('storybook')
        self.assertEqual(len(data['documents']), 1)

if __name__ == '__main__':
    unittest.main()
