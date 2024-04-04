import asyncio
import aiohttp
from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent
from CustomLMStudioAdapter import CustomLMStudioAdapter
from commenter_agent import CommenterAgent
async def main():
    async with aiohttp.ClientSession() as session:
        # Initialize the CustomLMStudioAdapter with necessary configurations
        custom_lm_studio_adapter = CustomLMStudioAdapter(api_key="lm-studio", session=session)
        commenter_agent = CommenterAgent("Python Code Commenter", session)
        # Initialize your agents with the shared aiohttp.ClientSession
        project_manager = ProjectManagerAgent("Project Manager", "http://localhost:1234/v11", "lm-studio", session)
        coder = CoderAgent("Coder", "http://localhost:1234/v1", "lm-studio", session, custom_lm_studio_adapter)
        reviewer = ReviewerAgent("Reviewer", "http://localhost:1234/v1", "lm-studio", session)

        # Example project description
        project_description = "Define a Python function to calculate the area of a rectangle."

        # Generate project plan
        project_plan = await project_manager.generate_project_plan(project_description)
        if not project_plan:
            print("Failed to generate project plan.")
            return

        # Generate code based on the project plan
        code = await coder.generate_code(project_plan)
        if not code:
            print("Failed to generate code.")
            return

        print(f"Generated Code:\n{code}")

        # Review the generated code
        review_results = await reviewer.review_code(code)
        print(f"Code Review Results:\n{review_results}")

        # Optionally: Execute additional steps, like testing the code
        # Assuming 'code' is a string containing your Python code
        task = {'code': review_results}
        commented_code = await commenter_agent.perform_task(task)
        print(f"Commented Code:\n{commented_code}")
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
