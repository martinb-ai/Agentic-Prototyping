from agents import Agent
from tools import get_tools

def get_triage_agent():
    """Creates and returns the main triage agent."""
    # TODO: Define your specialist agents here
    # specialist_agent_1 = Agent(name="Specialist1", ...)
    # specialist_agent_2 = Agent(name="Specialist2", ...)

    triage_agent = Agent(
        name="Triage Agent",
        instructions="""
        You are a helpful assistant. Your job is to understand the user's request
        and then hand off to the correct specialist agent. If you are not sure,
        you can ask clarifying questions.
        """,
        # TODO: Add your specialist agents to the handoffs list
        # handoffs=[specialist_agent_1, specialist_agent_2],
        tools=get_tools()
    )
    return triage_agent
