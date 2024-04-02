# examples/agents_collaboration_example.py
import sys
import os

# Append the parent directory to sys.path to import the upper-level modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# examples/agents_collaboration_example.py
import asyncio
from project_manager_agent import ProjectManagerAgent
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent

# Assume the existence of run_tests function as defined above

async def main():
    # Initialize agents
    project_manager = ProjectManagerAgent("Project Manager")
    coder = CoderAgent("Coder")
    reviewer = ReviewerAgent("Reviewer")

    # Step 1: Generate a project plan (simplified here for brevity)
    project_plan = "Define a Python function to calculate the area of a rectangle."
    
    # Step 2: Coder agent creates code based on the project plan and writes it to a file
    filename = "generated_code.py"
    await coder.generate_code_and_write_to_file(project_plan, filename)

    # Step 3: Reviewer agent reviews the generated file (not shown)
    review = await reviewer.review_code(filename)  # Assuming this method exists

    # Step 4: Run tests against the generated code
    test_results = run_tests(filename)

    # Output the results
    print(f"Generated Code File: {filename}")
    print(f"Test Results:\n{test_results}")

if __name__ == "__main__":
    asyncio.run(main())
