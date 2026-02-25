from python.helpers.api import ApiHandler, Request, Response
from python.helpers.journal_manager import JournalManager
from datetime import datetime
import os

class JournalGet(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        date_str = input.get("date") # Expected YYYY-MM-DD
        ctxid = input.get("context")

        context = self.get_context(ctxid)
        user_id = getattr(context, 'user_id', 'default_user')

        journal_manager = JournalManager()

        # Check comfort level
        comfort = journal_manager.get_comfort_level(user_id)
        if comfort < 0.7:
             return {
                 "error": "Aria is not yet comfortable sharing these deep thoughts with you.",
                 "comfort_level": f"{comfort:.2f}/0.70"
             }

        path = journal_manager.get_journal_path()
        if date_str:
             try:
                 date = datetime.strptime(date_str, "%Y-%m-%d")
                 path = journal_manager.get_journal_path(date)
             except:
                 return {"error": "Invalid date format. Use YYYY-MM-DD."}

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {
                "content": content,
                "date": date_str or datetime.now().strftime("%Y-%m-%d"),
                "comfort_level": f"{comfort:.2f}"
            }
        else:
            return {"error": "Journal entry not found for this date."}
