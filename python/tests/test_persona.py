import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import importlib

class TestPersonaEngine(unittest.TestCase):
    def setUp(self):
        # Set dummy API key to avoid OpenAI client initialization errors during import
        self.env_patcher = patch.dict(os.environ, {"OPENAI_API_KEY": "dummy"})
        self.env_patcher.start()

        # Mock out heavy dependencies
        self.modules_patcher = patch.dict(sys.modules, {
            "openai": MagicMock(),
            "elevenlabs": MagicMock(),
            "elevenlabs.client": MagicMock(),
            "flaredantic": MagicMock(),
        })
        self.modules_patcher.start()

        # Ensure we are testing with fresh imports
        # We must remove aria_tools first because persona imports from it
        if "python.helpers.aria_tools" in sys.modules:
            del sys.modules["python.helpers.aria_tools"]
        if "python.helpers.egirl.persona" in sys.modules:
            del sys.modules["python.helpers.egirl.persona"]

        import python.helpers.egirl.persona
        self.persona_module = python.helpers.egirl.persona
        self.engine = self.persona_module.PersonaEngine("Aria")

    def tearDown(self):
        self.modules_patcher.stop()
        self.env_patcher.stop()

        # Clean up to prevent side effects on other tests
        if "python.helpers.egirl.persona" in sys.modules:
            del sys.modules["python.helpers.egirl.persona"]
        if "python.helpers.aria_tools" in sys.modules:
            del sys.modules["python.helpers.aria_tools"]

    def test_generate_response_text_only(self):
        # We manualy patch because the module is reloaded in setUp
        # and using decorator might be tricky if the module doesn't exist at collection time
        # (though here it exists on disk, so it's fine).
        # But for safety/clarity with dynamic imports:
        with patch.object(self.persona_module, "gpt5") as mock_gpt5:
            # Mock the response from gpt5
            mock_response = MagicMock()
            mock_response.output = []
            mock_response.output_text = "Hello there!"
            mock_gpt5.return_value = mock_response

            response = self.engine.generate_response("Hi")

            self.assertEqual(response["text"], "Hello there!")
            self.assertIsNone(response["audio_path"])
            self.assertIsNone(response["tool_result"])

            # Verify history was updated
            self.assertEqual(self.engine.history[-2]["role"], "user")
            self.assertEqual(self.engine.history[-2]["content"], "Hi")
            self.assertEqual(self.engine.history[-1]["role"], "assistant")
            self.assertEqual(self.engine.history[-1]["content"], "Hello there!")

    def test_generate_response_with_tool_call(self):
        with patch.object(self.persona_module, "gpt5") as mock_gpt5, \
             patch.object(self.persona_module, "handle_tool_call") as mock_handle_tool_call:

            # First call returns a tool call
            tool_call_item = MagicMock()
            tool_call_item.type = "tool_call"
            tool_call_item.name = "eleven_tts"

            # Second call (followup) returns the final text
            final_response = MagicMock()
            final_response.output = []
            final_response.output_text = "Audio generated."

            mock_gpt5.return_value = MagicMock()
            mock_gpt5.return_value.output = [tool_call_item]

            # handle_tool_call returns (followup_response, result)
            mock_handle_tool_call.return_value = (final_response, "path/to/audio.mp3")

            response = self.engine.generate_response("Speak to me")

            self.assertEqual(response["text"], "Audio generated.")
            self.assertEqual(response["audio_path"], "path/to/audio.mp3")

            mock_handle_tool_call.assert_called_once()

    def test_generate_response_with_other_tool_result(self):
        with patch.object(self.persona_module, "gpt5") as mock_gpt5, \
             patch.object(self.persona_module, "handle_tool_call") as mock_handle_tool_call:

            # First call returns a tool call for something else (e.g., image)
            tool_call_item = MagicMock()
            tool_call_item.type = "tool_call"
            tool_call_item.name = "sd_image"

            final_response = MagicMock()
            final_response.output = []
            final_response.output_text = "Here is the image."

            mock_gpt5.return_value = MagicMock()
            mock_gpt5.return_value.output = [tool_call_item]

            mock_handle_tool_call.return_value = (final_response, "path/to/image.png")

            response = self.engine.generate_response("Draw me")

            self.assertEqual(response["text"], "Here is the image.")
            self.assertIsNone(response["audio_path"])
            self.assertEqual(response["tool_result"], "path/to/image.png")

if __name__ == "__main__":
    unittest.main()
