import unittest
from unittest.mock import patch, MagicMock
import os
import json
from flask import Flask
from python.api.image_generation_endpoint import register_image_routes

class TestImageGenerationEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        register_image_routes(self.app)
        self.client = self.app.test_client()

    @patch('python.api.image_generation_endpoint.requests.post')
    @patch('python.api.image_generation_endpoint.requests.get')
    def test_generate_image_success(self, mock_get, mock_post):
        # Mock environment variable
        with patch.dict(os.environ, {'REPLICATE_API_TOKEN': 'dummy_token'}):
            # Mock prediction creation
            mock_post_response = MagicMock()
            mock_post_response.json.return_value = {"id": "test_id", "status": "processing"}
            mock_post_response.raise_for_status.return_value = None
            mock_post.return_value = mock_post_response

            # Mock polling and image download
            mock_get_response_processing = MagicMock()
            mock_get_response_processing.json.return_value = {"id": "test_id", "status": "processing"}

            mock_get_response_success = MagicMock()
            mock_get_response_success.json.return_value = {
                "id": "test_id",
                "status": "succeeded",
                "output": ["http://example.com/image.png"]
            }

            mock_image_response = MagicMock()
            mock_image_response.content = b"image_data"
            mock_image_response.raise_for_status.return_value = None

            mock_get.side_effect = [
                mock_get_response_processing, # Polling 1
                mock_get_response_success,    # Polling 2
                mock_image_response           # Image download
            ]

            response = self.client.post('/api/generate-image', json={"prompt": "test prompt"})

            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(data['url'], "http://example.com/image.png")
            self.assertTrue(os.path.exists(data['filename']))

            # Clean up
            if os.path.exists(data['filename']):
                os.remove(data['filename'])

    def test_generate_image_no_prompt(self):
        response = self.client.post('/api/generate-image', json={})
        self.assertEqual(response.status_code, 400)

    def test_generate_image_no_token(self):
         with patch.dict(os.environ, {}, clear=True):
            response = self.client.post('/api/generate-image', json={"prompt": "test"})
            self.assertEqual(response.status_code, 500)
            self.assertIn("REPLICATE_API_TOKEN", response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
