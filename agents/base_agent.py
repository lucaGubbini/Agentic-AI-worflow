from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Defines a basic structure for different types of agents."""
    
    def __init__(self, name: str, agent=None, config: dict = None):
        self.name = name
        self.agent = agent
        self.config = config or {}

    @abstractmethod
    async def perform_task(self, task: dict):
        """Abstract method to be implemented by subclasses for performing tasks."""
        pass
