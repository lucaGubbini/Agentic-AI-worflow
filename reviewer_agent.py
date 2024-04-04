from base_agent import BaseAgent
import aiohttp
class ReviewerAgent(BaseAgent):
    def __init__(self, name: str, api_base_url: str, api_key: str, session: aiohttp.ClientSession):
        super().__init__(name, session)
        self.api_base_url = api_base_url
        self.api_key = api_key

    async def perform_task(self, task: dict):
        code = task.get('code')
        if not code:
            raise ValueError("Code is required for review.")

        review_results = await self.review_code(code)
        return review_results

    async def review_code(self, code: str) -> dict:
        url = f"{self.api_base_url}/review-code"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"code": code}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise Exception("Failed to review code through external service.")
            
            data = await response.json()
            return data
