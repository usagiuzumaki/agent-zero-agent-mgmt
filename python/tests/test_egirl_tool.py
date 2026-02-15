import unittest
from unittest.mock import MagicMock, patch
import sys
import asyncio

# Import the tool class.
from agents.egirl.tools.egirl_tool import EgirlTool

class TestEgirlTool(unittest.TestCase):
    def setUp(self):
        self.mock_agent = MagicMock()
        self.mock_loop_data = MagicMock()
        self.tool = EgirlTool(
            agent=self.mock_agent,
            name="egirl_tool",
            method=None,
            args={},
            message="dummy message",
            loop_data=self.mock_loop_data
        )

    def test_post_instagram(self):
        mock_insta = MagicMock()
        mock_insta.post_image.return_value = {"id": "123"}

        with patch.dict(sys.modules, {"python.helpers.egirl.instagram": mock_insta}):
            # Execute
            response = asyncio.run(self.tool.execute(
                task="post_instagram",
                image_url="http://example.com/img.jpg",
                caption="Hello world"
            ))

            # Verify
            mock_insta.post_image.assert_called_once_with("http://example.com/img.jpg", "Hello world")
            self.assertIn("{'id': '123'}", response.message)

    def test_generate_image(self):
        mock_sd = MagicMock()
        mock_sd.generate_image.return_value = "outputs/image.png"

        with patch.dict(sys.modules, {"python.helpers.stable_diffusion": mock_sd}):
            # Execute
            response = asyncio.run(self.tool.execute(
                task="generate_image",
                prompt="A cute cat",
                output_dir="outputs"
            ))

            # Verify
            mock_sd.generate_image.assert_called_once_with("A cute cat", output_dir="outputs")
            self.assertEqual(response.message, "generated outputs/image.png")

    def test_generate_voice(self):
        mock_eleven = MagicMock()
        mock_eleven.text_to_speech.return_value = "outputs/voice.mp3"

        with patch.dict(sys.modules, {"python.helpers.egirl.elevenlabs": mock_eleven}):
            # Execute
            response = asyncio.run(self.tool.execute(
                task="generate_voice",
                text="Hello",
                output_path="outputs/voice.mp3"
            ))

            # Verify
            mock_eleven.text_to_speech.assert_called_once_with("Hello", "outputs/voice.mp3")
            self.assertEqual(response.message, "voice at outputs/voice.mp3")

    def test_stripe_checkout(self):
        mock_stripe = MagicMock()
        mock_stripe.create_checkout_session.return_value = "http://stripe.com/checkout"

        with patch.dict(sys.modules, {"python.helpers.egirl.stripe": mock_stripe}):
            # Execute
            response = asyncio.run(self.tool.execute(
                task="stripe_checkout",
                price_id="price_123",
                success_url="http://success",
                cancel_url="http://cancel"
            ))

            # Verify
            mock_stripe.create_checkout_session.assert_called_once_with("price_123", "http://success", "http://cancel")
            self.assertEqual(response.message, "http://stripe.com/checkout")

    def test_persona_chat(self):
        mock_persona_module = MagicMock()
        mock_engine_instance = MagicMock()
        mock_persona_module.PersonaEngine.return_value = mock_engine_instance

        mock_engine_instance.generate_response.return_value = {
            "text": "Hi there!",
            "audio_path": "audio.mp3",
            "tool_result": None
        }

        with patch.dict(sys.modules, {"python.helpers.egirl.persona": mock_persona_module}):
            # Execute
            response = asyncio.run(self.tool.execute(
                task="persona_chat",
                message="Hi",
                name="Aria"
            ))

            # Verify
            mock_persona_module.PersonaEngine.assert_called_once_with("Aria")
            mock_engine_instance.generate_response.assert_called_once_with("Hi")
            self.assertIn("Hi there!", response.message)
            self.assertIn("(audio: audio.mp3)", response.message)

if __name__ == "__main__":
    unittest.main()
