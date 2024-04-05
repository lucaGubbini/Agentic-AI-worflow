from .base_agent import BaseAgent

class CoderAgent(BaseAgent):
    async def perform_task(self, task: dict):
        project_plan = task.get('project_plan')
        if not project_plan:
            raise ValueError("Project plan is required.")
        code = await self.agent.generate_code(project_plan)
        return {'code': code}
