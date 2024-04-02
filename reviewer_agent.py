# reviewer_agent.py
from base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    async def perform_task(self, task: dict):
        print(f"{self.name} is reviewing code for: {task['description']}")
        # Implement code reviewing logic here
