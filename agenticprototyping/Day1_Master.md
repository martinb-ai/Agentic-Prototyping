# Day 1: Foundations (LLMs, Prompts, Agent Mindset)

## 📝 Overview

Welcome to Day 1 of the Agentic AI Workshop! Today is all about building a strong foundation. We'll cover the core concepts of Large Language Models (LLMs), how to effectively communicate with them through prompt engineering, and start thinking like an agent designer.

## 🎯 Day 1 Goals

- Understand the basics of interacting with the OpenAI API.
- Learn and apply prompt engineering techniques.
- Select the right model for a given task.
- Begin designing an agent by defining its purpose, capabilities, and constraints.
- Understand how to manage conversational state.

---

## 📖 Key Concepts

### 1. Developer Quickstart

The OpenAI API provides a simple interface to state-of-the-art AI models. You can generate text, analyze images, and extend the model's capabilities with tools.

**Code Example: Text Creation**
```python
# Initalize Openai Client library and Setup API keys
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

### 2. Prompt Engineering

Prompt engineering is the art and science of crafting effective instructions for an LLM to get the desired output.

**Key Techniques:**
- **Message Roles:** Use `developer`, `user`, and `assistant` roles to structure conversations and provide instructions with different levels of authority.
- **Reusable Prompts:** Create and manage prompts in the OpenAI dashboard for easier iteration and deployment.
- **Formatting:** Use Markdown and XML tags to structure your prompts and provide clear context to the model.
- **Few-Shot Learning:** Provide examples in your prompt to guide the model's behavior.
- **Retrieval-Augmented Generation (RAG):** Include relevant context information in your prompt to ground the model's responses in specific data.

**Code Example: Using Message Roles**
```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript?"
        }
    ]
)

print(response.output_text)
```

### 3. Model Selection

Choosing the right model is crucial for balancing performance, cost, and latency.

| Model      | Core strength                | Ideal first reach‑for           |
|------------|-----------------------------|----------------------------------|
| GPT‑4o     | Real‑time voice / vision chat| Live multimodal agents           |
| GPT‑4.1    | 1 M‑token text accuracy king | Long‑doc analytics, code review  |
| o3         | Deep tool‑using agent        | High‑stakes, multi‑step reasoning|
| o4‑mini    | Cheap, fast reasoning        | High‑volume "good‑enough" logic  |

### 4. Agents Overview

An agent is a system that intelligently accomplishes tasks on your behalf. It uses an LLM to manage workflow execution, has access to tools, and operates within defined guardrails.

**Core Components of an Agent:**
1.  **Model:** The LLM powering the agent.
2.  **Tools:** External functions or APIs the agent can use.
3.  **Instructions:** Guidelines defining the agent's behavior.

### 5. Agent Design Foundations

Start with a single agent and incrementally add complexity. Use prompt templates to manage different use cases and consider multi-agent systems for more complex workflows.

**Code Example: Basic Agent Definition**
```python
weather_agent = Agent(
    name="Weather agent",
    instructions="You are a helpful agent who can talk to users about the weather.",
    tools=[get_weather],
)
```

### 6. Conversational State

You can manage conversation history by manually passing previous messages in each API call or by using the `previous_response_id` parameter to chain responses.

**Code Example: Manual State Management**
```python
from openai import OpenAI

client = OpenAI()

history = [
    {
        "role": "user",
        "content": "tell me a joke"
    }
]

response = client.responses.create(
    model="gpt-4o-mini",
    input=history,
    store=False
)

print(response.output_text)

# Add the response to the conversation
history += [{"role": el.role, "content": el.content} for el in response.output]

history.append({ "role": "user", "content": "tell me another" })

second_response = client.responses.create(
    model="gpt-4o-mini",
    input=history,
    store=False
)

print(second_response.output_text)
```

---

## 🚀 Activities

### Activity 1: Use-Case Kickoff & Team Formation

1.  Form teams.
2.  Brainstorm a use case for an AI agent.
3.  Fill out the **Agent Product Requirements Document (PRD)** below.

### Activity 2: Your First API Call

1.  Set up your environment with the necessary API keys.
2.  Run the "Text Creation" code from the **Developer Quickstart** section.
3.  Experiment with different prompts and models.

### Activity 3: Draft Your Agent

1.  Based on your PRD, write the initial "system" prompt for your agent.
2.  Define the key capabilities and tools your agent will need.
3.  Select a model for your agent and justify your choice using the **LLM Model Selection Worksheet**.

---

## 📄 Worksheets

### Agent Product Requirements Document (PRD)

**A. Project/Agent Name:**
<!-- Enter your team’s agent name or codename here -->

**B. Problem Statement:**
<!-- What specific business/user problem does this agent solve? -->

**C. Target Users / Stakeholders:**
<!-- Who will use the agent? Who are the main stakeholders? -->

**D. User Stories / Sample Prompts:**
<!-- Add at least 3 real user stories/questions your agent must handle -->
-
-
-

**E. Key Capabilities (MVP):**
_Mark must-have and nice-to-have. Use checkboxes._

- [ ] Natural language Q&A
- [ ] Retrieval from internal docs (RAG)
- [ ] Calls external APIs (specify which): ___________
- [ ] Handles file inputs (PDF, images)
- [ ] Follows multi-turn conversations
- [ ] Handoffs/escalations to humans
- [ ] Structured outputs (JSON)
- [ ] Multimodal (image, audio)
- [ ] Other: ___________

**F. Guardrails / Risks / Constraints:**
_List safety, compliance, privacy, refusal rules, etc._

- [ ] PII detection/redaction
- [ ] Moderation API on inputs/outputs
- [ ] Human-in-the-loop for edge cases
- [ ] Rate limiting / cost cap
- [ ] Blocklist for prohibited topics
- [ ] Others: ___________

**G. Success Metrics / KPIs:**
_How will you know this agent is successful?_

- e.g. 90% correct answers, <10% human handoff, sub-5s latency, user satisfaction, etc.

**H. Evaluation Plan:**
_How will you test & validate agent performance? (Eval set, manual review, etc.)_

**I. Initial System/Assistant Instructions:**
_Example “system” prompt for your agent. Try to make it realistic._

---

### LLM Model Selection Worksheet

| Criteria                   | Option 1 (e.g. GPT-4o) | Option 2 (e.g. o3-mini) | Notes                        |
|----------------------------|------------------------|-------------------------|------------------------------|
| Context length needed      |                        |                         |                              |
| Speed/latency              |                        |                         |                              |
| Cost                       |                        |                         |                              |
| Required features          |                        |                         | (function calling, vision?)  |
| Accuracy/quality           |                        |                         |                              |
| Compatibility (APIs/tools) |                        |                         |                              |
| Team preference            |                        |                         |                              |

**Decision:**
_Which model will you use for MVP and why?_

---

### Prompt Engineering Starter Table

| Prompt Version | System/Assistant Prompt              | User Input                  | Output/Goal                | Notes/Learnings          |
|----------------|-------------------------------------|-----------------------------|----------------------------|--------------------------|
| v1             |                                     |                             |                            |                          |
| v2             |                                     |                             |                            |                          |
| v3             |                                     |                             |                            |                          |

---

## ✅ Day 1 Success Checklist

- [ ] Agent PRD filled out and saved/shared
- [ ] “First draft” system/assistant prompt written
- [ ] Three+ realistic user stories or prompts
- [ ] LLM model selected (with rationale)
- [ ] MVP features sketched (tools, RAG, outputs)
- [ ] At least 2 guardrails/risks defined
- [ ] Acceptance criteria/KPIs written
- [ ] (Stretch) Run a test in Quickstart notebook
