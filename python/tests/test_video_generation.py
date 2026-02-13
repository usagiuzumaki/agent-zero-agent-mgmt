import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

class TestVideoGeneration(unittest.TestCase):
    def setUp(self):
        # We need to reload the module to apply patches if we modify sys.modules or os.environ
        if 'python.helpers.egirl.video' in sys.modules:
            del sys.modules['python.helpers.egirl.video']

    def test_generate_video_success(self):
        with patch.dict(os.environ, {'RUNWAY_API_KEY': 'dummy_key'}):
            from python.helpers.egirl.video import generate_video_from_image

            # Mock file reading
            mock_file = mock_open(read_data=b"image_data")

            # Mock requests
            with patch('python.helpers.egirl.video.requests.post') as mock_post, \
                 patch('python.helpers.egirl.video.requests.get') as mock_get, \
                 patch('builtins.open', mock_file), \
                 patch('os.path.exists', return_value=True), \
                 patch('os.makedirs'):

                # Mock post response
                mock_post_resp = MagicMock()
                mock_post_resp.json.return_value = {"id": "task_id"}
                mock_post_resp.raise_for_status.return_value = None
                mock_post.return_value = mock_post_resp

                # Mock get responses (polling and download)
                mock_poll_resp = MagicMock()
                mock_poll_resp.json.return_value = {
                    "status": "succeeded",
                    "result": {"video": "http://example.com/video.mp4"}
                }
                mock_poll_resp.raise_for_status.return_value = None

                mock_video_resp = MagicMock()
                mock_video_resp.content = b"video_data"
                mock_video_resp.raise_for_status.return_value = None

                mock_get.side_effect = [mock_poll_resp, mock_video_resp]

                output_path = generate_video_from_image("image.png", "prompt")

                self.assertEqual(output_path, "outputs/video.mp4")
                mock_post.assert_called_once()
                self.assertEqual(mock_get.call_count, 2)

    def test_generate_video_no_key(self):
        with patch.dict(os.environ, {}, clear=True):
            from python.helpers.egirl.video import generate_video_from_image
            result = generate_video_from_image("image.png", "prompt")
            self.assertIsNone(result)

    def test_generate_video_file_not_found(self):
        with patch.dict(os.environ, {'RUNWAY_API_KEY': 'dummy_key'}):
             with patch('os.path.exists', return_value=False):
                from python.helpers.egirl.video import generate_video_from_image
                result = generate_video_from_image("image.png", "prompt")
                self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
