# examples/agents_collaboration_example.py
import sys
import os

# Append the parent directory to sys.path to import the upper-level modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent
import asyncio

# ... [rest of your imports]

async def main():
    # Initialize agents
    project_manager = ProjectManagerAgent("Project Manager")
    coder = CoderAgent("Coder")
    reviewer = ReviewerAgent("Reviewer")

    # Get the project plan text
    project_plan_response = await project_manager.generate_project_plan("Define a simple Python function to calculate the area of a rectangle.")
    # Since project_plan_response is already a string, we can strip it directly
    project_plan_text = project_plan_response.strip()
    # Step 2: Coder agent creates the code based on the project plan
    code = await coder.generate_code(project_plan_text)

    # Step 3: Reviewer agent reviews the generated code
    review = await reviewer.review_code(code)

    # Output the results
    print(f"Project Plan: {project_plan_text}")
    print(f"Generated Code: {code}")
    print(f"Code Review: {review}")

if __name__ == "__main__":
    asyncio.run(main())
