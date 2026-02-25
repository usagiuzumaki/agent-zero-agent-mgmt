from python.helpers.mvl_manager import MVLManager
from python.helpers.print_style import PrintStyle
from python.helpers.errors import SilentResponseException

async def main(agent, loop_data):
    # Only run for main agent
    if agent.number != 0:
        return

    # Only process on the first iteration (the user message)
    if loop_data.iteration != 0:
        return

    user_id = getattr(agent.context, 'user_id', 'default_user')
    last_user_msg = agent.last_user_message
    if not last_user_msg:
         return

    # Extract text from history message
    text = ""
    if isinstance(last_user_msg.content, str):
         text = last_user_msg.content
    elif isinstance(last_user_msg.content, dict):
         # Our history messages are often dicts from templates
         text = last_user_msg.content.get('message', '')

    if not text:
         return

    mvl = MVLManager(agent=agent)
    gate = await mvl.process_message(user_id, text)

    # Store MVL state in loop_data for other extensions (like system_prompt)
    loop_data.params_persistent['mvl_gate'] = gate

    # Get current state for prompt injection
    state = mvl.get_state(user_id)
    loop_data.params_persistent['mvl_state'] = state

    PrintStyle().info(f"MVL analysis complete. Gate: {gate.upper()} | Entropy: {state['entropy']:.2f} | Mask: {state['active_mask']}")

    if gate == "silence":
         raise SilentResponseException()
