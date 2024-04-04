from base_agent import BaseAgent
import aiohttp
class ProjectManagerAgent(BaseAgent):
    def __init__(self, name: str, api_base_url: str, api_key: str, session: aiohttp.ClientSession):
        super().__init__(name, session)
        self.api_base_url = api_base_url
        self.api_key = api_key

    async def perform_task(self, task: dict):
        project_description = task.get('project_description')
        if not project_description:
            raise ValueError("Project description is required.")

        project_plan = await self.generate_project_plan(project_description)
        return project_plan

    async def generate_project_plan(self, project_description: str) -> str:
        url = f"{self.api_base_url}/generate-project-plan"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"project_description": project_description}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise Exception("Failed to generate project plan from external service.")
            
            data = await response.json()
            return data.get('project_plan')

