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
    coder = CoderAgent("Coder", "http://localhost:1234/v1", "lm-studio", "http://localhost:1234/v1")
    reviewer = ReviewerAgent("Reviewer", "http://localhost:1234/v1", "lm-studio")

    # Define a Python function to calculate the area of a rectangle as a project plan.
    project_description = "Define a Python function to calculate the area of a rectangle. Comment all non-essential lines."
    project_plan = await project_manager.generate_project_plan(project_description)
    
    # Develop code using the coder agent which involves generating code, testing, and revising it until it passes all tests.
    code = await coder.develop_code(project_plan)
    print(f"Developed Code:\n{code}")

    # Optionally, you might want to write the code to a file.
    filename = "developed_code.py"
    with open(filename, 'w') as file:
        file.write(code)
    print(f"Code has been written to {filename}")

    # The reviewer agent reviews the developed code.
    review_results = await reviewer.review_code(code)
    print(f"Code Review: {review_results}")

    # Generate suggestions for improvements if there are issues.
    if 'issues' in review_results and review_results['issues']:
        suggestions = await reviewer.suggest_improvements(code)
        print("Suggestions for improvement:\n", suggestions)
    else:
        print("No suggestions for improvement. The code meets the quality standards.")

if __name__ == "__main__":
    asyncio.run(main())
