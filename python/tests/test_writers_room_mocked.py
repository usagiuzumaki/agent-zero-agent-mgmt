import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock agents to avoid Litellm and Langchain dependencies
sys.modules['agents'] = MagicMock()
sys.modules['agents.agent'] = MagicMock()

# Import Tool after mocking
from python.helpers.tool import Tool, Response

# Now import the tools to test
from python.tools.writers_room import ToolGeneratePlotTwist, ToolRewriteFromPerspective

def test_tool_generate_plot_twist():
    tool = ToolGeneratePlotTwist(agent=None, name="generate_plot_twist", method=None, args={"current_scenario": "The hero meets the villain", "twist_type": "Betrayal", "twist_description": "The hero's mentor is actually the villain."}, message="", loop_data=None)

    response = __import__('asyncio').run(tool.execute())
    assert "PLOT TWIST" in response.message
    assert "Betrayal" in response.message
    assert "The hero's mentor" in response.message
    assert "The hero meets the villain" in response.message

def test_tool_rewrite_from_perspective():
    tool = ToolRewriteFromPerspective(agent=None, name="rewrite_from_perspective", method=None, args={"new_perspective_character": "The cat", "rewritten_scene": "Meow meow, the humans are fighting."}, message="", loop_data=None)

    response = __import__('asyncio').run(tool.execute())
    assert "PERSPECTIVE SHIFT" in response.message
    assert "The cat" in response.message
    assert "Meow meow" in response.message
