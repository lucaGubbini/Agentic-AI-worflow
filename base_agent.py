import aiohttp

class BaseAgent:
    def __init__(self, name: str, session: aiohttp.ClientSession, config: dict = None):
        self.name = name
        self.session = session
        self.config = config or {}

    async def perform_task(self, task: dict):
        raise NotImplementedError("This method must be implemented by subclasses.")
