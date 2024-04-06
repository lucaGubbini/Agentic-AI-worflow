import aiohttp
from aiohttp import ClientSession

class CustomLMStudioAdapter:
    def __init__(self, api_key: str, api_base_url: str = 'http://localhost:1234/v1'):
        """
        Initialize the CustomLMStudioAdapter with necessary configurations.
        
        :param api_key: API key for authentication with the LM Studio service.
        :param api_base_url: Base URL of the LM Studio API.
        """
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.session: ClientSession = None

    async def _ensure_session(self):
        """
        Ensure the aiohttp ClientSession is created and reused for each request.
        """
        if not self.session or self.session.closed:
            self.session = ClientSession()

    async def _make_request(self, endpoint: str, payload: dict) -> dict:
        """
        Helper method to make POST requests to the given API endpoint with the specified payload.
        
        :param endpoint: The API endpoint to hit.
        :param payload: The payload for the POST request.
        :return: The JSON response as a dictionary.
        """
        await self._ensure_session()
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with self.session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()  # This will automatically throw an exception for non-200 responses
            return await response.json()

    async def generate_code(self, project_description: str) -> str:
        """
        Generate code based on a given project description using the /v1/completions endpoint.
        
        :param project_description: The description of the project for which code needs to be generated.
        :return: Generated code as a string or a message indicating failure.
        """
        payload = {
            "prompt": project_description,
            "max_tokens": 150,
            "temperature": 0.5,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop": ["\n"]
        }
        try:
            response = await self._make_request("completions", payload)
            return response["choices"][0]["text"] if response.get("choices") else "No code generated"
        except aiohttp.ClientResponseError as e:
            print(f"API request failed: {e.status} - {e.message}")
            return "API request failed"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "API request failed due to an unexpected error"

    async def close(self):
        """
        Close the aiohttp session if it has been opened.
        """
        if self.session and not self.session.closed:
            await self.session.close()
