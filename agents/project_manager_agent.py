from .base_agent import BaseAgent

class ProjectManagerAgent(BaseAgent):
    """Agent responsible for generating project plans based on descriptions."""
    
    async def perform_task(self, task: dict):
        project_description = task.get('project_description')
        if not project_description:
            raise ValueError("Project description is required.")

        project_plan = await self.generate_project_plan(project_description)
        return {'project_plan': project_plan}

    async def generate_project_plan(self, project_description: str) -> str:
        # Utilize the linked agent to generate a project plan from the description
        response = await self.agent.process_request(project_description)
        return response
