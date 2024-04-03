from base_agent import BaseAgent
from openai import OpenAI

class CoderAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        # Initialize the OpenAI client with the specified base URL and API key
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    async def generate_code(self, project_plan: str) -> str:
        """
        Generates code based on the project plan by querying an AI model.
        """
        # Use the OpenAI client to make a request to the chat completion endpoint
        completion = self.client.chat.completions.create(
            model="mistral instruct v0 2 7B Q8_0 ggpu",  # Adjust with the actual model name
            messages=[
                {"role": "system", "content": "Generate a code snippet based on the project plan."},
                {"role": "user", "content": project_plan}
            ],
            temperature=0.5
        )
        # Return the generated code snippet from the completion response
        return completion.choices[0].message.content
