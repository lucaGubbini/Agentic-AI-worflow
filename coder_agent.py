# coder_agent.py
from base_agent import BaseAgent

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class CoderAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="dummy")

    async def generate_code(self, task_description: str) -> str:
        completion = self.client.chat.completions.create(
            model="mistral instruct v0 2 7B Q8_0 ggpu",  # replace with your actual model name
            messages=[
                {"role": "system", "content": "Generate concise Python code for the task without additional comments."},
                {"role": "user", "content": task_description}
            ],
            temperature=0.3  # Lower temperature encourages more straightforward responses
        )
        # Return the content of the message directly
        return completion.choices[0].message.content
