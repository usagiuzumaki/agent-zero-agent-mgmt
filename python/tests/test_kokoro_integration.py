import unittest
from unittest.mock import MagicMock, patch
import sys
import asyncio

# Mock modules
sys.modules['kokoro'] = MagicMock()
sys.modules['soundfile'] = MagicMock()
sys.modules['torch'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['webcolors'] = MagicMock() # Mock missing dependency

# Mock numpy behavior
mock_np = sys.modules['numpy']
# We need to set attributes on the mock object that sys.modules['numpy'] points to
# But sys.modules['numpy'] is the mock itself.
# Wait, MagicMock creates attributes on access by default.
# But we want specific return values.
mock_np.concatenate.return_value = b'fake_audio_bytes'

from python.helpers import kokoro_tts

class TestKokoroTTS(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        kokoro_tts._pipeline = None

    async def test_preload(self):
        # We need to ensure KPipeline is available on the mocked module
        mock_kpipeline = MagicMock()
        sys.modules['kokoro'].KPipeline = mock_kpipeline
        sys.modules['torch'].cuda.is_available.return_value = False

        await kokoro_tts.preload()

        mock_kpipeline.assert_called_once()
        self.assertTrue(await kokoro_tts.is_downloaded())

    async def test_synthesize_sentences(self):
        # Mock KPipeline instance
        mock_kpipeline = MagicMock()
        sys.modules['kokoro'].KPipeline = mock_kpipeline
        sys.modules['torch'].cuda.is_available.return_value = False

        mock_pipeline_instance = mock_kpipeline.return_value

        # Generator yields (graphemes, phonemes, audio)
        fake_audio_chunk = MagicMock()
        fake_audio_chunk.__len__.return_value = 100 # Simulate length > 0
        mock_pipeline_instance.return_value = iter([
            (None, None, fake_audio_chunk)
        ])

        # Preload
        await kokoro_tts.preload()

        # Test synthesis
        # Mock soundfile.write side effect
        def write_side_effect(buffer, audio, rate, format):
            buffer.write(b"encoded_audio")

        sys.modules['soundfile'].write.side_effect = write_side_effect

        result = await kokoro_tts.synthesize_sentences(["Hello"])

        self.assertTrue(len(result) > 0)

        # Verify soundfile.write called
        sys.modules['soundfile'].write.assert_called()
        args, _ = sys.modules['soundfile'].write.call_args
        # args[0] is buffer, args[1] is audio, args[2] is rate
        # We expect args[1] to be the result of np.concatenate which we mocked
        self.assertEqual(args[1], b'fake_audio_bytes')
        self.assertEqual(args[2], 24000)

if __name__ == '__main__':
    unittest.main()
