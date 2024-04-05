import aiohttp

class CustomLMStudioAdapter:
    def __init__(self, api_key: str, api_base_url: str = 'http://localhost:1234/v1'):
        """
        Initialize the CustomLMStudioAdapter with necessary configurations.
        
        :param api_key: API key for authentication with the LM Studio service.
        :param api_base_url: Base URL of the LM Studio API.
        """
        self.api_key = api_key
        self.api_base_url = api_base_url

    async def _make_request(self, endpoint: str, payload: dict) -> dict:
        """
        Helper method to make POST requests to the given API endpoint with the specified payload.
        
        :param endpoint: The API endpoint to hit.
        :param payload: The payload for the POST request.
        :return: The JSON response as a dictionary.
        """
        url = f"{self.api_base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response_text = await response.text()
                    raise Exception(f"Failed on {endpoint}: {response.status} - {response_text}")

    async def generate_code(self, project_description: str) -> str:
        """
        Generate code based on a given project description using the /v1/completions endpoint.
        
        :param project_description: The description of the project for which code needs to be generated.
        :return: Generated code as a string or a message indicating failure.
        """
        payload = {
            "prompt": project_description,  # Your prompt here
            "max_tokens": 150,  # Specify the max number of tokens to generate
            "temperature": 0.5,  # Control the randomness of completions
            "top_p": 1.0,  # Nucleus sampling
            "frequency_penalty": 0.0,  # Adjust if needed
            "presence_penalty": 0.0,  # Adjust if needed
            "stop": ["\n"]  # Stop sequence to end the generation
        }
        # Endpoint adjusted to the assumed correct one for generating completions
        response = await self._make_request("completions", payload)
        # Parsing the response to extract the generated code
        if response and "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["text"]
        else:
            return "No code generated"

# Example usage:
# Please ensure aiohttp is installed: pip install aiohttp
# async def main():
#     adapter = CustomLMStudioAdapter(api_key="your_api_key_here")
#     code = await adapter.generate_code("Write a Python function to reverse a string.")
#     print(code)
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
