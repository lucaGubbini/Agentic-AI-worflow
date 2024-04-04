import sys
import os
import asyncio
from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent

# Append the parent directory to sys.path to import the upper-level modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    # Initialize agents with corrected parameters
    project_manager = ProjectManagerAgent("Project Manager", "http://localhost:1234/v1", "lm-studio")
    coder = CoderAgent("Coder", "http://localhost:1234/v1", "lm-studio", "http://localhost:1234/v1")
    reviewer = ReviewerAgent("Reviewer", "http://localhost:1234/v1", "lm-studio")

    project_description = "Define a Python function to calculate the area of a rectangle. Comment all non-essential lines."
    project_plan = await project_manager.generate_project_plan(project_description)

    # Assuming perform_task is correctly implemented in CoderAgent
    task = {'project_plan': project_plan}
    code = await coder.perform_task(task)
    print(f"Developed Code:\n{code}")

    review_results = await reviewer.perform_task({'code': code})
    print(f"Code Review: {review_results}")

    # Generate suggestions for improvements if there are issues.
    if 'issues' in review_results and review_results['issues']:
        suggestions = await reviewer.suggest_improvements(code)
        print("Suggestions for improvement:\n", suggestions)
    else:
        print("No suggestions for improvement. The code meets the quality standards.")

if __name__ == "__main__":
    asyncio.run(main())
