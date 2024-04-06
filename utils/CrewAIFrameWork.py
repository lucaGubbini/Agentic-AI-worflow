# Import necessary libraries and frameworks
from crewai import Agent, Orchestrator
from agents.coder_agent import CoderAgent
from agents.reviewer_agent import ReviewerAgent
from agents.tester_agent import TesterAgent
from adapters.CustomLMStudioAdapter import CustomLMStudioAdapter
from adapters.CustomMemGPTAdapter import CustomMemGPTAdapter, memgpt_agent

class BaseCrewAIAgent(Agent):
    """
    Base class for all CrewAI Agents. Initializes with common adapter and
    defines the async run method structure.
    """
    def __init__(self, name, adapter):
        super().__init__(name)
        self.adapter = adapter

    async def run(self, task):
        raise NotImplementedError("Subclasses must implement this method")

class CrewAICoderAgent(BaseCrewAIAgent):
    """
    CrewAI Coder Agent for generating code based on task descriptions.
    """
    async def run(self, task):
        task_description = task.get('description')
        generated_code = await self.adapter.generate_code(task_description)
        self.send_result(generated_code)

class CrewAIReviewerAgent(BaseCrewAIAgent):
    """
    CrewAI Reviewer Agent for reviewing code snippets.
    """
    async def run(self, task):
        code_snippet = task.get('code_snippet')
        review = await self.adapter.review_code(code_snippet)
        self.send_result(review)

class CrewAITesterAgent(BaseCrewAIAgent):
    """
    CrewAI Tester Agent for testing code snippets.
    """
    async def run(self, task):
        code_snippet = task.get('code_snippet')
        test_results = await self.adapter.test_code(code_snippet)
        self.send_result(test_results)

def setup_agents():
    """
    Setups agents by instantiating them with a CustomMemGPTAdapter and registering
    them with the orchestrator.
    """
    custom_memgpt_adapter = CustomMemGPTAdapter(memgpt_agent)

    coder_agent = CrewAICoderAgent('Coder', custom_memgpt_adapter)
    reviewer_agent = CrewAIReviewerAgent('Reviewer', custom_memgpt_adapter)
    tester_agent = CrewAITesterAgent('Tester', custom_memgpt_adapter)

    orchestrator = Orchestrator()
    orchestrator.register_agent(coder_agent)
    orchestrator.register_agent(reviewer_agent)
    orchestrator.register_agent(tester_agent)

    return orchestrator

def main():
    """
    Main function to run the CrewAI Framework setup and assign tasks.
    """
    orchestrator = setup_agents()

    # Define a task for the CoderAgent and start the workflow
    task = {
        'description': 'Write a Python function to calculate Fibonacci numbers.'
    }
    orchestrator.assign_task('Coder', task)

if __name__ == '__main__':
    main()
