import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

sys.path.append(os.getcwd())

from python.helpers.egirl import video

class TestVideo(unittest.TestCase):

    @patch("python.helpers.egirl.video.RUNWAY_API_KEY", "test_key")
    @patch("python.helpers.egirl.video.requests")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_image_data")
    @patch("python.helpers.egirl.video.time.sleep")
    def test_generate_video_success(self, mock_sleep, mock_file, mock_requests):
        # Setup Mocks
        # 1. POST task creation
        mock_post_resp = MagicMock()
        mock_post_resp.json.return_value = {"id": "task_123"}
        mock_requests.post.return_value = mock_post_resp

        # 2. GET status (pending then success)
        mock_status_pending = MagicMock()
        mock_status_pending.json.return_value = {"status": "pending"}

        mock_status_success = MagicMock()
        mock_status_success.json.return_value = {
            "status": "succeeded",
            "result": {"video": "http://fake.url/video.mp4"}
        }

        # 3. GET video content
        mock_video_resp = MagicMock()
        mock_video_resp.content = b"video_bytes"

        # Side effect sequence: Status (Pending) -> Status (Success) -> Download Video
        mock_requests.get.side_effect = [
            mock_status_pending,
            mock_status_success,
            mock_video_resp
        ]

        # Execute
        output_path = "outputs/test_video.mp4"
        result = video.generate_video_from_image("input.png", "prompt", output_path)

        # Verify
        self.assertEqual(result, output_path)
        mock_requests.post.assert_called()
        self.assertEqual(mock_requests.get.call_count, 3)

        # Verify file write: last write should be video bytes
        # Note: mock_file is used for reading "input.png" AND writing "test_video.mp4"
        handle = mock_file()
        handle.write.assert_called_with(b"video_bytes")

    @patch("python.helpers.egirl.video.RUNWAY_API_KEY", "")
    def test_missing_key(self):
        self.assertIsNone(video.generate_video_from_image("in.png", "p"))

    @patch("python.helpers.egirl.video.RUNWAY_API_KEY", "test_key")
    @patch("python.helpers.egirl.video.requests")
    @patch("builtins.open", new_callable=mock_open, read_data=b"img")
    def test_api_failure_start(self, mock_file, mock_requests):
        # POST fails to return id
        mock_requests.post.return_value.json.return_value = {"error": "bad request"}
        self.assertIsNone(video.generate_video_from_image("in.png", "p"))

    @patch("python.helpers.egirl.video.RUNWAY_API_KEY", "test_key")
    @patch("python.helpers.egirl.video.requests")
    @patch("builtins.open", new_callable=mock_open, read_data=b"img")
    @patch("python.helpers.egirl.video.time.sleep")
    def test_task_failed(self, mock_sleep, mock_file, mock_requests):
        # POST success
        mock_requests.post.return_value.json.return_value = {"id": "task_123"}
        # GET status failed
        mock_requests.get.return_value.json.return_value = {"status": "failed"}

        self.assertIsNone(video.generate_video_from_image("in.png", "p"))

if __name__ == '__main__':
    unittest.main()
