import unittest
from unittest.mock import patch, MagicMock, ANY
import json
import sys
import os

# Add repo root to path
sys.path.append(os.getcwd())

from python.helpers import aria_tools

class TestAriaTools(unittest.TestCase):

    def setUp(self):
        # Reset OpenAI client mock
        aria_tools.client = MagicMock()

    @patch('python.helpers.aria_tools._sd_generate')
    def test_handle_tool_call_sd_image(self, mock_generate):
        # Setup
        mock_generate.return_value = "outputs/image.png"
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "sd_image"
        msg.arguments = json.dumps({"prompt": "A cat", "steps": 20})
        msg.id = "call_123"

        # Execute
        followup, result = aria_tools.handle_tool_call(msg)

        # Verify
        self.assertEqual(result, "outputs/image.png")
        mock_generate.assert_called_once()
        args, kwargs = mock_generate.call_args
        self.assertEqual(args[0], "A cat")
        self.assertEqual(kwargs['steps'], 20)

        # Verify followup creation
        aria_tools.client.responses.create.assert_called_once()
        call_kwargs = aria_tools.client.responses.create.call_args[1]
        self.assertEqual(call_kwargs['model'], 'gpt-5')
        content = json.loads(call_kwargs['input'][0]['content'])
        self.assertEqual(content['result'], "outputs/image.png")

    @patch('python.helpers.aria_tools._eleven_tts')
    def test_handle_tool_call_eleven_tts(self, mock_tts):
        # Setup
        mock_tts.return_value = "outputs/speech.mp3"
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "eleven_tts"
        msg.arguments = "Hello world"
        msg.id = "call_tts"

        # Execute
        followup, result = aria_tools.handle_tool_call(msg)

        # Verify
        self.assertEqual(result, "outputs/speech.mp3")
        mock_tts.assert_called_once_with("Hello world")

    @patch('python.helpers.aria_tools._post_to_instagram')
    def test_handle_tool_call_instagram(self, mock_ig):
        # Setup
        mock_ig.return_value = "Success"
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "post_to_instagram"
        msg.arguments = json.dumps({"image_path": "p.png", "caption": "cap"})
        msg.id = "call_ig"

        # Execute
        followup, result = aria_tools.handle_tool_call(msg)

        # Verify
        self.assertEqual(result, "Success")
        mock_ig.assert_called_once_with("p.png", "cap")

    @patch('python.helpers.aria_tools._stripe_checkout')
    def test_handle_tool_call_stripe(self, mock_stripe):
        # Setup
        mock_stripe.return_value = "http://pay.me"
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "stripe_checkout"
        msg.arguments = json.dumps({"price_id": "p_1"})
        msg.id = "call_pay"

        # Execute
        followup, result = aria_tools.handle_tool_call(msg)

        # Verify
        self.assertEqual(result, "http://pay.me")
        mock_stripe.assert_called_once_with("p_1", None, None)

    def test_handle_tool_call_unknown(self):
        msg = MagicMock()
        msg.type = "tool_call"
        msg.name = "unknown_tool"

        followup, result = aria_tools.handle_tool_call(msg)

        self.assertEqual(followup, msg)
        self.assertIsNone(result)

    def test_handle_tool_call_not_tool(self):
        msg = MagicMock()
        msg.type = "message"

        followup, result = aria_tools.handle_tool_call(msg)

        self.assertEqual(followup, msg)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
