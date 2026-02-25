from python.helpers.journal_manager import JournalManager
from python.helpers.print_style import PrintStyle

async def main(agent, loop_data):
    # Only run for the main agent (number 0) to avoid duplicates from subordinate agents
    if agent.number != 0:
        return

    journal_manager = JournalManager(agent=agent)

    if journal_manager.should_journal_now():
        PrintStyle().info("8 PM reached. Core Aria is starting her silent daily reflection...")

        # Get user_id from context
        user_id = getattr(agent.context, 'user_id', 'default_user')

        # Run journaling in the background to not delay the response
        import asyncio
        asyncio.create_task(journal_manager.generate_daily_reflection(user_id))
