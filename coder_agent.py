from base_agent import BaseAgent
import aiohttp

class CoderAgent(BaseAgent):
    def __init__(self, name: str, api_base_url: str, api_key: str, session: aiohttp.ClientSession):
        super().__init__(name, session)
        self.api_base_url = api_base_url
        self.api_key = api_key

    async def perform_task(self, task: dict):
        project_plan = task.get('project_plan')
        if not project_plan:
            raise ValueError("Project plan is required.")

        code = await self.generate_code(project_plan)
        return code

    async def generate_code(self, project_plan: str) -> str:
        url = f"{self.api_base_url}/generate-code"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"project_plan": project_plan}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise Exception("Failed to generate code from external service.")
            
            data = await response.json()
            return data.get('code')
