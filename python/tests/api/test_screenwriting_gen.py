import unittest
import json
import os
import sys
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from flask import Flask
import importlib

# Add repo root to path
sys.path.append(os.getcwd())

class TestScreenwritingGenAPI(unittest.TestCase):
    def setUp(self):
        # Setup mocks for dependencies
        self.modules_patcher = patch.dict(sys.modules, {
            'initialize': MagicMock(),
            'agents': MagicMock(),
            'agents.agent': MagicMock(),
            'webcolors': MagicMock(),
        })
        self.modules_patcher.start()

        # Reload the module under test to pick up mocks
        # We need to make sure python.api.screenwriting is reloaded
        if 'python.api.screenwriting' in sys.modules:
            importlib.reload(sys.modules['python.api.screenwriting'])
        else:
            import python.api.screenwriting

        from python.api.screenwriting import screenwriting_bp, manager
        self.screenwriting_bp = screenwriting_bp
        self.manager = manager

        self.app = Flask(__name__)
        self.app.register_blueprint(self.screenwriting_bp)
        self.client = self.app.test_client()

        # Mock manager methods
        self.original_add_story_document = self.manager.add_story_document
        self.manager.add_story_document = MagicMock(return_value=True)

    def tearDown(self):
        # Restore manager methods
        self.manager.add_story_document = self.original_add_story_document

        self.modules_patcher.stop()

        # Reload python.api.screenwriting again to restore original imports if possible
        # or just let it be reloaded by next test if it does similar things.
        # But cleanest is to remove it from sys.modules
        if 'python.api.screenwriting' in sys.modules:
             del sys.modules['python.api.screenwriting']

    def test_generate_storybook_success(self):
        # We need to patch StoryGenerator inside python.api.screenwriting
        # Since we reloaded it, we patch the object in sys.modules
        with patch('python.api.screenwriting.StoryGenerator') as MockStoryGenerator:
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
            self.manager.add_story_document.assert_called_with(fake_doc)

    def test_generate_storybook_missing_prompt(self):
        payload = {}
        response = self.client.post('/api/screenwriting/storybook/generate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
