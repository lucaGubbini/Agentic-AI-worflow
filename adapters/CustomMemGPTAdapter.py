from typing import Optional, Dict
import aiohttp
import asyncio

class MemGPTAdapter:
    def __init__(self, agent_endpoint: str):
        """
        Initialize the adapter with the MemGPT agent's endpoint.
        
        :param agent_endpoint: The URL endpoint for the MemGPT agent.
        """
        self.agent_endpoint = agent_endpoint
        self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, data: dict) -> Optional[Dict]:
        """
        Generic method to make POST requests to the MemGPT agent.
        
        :param endpoint: The specific API endpoint (e.g., 'generate-code', 'review-code').
        :param data: The payload to send in the request.
        :return: The JSON response as a dictionary, or None if an error occurs.
        """
        url = f"{self.agent_endpoint}/{endpoint}"
        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                response.raise_for_status()
        except aiohttp.ClientError as e:
            print(f"Request to {url} failed: {e}")
        return None

    async def generate_code(self, project_description: str) -> str:
        """
        Generate code based on a given project description using MemGPT.
        
        :param project_description: The description of the project for code generation.
        :return: Generated code as a string, or an error message.
        """
        data = {"description": project_description}
        response = await self._make_request('generate-code', data)
        return response.get('code', 'No code generated') if response else "API request failed"

    async def review_code(self, code_snippet: str) -> Dict:
        """
        Review generated code for quality and standards.
        
        :param code_snippet: The code snippet to review.
        :return: A dictionary with the review results, or an error.
        """
        data = {"code": code_snippet}
        response = await self._make_request('review-code', data)
        return response if response else {"error": "API request failed"}

    async def test_code(self, code_snippet: str) -> Dict:
        """
        Test the generated code for functional requirements.
        
        :param code_snippet: The code snippet to test.
        :return: A dictionary with the test results, or an error.
        """
        data = {"code": code_snippet}
        response = await self._make_request('test-code', data)
        return response if response else {"error": "API request failed"}

    async def close(self):
        """
        Close the aiohttp session.
        """
        await self.session.close()
