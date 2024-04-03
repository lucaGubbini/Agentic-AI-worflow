# base_agent.py
class BaseAgent:
    """
    A base class for defining agents in the system. Each agent should have a name and optionally, a configuration.
    Agents can perform tasks, communicate with other agents, and receive messages.
    """

    def __init__(self, name: str, config: dict = None):
        """
        Initializes a new instance of the BaseAgent class.

        :param name: A string representing the name of the agent.
        :param config: An optional dictionary containing configuration settings for the agent.
        """
        self.name = name
        self.config = config or {}

    async def perform_task(self, task: dict):
        """
        An asynchronous method that performs a given task. This method should be implemented by derived classes.

        :param task: A dictionary representing the task to be performed.
        :raises NotImplementedError: Indicates that the derived class must implement this method.
        """
        raise NotImplementedError("This method needs to be implemented in the derived class.")

    def communicate(self, message: str, target_agent: 'BaseAgent'):
        """
        Sends a message from this agent to another target agent.

        :param message: A string representing the message to be sent.
        :param target_agent: An instance of BaseAgent representing the target agent to send the message to.
        """
        print(f"{self.name} to {target_agent.name}: {message}")
        target_agent.receive_message(message)

    def receive_message(self, message: str):
        """
        Handles receiving a message sent to this agent.

        :param message: A string representing the message received.
        """
        print(f"{self.name} received: {message}")
