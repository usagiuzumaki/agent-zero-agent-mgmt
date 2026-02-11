import unittest
from unittest.mock import patch, MagicMock
import os
import json
import importlib.util
import sys

class TestImageGeneratorSimple(unittest.TestCase):
    def setUp(self):
        # Load the module directly from file path to avoid importing python.tools package
        spec = importlib.util.spec_from_file_location("image_generator_simple", "python/tools/image_generator_simple.py")
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["image_generator_simple"] = self.module
        spec.loader.exec_module(self.module)
        self.generate_image_direct = self.module.generate_image_direct

    def tearDown(self):
        if "image_generator_simple" in sys.modules:
            del sys.modules["image_generator_simple"]

    def test_generate_image_direct_success(self):
        # Patch requests inside the test method, after module is loaded
        with patch('image_generator_simple.requests.post') as mock_post, \
             patch('image_generator_simple.requests.get') as mock_get:

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
                    mock_get_response_processing,
                    mock_get_response_success,
                    mock_image_response
                ]

                result = self.generate_image_direct("test prompt")

                self.assertTrue(result['success'])
                self.assertTrue(os.path.exists(result['filename']))

                # Clean up
                if os.path.exists(result['filename']):
                    os.remove(result['filename'])

    def test_generate_image_direct_no_token(self):
         with patch.dict(os.environ, {}, clear=True):
            result = self.generate_image_direct("test")
            self.assertFalse(result['success'])
            self.assertIn("REPLICATE_API_TOKEN", result['message'])

if __name__ == '__main__':
    unittest.main()
