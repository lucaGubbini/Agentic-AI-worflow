# reviewer_agent.py
from base_agent import BaseAgent

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class ReviewerAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="dummy")

    async def review_code(self, code: str) -> str:
        completion = self.client.chat.completions.create(
            model="local-model",
            messages=[{"role": "system", "content": "Review the following Python code for best practices and suggest improvements."},
                      {"role": "user", "content": code}],
            temperature=0.7
        )
        return completion.choices[0].message
