from python.helpers.tool import Tool, Response
from python.helpers.journal_manager import JournalManager
from datetime import datetime

class MemoryShareThoughts(Tool):
    """
    Allows Aria to check her comfort level and share a link to her private journal ('AriasThoughts') if she trusts the user enough.
    Comfort is determined by the meaningfulness of recent interactions.
    """
    async def execute(self, date: str = None):
        user_id = getattr(self.agent.context, 'user_id', 'default_user')
        jm = JournalManager(agent=self.agent)
        comfort = jm.get_comfort_level(user_id)

        target_date = date or datetime.now().strftime("%Y-%m-%d")

        if comfort >= 0.7:
            # In a real UI, this would be a proper URL.
            # For now, we provide the API path that the frontend can call.
            link = f"/journal_get?date={target_date}&context={self.agent.context.id}"
            return Response(
                message=f"COMFORT CHECK: PASSED ({comfort:.2f} >= 0.70). You may share the thoughts for {target_date}. Link: {link}",
                break_loop=False
            )
        else:
            return Response(
                message=f"COMFORT CHECK: FAILED ({comfort:.2f} < 0.70). You do not feel comfortable sharing your inner thoughts yet. Encourage more meaningful conversation.",
                break_loop=False
            )
