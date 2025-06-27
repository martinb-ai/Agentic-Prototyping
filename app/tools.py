from agents import function_tool

# TODO: Define your custom tools here

@function_tool
def example_tool(query: str) -> str:
    """An example tool that returns a fixed string."""
    return f"You searched for: {query}"

def get_tools():
    """Returns a list of all tools for the agents."""
    return [example_tool]
