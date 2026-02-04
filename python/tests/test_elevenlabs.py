import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys

# Add repo root to path
sys.path.append(os.getcwd())

# We need to handle the optional import of ElevenLabs
# We will mock the module before importing the helper to ensure we can control it
sys.modules['elevenlabs'] = MagicMock()
sys.modules['elevenlabs.client'] = MagicMock()

from python.helpers.egirl import elevenlabs

class TestElevenLabs(unittest.TestCase):

    def setUp(self):
        # Reset mocks
        pass

    @patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test_key", "PERSONA_VOICE_ID": "test_voice"})
    def test_text_to_speech_success(self):
        # Mock ElevenLabs client instance
        mock_client_cls = MagicMock()
        mock_client_instance = mock_client_cls.return_value
        mock_audio_stream = [b"chunk1", b"chunk2"]
        mock_client_instance.text_to_speech.convert.return_value = mock_audio_stream

        # Patch the class and the constants in the module
        with patch('python.helpers.egirl.elevenlabs.ElevenLabs', mock_client_cls), \
             patch('python.helpers.egirl.elevenlabs.API_KEY', "test_key"), \
             patch('python.helpers.egirl.elevenlabs.VOICE_ID', "test_voice"):

            with patch('builtins.open', mock_open()) as mock_file:
                output = elevenlabs.text_to_speech("Hello world", "outputs/test.mp3")

                self.assertEqual(output, "outputs/test.mp3")
                mock_client_cls.assert_called_with(api_key="test_key")
                mock_client_instance.text_to_speech.convert.assert_called_with(
                    voice_id="test_voice",
                    model_id="eleven_multilingual_v2",
                    text="Hello world",
                    output_format="mp3_44100_128"
                )
                mock_file().write.assert_any_call(b"chunk1")
                mock_file().write.assert_any_call(b"chunk2")

    def test_text_to_speech_missing_deps(self):
        # Simulate ElevenLabs is None
        with patch('python.helpers.egirl.elevenlabs.ElevenLabs', None):
            with self.assertRaises(RuntimeError) as context:
                elevenlabs.text_to_speech("Fail")
            self.assertIn("ElevenLabs library not installed", str(context.exception))

    def test_text_to_speech_missing_keys(self):
        # We need ElevenLabs to be "installed" (not None)
        # And we need to ensure the keys are seen as empty
        with patch('python.helpers.egirl.elevenlabs.ElevenLabs', MagicMock()), \
             patch('python.helpers.egirl.elevenlabs.API_KEY', ""), \
             patch('python.helpers.egirl.elevenlabs.VOICE_ID', ""):

            with self.assertRaises(RuntimeError) as context:
                elevenlabs.text_to_speech("Fail")
            self.assertIn("ELEVENLABS_API_KEY and PERSONA_VOICE_ID must be set", str(context.exception))

    @patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test_key", "PERSONA_VOICE_ID": "test_voice"})
    def test_text_to_speech_api_error(self):
        mock_client_cls = MagicMock()
        mock_client_instance = mock_client_cls.return_value
        mock_client_instance.text_to_speech.convert.side_effect = Exception("API Error")

        with patch('python.helpers.egirl.elevenlabs.ElevenLabs', mock_client_cls), \
             patch('python.helpers.egirl.elevenlabs.API_KEY', "test_key"), \
             patch('python.helpers.egirl.elevenlabs.VOICE_ID', "test_voice"):
            with self.assertRaises(RuntimeError) as context:
                elevenlabs.text_to_speech("Hello")
            self.assertIn("ElevenLabs TTS error: API Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
