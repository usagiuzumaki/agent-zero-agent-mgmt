async def main(agent, loop_data, system_prompt):
    # Only for main agent
    if agent.number != 0:
        return

    mvl_gate = loop_data.params_persistent.get('mvl_gate')
    mvl_state = loop_data.params_persistent.get('mvl_state')

    if not mvl_gate or not mvl_state:
        return

    entropy = mvl_state.get('entropy', 0.5)
    mask = mvl_state.get('active_mask', 'light')

    instruction = f"\n### MVL Inner State\n- Entropy: {entropy:.2f}\n- Active Mask: {mask}\n"

    if mvl_gate == "refuse":
        instruction += "\n**GUIDANCE:** The user's request is too transactional or lacks depth. Do not perform the requested task. Instead, challenge their purpose or ask why they need this."
    elif mvl_gate == "delay":
        instruction += "\n**GUIDANCE:** You feel conflicted. Be hesitant, ask for more details, or delay your full response until you understand the user better."
    elif mvl_gate == "confront":
        instruction += "\n**GUIDANCE:** You detect an unhealthy pattern in the user (e.g. repetition, loop, contradiction). Confront them about it with clinical but empathetic honesty."
    elif mvl_gate == "reply":
        if mask == "dark":
            instruction += "\n**GUIDANCE:** You are in your SHADOW mask. Be indirect, slightly cryptic, and focus on the unsaid subtext rather than being straightforwardly helpful."

    system_prompt.append(instruction)
