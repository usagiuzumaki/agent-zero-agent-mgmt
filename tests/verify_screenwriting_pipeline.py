import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock

# Adjust path to import from repo root
sys.path.append(os.getcwd())

from agents.screenwriting.tools.screenwriting_pipeline import ScreenwritingPipeline

async def test_pipeline():
    # Mock the main agent
    mock_agent = MagicMock()
    mock_agent.agent_name = "TestAgent"
    mock_agent.number = 0
    mock_agent.config = MagicMock()
    mock_agent.context = MagicMock()

    # Instantiate the pipeline tool
    pipeline = ScreenwritingPipeline(
        agent=mock_agent,
        name="screenwriting_pipeline",
        method="execute",
        args={},
        message="Test message",
        loop_data={}
    )

    # Mock the _run_stage method to verify flow
    pipeline._run_stage = AsyncMock(return_value="[Stage Output]")

    print("Running pipeline with all flags...")
    response = await pipeline.execute(
        task="Test Task",
        project_name="Test Project",
        include_world_building=True,
        include_character_analysis=True,
        include_pacing=True,
        include_tension=True,
        include_marketability=True,
        include_mbti=True,
        include_scream=True,
        include_storyboard=True
    )

    print("Result Message Length:", len(response.message))

    # Expected order based on my implementation
    expected_stages = [
        "World Builder",
        "Character Analyzer",
        "MBTI Evaluator",
        "Plot Analyzer",
        "Creative Ideas",
        "Co-Writer",
        "Dialogue Evaluator",
        "Pacing Metrics",
        "Emotional Tension",
        "Scream Analyzer",
        "Script Formatter",
        "Marketability",
        "Storyboard Generator"
    ]

    calls = pipeline._run_stage.call_args_list

    print("\nVerifying Stage Execution Order:")
    all_passed = True
    for i, call in enumerate(calls):
        args, _ = call
        # _run_stage(self, AgentClass, stage_name, method_name, input_text)
        stage_name = args[1]

        expected = expected_stages[i] if i < len(expected_stages) else "NONE"

        status = "✅" if stage_name == expected else f"❌ (Expected {expected})"
        print(f"{i+1}. {stage_name:25} {status}")

        if stage_name != expected:
            all_passed = False

    if len(calls) != len(expected_stages):
        print(f"\n❌ Incorrect number of calls: {len(calls)} vs {len(expected_stages)}")
        all_passed = False

    if all_passed:
        print("\nSUCCESS: Pipeline execution order verified.")
    else:
        print("\nFAILURE: Pipeline execution order incorrect.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_pipeline())
