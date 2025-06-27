# Day 2: Building Agents - From Single to Multi-Agent

## 📝 Overview

Welcome to Day 2! Today, we transition from theory to practice. You will learn how to use the OpenAI Agents SDK to build, run, and empower your agents. We'll start with a single agent, give it a memory and tools, and then scale up to complex multi-agent systems. By the end of the day, you will have a functioning, tool-using agent and a clear understanding of how to design sophisticated agentic workflows.

## 🎯 Day 2 Goals

-   Install the OpenAI Agents SDK and run your first agent.
-   Understand the core components of the SDK: `Agent`, `Runner`, and `tools`.
-   Implement conversational state to give your agent memory.
-   Master function calling to equip your agent with custom tools.
-   Design and build multi-agent systems using handoffs and orchestration.
-   Visualize your agent architecture to understand its flow.

---

## 📖 Key Concepts

### 1. The OpenAI Agents SDK: Your Toolkit

The Agents SDK is a lightweight, Python-first library for building agentic apps. Its main features are:

-   **`Agent`**: The core building block—an LLM with instructions and tools.
-   **`Runner`**: The engine that executes an agent loop, handling tool calls and state.
-   **`@function_tool`**: A simple decorator to turn any Python function into a tool for your agent.
-   **Handoffs**: A mechanism for one agent to delegate a task to another.

**Code Example: Your First Agent with the SDK**

```python
# Ensure you have the SDK installed: pip install openai-agents
from agents import Agent, Runner

# 1. Define the Agent
assistant_agent = Agent(
    name="Assistant", 
    instructions="You are a helpful and friendly assistant."
)

# 2. Run the Agent
result = Runner.run_sync(assistant_agent, "Write a haiku about a robot learning to paint.")

# 3. Print the final output
print(result.final_output)

# Expected Output:
# Metal hand holds brush,
# Learns the colors of the world,
# Canvas starts to bloom.
```

### 2. Giving Your Agent Memory: Conversational State

For an agent to be useful, it needs to remember the context of a conversation. You can manage this by passing the conversation history back to the model with each turn.

**Code Example: Manual State Management**

```python
from openai import OpenAI
client = OpenAI()

# Start with the initial user message
history = [
    {"role": "user", "content": "My name is Alex. What is the capital of France?"}
]

# First turn
response1 = client.responses.create(model="gpt-4.1", input=history)
print(f"Assistant: {response1.output_text}")

# Append the assistant's response to the history
history.append({"role": "assistant", "content": response1.output_text})

# Second turn: Ask a follow-up question
history.append({"role": "user", "content": "What is my name?"})
response2 = client.responses.create(model="gpt-4.1", input=history)
print(f"Assistant: {response2.output_text}")

# Expected Output:
# Assistant: The capital of France is Paris.
# Assistant: Your name is Alex.
```

### 3. Empowering Agents with Tools: Function Calling

Tools are what separate a simple chatbot from a powerful agent. By defining functions, you allow the agent to interact with the outside world—fetch data, call APIs, or perform actions.

The Agents SDK makes this incredibly simple with the `@function_tool` decorator.

**Code Example: A Weather Tool**

```python
from agents import Agent, Runner, function_tool
import requests

# 1. Define the function with a clear docstring
@function_tool
def get_current_weather(city: str) -> str:
    """Gets the current weather for a specified city."""
    # In a real app, you'd call a weather API
    if "paris" in city.lower():
        return "The weather in Paris is sunny and 22°C."
    return f"Sorry, I don't have weather information for {city}."

# 2. Create an agent and give it the tool
weather_agent = Agent(
    name="Weather Reporter",
    instructions="You provide current weather information. Use your tools when asked about the weather.",
    tools=[get_current_weather]
)

# 3. Run the agent
result = Runner.run_sync(weather_agent, "What's the weather like in Paris today?")
print(result.final_output)

# Expected Output: The weather in Paris is sunny and 22°C.
```

