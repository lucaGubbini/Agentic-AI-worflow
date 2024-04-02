# project_manager_agent.py
from base_agent import BaseAgent

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ProjectManagerAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="dummy")

    async def generate_project_plan(self, description: str) -> str:
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[{"role": "system", "content": "Create a detailed project plan based on the following description."},
                      {"role": "user", "content": description}],
            temperature=0.7
        )
        return completion.choices[0].message
