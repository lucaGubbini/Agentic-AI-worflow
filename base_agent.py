# base_agent.py
class BaseAgent:
    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.config = config or {}

    async def perform_task(self, task: dict):
        pass

    def communicate(self, message: str, target_agent: 'BaseAgent'):
        print(f"{self.name} to {target_agent.name}: {message}")
        target_agent.receive_message(message)

    def receive_message(self, message: str):
        print(f"{self.name} received: {message}")
