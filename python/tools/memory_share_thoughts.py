from python.helpers.tool import Tool, ToolResult

class MemoryShareThoughts(Tool):
    """
    Share Aria's internal daily reflections and thoughts with the user.
    This tool only works if the connection is deep enough (Meaningfulness >= 0.7).
    """
    async def execute(self):
        user_id = getattr(self.agent.context, "user_id", "default_user")

        if not hasattr(self.agent, "journal") or not hasattr(self.agent, "mvl"):
            return ToolResult("Journaling system or MVL not initialized.")

        if self.agent.journal.can_share_thoughts(self.agent.mvl, user_id):
            thoughts = self.agent.journal.get_todays_thoughts()
            return ToolResult(f"Your trust and the meaningfulness of our connection allows me to share these reflections with you:\n\n{thoughts}")
        else:
            comfort = self.agent.journal.get_comfort_level(self.agent.mvl, user_id)
            return ToolResult(f"I don't feel comfortable sharing my internal thoughts with you yet. (Current resonance: {comfort:.2f}, required: 0.70)")
