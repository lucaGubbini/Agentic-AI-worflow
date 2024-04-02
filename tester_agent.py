# tester_agent.py
import cv2
from base_agent import BaseAgent

from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


class TesterAgent(BaseAgent):
    async def perform_task(self, task: dict):
        if 'image_analysis' in task:
            print(f"{self.name} is performing image analysis")
            # Add OpenCV code for image analysis here
