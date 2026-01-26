import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import shutil

# Add repo root to path
sys.path.append(os.getcwd())

# Mock dependencies BEFORE importing
sys.modules['torch'] = MagicMock()
sys.modules['diffusers'] = MagicMock()
sys.modules['replicate'] = MagicMock()
sys.modules['httpx'] = MagicMock()
sys.modules['python.helpers.stable_diffusion_simple'] = MagicMock()

from python.helpers import stable_diffusion

class TestStableDiffusion(unittest.TestCase):

    def setUp(self):
        # Reset mocks
        sys.modules['replicate'].reset_mock()
        mock_simple = sys.modules['python.helpers.stable_diffusion_simple']
        mock_simple.reset_mock()
        mock_simple.generate_image.side_effect = None # Clear side effects
        stable_diffusion._pipe = None # Reset cached pipeline

    @patch.dict(os.environ, {"REPLICATE_API_TOKEN": "r8_test_token"})
    def test_generate_image_replicate_simple_success(self):
        # Setup Mock for simple subprocess method
        mock_simple = sys.modules['python.helpers.stable_diffusion_simple']
        mock_simple.generate_image.return_value = "outputs/simple_sd.png"

        # Execute
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = stable_diffusion.generate_image("A cat", steps=20, output_dir=tmpdirname)

            # Verify
            self.assertEqual(result, "outputs/simple_sd.png")
            mock_simple.generate_image.assert_called_once()
            args, kwargs = mock_simple.generate_image.call_args
            self.assertEqual(args[0], "A cat")
            self.assertEqual(kwargs['steps'], 20)
            self.assertEqual(kwargs['output_dir'], tmpdirname)

    @patch.dict(os.environ, {"REPLICATE_API_TOKEN": "r8_test_token"})
    def test_generate_image_replicate_fallback_success(self):
        # Setup Mock: simple fails, replicate works
        mock_simple = sys.modules['python.helpers.stable_diffusion_simple']
        mock_simple.generate_image.side_effect = Exception("Subprocess failed")

        mock_replicate = sys.modules['replicate']
        mock_replicate.run.return_value = ["https://replicate.com/image.png"]

        # Mock requests/httpx needed for downloading
        with patch('httpx.get') as mock_get:
            mock_get.return_value.content = b"fake_image_data"
            mock_get.return_value.raise_for_status = MagicMock()

            # Execute
            with tempfile.TemporaryDirectory() as tmpdirname:
                result = stable_diffusion.generate_image("A dog", output_dir=tmpdirname)

                # Verify
                self.assertTrue(result.startswith(os.path.join(tmpdirname, "sd_image_")))
                mock_replicate.run.assert_called_once()

                # Verify inputs to run
                args, kwargs = mock_replicate.run.call_args
                self.assertIn("prompt", kwargs['input'])
                self.assertEqual(kwargs['input']['prompt'], "A dog")

    @patch.dict(os.environ, {}, clear=True)
    def test_generate_image_local_success(self):
        # Ensure NO Replicate token
        if "REPLICATE_API_TOKEN" in os.environ:
            del os.environ["REPLICATE_API_TOKEN"]

        # Setup Mock for local pipeline
        mock_diffusers = sys.modules['diffusers']
        mock_pipe_instance = MagicMock()
        mock_diffusers.StableDiffusionPipeline.from_pretrained.return_value = mock_pipe_instance

        # Mock the pipeline call result
        mock_result = MagicMock()
        mock_image = MagicMock()
        mock_result.images = [mock_image]
        mock_pipe_instance.return_value = mock_result

        # Execute
        with tempfile.TemporaryDirectory() as tmpdirname:
            result = stable_diffusion.generate_image("A bird", steps=15, output_dir=tmpdirname)

            # Verify
            self.assertTrue(result.startswith(os.path.join(tmpdirname, "sd_image_")))
            mock_diffusers.StableDiffusionPipeline.from_pretrained.assert_called()
            mock_pipe_instance.assert_called_once()
            args, kwargs = mock_pipe_instance.call_args
            self.assertEqual(args[0], "A bird")
            self.assertEqual(kwargs['num_inference_steps'], 15)
            mock_image.save.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_generate_image_local_missing_deps(self):
         # Ensure NO Replicate token
        if "REPLICATE_API_TOKEN" in os.environ:
            del os.environ["REPLICATE_API_TOKEN"]

        # Simulate missing torch/diffusers
        stable_diffusion.torch = None
        stable_diffusion.StableDiffusionPipeline = None

        # Execute & Verify
        with self.assertRaises(RuntimeError) as context:
             stable_diffusion.generate_image("Fail")
        self.assertIn("Stable Diffusion dependencies missing", str(context.exception))

        # Restore mocks for other tests (though setUp handles re-imports/resets somewhat, module level vars persist)
        stable_diffusion.torch = sys.modules['torch']
        stable_diffusion.StableDiffusionPipeline = sys.modules['diffusers'].StableDiffusionPipeline

if __name__ == '__main__':
    unittest.main()
