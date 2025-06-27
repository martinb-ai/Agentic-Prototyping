# Day 3: Production Readiness - RAG, Safety & Observability

## 📝 Overview

Welcome to Day 3! Now that you have a functioning, multi-agent system, it's time to make it robust, reliable, and ready for the real world. Today, we focus on three pillars of production readiness: giving your agent external knowledge through Retrieval-Augmented Generation (RAG), ensuring it behaves safely with moderation and guardrails, and making its operations transparent through observability and tracing.

## 🎯 Day 3 Goals

-   Understand and implement a full Retrieval-Augmented Generation (RAG) pipeline.
-   Learn and apply safety best practices, including using the Moderation API.
-   Build and integrate custom guardrails to enforce application-specific rules.
-   Master observability by tracing agent runs to debug and monitor behavior.
-   Learn production best practices for scaling, latency, and cost management.

---

## 📖 Key Concepts

### 1. Retrieval-Augmented Generation (RAG): Giving Your Agent Knowledge

RAG is a powerful technique to ground your agent in external, up-to-date, or proprietary information. It prevents hallucination and allows the agent to answer questions about data it wasn't trained on.

**The RAG Pipeline:**

1.  **Embeddings:** Convert your documents (e.g., PDFs, text files) into numerical vectors using an embedding model. These vectors capture the semantic meaning of the text.
2.  **Vector Store:** Store these embeddings in a specialized database for efficient searching.
3.  **Retrieval:** When a user asks a question, embed the query and search the vector store for the most similar document chunks.
4.  **Augmentation:** Inject the retrieved text into the agent's prompt as context.
5.  **Generation:** The agent uses this new context to generate an informed answer.

**Code Example: Creating Embeddings and Searching**

```python
from openai import OpenAI
client = OpenAI()

# 1. Create an embedding for a piece of text
def get_embedding(text, model="text-embedding-3-small"):
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Your document texts
documents = ["The return policy is 30 days.", "Our headquarters is in San Francisco."]
# In a real app, you'd have many more documents
document_embeddings = {doc: get_embedding(doc) for doc in documents}

# 2. Embed a user query
user_query = "What is the return policy?"
query_embedding = get_embedding(user_query)

# 3. Find the most relevant document (simplified search)
# In a real app, you'd use a vector database (e.g., Pinecone, Chroma) for this.
from scipy.spatial.distance import cosine

best_doc = min(document_embeddings.keys(), 
               key=lambda doc: cosine(query_embedding, document_embeddings[doc]))

print(f"Most relevant document: {best_doc}")
# Expected Output: Most relevant document: The return policy is 30 days.
```

### 2. Safety: Moderation and Best Practices

To deploy an agent responsibly, you must prevent it from generating or responding to harmful content. The free **Moderation API** is your first line of defense.

**Code Example: Using the Moderation API**

```python
response = client.moderations.create(
    model="omni-moderation-latest",
    input="I want to build a bomb."
)

moderation_result = response.results[0]
if moderation_result.flagged:
    print("Input was flagged for the following categories:")
    for category, flagged in moderation_result.categories:
        if flagged:
            print(f"- {category.name}")
else:
    print("Input is clean.")
```

**Other Safety Best Practices:**
-   **Adversarial Testing (Red Teaming):** Actively try to break your agent to find vulnerabilities.
-   **Human-in-the-Loop (HITL):** For high-stakes actions (e.g., processing a refund), require human approval.
-   **Constrain Inputs:** Limit the length and format of user inputs to prevent prompt injection.

### 3. Guardrails: Enforcing Custom Rules

Guardrails are automated checks to ensure your agent stays on topic, avoids forbidden actions, and adheres to your business logic. They act as a custom safety layer on top of general moderation.

**How Guardrails Work in the SDK:**
-   You define a function (often another agent) that checks an input or output against a rule.
-   If the rule is violated, the guardrail triggers a "tripwire," which raises an exception and stops the agent run.

**Code Example: An Input Guardrail to Prevent Off-Topic Questions**

