import unittest
from unittest.mock import patch, MagicMock
import os
import sys

class TestGenerateImageTool(unittest.TestCase):
    def setUp(self):
        # Read the file content
        with open('python/tools/generate_image_tool.py', 'r') as f:
            self.code = f.read()

    def test_execute_success(self):
        # Mock dependencies
        mock_tool_module = MagicMock()
        mock_tool_class = type('Tool', (object,), {})
        mock_response_class = MagicMock(return_value="ResponseObject")
        mock_tool_module.Tool = mock_tool_class
        mock_tool_module.Response = mock_response_class

        mock_replicate = MagicMock()
        mock_replicate.run.return_value = ["http://example.com/image.png"]

        mock_requests = MagicMock()
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.content = b"image_data"
        mock_requests.get.return_value = mock_response_obj

        with patch.dict(sys.modules, {
            'python.helpers.tool': mock_tool_module,
            'replicate': mock_replicate,
            'requests': mock_requests
        }):
            # We also need to prevent 'from python.helpers.tool import Tool, Response' from failing
            # import statement in the code will use sys.modules

            # Exec the code in a new namespace
            namespace = {}
            exec(self.code, namespace)

            GenerateImage = namespace['GenerateImage']
            tool_instance = GenerateImage()
            tool_instance.agent = MagicMock() # Mock agent

            # Setup environment variable
            with patch.dict(os.environ, {'REPLICATE_API_TOKEN': 'dummy_token'}):
                result = tool_instance.execute(prompt="test prompt")

                self.assertEqual(result, "ResponseObject")
                # Check if replicate.run was called
                mock_replicate.run.assert_called_once()
                # Check if image was downloaded
                mock_requests.get.assert_called_once_with("http://example.com/image.png", timeout=30)

                # Check message in Response constructor call
                call_args = mock_response_class.call_args
                self.assertIn("Image generated successfully", call_args.kwargs['message'])

    def test_execute_no_token(self):
        # Mock dependencies
        mock_tool_module = MagicMock()
        mock_tool_class = type('Tool', (object,), {})
        mock_response_class = MagicMock(return_value="ResponseObject")
        mock_tool_module.Tool = mock_tool_class
        mock_tool_module.Response = mock_response_class

        mock_replicate = MagicMock()

        with patch.dict(sys.modules, {
            'python.helpers.tool': mock_tool_module,
            'replicate': mock_replicate,
            'requests': MagicMock()
        }):
            namespace = {}
            exec(self.code, namespace)

            GenerateImage = namespace['GenerateImage']
            tool_instance = GenerateImage()
            tool_instance.agent = MagicMock()

            with patch.dict(os.environ, {}, clear=True):
                 result = tool_instance.execute(prompt="test")
                 call_args = mock_response_class.call_args
                 self.assertIn("REPLICATE_API_TOKEN not configured", call_args.kwargs['message'])

if __name__ == '__main__':
    unittest.main()
