from python.helpers.extension import Extension

class MVLInstructions(Extension):
    async def execute(self, system_prompt, loop_data, **kwargs):
        mvl_instr = loop_data.params_temporary.get("mvl_instruction")
        if mvl_instr:
            # Inject into system prompt to guide the agent's behavior
            system_prompt.append(f"\n[INTERNAL STATE / MANDATE: {mvl_instr}]\n")
