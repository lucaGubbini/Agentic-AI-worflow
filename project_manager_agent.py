import aiohttp
from base_agent import BaseAgent

class ProjectManagerAgent(BaseAgent):
    def __init__(self, name: str, api_base_url: str, api_key: str):
        super().__init__(name)
        self.api_base_url = api_base_url
        self.api_key = api_key

    async def perform_task(self, task: dict):
        project_description = task.get('project_description')
        if not project_description:
            raise ValueError("Task does not contain 'project_description' key")
        project_plan = await self.generate_project_plan(project_description)
        return project_plan

    async def generate_project_plan(self, project_description: str) -> str:
        async with aiohttp.ClientSession() as session:
            payload = {
                "prompt": f"Create a succinct project plan based on the following description:\n\n{project_description}",
                "temperature": 0.5,
                "max_tokens": 100,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "stop": ["\n"]
            }
            headers = {"Authorization": f"Bearer {self.api_key}"}
            async with session.post(f"{self.api_base_url}/completions", json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    project_plan = data['choices'][0]['text'].strip()
                    return project_plan
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed to generate project plan: {response_text}")

