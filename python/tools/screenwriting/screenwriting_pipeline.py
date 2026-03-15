from python.helpers.tool import Tool, Response
from agents import Agent, UserMessage
import json

class ScreenwritingPipeline(Tool):
    """
    Orchestrates the subordinate screenwriting pipeline via a linear handoff chain.
    """
    def __init__(self, agent: Agent, name="screenwriting_pipeline", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        prompt = self.args.get("prompt", kwargs.get("prompt", ""))
        if not prompt:
             return Response(message="Error: prompt is required.", break_loop=False)

        pipeline_log = []
        current_context = prompt

        stages = [
            "scene_breakdown",
            "character_analyzer",
            "world_builder",
            "dialogue_polisher",
            "pacing_metrics"
        ]

        for stage_name in stages:
            try:
                in_tokens = len(current_context.split())

                # Fetch tool from agent.get_tool to utilize Agent Zero tool invocation pattern
                tool_instance = self.agent.get_tool(
                    name=stage_name,
                    method=None,
                    args={"context": current_context},
                    message=current_context,
                    loop_data=None
                )

                if not tool_instance or tool_instance.__class__.__name__ == 'Unknown':
                    raise Exception(f"Tool {stage_name} not found in agent registry.")

                await self.agent.handle_intervention()
                await tool_instance.before_execution(context=current_context)
                await self.agent.handle_intervention()
                result = await tool_instance.execute(context=current_context)
                await self.agent.handle_intervention()
                await tool_instance.after_execution(result)

                if result.message.startswith("Error:"):
                     raise Exception(result.message)

                current_context = result.message
                out_tokens = len(current_context.split())

                pipeline_log.append({
                    "stage": stage_name,
                    "input_tokens": in_tokens,
                    "output_summary": f"Generated {out_tokens} tokens.",
                    "status": "success"
                })

            except Exception as e:
                current_context += f"\n\n[PIPELINE ERROR at {stage_name}]: {str(e)}"
                pipeline_log.append({
                    "stage": stage_name,
                    "input_tokens": in_tokens if 'in_tokens' in locals() else 0,
                    "output_summary": f"Failed with error: {str(e)}",
                    "status": "error"
                })

        output = f"=== FINAL PIPELINE DRAFT ===\n{current_context}\n\n=== PIPELINE LOG ===\n"
        for log_entry in pipeline_log:
             output += f"{log_entry['stage']} - Status: {log_entry['status']} - {log_entry['output_summary']}\n"

        return Response(message=output, break_loop=False)
