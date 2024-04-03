import sys
import os
import asyncio
from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent

# Append the parent directory to sys.path to import the upper-level modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    project_manager = ProjectManagerAgent("Project Manager")
    coder = CoderAgent("Coder")
    reviewer = ReviewerAgent("Reviewer")

    # Define a Python function to calculate the area of a rectangle as a project plan.
    project_description = "Define a Python function to calculate the area of a rectangle. Comment all non-essential lines."
    project_plan = await project_manager.generate_project_plan(project_description)
    
    # Use the new generate_code method
    code = await coder.generate_code(project_plan)
    print(f"Generated Code:\n{code}")

    # Optionally, write the code to a file.
    filename = "generated_code.py"
    await coder.generate_code_and_write_to_file(project_plan, filename)

    # The reviewer agent reviews the generated code.
    review = await reviewer.review_code(code)
    print(f"Code Review: {review}")

    # Inside the main function
    code = await coder.generate_code(project_plan)
    await coder.generate_code_and_write_to_file(project_plan, filename)  # Writes the generated code to a file

    # If a run_tests function exists, you can include it here to run tests.
    # test_results = run_tests(filename)
    # print(f"Test Results: {test_results}")

if __name__ == "__main__":
    asyncio.run(main())