### 4. Multi-Agent Systems: Handoffs and Orchestration

As tasks become more complex, a single agent can become overwhelmed. The solution is to create a team of specialized agents and orchestrate their collaboration.

-   **Handoffs**: A simple and powerful pattern where one agent passes control to another. This is perfect for triage scenarios.
-   **Agents as Tools**: A more advanced pattern where a "manager" agent calls other agents as tools to perform sub-tasks and then synthesizes the results.

**Code Example: Triage Agent with Handoffs**

```python
from agents import Agent, Runner, handoff

# Define specialist agents
tech_support_agent = Agent(name="Tech Support", instructions="You are an expert in troubleshooting technical issues.")
billing_agent = Agent(name="Billing Support", instructions="You are an expert in handling billing and subscription questions.")

# Define the triage agent that knows how to hand off
triage_agent = Agent(
    name="Triage Agent",
    instructions="You are the first point of contact. Your job is to understand the user's query and hand off to the correct specialist agent.",
    handoffs=[tech_support_agent, billing_agent]
)

# Run the triage agent
result = Runner.run_sync(triage_agent, "I can't log in to my account.")
print(f"Final output from {result.last_agent.name}: {result.final_output}")

# Expected Output: Final output from Tech Support: I can help with that. Have you tried resetting your password?
```

### 5. Visualization and Output

Understanding what your agent is doing is key to debugging and improving it. The SDK provides tools for this:

-   **`draw_graph`**: Generates a visual diagram of your agent's architecture, showing agents, tools, and handoffs.
-   **`RunResult`**: The object returned by `Runner.run` contains rich information, including the `final_output`, the `last_agent` that ran, and a list of all `new_items` (tool calls, messages) generated during the run.

---

## 🚀 Activities

### Activity 1: Your First SDK Agent

1.  **Install the SDK:** `pip install openai-agents`.
2.  **Create an Agent:** Write the code for a simple `Assistant` agent, similar to the "Hello World" example.
3.  **Run it:** Use `Runner.run_sync` to ask your agent a question and print the output.
4.  **Add Memory:** Modify your code to handle a multi-turn conversation. Ask it a question, then ask a follow-up that relies on the context of the first question.

### Activity 2: Build a Tool-Using Agent

1.  **Define a Tool:** Create a simple Python function for a task of your choice (e.g., `search_company_knowledge_base(query: str)`, `create_calendar_event(title: str, date: str)`). Use the `@function_tool` decorator.
2.  **Equip Your Agent:** Create a new agent and pass your new function in the `tools` list.
3.  **Write a Good Prompt:** Your agent's instructions should clearly state when and how to use the tool.
4.  **Test it:** Run the agent with a prompt that should trigger the tool. Check the output to see if it worked.

### Activity 3: Design a Multi-Agent System

1.  **On Paper First:** Based on your PRD from Day 1, sketch out a multi-agent architecture. Do you need a triage agent? What are the specialized roles?
2.  **Implement Handoffs:** Create a `Triage Agent` and at least two `Specialist Agents`.
3.  **Configure Handoffs:** Add the specialist agents to the `handoffs` list of your triage agent.
4.  **Test the Flow:** Run the triage agent with a query that should be handed off to one of your specialists. Verify that the correct agent provides the final response.

### Activity 4: Visualize Your Creation

1.  **Install Visualization Libs:** `pip install "openai-agents[viz]"`.
2.  **Generate the Graph:** Use the `draw_graph` function on your multi-agent system from Activity 3.
3.  **Analyze:** Study the generated graph. Does it match the architecture you designed? Use it to explain your agent's workflow to your team.

---

## ✅ Day 2 Success Checklist

-   [ ] You have successfully built and run a single agent using the Agents SDK.
-   [ ] Your agent can maintain a conversation across multiple turns.
-   [ ] You have created a custom Python function and turned it into a tool for your agent.
-   [ ] You have designed and implemented a multi-agent system using handoffs.
-   [ ] You have generated a visualization of your agent architecture.
