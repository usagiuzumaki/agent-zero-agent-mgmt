import unittest
import json
import os
import shutil
from flask import Flask
from python.api.screenwriting import screenwriting_bp
from python.helpers.screenwriting_manager import ScreenwritingManager

class TestScreenwritingAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(screenwriting_bp)
        self.client = self.app.test_client()

        # Setup test data directory
        self.test_dir = "test_screenwriting_data"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Patch manager to use test dir
        # Note: This relies on the manager instance being global in the blueprint
        # Ideally we would inject it, but for this test we'll rely on the import
        from python.api.screenwriting import manager
        manager.storage_dir = self.test_dir
        manager.files = {
            'book_outline': os.path.join(self.test_dir, 'book_outline.json'),
            'story_bible': os.path.join(self.test_dir, 'story_bible.json'),
            'character_profiles': os.path.join(self.test_dir, 'character_profiles.json'),
            'sick_quotes': os.path.join(self.test_dir, 'sick_quotes.json'),
            'sketches_imagery': os.path.join(self.test_dir, 'sketches_imagery.json'),
            'projects': os.path.join(self.test_dir, 'projects.json'),
            'storybook': os.path.join(self.test_dir, 'storybook.json')
        }

    def tearDown(self):
        # Cleanup test data
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_storybook(self):
        response = self.client.get('/api/screenwriting/storybook')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('documents', data)

    def test_upload_storybook_success(self):
        payload = {
            'name': 'Test Doc',
            'content': 'This is a test document.\n\nIt has multiple paragraphs.',
            'description': 'A test upload'
        }
        response = self.client.post('/api/screenwriting/storybook/upload',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Doc')
        self.assertTrue(len(data['chapters']) > 0)

    def test_upload_storybook_failure(self):
        # Empty content should fail
        payload = {
            'name': 'Empty Doc',
            'content': ''
        }
        response = self.client.post('/api/screenwriting/storybook/upload',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_storybook_document(self):
        # First upload a document
        payload = {
            'name': 'To Delete',
            'content': 'Content to delete.'
        }
        upload_response = self.client.post('/api/screenwriting/storybook/upload',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(upload_response.status_code, 200)
        doc_data = json.loads(upload_response.data)
        doc_id = doc_data['id']

        # Now delete it
        delete_response = self.client.post('/api/screenwriting/storybook/delete',
                                         data=json.dumps({'id': doc_id}),
                                         content_type='application/json')
        self.assertEqual(delete_response.status_code, 200)

        # Verify it's gone
        get_response = self.client.get('/api/screenwriting/storybook')
        data = json.loads(get_response.data)
        self.assertEqual(len(data['documents']), 0)

    def test_delete_storybook_missing_id(self):
        response = self.client.post('/api/screenwriting/storybook/delete',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
