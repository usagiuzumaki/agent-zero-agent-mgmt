import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add repo root to path
sys.path.append(os.getcwd())

# Mock dependencies BEFORE importing anything that uses them
sys.modules['flaredantic'] = MagicMock()

from python.helpers.aria_tools import _post_to_instagram

class TestInstagramIntegration(unittest.TestCase):

    @patch('python.helpers.aria_tools.TunnelManager')
    @patch('python.helpers.aria_tools.instagram')
    def test_post_to_instagram_success(self, mock_instagram, mock_tunnel_manager):
        # Setup Tunnel Mock
        mock_tunnel_instance = MagicMock()
        mock_tunnel_instance.get_tunnel_url.return_value = "https://test.tunnel"
        mock_tunnel_manager.get_instance.return_value = mock_tunnel_instance

        # Setup Instagram Mock
        mock_instagram.post_image.return_value = {"id": "12345"}

        # Execute
        image_path = "outputs/test_image.png"
        caption = "Hello World"
        result = _post_to_instagram(image_path, caption)

        # Verify
        expected_url = "https://test.tunnel/public_image?filename=test_image.png"
        mock_instagram.post_image.assert_called_once_with(expected_url, caption)
        self.assertIn("Success", result)
        self.assertIn("12345", result)

    @patch('python.helpers.aria_tools.TunnelManager')
    def test_post_to_instagram_no_tunnel(self, mock_tunnel_manager):
        # Setup Tunnel Mock to return None
        mock_tunnel_instance = MagicMock()
        mock_tunnel_instance.get_tunnel_url.return_value = None
        mock_tunnel_manager.get_instance.return_value = mock_tunnel_instance

        # Execute
        result = _post_to_instagram("path", "caption")

        # Verify
        self.assertIn("Error: No public tunnel active", result)

    @patch('python.helpers.aria_tools.TunnelManager')
    @patch('python.helpers.aria_tools.instagram')
    def test_post_to_instagram_api_fail(self, mock_instagram, mock_tunnel_manager):
        # Setup Tunnel
        mock_tunnel_instance = MagicMock()
        mock_tunnel_instance.get_tunnel_url.return_value = "https://url"
        mock_tunnel_manager.get_instance.return_value = mock_tunnel_instance

        # Setup Instagram fail
        mock_instagram.post_image.return_value = {"error": "Bad Token"}

        # Execute
        result = _post_to_instagram("path", "caption")

        # Verify
        self.assertIn("Failed", result)
        self.assertIn("Bad Token", result)

if __name__ == '__main__':
    unittest.main()
