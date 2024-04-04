import aiohttp

class CustomLMStudioAdapter:
    def __init__(self, api_key: str, api_base_url: str = 'http://localhost:1234/v1'):
        """
        Initialize the CustomLMStudioAdapter with necessary configurations.
        
        :param api_key: API key for authentication with the external service.
        :param api_base_url: Base URL of the external code generation service.
        """
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.session = None

    async def _ensure_session(self):
        """
        Ensure an aiohttp.ClientSession is available and open.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def generate_code(self, project_description: str) -> str:
        """
        Generate code based on a given project description.
        
        :param project_description: The description of the project for which code needs to be generated.
        :return: Generated code as a string.
        """
        await self._ensure_session()
        url = f"{self.api_base_url}/generate-code"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"description": project_description}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('code', 'No code generated')
            else:
                raise Exception(f"Failed to generate code: {response.status}")

    async def review_code(self, code: str) -> dict:
        """
        Review generated code for quality and standards.
        
        :param code: The code snippet to be reviewed.
        :return: A dictionary containing review results.
        """
        await self._ensure_session()
        url = f"{self.api_base_url}/review-code"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"code_snippet": code}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to review code: {response.status}")

    async def test_code(self, code: str) -> dict:
        """
        Test the generated code to ensure it meets functional requirements.
        
        :param code: The code snippet to be tested.
        :return: A dictionary containing test results.
        """
        await self._ensure_session()
        url = f"{self.api_base_url}/test-code"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"code_snippet": code}

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to test code: {response.status}")

    async def close(self):
        """
        Close the aiohttp.ClientSession when the adapter is no longer needed.
        """
        if self.session:
            await self.session.close()
            self.session = None
