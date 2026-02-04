import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

# Add repo root to path
sys.path.append(os.getcwd())

# We need to mock requests and time for video.py
# Since video.py imports them, we can patch them during tests,
# but we need to patch the RUNWAY_API_KEY constant in the module.

# Mock requests before importing video because it might not be installed
sys.modules['requests'] = MagicMock()

from python.helpers.egirl import video

class TestVideo(unittest.TestCase):

    def setUp(self):
        pass

    @patch('python.helpers.egirl.video.requests')
    @patch('python.helpers.egirl.video.time')
    def test_generate_video_from_image_success(self, mock_time, mock_requests):
        # Setup mocks
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id": "task_123"}
        mock_requests.post.return_value = mock_post_response

        # Mock status check responses: running -> running -> succeeded
        mock_get_status_running = MagicMock()
        mock_get_status_running.json.return_value = {"status": "running"}

        mock_get_status_success = MagicMock()
        mock_get_status_success.json.return_value = {
            "status": "succeeded",
            "result": {"video": "http://fake.url/video.mp4"}
        }

        mock_get_video_content = MagicMock()
        mock_get_video_content.content = b"video_data"

        # status check 1, status check 2, download video
        mock_requests.get.side_effect = [
            mock_get_status_running,
            mock_get_status_success,
            mock_get_video_content
        ]

        # Patch API KEY
        with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
            with patch('builtins.open', mock_open(read_data=b"image_data")) as mock_file:
                 result = video.generate_video_from_image("input.png", "A dancing cat", "outputs/video.mp4")

                 self.assertEqual(result, "outputs/video.mp4")

                 # Verify POST
                 mock_requests.post.assert_called_once()
                 mock_post_response.raise_for_status.assert_called_once()

                 args, kwargs = mock_requests.post.call_args
                 self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_key")
                 self.assertIn("prompt_image", kwargs['json'])
                 self.assertEqual(kwargs['json']['prompt_text'], "A dancing cat")

                 # Verify GET (status checks and download)
                 self.assertEqual(mock_requests.get.call_count, 3)

                 # Verify download success check
                 mock_get_video_content.raise_for_status.assert_called_once()

    @patch('python.helpers.egirl.video.requests')
    def test_generate_video_missing_key(self, mock_requests):
        with patch('python.helpers.egirl.video.RUNWAY_API_KEY', None):
            result = video.generate_video_from_image("input.png", "prompt")
            self.assertIsNone(result)
            mock_requests.post.assert_not_called()

    @patch('python.helpers.egirl.video.requests')
    def test_generate_video_task_creation_fail_no_id(self, mock_requests):
         mock_post_response = MagicMock()
         mock_post_response.json.return_value = {"error": "Invalid prompt"} # No ID
         mock_requests.post.return_value = mock_post_response

         with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
             with patch('builtins.open', mock_open(read_data=b"img")):
                 result = video.generate_video_from_image("input.png", "prompt")
                 self.assertIsNone(result)

    @patch('python.helpers.egirl.video.requests')
    def test_generate_video_task_creation_exception(self, mock_requests):
         mock_requests.post.side_effect = Exception("Network error")

         with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
             with patch('builtins.open', mock_open(read_data=b"img")):
                 result = video.generate_video_from_image("input.png", "prompt")
                 self.assertIsNone(result)

    @patch('python.helpers.egirl.video.requests')
    @patch('python.helpers.egirl.video.time')
    def test_generate_video_task_failed_status(self, mock_time, mock_requests):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id": "task_123"}
        mock_requests.post.return_value = mock_post_response

        mock_get_status_failed = MagicMock()
        mock_get_status_failed.json.return_value = {"status": "failed", "error": "Something went wrong"}
        mock_requests.get.return_value = mock_get_status_failed

        with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
             with patch('builtins.open', mock_open(read_data=b"img")):
                 result = video.generate_video_from_image("input.png", "prompt")
                 self.assertIsNone(result)

    @patch('python.helpers.egirl.video.requests')
    @patch('python.helpers.egirl.video.time')
    def test_generate_video_timeout(self, mock_time, mock_requests):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id": "task_123"}
        mock_requests.post.return_value = mock_post_response

        # Always running
        mock_get_status_running = MagicMock()
        mock_get_status_running.json.return_value = {"status": "running"}
        mock_requests.get.return_value = mock_get_status_running

        # Reduce loop count for test or trust that mock_time doesn't actually wait
        # The loop is hardcoded range(120). 120 iterations is fine if sleep is mocked.

        with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
             with patch('builtins.open', mock_open(read_data=b"img")):
                 result = video.generate_video_from_image("input.png", "prompt")
                 self.assertIsNone(result)
                 # Should have called get 120 times
                 self.assertEqual(mock_requests.get.call_count, 120)

    @patch('python.helpers.egirl.video.requests')
    @patch('python.helpers.egirl.video.time')
    def test_generate_video_download_fail(self, mock_time, mock_requests):
        mock_post_response = MagicMock()
        mock_post_response.json.return_value = {"id": "task_123"}
        mock_requests.post.return_value = mock_post_response

        mock_get_status_success = MagicMock()
        mock_get_status_success.json.return_value = {
            "status": "succeeded",
            "result": {"video": "http://fake.url/video.mp4"}
        }

        # First GET for status, Second GET for video download (which fails)
        mock_requests.get.side_effect = [
            mock_get_status_success,
            Exception("Download failed")
        ]

        with patch('python.helpers.egirl.video.RUNWAY_API_KEY', "test_key"):
             with patch('builtins.open', mock_open(read_data=b"img")):
                 result = video.generate_video_from_image("input.png", "prompt")
                 self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
