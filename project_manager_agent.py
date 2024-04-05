from base_agent import BaseAgent
import asyncio

class ProjectManagerAgent(BaseAgent):
    def __init__(self, name: str, agent):
        super().__init__(name, agent)

    async def perform_task(self, task: dict):
        project_description = task.get('project_description')
        if not project_description:
            raise ValueError("Project description is required.")

        project_plan = await self.generate_project_plan(project_description)
        return {'project_plan': project_plan}

    async def generate_project_plan(self, project_description: str) -> str:
        # Utilize the MemGPT agent to generate a project plan from the description
        response = await self.agent.process_request(project_description)
        return response
