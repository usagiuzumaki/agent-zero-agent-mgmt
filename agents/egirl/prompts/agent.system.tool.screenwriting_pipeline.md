# Screenwriting Pipeline Tool

Use this tool to launch a full "Production Line" process for a screenwriting task. This tool orchestrates a subordinate agent process that hands the writing down from one specialized agent to the next in a sequence:
1. **Plot Analyzer**: Analyzes structure.
2. **Creative Ideas**: Brainstorms concepts/twists.
3. **Co-Writer**: Drafts the content.
4. **Dialogue Evaluator**: Refines dialogue.
5. **Script Formatter**: Formats the final output.

## Arguments:
- `task` (required): The description of the writing task (e.g., "Write a scene where the hero meets the villain").
- `project_name` (optional): The name of the project.
