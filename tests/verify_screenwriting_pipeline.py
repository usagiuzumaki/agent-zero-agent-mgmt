import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock

# Mock modules BEFORE importing from repo
sys.modules["nest_asyncio"] = MagicMock()
sys.modules["litellm"] = MagicMock()
sys.modules["regex"] = MagicMock()
sys.modules["tiktoken"] = MagicMock()
sys.modules["git"] = MagicMock()
sys.modules["psutil"] = MagicMock()
sys.modules["diskcache"] = MagicMock()
sys.modules["crontab"] = MagicMock()
sys.modules["yaml"] = MagicMock()
sys.modules["pytz"] = MagicMock()
sys.modules["paramiko"] = MagicMock()
sys.modules["dotenv"] = MagicMock()
sys.modules["aiohttp"] = MagicMock()
sys.modules["webcolors"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["cryptography"] = MagicMock()
sys.modules["cryptography.hazmat"] = MagicMock()
sys.modules["cryptography.hazmat.primitives"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.asymmetric"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.hashes"] = MagicMock()
sys.modules["cryptography.hazmat.primitives.serialization"] = MagicMock()
sys.modules["langchain"] = MagicMock()
sys.modules["langchain_community"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_core.language_models"] = MagicMock()
sys.modules["langchain_core.language_models.chat_models"] = MagicMock()
sys.modules["langchain_core.language_models.llms"] = MagicMock()
sys.modules["langchain_core.outputs"] = MagicMock()
sys.modules["langchain_core.outputs.chat_generation"] = MagicMock()
sys.modules["langchain_core.callbacks"] = MagicMock()
sys.modules["langchain_core.callbacks.manager"] = MagicMock()
sys.modules["flask"] = MagicMock()
sys.modules["flask_basicauth"] = MagicMock()
sys.modules["flask_login"] = MagicMock()
sys.modules["flask_sqlalchemy"] = MagicMock()
sys.modules["simpleeval"] = MagicMock()
sys.modules["flaredantic"] = MagicMock()
sys.modules["pathspec"] = MagicMock()
sys.modules["python-crontab"] = MagicMock()
sys.modules["a2wsgi"] = MagicMock()
sys.modules["flask_cors"] = MagicMock()
sys.modules["faiss-cpu"] = MagicMock()
sys.modules["numpy"] = MagicMock()
sys.modules["elevenlabs"] = MagicMock()
sys.modules["diffusers"] = MagicMock()
sys.modules["torch"] = MagicMock()
sys.modules["browser-use"] = MagicMock()
sys.modules["fastmcp"] = MagicMock()
sys.modules["models"] = MagicMock()

# Adjust path to import from repo root
sys.path.append(os.getcwd())

# Import after mocking
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
    # Corrected arguments based on ScreenwritingPipeline definition
    response = await pipeline.execute(
        task="Test Task",
        project_name="Test Project",
        include_world_building=True,
        include_character_analysis=True,
        include_pacing=True,
        include_tension=True,      # Fixed name
        include_marketability=True,
        include_mbti=True,
        include_scream=True,       # Fixed name
        include_storyboard=True
    )

    print("Result Message Length:", len(response.message))

    # Expected order based on my implementation
    expected_stages = [
        "World Builder",
        "Character Analyzer",
        "MBTI Evaluator", # Called inside character analysis block if include_character_analysis and include_mbti
        "Plot Analyzer",
        "Creative Ideas",
        "Co-Writer",
        "Dialogue Evaluator",
        "Pacing Metrics",
        "Emotional Tension",
        "Scream Analyzer",
        # MBTI might be called again if include_character_analysis is False, but here it is True.
        # Wait, let's check code logic for MBTI.
        "Script Formatter",
        "Marketability",
        "Storyboard Generator"
    ]

    # Let's double check MBTI logic in code:
    # if include_character_analysis:
    #     results.append(await self._run_stage(CharacterAnalyzer, ...))
    #     if include_mbti:
    #         report = await self._run_stage(MBTIEvaluator, ...)
    # ...
    # if include_mbti and not include_character_analysis:
    #      report = await self._run_stage(MBTIEvaluator, ...)

    # So if both are True, it runs ONCE after Character Analyzer.

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
