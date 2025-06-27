# Day 1: Foundations (LLMs, Prompts, Agent Mindset)

## 📝 Overview

Welcome to Day 1 of the Agentic AI Workshop! Today is all about building a strong foundation. We'll cover the core concepts of Large Language Models (LLMs), how to effectively communicate with them through prompt engineering, and start thinking like an agent designer. By the end of the day, you will have a clear understanding of what an agent is, how to design one, and the fundamental tools you'll need to start building.

## 🎯 Day 1 Goals

-   Understand the basics of interacting with the OpenAI API for text and image analysis.
-   Master the art of prompt engineering to guide LLM behavior effectively.
-   Learn how to select the most appropriate model for a given task by weighing trade-offs.
-   Grasp the core concepts of agentic AI, including what an agent is and when to build one.
-   Draft a Product Requirements Document (PRD) for your own agent idea.

---

## 📖 Key Concepts

### 1. Developer Quickstart: Your First API Calls

The OpenAI API is your gateway to powerful AI models. You can generate text, analyze images, and much more with just a few lines of code.

**Code Example: Your First Text Generation**

```python
# Make sure to install the OpenAI library: pip install openai
# and set your OPENAI_API_KEY environment variable.
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a brave little robot."
)

print(response.output_text)
# Expected Output: In a world of towering giants, a tiny robot named Bolt rolled through the moonlit city, guarding the dreams of its sleeping citizens.
```

**Code Example: Analyzing an Image**

```python
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user", "content": "Describe the architectural style of this building."},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Gaudi_Casa_Batllo_2005.jpg"
                }
            ]
        }
    ]
)

print(response.output_text)
# Expected Output: This building is a prime example of Catalan Modernisme, characterized by its flowing, organic lines, colorful mosaic facade, and skeletal-like balconies. It was designed by Antoni Gaudí.
```

### 2. Prompt Engineering: The Art of Instruction

Prompt engineering is the process of designing and refining the inputs you give to an LLM to ensure it produces the desired output consistently. It's a blend of art and science.

**Key Techniques:**

-   **Clear Instructions:** Be explicit and specific. Tell the model what to do, what not to do, and the format for the output.
-   **Message Roles (`developer`, `user`, `assistant`):** Use roles to structure the conversation. The `developer` role sets the high-level rules and persona, while the `user` role provides the specific query.
-   **Few-Shot Learning:** Provide a few examples of input-output pairs in your prompt to teach the model the desired pattern.
-   **Markdown and XML Formatting:** Use headers, lists, and XML tags (`<example>`, `</example>`) to create a clear, structured prompt that is easy for the model to parse.

**Code Example: Using Roles and Few-Shot Learning**

```python
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "developer",
            "content": """
# Identity
You are a sentiment analysis expert. Classify the following user review as Positive, Negative, or Neutral. Respond with only a single word.

# Examples
<review>The battery life is incredible!</review>
<response>Positive</response>

<review>The screen scratches easily.</review>
<response>Negative</response>
"""
        },
        {
            "role": "user",
            "content": "<review>It's an okay phone for the price.</review>"
        }
    ]
)

print(response.output_text)
# Expected Output: Neutral
```

### 3. Model Selection: Choosing Your Engine

OpenAI offers a range of models, each with different strengths. The choice depends on your needs for accuracy, speed, cost, and reasoning capabilities.

| Model     | Core Strength                 | Ideal For                               |
|-----------|-------------------------------|-----------------------------------------|
| **GPT-4.1** | 1M token context, high accuracy | Long-document analysis, complex text tasks |
| **o3**      | Deep, multi-step reasoning    | High-stakes decisions, complex tool use |
| **o4-mini** | Fast, cost-effective reasoning  | High-volume, "good-enough" logic      |
| **GPT-4o**  | Real-time voice/vision chat   | Live, multimodal agents                 |

**Key Takeaway:** Start with a powerful model like `gpt-4.1` to establish a baseline, then experiment with smaller/cheaper models like `o4-mini` if your task allows.

### 4. Agents: The What and Why

An **agent** is a system that uses an LLM to intelligently and independently accomplish tasks on your behalf. Unlike a simple chatbot, an agent can:

1.  **Make decisions** and manage a workflow.
2.  **Use tools** to interact with external systems (APIs, databases, etc.).
3.  Operate within **guardrails** to ensure safe and predictable behavior.

Build an agent when your workflow involves complex decision-making, hard-to-maintain rules, or requires understanding unstructured data.

### 5. Agent Design Foundations: The Blueprint

