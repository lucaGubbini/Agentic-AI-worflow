import unittest
from base_agent import BaseAgent

class TestBaseAgent(unittest.TestCase):
    def test_initialization(self):
        """Test the initialization of a BaseAgent."""
        agent = BaseAgent(name="Test Agent")
        self.assertEqual(agent.name, "Test Agent")

    def test_communication(self):
        """Test the communication between two BaseAgents."""
        agent1 = BaseAgent(name="Agent 1")
        agent2 = BaseAgent(name="Agent 2")
        self.assertIsNone(agent1.communicate("Hello, Agent 2", agent2))
        # Note: This test assumes communicate() method does not return a value.
        # You might need to adjust this test based on your implementation.

if __name__ == '__main__':
    unittest.main()
