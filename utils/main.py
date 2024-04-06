import asyncio
from abc import ABC, abstractmethod
from adapters.CustomMemGPTAdapter import CustomMemGPTAdapter
# Assuming CustomMemGPTAdapter is implemented and imported correctly

class BaseAgent(ABC):
    """
    Abstract base class for all agents, requiring the implementation of 
    the perform_task async method.
    """
    @abstractmethod
    async def perform_task(self, task):
        pass

class ProjectManagerAgent(BaseAgent):
    """
    Agent responsible for creating project plans based on descriptions.
    """
    async def perform_task(self, task):
        description = task.get('project_description')
        if not description:
            raise ValueError("Project description is missing.")
        return f"Project plan based on: {description}"

class CoderAgent(BaseAgent):
    """
    Agent that generates code based on a project plan using a MemGPT adapter.
    """
    def __init__(self, memgpt_adapter: CustomMemGPTAdapter):
        self.memgpt_adapter = memgpt_adapter

    async def perform_task(self, task):
        project_plan = task.get('project_plan')
        if not project_plan:
            raise ValueError("Project plan is missing.")
        return await self.memgpt_adapter.generate_code(project_plan)

class ReviewerAgent(BaseAgent):
    """
    Agent for conducting code reviews.
    """
    def __init__(self, memgpt_adapter: CustomMemGPTAdapter):
        self.memgpt_adapter = memgpt_adapter

    async def perform_task(self, task):
        code = task.get('code')
        if not code:
            raise ValueError("Code is missing for review.")
        return f"Reviewed code: {code[:10]}..."

class CommenterAgent(BaseAgent):
    """
    Agent for adding comments to the code.
    """
    async def perform_task(self, task):
        code = task.get('code')
        if not code:
            raise ValueError("Code is missing for commenting.")
        return f"# Commented\n{code}"

async def workflow_simulation():
    """
    Simulates a workflow that includes creating a project plan, generating code,
    reviewing the code, and adding comments to it.
    """
    memgpt_adapter = CustomMemGPTAdapter(api_key='your_api_key', base_url='your_base_url')

    project_manager = ProjectManagerAgent()
    coder = CoderAgent(memgpt_adapter)
    reviewer = ReviewerAgent(memgpt_adapter)
    commenter = CommenterAgent()

    project_description = "Define a Python function to calculate the area of a rectangle."
    project_plan = await project_manager.perform_task({'project_description': project_description})
    code = await coder.perform_task({'project_plan': project_plan})
    review_results = await reviewer.perform_task({'code': code})
    commented_code = await commenter.perform_task({'code': code})

    print(f"Project Plan: {project_plan}\nGenerated Code:\n{code}\nReview Results: {review_results}\nCommented Code:\n{commented_code}")

if __name__ == "__main__":
    asyncio.run(workflow_simulation())
