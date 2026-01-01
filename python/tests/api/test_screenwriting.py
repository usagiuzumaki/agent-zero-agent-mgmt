import unittest
import json
import os
from unittest.mock import MagicMock, patch
from flask import Flask
from python.api.screenwriting import screenwriting_bp, manager

class TestScreenwritingAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(screenwriting_bp)
        self.client = self.app.test_client()

        # Mock the manager's methods to prevent file I/O during tests
        self.original_load_data = manager.load_data
        self.original_save_data = manager.save_data
        manager.load_data = MagicMock(return_value={'documents': []})
        manager.save_data = MagicMock(return_value=True)

    def tearDown(self):
        # Restore original methods
        manager.load_data = self.original_load_data
        manager.save_data = self.original_save_data

    def test_get_storybook(self):
        manager.load_data.return_value = {'documents': [{'id': '1', 'name': 'Test Doc'}]}
        response = self.client.get('/api/screenwriting/storybook')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['documents']), 1)
        self.assertEqual(data['documents'][0]['name'], 'Test Doc')

    def test_upload_storybook_success(self):
        # Mock ingest_story_document to return a fake document
        manager.ingest_story_document = MagicMock(return_value={
            'id': '123',
            'name': 'New Story',
            'chapters': []
        })

        payload = {
            'name': 'New Story',
            'content': 'Once upon a time...',
            'description': 'A test story'
        }

        response = self.client.post('/api/screenwriting/storybook/upload',
                                  data=json.dumps(payload),
                                  content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'New Story')
        manager.ingest_story_document.assert_called_once()

    def test_upload_storybook_failure(self):
        manager.ingest_story_document = MagicMock(return_value=None)

        payload = {'name': 'Bad Story', 'content': ''}
        response = self.client.post('/api/screenwriting/storybook/upload',
                                  data=json.dumps(payload),
                                  content_type='application/json')

        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
