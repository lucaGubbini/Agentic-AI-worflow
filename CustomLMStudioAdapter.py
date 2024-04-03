import aiohttp
import asyncio
import json

class CustomLMStudioAdapter:
    def __init__(self, api_key: str, api_base_url: str = 'https://example-api.com'):
        self.session = aiohttp.ClientSession()
        self.api_key = api_key
        self.api_base_url = api_base_url

    async def generate_code(self, task_description: str) -> str:
        url = f"{self.api_base_url}/generate-code"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"description": task_description}
        async with self.session.post(url, headers=headers, data=json.dumps(body)) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('code', 'No code generated')
            else:
                raise Exception(f"Failed to generate code: {response.status}")

    async def review_code(self, code_snippet: str) -> dict:
        url = f"{self.api_base_url}/review-code"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"code_snippet": code_snippet}
        async with self.session.post(url, headers=headers, data=json.dumps(body)) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to review code: {response.status}")

    async def test_code(self, code_snippet: str) -> dict:
        url = f"{self.api_base_url}/test-code"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"code_snippet": code_snippet}
        async with self.session.post(url, headers=headers, data=json.dumps(body)) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to test code: {response.status}")

    async def close(self):
        await self.session.close()