Every agent is built on three pillars:

1.  **Model:** The LLM brain.
2.  **Tools:** The agent's hands and eyes to interact with the world.
3.  **Instructions:** The rulebook and personality.

**Best Practices for Instructions:**

-   **Be Specific:** Define clear actions and steps.
-   **Use Existing Docs:** Convert your existing SOPs or help articles into agent instructions.
-   **Handle Edge Cases:** Tell the agent how to react when things go wrong or the user asks something unexpected.

---

## 🚀 Activities

### Activity 1: Use-Case Kickoff & Team Formation

1.  **Form Teams:** Group up with 2-3 other participants.
2.  **Brainstorm:** Discuss and choose a real-world problem that an AI agent could solve. Think about your own workflows or business challenges.
3.  **Fill out the PRD:** Collaboratively complete the **Agent Product Requirements Document (PRD)** for your chosen use case. This will be your guiding document for the rest of the workshop.

### Activity 2: Your First API Calls & Prompt Engineering

1.  **Setup:** Ensure your `OPENAI_API_KEY` is set.
2.  **Run the Code:** Execute the **Text Generation** and **Image Analysis** examples from the Key Concepts section.
3.  **Experiment:**
    *   Modify the text generation prompt to create a different kind of story or a poem.
    *   Try the sentiment analysis example with your own reviews.
    *   Change the `developer` prompt to make the agent respond in a different style (e.g., as a Shakespearean character).

### Activity 3: Model Selection

1.  **Discuss:** As a team, review the **LLM Model Selection Worksheet**.
2.  **Decide:** Based on your Agent PRD, choose a starting model for your agent. Fill out the worksheet to justify your choice. Consider the trade-offs between cost, speed, and intelligence for your specific use case.

---

## 📄 Worksheets

### Agent Product Requirements Document (PRD)

**A. Project/Agent Name:**
<!-- Enter your team’s agent name or codename here -->

**B. Problem Statement:**
<!-- What specific business/user problem does this agent solve? Be specific. -->

**C. Target Users / Stakeholders:**
<!-- Who will use the agent? Who benefits from it? -->

**D. User Stories / Sample Prompts:**
<!-- Write at least 3 realistic user prompts your agent must handle successfully. -->
-   As a user, I want to ask... so that I can...
-   
-   

**E. Key Capabilities (MVP):**
<!-- Mark must-have [x] and nice-to-have [ ] features. -->

-   [ ] Natural language Q&A
-   [ ] Retrieval from internal docs (RAG)
-   [ ] Calls external APIs (specify which): ___________
-   [ ] Handles file inputs (PDF, images)
-   [ ] Follows multi-turn conversations
-   [ ] Handoffs/escalations to humans
-   [ ] Structured outputs (JSON)

**F. Guardrails / Risks / Constraints:**
<!-- What are the biggest risks? What should the agent NEVER do? -->

-   [ ] PII detection/redaction
-   [ ] Moderation API on inputs/outputs
-   [ ] Blocklist for prohibited topics (e.g., financial advice)
-   [ ] Human-in-the-loop for sensitive actions

**G. Success Metrics / KPIs:**
<!-- How will you measure success? Be specific and measurable. -->

-   e.g., 90% accuracy on categorizing support tickets, <5% human handoff rate, average response time under 3 seconds.

**H. Initial System/Assistant Instructions:**
<!-- Write a first draft of the main prompt for your agent. -->

---

### LLM Model Selection Worksheet

| Criteria                   | Option 1 (e.g. GPT-4.1) | Option 2 (e.g. o4-mini) | Notes & Justification for Your Choice |
|----------------------------|-------------------------|-------------------------|---------------------------------------|
| **Accuracy/Reasoning**     |                         |                         | *Does your task require deep, complex reasoning or is it straightforward?* |
| **Speed/Latency**          |                         |                         | *How quickly does the user need a response?* |
| **Cost**                   |                         |                         | *What is your budget for this agent?* |
| **Context Length**         |                         |                         | *Will you need to process large documents?* |
| **Required Features**      |                         |                         | *Do you need function calling, vision, etc.?* |

**Final Decision & Rationale:**
_We will start with the ________ model because..._

---

## ✅ Day 1 Success Checklist

-   [ ] Your team has a completed Agent PRD.
-   [ ] You have successfully run basic OpenAI API calls for text and images.
-   [ ] You have experimented with prompt engineering techniques.
-   [ ] Your team has selected a starting LLM and justified the choice.
-   [ ] You have a clear vision for the agent you will build over the next few days.
