from python.helpers.extension import Extension
from python.helpers.mvl_manager import MVLManager
from python.helpers.journal_manager import JournalManager

class MVLInit(Extension):
    async def execute(self, **kwargs):
        if not hasattr(self.agent, "mvl"):
            self.agent.mvl = MVLManager(agent=self.agent)
        if not hasattr(self.agent, "journal"):
            self.agent.journal = JournalManager()
