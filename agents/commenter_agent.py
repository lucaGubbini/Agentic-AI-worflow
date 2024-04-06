from .base_agent import BaseAgent

class CommenterAgent(BaseAgent):
    """Agent that comments non-essential lines of code."""
    
    def comment_non_essential_lines(self, code: str) -> str:
        keywords = ['print', 'import logging', 'logging.info', 'logging.debug', '# DEBUG:', '"""', "'''"]
        return '\n'.join(['# ' + line if any(keyword in line for keyword in keywords) else line for line in code.split('\n')])

    async def perform_task(self, task: dict):
        code = task.get('code')
        if not code:
            raise ValueError("Code is required for commenting.")
        commented_code = self.comment_non_essential_lines(code)
        return {'commented_code': commented_code}
