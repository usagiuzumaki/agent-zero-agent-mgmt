### screenwriting_specialist:
- Use this tool to consult a specific screenwriting expert agent.
- Arguments: `specialist` (name) and `task` (instruction).
- Available specialists:
  - `PlotAnalyzer`: Structure and beats.
  - `CreativeIdeas`: Brainstorming twists/concepts.
  - `CoWriter`: Drafting scenes/chapters.
  - `DialogueEvaluator`: Refining dialogue.
  - `ScriptFormatter`: Formatting to Fountain/HTML.
  - `CharacterAnalyzer`: Deep character arcs.
  - `PacingMetrics`: Story pacing analysis.
  - `EmotionalTension`: Emotional arc tracking.
  - `Marketability`: Commercial potential assessment.
  - `MBTIEvaluator`: Character personality analysis.
  - `WorldBuilder`: Setting and lore development.
  - `ScreamAnalyzer`: Horror/thriller specific analysis.
  - `StoryboardGenerator`: Visual storyboard descriptions.

**Example usage**:
~~~json
{
    "thoughts": ["I need to check the pacing of this scene."],
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "PacingMetrics",
        "task": "Analyze the pacing of the chase scene in Act 2."
    }
}
~~~
