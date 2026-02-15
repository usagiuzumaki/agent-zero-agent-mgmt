import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import tempfile

# Add repo root to path
sys.path.append(os.getcwd())

class TestElevenLabs(unittest.TestCase):

    def setUp(self):
        # Create a patcher for sys.modules to mock elevenlabs and env vars
        self.modules_patcher = patch.dict(sys.modules, {
            'elevenlabs.client': MagicMock(),
        })
        self.modules_patcher.start()

        # Patch os.environ for API keys
        self.env_patcher = patch.dict(os.environ, {
            "ELEVENLABS_API_KEY": "test_key",
            "PERSONA_VOICE_ID": "test_voice"
        })
        self.env_patcher.start()

        # Import the module under test (re-import to pick up patches if needed)
        import python.helpers.egirl.elevenlabs as elevenlabs_module
        import importlib
        self.elevenlabs = importlib.reload(elevenlabs_module)

    def tearDown(self):
        self.modules_patcher.stop()
        self.env_patcher.stop()

    def test_text_to_speech_success(self):
        # Setup
        mock_client_cls = sys.modules['elevenlabs.client'].ElevenLabs
        mock_client_instance = mock_client_cls.return_value

        # Mock the convert method to return bytes
        mock_audio_chunk = b"audio_data"
        mock_client_instance.text_to_speech.convert.return_value = [mock_audio_chunk]

        # Execute
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.elevenlabs.text_to_speech("Hello", "output.mp3")

        # Verify result path
        self.assertEqual(result, "output.mp3")

        # Verify API call
        mock_client_cls.assert_called_with(api_key="test_key")
        mock_client_instance.text_to_speech.convert.assert_called_once()
        _, kwargs = mock_client_instance.text_to_speech.convert.call_args
        self.assertEqual(kwargs['text'], "Hello")
        self.assertEqual(kwargs['voice_id'], "test_voice")
        self.assertEqual(kwargs['model_id'], "eleven_multilingual_v2")

        # Verify file write
        mock_file.assert_called_with("output.mp3", "wb")
        mock_file().write.assert_called_with(mock_audio_chunk)

    def test_text_to_speech_missing_config(self):
        # Unset env vars
        with patch.dict(os.environ, {}, clear=True):
            # Reload to pick up empty env
            import importlib
            importlib.reload(self.elevenlabs)

            with self.assertRaises(RuntimeError) as context:
                self.elevenlabs.text_to_speech("Hello")

            self.assertIn("must be set", str(context.exception))

    def test_text_to_speech_missing_library(self):
        # Mock import failure by setting ElevenLabs to None in the module
        # Note: The module handles ImportError by setting ElevenLabs = None

        # We need to force re-import where ImportError happens?
        # Or just manually set it to None for the test
        self.elevenlabs.ElevenLabs = None

        with self.assertRaises(RuntimeError) as context:
            self.elevenlabs.text_to_speech("Hello")

        self.assertIn("ElevenLabs library not installed", str(context.exception))

if __name__ == '__main__':
    unittest.main()
