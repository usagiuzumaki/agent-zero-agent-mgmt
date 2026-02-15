import unittest
from unittest.mock import patch, MagicMock, ANY
import json
import sys
import os
import importlib

# Add repo root to path
sys.path.append(os.getcwd())

class TestAriaTools(unittest.TestCase):

    def setUp(self):
        # Create a patcher for sys.modules
        self.modules_patcher = patch.dict(sys.modules, {
            'openai': MagicMock(),
            'elevenlabs.client': MagicMock(),
            'python.helpers.stable_diffusion': MagicMock(),
            'python.helpers.tunnel_manager': MagicMock(),
            'python.helpers.egirl.instagram': MagicMock(),
            'python.helpers.egirl.stripe': MagicMock(),
            'python.helpers.egirl.elevenlabs': MagicMock(),
        })
        self.modules_patcher.start()

        # Now safe to import/reload aria_tools
        # We must ensure we get a fresh version that uses the mocks
        try:
            import python.helpers.aria_tools
            self.aria_tools = importlib.reload(python.helpers.aria_tools)
        except ImportError:
            # Should not happen given mocks, but if it does, it's a test failure
            self.fail("Could not import python.helpers.aria_tools")

        # Mock the client within the reloaded module
        self.aria_tools.client = MagicMock()

    def tearDown(self):
        self.modules_patcher.stop()

    def test_handle_tool_call_sd_image(self):
        # We cannot use @patch decorator easily because we need to patch the object
        # on self.aria_tools, which changes every setUp.
        # So we patch manually or use patch.object on the instance.

        with patch.object(self.aria_tools, '_sd_generate') as mock_generate:
            # Setup
            mock_generate.return_value = "outputs/image.png"
            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "sd_image"
            msg.arguments = json.dumps({"prompt": "A cat", "steps": 20})
            msg.id = "call_123"

            # Execute
            followup, result = self.aria_tools.handle_tool_call(msg)

            # Verify
            self.assertEqual(result, "outputs/image.png")
            mock_generate.assert_called_once()
            args, kwargs = mock_generate.call_args
            self.assertEqual(args[0], "A cat")
            self.assertEqual(kwargs['steps'], 20)

            # Verify followup creation
            self.aria_tools.client.responses.create.assert_called_once()
            call_kwargs = self.aria_tools.client.responses.create.call_args[1]
            self.assertEqual(call_kwargs['model'], 'gpt-5')
            content = json.loads(call_kwargs['input'][0]['content'])
            self.assertEqual(content['result'], "outputs/image.png")

    def test_handle_tool_call_eleven_tts(self):
        with patch.object(self.aria_tools, '_eleven_tts') as mock_tts:
            # Setup
            mock_tts.return_value = "outputs/speech.mp3"
            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "eleven_tts"
            msg.arguments = "Hello world"
            msg.id = "call_tts"

            # Execute
            followup, result = self.aria_tools.handle_tool_call(msg)

            # Verify
            self.assertEqual(result, "outputs/speech.mp3")
            mock_tts.assert_called_once_with("Hello world")

    def test_handle_tool_call_instagram(self):
        with patch.object(self.aria_tools, '_post_to_instagram') as mock_ig:
            # Setup
            mock_ig.return_value = "Success"
            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "post_to_instagram"
            msg.arguments = json.dumps({"image_path": "p.png", "caption": "cap"})
            msg.id = "call_ig"

            # Execute
            followup, result = self.aria_tools.handle_tool_call(msg)

            # Verify
            self.assertEqual(result, "Success")
            mock_ig.assert_called_once_with("p.png", "cap")

    def test_handle_tool_call_stripe(self):
        with patch.object(self.aria_tools, '_stripe_checkout') as mock_stripe:
            # Setup
            mock_stripe.return_value = "http://pay.me"
            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "stripe_checkout"
            msg.arguments = json.dumps({"price_id": "p_1"})
            msg.id = "call_pay"

            # Execute
            followup, result = self.aria_tools.handle_tool_call(msg)

            # Verify
            self.assertEqual(result, "http://pay.me")
            mock_stripe.assert_called_once_with("p_1", None, None)

    def test_handle_tool_call_unknown(self):
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "unknown_tool"

        followup, result = self.aria_tools.handle_tool_call(msg)

        self.assertEqual(followup, msg)
        self.assertIsNone(result)

    def test_handle_tool_call_not_tool(self):
        msg = MagicMock()
        msg.type = "message"

        followup, result = self.aria_tools.handle_tool_call(msg)

        self.assertEqual(followup, msg)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
