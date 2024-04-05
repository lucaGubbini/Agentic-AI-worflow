from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str, agent=None, config: dict = None):
        self.name = name
        self.agent = agent
        self.config = config or {}

    @abstractmethod
    async def perform_task(self, task: dict):
        pass
