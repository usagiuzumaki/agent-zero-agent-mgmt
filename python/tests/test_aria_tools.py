import unittest
from unittest.mock import MagicMock, patch
import sys
import json

# Mock dependencies before importing the module under test
sys.modules["python.helpers.stable_diffusion"] = MagicMock()
sys.modules["python.helpers.tunnel_manager"] = MagicMock()
sys.modules["python.helpers.egirl.instagram"] = MagicMock()
sys.modules["python.helpers.egirl.stripe"] = MagicMock()
sys.modules["openai"] = MagicMock()
sys.modules["elevenlabs.client"] = MagicMock()

from python.helpers import aria_tools

class TestAriaTools(unittest.TestCase):
    def test_coerce_int(self):
        self.assertEqual(aria_tools._coerce_int(5), 5)
        self.assertEqual(aria_tools._coerce_int("5"), 5)
        self.assertEqual(aria_tools._coerce_int(" 5 "), 5)
        self.assertEqual(aria_tools._coerce_int(5.9), 5)
        self.assertEqual(aria_tools._coerce_int(True), 1)
        self.assertIsNone(aria_tools._coerce_int(None))
        self.assertIsNone(aria_tools._coerce_int("invalid"))
        self.assertIsNone(aria_tools._coerce_int(""))

    def test_coerce_float(self):
        self.assertEqual(aria_tools._coerce_float(5.5), 5.5)
        self.assertEqual(aria_tools._coerce_float("5.5"), 5.5)
        self.assertEqual(aria_tools._coerce_float(" 5.5 "), 5.5)
        self.assertEqual(aria_tools._coerce_float(5), 5.0)
        self.assertEqual(aria_tools._coerce_float(True), 1.0)
        self.assertIsNone(aria_tools._coerce_float(None))
        self.assertIsNone(aria_tools._coerce_float("invalid"))
        self.assertIsNone(aria_tools._coerce_float(""))

    def test_parse_tool_arguments(self):
        # Dict
        self.assertEqual(aria_tools._parse_tool_arguments({"a": 1}), {"a": 1})
        # JSON string
        self.assertEqual(aria_tools._parse_tool_arguments('{"a": 1}'), {"a": 1})
        # Plain string (treated as prompt)
        self.assertEqual(aria_tools._parse_tool_arguments("some text"), {"prompt": "some text"})
        # Scalar/List (generic value)
        self.assertEqual(aria_tools._parse_tool_arguments("[1, 2]"), {"value": [1, 2]})
        # Empty
        self.assertEqual(aria_tools._parse_tool_arguments(""), {})
        self.assertEqual(aria_tools._parse_tool_arguments(None), {})

    def test_extract_sd_request_simple(self):
        prompt, kwargs = aria_tools._extract_sd_request("a cat")
        self.assertEqual(prompt, "a cat")
        self.assertEqual(kwargs, {})

    def test_extract_sd_request_json(self):
        args = json.dumps({
            "prompt": "a dog",
            "seed": 123,
            "steps": "20",
            "guidance_scale": 7.5,
            "output_dir": "/tmp"
        })
        prompt, kwargs = aria_tools._extract_sd_request(args)
        self.assertEqual(prompt, "a dog")
        self.assertEqual(kwargs["seed"], 123)
        self.assertEqual(kwargs["steps"], 20)
        self.assertEqual(kwargs["guidance_scale"], 7.5)
        self.assertEqual(kwargs["output_dir"], "/tmp")

    def test_extract_sd_request_input_nested(self):
        # Support for nested "input" key (common in some tool calls)
        args = {"input": {"prompt": "nested prompt"}}
        prompt, kwargs = aria_tools._extract_sd_request(args)
        self.assertEqual(prompt, "nested prompt")

    def test_extract_sd_request_text_fallback(self):
        args = {"text": "fallback text"}
        prompt, kwargs = aria_tools._extract_sd_request(args)
        self.assertEqual(prompt, "fallback text")

    def test_extract_sd_request_invalid_steps(self):
        args = {"prompt": "test", "steps": 0} # Steps must be >= 1 (implied logic, checking coerce)
        # Looking at implementation: steps > 0 check is present
        prompt, kwargs = aria_tools._extract_sd_request(args)
        self.assertNotIn("steps", kwargs)

    def test_handle_tool_call_sd_image(self):
        # Mock client and response creation
        mock_client = MagicMock()
        aria_tools.client = mock_client

        # Mock generation function
        with patch("python.helpers.aria_tools._sd_generate") as mock_gen:
            mock_gen.return_value = "path/to/image.png"

            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "sd_image"
            msg.arguments = '{"prompt": "test image"}'
            msg.id = "call_123"

            followup, result = aria_tools.handle_tool_call(msg)

            mock_gen.assert_called_with("test image")
            self.assertEqual(result, "path/to/image.png")

            # Verify followup response creation
            mock_client.responses.create.assert_called_once()
            call_args = mock_client.responses.create.call_args[1]
            self.assertEqual(call_args["model"], "gpt-5")
            content = json.loads(call_args["input"][0]["content"])
            self.assertEqual(content["result"], "path/to/image.png")

    def test_handle_tool_call_sd_image_error(self):
        mock_client = MagicMock()
        aria_tools.client = mock_client

        with patch("python.helpers.aria_tools._sd_generate") as mock_gen:
            mock_gen.side_effect = Exception("Generation failed")

            msg = MagicMock()
            msg.type = "tool_call"
            msg.name = "sd_image"
            msg.arguments = '{"prompt": "test image"}'

            followup, result = aria_tools.handle_tool_call(msg)

            self.assertIsNone(result)

            call_args = mock_client.responses.create.call_args[1]
            content = json.loads(call_args["input"][0]["content"])
            self.assertEqual(content["error"], "Generation failed")

if __name__ == "__main__":
    unittest.main()
