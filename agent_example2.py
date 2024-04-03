import asyncio
from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent

async def main():
    project_manager = ProjectManagerAgent("Project Manager")
    coder = CoderAgent("Coder")
    reviewer = ReviewerAgent("Reviewer")

    # Step 1: Project Manager generates a project plan
    project_description = "Develop a Python function to calculate the factorial of a number."
    project_plan = await project_manager.generate_project_plan(project_description)
    print(f"Project Plan: {project_plan}")

    # Step 2: Coder Agent generates code based on the project plan
    generated_code = await coder.generate_code(project_plan)
    print(f"\nGenerated Code:\n{generated_code}")

    # Step 3: Reviewer Agent reviews the generated code
    review = await reviewer.review_code(generated_code)
    print(f"\nCode Review:\n{review}")

if __name__ == "__main__":
    asyncio.run(main())
