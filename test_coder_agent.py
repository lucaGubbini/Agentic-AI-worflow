# test_coder_agent.py
from coder_agent import CoderAgent

async def test_generate_code():
    coder = CoderAgent("Coder")
    prompt = "Write a Python function to add two numbers."
    code = await coder.generate_code(prompt)
    print("Generated Code:\n", code)

# This is a simplistic example; in practice, you might compare the generated code against expected outcomes.

import asyncio

asyncio.run(test_generate_code())
