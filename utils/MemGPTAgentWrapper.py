import aiohttp
import logging
from typing import Optional, Dict

# Configure logging at the module level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MemGPTAgent:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        """Ensure that an aiohttp session is available and open."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _make_request(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """Perform an asynchronous POST request to a specified endpoint."""
        await self._ensure_session()
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                logger.error(f"Failed to make request to {url}: {response.status}")
                return None  # Explicit return for clarity
        except aiohttp.ClientError as e:
            logger.error(f"Client error occurred while making request to {url}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while making request to {url}: {e}")
        return None

    async def generate_code(self, project_description: str) -> str:
        """Generate code based on the project description."""
        payload = {
            "prompt": project_description,
            "max_tokens": 100,
            "temperature": 0.5
        }
        response = await self._make_request("completions", payload)
        if response:
            return response.get('choices', [{'text': 'No code generated'}])[0]['text']
        return "Failed to generate code due to an internal error"

    async def close(self):
        """Close the aiohttp session if it's open."""
        if self.session:
            await self.session.close()
