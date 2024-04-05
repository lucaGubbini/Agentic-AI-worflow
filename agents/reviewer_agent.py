from base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    async def perform_task(self, task: dict):
        code_snippet = task.get('code')
        if not code_snippet:
            raise ValueError("Code is required for review.")
        review = await self.agent.review_code(code_snippet)
        return {'review_results': review}
