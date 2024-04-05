import aiohttp
import logging
from typing import Optional, Dict

logging.basicConfig(level=logging.INFO)

class MemGPTAgent:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = None  # Session will be initialized in an async context

    async def _ensure_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, data: dict) -> Optional[Dict]:
        await self._ensure_session()  # Ensure the session is open
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Failed to make request to {url}: {response.status}")
        except Exception as e:
            logging.error(f"An error occurred while making request to {url}: {e}")

        return None  # Return None in case of any failure

    async def generate_code(self, project_description: str) -> str:
        payload = {
            "prompt": project_description,
            "max_tokens": 100,
            "temperature": 0.5
        }
        response = await self._make_request("completions", payload)
        if response:
            return response.get('choices', [{'text': 'No code generated'}])[0]['text']
        else:
            return "Failed to generate code due to an internal error"

    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

