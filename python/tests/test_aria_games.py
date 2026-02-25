
import pytest
from unittest.mock import MagicMock, patch
from python.tools.aria_games import AriaGames
import os

class TestAriaGames:
    @pytest.fixture
    def mock_agent(self):
        agent = MagicMock()
        agent.context.log.log = MagicMock()
        return agent

    @pytest.mark.asyncio
    async def test_start_story_image_generation_call(self, mock_agent):
        """Test that start_story attempts to generate an image."""
        tool = AriaGames(
            agent=mock_agent,
            name="aria_games",
            method="execute",
            args={},
            message="Test message",
            loop_data=None
        )

        # Mock generate_image from stable_diffusion
        # We need to mock it where it is imported in the module under test
        with patch('python.tools.aria_games.generate_image') as mock_generate:
            # Mock return value (filepath)
            mock_generate.return_value = "/path/to/outputs/generated_image.png"

            # Start story
            response = await tool.execute(action="start_story", story_type="romantic_evening")

            # Verify generate_image was called
            assert mock_generate.called
            args, _ = mock_generate.call_args
            # Verify prompt is a string (checking exact prompt is brittle as it comes from random selection or fixed template)
            assert isinstance(args[0], str)

            # Verify the image URL is in the response message and formatted correctly
            expected_url = "/api/public_image?filename=generated_image.png"
            assert expected_url in response.message

    @pytest.mark.asyncio
    async def test_start_roleplay_image_generation_call(self, mock_agent):
        """Test that start_roleplay attempts to generate an image."""
        tool = AriaGames(
            agent=mock_agent,
            name="aria_games",
            method="execute",
            args={},
            message="Test message",
            loop_data=None
        )

        with patch('python.tools.aria_games.generate_image') as mock_generate:
            mock_generate.return_value = "/path/to/outputs/roleplay_image.png"

            response = await tool.execute(action="start_roleplay", scenario_type="space_explorer")

            assert mock_generate.called
            expected_url = "/api/public_image?filename=roleplay_image.png"
            assert expected_url in response.message

    @pytest.mark.asyncio
    async def test_image_generation_failure(self, mock_agent):
        """Test graceful handling of image generation failure."""
        tool = AriaGames(
            agent=mock_agent,
            name="aria_games",
            method="execute",
            args={},
            message="Test message",
            loop_data=None
        )

        with patch('python.tools.aria_games.generate_image') as mock_generate:
            # Simulate failure
            mock_generate.side_effect = Exception("Generation failed")

            response = await tool.execute(action="start_story", story_type="romantic_evening")

            # Verify exception was logged
            assert mock_agent.context.log.log.called
            call_args = mock_agent.context.log.log.call_args[1]
            assert call_args['type'] == 'error'
            assert "Generation failed" in call_args['content']

            # Message should still exist but without image
            assert "Our Perfect Evening" in response.message
            assert "Scene image" not in response.message
