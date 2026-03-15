# Screenwriting Tools Audit

## 1. Inventory of Files & Classes

- `ToolInjectFourthWallBreak` found in `python/tools/writers_room.py`
- `ToolFormatActionSequence` found in `python/tools/writers_room.py`
- `ToolGenerateCharacterMotivation` found in `python/tools/writers_room.py`
- `ToolEscalateTension` found in `python/tools/writers_room.py`
- `ToolWriteDialogue` found in `python/tools/writers_room.py`
- `ToolOptimizePacing` found in `python/tools/writers_room.py`
- `ToolWeaveBackstory` found in `python/tools/writers_room.py`
- `ToolWriteClimax` found in `python/tools/writers_room.py`
- `ToolGeneratePlotTwist` found in `python/tools/writers_room.py`
- `ToolRewriteFromPerspective` found in `python/tools/writers_room.py`
- `ScriptOrchestrator` found in `python/tools/writers_room.py`

## 2. Inventory of Prompts

- `agents/egirl/prompts/agent.system.tool.screenwriting.md`
- `agents/egirl/prompts/agent.system.tool.screenwriting_specialist.md`
- `agents/egirl/prompts/agent.system.tool.screenwriting_pipeline.md`

## 3. Findings

1. No `python/tools/screenwriting` folder exists yet.
2. Expected classes (CharacterAnalyzer, WorldBuilder, PacingMetrics, DialoguePolisher, SceneBreakdown, ScreenwritingPipeline, ScreenwritingSpecialist) are either missing or need to be built/renamed from writers_room.py.
3. Prompts are missing for the individual tools.
4. __init__.py does not export these properly yet.