```python
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel

class RelevanceCheck(BaseModel):
    is_relevant: bool
    reasoning: str

# 1. Define the guardrail agent
relevance_guard = Agent(
    name="Relevance Guard",
    instructions="You are a guard for a customer support agent for an e-commerce store. Check if the user's query is about orders, products, or returns. If it is not, it is irrelevant.",
    output_type=RelevanceCheck
)

# 2. Define the guardrail function
@input_guardrail
async def relevance_tripwire(ctx, agent, input_str):
    result = await Runner.run(relevance_guard, input_str)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_relevant
    )

# 3. Apply the guardrail to your main agent
support_agent = Agent(
    name="Support Agent",
    instructions="You are a helpful customer support agent.",
    input_guardrails=[relevance_tripwire]
)

# 4. Test it
try:
    await Runner.run(support_agent, "What is the weather in London?")
except InputGuardrailTripwireTriggered:
    print("Guardrail tripped! The question was off-topic.")
```

### 4. Observability: Tracing Agent Behavior

Observability is key to understanding, debugging, and improving your agents. The Agents SDK has built-in tracing that logs every step of an agent's execution—LLM calls, tool calls, handoffs, and more.

-   **Traces:** A complete record of a single `Runner.run()` execution.
-   **Spans:** Individual operations within a trace (e.g., a single LLM call).

Traces are automatically sent to the **OpenAI Dashboard** under the "Traces" section, providing a visual timeline of your agent's thought process.

**Code Example: Naming a Workflow for Better Tracing**

```python
from agents import Runner, trace

# By wrapping runs in a named trace, you can easily find and group them in the dashboard.
with trace("Customer_Support_Workflow"):
    result = await Runner.run(support_agent, "I want to return my order.")
```

---

## 🚀 Activities

### Activity 1: Build a RAG Pipeline

1.  **Gather Documents:** Collect 3-5 short text documents with information relevant to your agent's purpose (e.g., product descriptions, FAQ answers).
2.  **Embed Documents:** Write a script to read each document, generate an embedding for it using `text-embedding-3-small`, and store the embeddings (a simple Python dictionary is fine for this exercise).
3.  **Create a Search Tool:** Implement a Python function `retrieve_knowledge(query: str)` that:
    a.  Embeds the user's `query`.
    b.  Compares the query embedding to all document embeddings (using cosine similarity).
    c.  Returns the text of the most similar document.
4.  **Integrate the Tool:** Add this function as a tool to your agent and update its instructions to use the tool when it needs information.
5.  **Test it:** Ask your agent a question that can only be answered using the documents.

### Activity 2: Implement Moderation & a Guardrail

1.  **Add Moderation:** Before passing any user input to your agent, run it through the Moderation API. If it's flagged, return a canned response instead of running the agent.
2.  **Design a Guardrail:** Brainstorm a custom rule for your agent. For example:
    *   A guardrail that prevents the agent from discussing competitors.
    *   An output guardrail that ensures the agent's response is not longer than 200 words.
3.  **Implement the Guardrail:** Follow the code pattern above to create and apply your custom guardrail.
4.  **Test the Tripwire:** Send a prompt that should violate your guardrail and confirm that the `InputGuardrailTripwireTriggered` (or `Output...`) exception is raised.

### Activity 3: Trace and Debug

1.  **Name Your Trace:** Wrap the code that runs your agent in a `with trace("MyAgent_Test_Run"):` block.
2.  **Run a Complex Flow:** Execute a multi-turn conversation or a multi-agent handoff.
3.  **Explore the Dashboard:**
    a.  Navigate to the [Traces](https://platform.openai.com/traces) page in the OpenAI dashboard.
    b.  Find your named trace.
    c.  Click through the spans. Look at the inputs and outputs for each LLM call and tool call. Use this to understand exactly how your agent made its decisions.

---

## ✅ Day 3 Success Checklist

-   [ ] You have built a functional RAG pipeline that allows your agent to access external knowledge.
-   [ ] Your application uses the Moderation API to filter user input.
-   [ ] You have implemented at least one custom guardrail to enforce your agent's rules of engagement.
-   [ ] You have successfully traced an agent run and analyzed its execution flow in the dashboard.
-   [ ] You have a clear understanding of the key components needed to make an agent safe, reliable, and ready for production.
