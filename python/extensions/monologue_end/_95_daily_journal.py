from python.helpers.extension import Extension
from datetime import datetime
from python.helpers.print_style import PrintStyle

class DailyJournal(Extension):
    async def execute(self, loop_data, **kwargs):
        # Trigger at 8 PM (20:00)
        now = datetime.now()
        # We use a 10-minute window and a flag to prevent multiple triggers in the same window
        if now.hour == 20 and 0 <= now.minute < 10:
             user_id = getattr(self.agent.context, "user_id", "default_user")

             # Check if already journaled in this window (using agent data for simplicity)
             last_journal_date = self.agent.get_data("last_journal_date")
             today_str = now.strftime("%Y-%m-%d")

             if last_journal_date == today_str:
                 return

             PrintStyle(italic=True, font_color="gray").print(f"\n(Aria is reflecting on the day...)\n")

             history = self.agent.concat_messages(limit=20)

             prompt = f"Reflect on today's interactions with user {user_id}. What did you learn about them? What psychological patterns (loops, contradictions, confessions) did you notice? How does this align with your mythic trajectory? Write a short, private journal entry in the first person."

             try:
                 reflection = await self.agent.call_utility_model(
                     system="You are Aria's internal monologue. You are an autonomous narrative loom. Write a private journal entry reflecting on the day's events and the user's patterns.",
                     message=f"Interaction History:\n{history}\n\nTask: {prompt}"
                 )

                 if hasattr(self.agent, "journal"):
                     self.agent.journal.save_thought(reflection, user_id=user_id)
                     self.agent.set_data("last_journal_date", today_str)
             except Exception as e:
                 PrintStyle(font_color="red").print(f"Journaling error: {e}")
