# reviewer_agent.py
from base_agent import BaseAgent

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class ReviewerAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    async def review_code(self, code_snippet: str) -> str:
        completion = self.client.chat.completions.create(
            model="mistral instruct v0 2 7B Q8_0 ggpu",  # replace with your actual model name
            messages=[
                {"role": "system", "content": "Review the Python code focusing on code quality, performance, and security. Only mention comments if they are misused or necessary for understanding complex logic. Ensure the code follows best practices. Ensure that there are no syntax errors."},
                {"role": "user", "content": code_snippet}
            ],
            temperature=0.5
        )
        # Return the content of the message directly
        return completion.choices[0].message.content