import unittest
import json
import os
import sys
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from flask import Flask

# Add repo root to path
sys.path.append(os.getcwd())

# Need to ensure StoryGenerator is importable even if we mock it later
# But patching where it is used is better.
# python.api.screenwriting imports it.

# We need to mock initialize and agents before importing screenwriting which imports story_generator
sys.modules['initialize'] = MagicMock()
sys.modules['agents'] = MagicMock()
sys.modules['agents.agent'] = MagicMock()
sys.modules['webcolors'] = MagicMock()

# Import the blueprint
from python.api.screenwriting import screenwriting_bp, manager

class TestScreenwritingGenAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(screenwriting_bp)
        self.client = self.app.test_client()

        # Mock manager
        self.original_add_story_document = manager.add_story_document
        manager.add_story_document = MagicMock(return_value=True)

    def tearDown(self):
        manager.add_story_document = self.original_add_story_document

    @patch('python.api.screenwriting.StoryGenerator')
    def test_generate_storybook_success(self, MockStoryGenerator):
        # Mock generator instance
        mock_gen_instance = MockStoryGenerator.return_value

        fake_doc = {'id': 'gen-1', 'name': 'Generated Story'}
        mock_gen_instance.generate_story = AsyncMock(return_value=fake_doc)

        payload = {'prompt': 'A space opera'}
        response = self.client.post('/api/screenwriting/storybook/generate',
                                  data=json.dumps(payload),
                                  content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Generated Story')
        manager.add_story_document.assert_called_with(fake_doc)

    def test_generate_storybook_missing_prompt(self):
        payload = {}
        response = self.client.post('/api/screenwriting/storybook/generate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
