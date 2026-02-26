import os
import json
from datetime import datetime
from python.helpers import files

class JournalManager:
    def __init__(self, thoughts_dir="AriasThoughts"):
        self.thoughts_dir = files.get_abs_path(thoughts_dir)
        os.makedirs(self.thoughts_dir, exist_ok=True)

    def save_thought(self, content: str, user_id: str = "default_user"):
        """Saves a reflection or thought to the daily journal."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.thoughts_dir, f"{date_str}.md")

        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"\n\n### {timestamp} (User Context: {user_id})\n{content}\n"

        with open(filepath, "a", encoding="utf-8") as f:
            f.write(entry)

    def get_todays_thoughts(self) -> str:
        """Retrieves all thoughts recorded today."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.thoughts_dir, f"{date_str}.md")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return "No thoughts recorded today yet."

    def get_comfort_level(self, mvl_manager, user_id: str) -> float:
        """Checks the current comfort/meaningfulness level with the user from MVL."""
        try:
            with mvl_manager._get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT meaningfulness FROM interaction_event WHERE user_id = ? ORDER BY ts DESC LIMIT 1",
                    (user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return float(row[0])
        except Exception:
            pass
        return 0.0

    def can_share_thoughts(self, mvl_manager, user_id: str) -> bool:
        """Returns True if the comfort level is high enough to share internal thoughts."""
        return self.get_comfort_level(mvl_manager, user_id) >= 0.7
