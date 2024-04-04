from base_agent import BaseAgent
import asyncio
import aiohttp

class CommenterAgent(BaseAgent):
    def __init__(self, name: str, session: aiohttp.ClientSession):
        super().__init__(name, session)

    async def perform_task(self, task: dict):
        code = task.get('code')
        if not code:
            raise ValueError("Code is required for commenting.")

        commented_code = self.comment_non_essential_lines(code)
        return commented_code

    def comment_non_essential_lines(self, code: str) -> str:
        # Split the code into lines for processing
        lines = code.split('\n')

        # Define a simple rule to identify non-essential lines. This can be expanded based on specific requirements.
        non_essential_keywords = ['python', 'print', 'import logging', 'logging.info', 'logging.debug', '# DEBUG:', '"""', "'''", "'''python"]

        # Process each line, adding a comment symbol if the line is considered non-essential
        commented_lines = []
        for line in lines:
            if any(keyword in line for keyword in non_essential_keywords):
                # Add a comment symbol to non-essential lines
                commented_lines.append('# ' + line)
            else:
                commented_lines.append(line)

        # Join the processed lines back into a single string
        commented_code = '\n'.join(commented_lines)
        return commented_code
