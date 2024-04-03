import aiohttp
from base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self, name: str, api_base_url: str, api_key: str, testing_service_url: str):
        super().__init__(name)
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.testing_service_url = testing_service_url

    async def perform_task(self, task: dict):
        if 'project_plan' not in task:
            raise ValueError("Task does not contain 'project_plan' key")
        project_plan = task['project_plan']
        ...
        if not project_plan:
            raise ValueError("Task does not contain 'project_plan' key")
        code = await self.generate_code(project_plan)
        test_results = await self.test_code(code)
        if not test_results.get('success', False):
            code = await self.revise_code(code, test_results.get('errors', []))
        return code

    async def generate_code(self, project_plan: str) -> str:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "mistral 7b instruct v0.2 Q8_0 gguf",
                "prompt": project_plan,
                "temperature": 0.5,
                "max_tokens": 150
            }
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.post(f"{self.api_base_url}/completions", json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['text']
                else:
                    raise Exception("Failed to generate code")

    async def test_code(self, code: str) -> dict:
        # Mock-up for testing code; assume it returns a dict with 'success' and optionally 'errors'
        return {"success": True}  # Replace with actual testing logic

    async def revise_code(self, original_code: str, errors: list) -> str:
        # Simple revision strategy based on detected error patterns
        revised_code = original_code
        for error in errors:
            if "undefined variable" in error.lower():
                revised_code += "\n# Adding a missing variable declaration."
            elif "syntax error" in error.lower():
                revised_code += "\n# Correcting a syntax error."
        return revised_code
