from .base_agent import BaseAgent
import asyncio
import tempfile
import subprocess

class TesterAgent(BaseAgent):
    """Agent responsible for testing code snippets."""
    
    async def perform_task(self, task: dict):
        code_snippet = task.get('code_snippet')
        if not code_snippet:
            raise ValueError("Code snippet is required for testing.")
        
        test_results = await self.run_tests(code_snippet)
        return {'test_results': test_results}

    async def run_tests(self, code_snippet: str) -> dict:
        async with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as temp_file:
            temp_file.write(code_snippet)
            temp_file.seek(0)

        process = await asyncio.create_subprocess_exec(
            'pytest', temp_file.name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()

        # Cleanup the temporary file after running the tests
        subprocess.run(['rm', temp_file.name])

        return {
            'success': process.returncode == 0,
            'stdout': stdout.decode().strip(),
            'stderr': stderr.decode().strip()
        }
