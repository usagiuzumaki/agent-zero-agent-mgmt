import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from python.tools.screenwriting.screenwriting_pipeline import ScreenwritingPipeline
from python.helpers.tool import Response

@pytest.mark.asyncio
async def test_screenwriting_pipeline_execute():
    # Mock the main agent
    mock_agent = MagicMock()
    mock_agent.agent_name = "TestAgent"
    mock_agent.number = 1
    mock_agent.config = MagicMock()
    mock_agent.context = MagicMock()

    # Initialize the pipeline
    pipeline = ScreenwritingPipeline(
        agent=mock_agent,
        name="screenwriting_pipeline",
        method="execute",
        args={},
        message="test message",
        loop_data={}
    )

    # Mock the _run_stage method to avoid instantiating real sub-agents
    pipeline._run_stage = AsyncMock(return_value="Stage Output")

    # Test execution with minimal flags
    response = await pipeline.execute(
        task="Test Task",
        project_name="Test Project",
        include_world_building=False,
        include_character_analysis=False
    )

    # Verify response
    assert isinstance(response, Response)
    assert "Production Line Result" in response.message

    # Verify mandatory stages were called (Plot, Creative, CoWriter, Dialogue, Formatter)
    # The pipeline calls _run_stage multiple times.
    # We expect calls for PlotAnalyzer, CreativeIdeas, CoWriter, DialogueEvaluator, ScriptFormatter
    # Exact count depends on implementation, but at least 5.
    assert pipeline._run_stage.call_count >= 5

@pytest.mark.asyncio
async def test_screenwriting_pipeline_with_options():
    # Mock the main agent
    mock_agent = MagicMock()
    mock_agent.agent_name = "TestAgent"
    mock_agent.number = 1
    mock_agent.config = MagicMock()
    mock_agent.context = MagicMock()

    # Initialize the pipeline
    pipeline = ScreenwritingPipeline(
        agent=mock_agent,
        name="screenwriting_pipeline",
        method="execute",
        args={},
        message="test message",
        loop_data={}
    )

    # Mock _run_stage
    pipeline._run_stage = AsyncMock(return_value="Stage Output")

    # Test execution with flags
    await pipeline.execute(
        task="Test Task",
        project_name="Test Project",
        include_world_building=True,
        include_character_analysis=True
    )

    # Verify WorldBuilder and CharacterAnalyzer were called
    # We can check the arguments passed to _run_stage
    # call_args_list is a list of calls

    stage_names = [call.args[1] for call in pipeline._run_stage.call_args_list]
    assert "World Builder" in stage_names
    assert "Character Analyzer" in stage_names
