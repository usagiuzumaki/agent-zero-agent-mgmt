import pytest
import os
import json
from unittest.mock import MagicMock

from python.tools.writers_room import ScriptOrchestrator
from agents import Agent

class MockAgent:
    def __init__(self):
        pass

@pytest.fixture
def mock_agent():
    return MagicMock(spec=Agent)

@pytest.mark.asyncio
async def test_writers_room_orchestrator(mock_agent):
    orchestrator = ScriptOrchestrator(mock_agent)

    initial_script = "Scene 1: Int. Tavern - Night"
    response = await orchestrator.execute(initial_script=initial_script)

    assert response.break_loop == False

    message = response.message

    # Check trace output
    assert "Aria is initiating the Showrunner & Lead Architect sequence..." in message
    assert "Passing the baton to: Meta-Humor Specialist..." in message
    assert "Passing the baton to: Arcade Action Junkie..." in message
    assert "Passing the baton to: Mystical Loreweaver..." in message
    assert "Passing the baton to: High-Stakes Closer..." in message
    assert "Aria has received the final script back. Execution complete." in message

    # Check final state marker
    assert "=== FINAL SCRIPT STATE ===" in message

    # Check the actual script modifications
    assert initial_script in message
    assert "[Processed by Meta-Humor Specialist]" in message
    assert "Applied tools: inject_fourth_wall_break, write_dialogue" in message
    assert "[Processed by Arcade Action Junkie]" in message
    assert "Applied tools: format_action_sequence, optimize_pacing" in message
    assert "[Processed by Mystical Loreweaver]" in message
    assert "Applied tools: generate_character_motivation, weave_backstory" in message
    assert "[Processed by High-Stakes Closer]" in message
    assert "Applied tools: escalate_tension, write_climax" in message

@pytest.mark.asyncio
async def test_writers_room_orchestrator_missing_script(mock_agent):
    orchestrator = ScriptOrchestrator(mock_agent)

    response = await orchestrator.execute()

    assert response.break_loop == False
    assert "Error: initial_script is required." in response.message
