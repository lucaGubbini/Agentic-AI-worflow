# project_manager_agent.py
from base_agent import BaseAgent

from openai import OpenAI

# Inside project_manager_agent.py or a new file test_agent.py
import subprocess

def run_tests(test_file: str):
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    return result.stdout


client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ProjectManagerAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    async def generate_project_plan(self, project_description: str) -> str:
        completion = self.client.chat.completions.create(
            model="mistral instruct v0 2 7B Q8_0 ggpu",  # replace with your actual model name
            messages=[
                {"role": "system", "content": "Create a succinct project plan based on the description, avoiding any unnecessary details."},
                {"role": "user", "content": project_description}
            ],
            temperature=0.5
        )
        # Return the content of the message directly
        return completion.choices[0].message.content