import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

# Add repo root to path
sys.path.append(os.getcwd())

# Pre-mock dependencies to ensure import works if checking sys.modules
sys.modules['elevenlabs'] = MagicMock()
sys.modules['elevenlabs.client'] = MagicMock()

from python.helpers.egirl import elevenlabs

class TestElevenLabs(unittest.TestCase):

    def setUp(self):
        # Reset the ElevenLabs class mock on the module
        self.mock_client_cls = MagicMock()
        elevenlabs.ElevenLabs = self.mock_client_cls

    @patch("python.helpers.egirl.elevenlabs.API_KEY", "test_key")
    @patch("python.helpers.egirl.elevenlabs.VOICE_ID", "test_voice")
    @patch("builtins.open", new_callable=mock_open)
    def test_text_to_speech_success(self, mock_file):
        # Setup Mock instance
        mock_client_instance = MagicMock()
        self.mock_client_cls.return_value = mock_client_instance

        # Mock generator return for audio chunks
        mock_client_instance.text_to_speech.convert.return_value = iter([b"chunk1", b"chunk2"])

        # Execute
        output_path = "outputs/test.mp3"
        result = elevenlabs.text_to_speech("Hello world", output_path)

        # Verify
        self.assertEqual(result, output_path)
        self.mock_client_cls.assert_called_with(api_key="test_key")
        mock_client_instance.text_to_speech.convert.assert_called_with(
            voice_id="test_voice",
            model_id="eleven_multilingual_v2",
            text="Hello world",
            output_format="mp3_44100_128",
        )
        mock_file.assert_called_with(output_path, "wb")
        handle = mock_file()
        handle.write.assert_any_call(b"chunk1")
        handle.write.assert_any_call(b"chunk2")

    @patch("python.helpers.egirl.elevenlabs.API_KEY", "")
    @patch("python.helpers.egirl.elevenlabs.VOICE_ID", "")
    def test_missing_keys(self):
        # Ensure keys are missing/empty

        # Ensure library is "present"
        elevenlabs.ElevenLabs = MagicMock()

        with self.assertRaises(RuntimeError) as context:
            elevenlabs.text_to_speech("fail")
        self.assertIn("must be set", str(context.exception))

    def test_library_missing(self):
        # Simulate library missing
        elevenlabs.ElevenLabs = None

        with self.assertRaises(RuntimeError) as context:
            elevenlabs.text_to_speech("fail")
        self.assertIn("library not installed", str(context.exception))

    @patch("python.helpers.egirl.elevenlabs.API_KEY", "test_key")
    @patch("python.helpers.egirl.elevenlabs.VOICE_ID", "test_voice")
    def test_api_error(self):
        # Simulate API error
        mock_client_instance = MagicMock()
        self.mock_client_cls.return_value = mock_client_instance
        mock_client_instance.text_to_speech.convert.side_effect = Exception("API Error")

        with self.assertRaises(RuntimeError) as context:
            elevenlabs.text_to_speech("Hello")
        self.assertIn("ElevenLabs TTS error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
