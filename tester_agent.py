# tester_agent.py
import subprocess
from base_agent import BaseAgent
import asyncio

class TesterAgent(BaseAgent):
    async def run_tests(self, filename: str) -> str:
        # Run pytest or any other test command and return the results
        process = await asyncio.create_subprocess_shell(
            f"pytest {filename}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            return stdout.decode()
        else:
            return stderr.decode()
