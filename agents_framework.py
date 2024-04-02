# agents_framework.py
import asyncio
from coder_agent import CoderAgent
from reviewer_agent import ReviewerAgent
from tester_agent import TesterAgent
from project_manager_agent import ProjectManagerAgent

async def main():
    coder = CoderAgent("Coder")
    reviewer = ReviewerAgent("Reviewer")
    tester = TesterAgent("Tester")
    project_manager = ProjectManagerAgent("Project Manager")

    # Define a simple task
    task = {"description": "Create enemy AI behavior"}

    # Simulate the workflow
    await coder.perform_task(task)
    await reviewer.perform_task(task)
    await tester.perform_task({"description": "Verify enemy AI animations", "image_analysis": True})
    await project_manager.perform_task(task)

if __name__ == "__main__":
    asyncio.run(main())
