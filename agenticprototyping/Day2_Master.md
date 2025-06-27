# Day 2: SDK, Agent Building, Tools, RAG & Visualization

## 📝 Overview

Welcome to Day 2! Today, we dive into the practical aspects of building agents using the OpenAI Agents SDK. We'll cover everything from setting up your first agent to equipping it with tools, enabling it to retrieve information, and visualizing its structure.

## 🎯 Day 2 Goals

-   Get comfortable with the OpenAI Agents SDK.
-   Build and run a basic agent.
-   Understand and implement function calling to give your agent tools.
-   Build a Retrieval-Augmented Generation (RAG) pipeline.
-   Visualize your agent's architecture.
-   Analyze and understand agent outputs.

---

## 📖 Key Concepts

### 1. OpenAI Agents SDK

The SDK provides a lightweight and flexible framework for building agentic AI applications. The core primitives are:

-   **Agents:** LLMs with instructions and tools.
-   **Handoffs:** Allow agents to delegate tasks to other agents.
-   **Guardrails:** Validate inputs to agents.

**Code Example: Hello World**

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

### 2. Building Agents

Agents are the core of your application. You can configure their instructions, model, and tools.

**Code Example: Agent with a Tool**

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
```

### 3. Function Calling

Function calling allows your agent to interact with your code and external services. You can define functions with clear descriptions and parameters, and the model will decide when to call them.

**Code Example: Defining a Function Tool**

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City and country e.g. Bogotá, Colombia"
            }
        },
        "required": ["location"],
        "additionalProperties": False
    }
}]

response = client.responses.create(
    model="gpt-4.1",
    input=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    tools=tools
)
```

### 4. Embeddings and Retrieval (RAG)

To build a RAG pipeline, you first need to convert your documents into numerical representations called embeddings. These embeddings can then be stored in a vector database for efficient retrieval.

**Code Example: Getting Embeddings**

```python
from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding
```

Once you have embeddings, you can perform semantic search to find the most relevant documents for a given query.

**Code Example: Semantic Search**

```python
from openai.embeddings_utils import get_embedding, cosine_similarity

def search_reviews(df, product_description, n=3, pprint=True):
    embedding = get_embedding(product_description, model='text-embedding-3-small')
    df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
    res = df.sort_values('similarities', ascending=False).head(n)
    return res
```

### 5. Agent Visualization

You can visualize your agent's structure, including its tools and handoffs, using the `draw_graph` function.

**Code Example: Visualizing an Agent**

```python
from agents import Agent, function_tool
from agents.extensions.visualization import draw_graph

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent],
    tools=[get_weather],
)

draw_graph(triage_agent)
```

### 6. Agent Output

The `Runner.run` methods return a `RunResult` or `RunResultStreaming` object, which contains valuable information about the agent's execution, including the final output, new items generated, and the last agent that ran.

---

## 🚀 Activities

### Activity 1: "Hello World" Agent

1.  Set up your project and install the `openai-agents` SDK.
2.  Create a simple "Hello World" agent and run it.
3.  Experiment with different instructions and observe the output.

### Activity 2: Adding Tools

1.  Define a Python function that you want your agent to use as a tool.
2.  Use the `@function_tool` decorator to turn it into a tool.
3.  Add the tool to your agent and write a prompt that requires the agent to use it.

### Activity 3: Building a RAG Pipeline

1.  Choose a small set of documents (e.g., text files, articles).
2.  Write a script to generate embeddings for each document using OpenAI's embedding models.
3.  Implement a simple semantic search function that takes a query, embeds it, and finds the most similar documents from your set.
4.  Integrate this search function as a tool for your agent.

### Activity 4: Visualize Your Agent

1.  Take the agent you built in the previous activities.
2.  Use the `draw_graph` function to generate a visualization of your agent's architecture.
3.  Analyze the graph to understand the relationships between your agent, its tools, and any handoffs.

---

## ✅ Day 2 Success Checklist

-   [ ] Successfully installed the OpenAI Agents SDK and ran a "Hello World" agent.
-   [ ] Created a custom tool and integrated it with an agent.
-   [ ] Built a basic RAG pipeline with embeddings and semantic search.
-   [ ] Visualized the architecture of your agent.
-   [ ] Understood how to access and interpret the output of an agent run.

```