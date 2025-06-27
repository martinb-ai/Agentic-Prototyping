# Day 3: Production Readiness (Safety, Guardrails, Observability)

## 📝 Overview

Welcome to Day 3! Now that we have a functional agent, it's time to get it ready for the real world. This session focuses on the critical aspects of production readiness: ensuring safety, implementing guardrails, and making your agent observable.

## 🎯 Day 3 Goals

-   Understand and implement moderation and safety best practices.
-   Build and apply guardrails to control agent behavior.
-   Learn how to trace and monitor agent runs for observability.
-   Explore different agent orchestration patterns.
-   Understand how to use handoffs to delegate tasks between agents.

---

## 📖 Key Concepts

### 1. Safety and Moderation

Ensuring the safety of your application is paramount. OpenAI provides a free Moderation API to help you identify and filter harmful content.

**Key Safety Practices:**
-   **Adversarial Testing:** Test your application with a wide range of inputs to identify vulnerabilities.
-   **Human in the Loop (HITL):** Have a human review outputs, especially in high-stakes domains.
-   **Prompt Engineering:** Constrain the topic and tone of outputs.
-   **End-User IDs:** Send unique user identifiers in your API requests to help monitor and detect abuse.

**Code Example: Moderation API**

```python
from openai import OpenAI
client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input="...text to classify goes here...",
)

print(response)
```

### 2. Guardrails

Guardrails are checks and validations on user inputs and agent outputs to manage risks and enforce policies.

**Types of Guardrails:**
-   **Input Guardrails:** Run on the initial user input.
-   **Output Guardrails:** Run on the final agent output.

**Code Example: Input Guardrail**

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )
```

### 3. Observability (Tracing)

The Agents SDK has built-in tracing to help you debug, visualize, and monitor your agent workflows. You can view traces in the OpenAI Dashboard.

**Key Concepts:**
-   **Traces:** Represent a single end-to-end operation.
-   **Spans:** Represent operations within a trace that have a start and end time.

**Code Example: Creating a Trace**

```python
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"):
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
```

### 4. Orchestration and Handoffs

Orchestration is about managing the flow of agents in your application. You can orchestrate agents using the LLM's intelligence or through code.

**Handoffs** allow one agent to delegate a task to another, which is useful for creating specialized agents.

**Code Example: Creating a Handoff**

```python
from agents import Agent, handoff

billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

triage_agent = Agent(name="Triage agent", handoffs=[billing_agent, handoff(refund_agent)])
```

### 5. Production Best Practices

When moving to production, consider:
-   **Scaling:** Horizontal and vertical scaling strategies.
-   **Latency:** Optimize for speed by choosing the right models and using techniques like streaming.
-   **Cost:** Manage costs by selecting appropriate models and using prompt caching.
-   **Security:** Implement robust security and compliance measures.

---

## 🚀 Activities

### Activity 1: Add Moderation

1.  Integrate the Moderation API into your application.
2.  Create a function that takes user input, sends it to the Moderation API, and flags any potentially harmful content.
3.  Test your moderation function with various inputs.

### Activity 2: Implement a Guardrail

1.  Identify a behavior you want to prevent in your agent (e.g., going off-topic, providing financial advice).
2.  Create a guardrail agent that checks for this behavior.
3.  Implement an input or output guardrail using the `@input_guardrail` or `@output_guardrail` decorator.
4.  Test your guardrail to ensure it triggers correctly.

### Activity 3: Trace Your Agent

1.  Wrap a multi-turn conversation with your agent in a `with trace(...)` block.
2.  Run the conversation.
3.  Go to the Traces dashboard in your OpenAI account and inspect the trace. Identify the different spans and understand the flow of your agent.

### Activity 4: Create a Multi-Agent System

1.  Design a simple multi-agent system with a triage agent and at least two specialized agents.
2.  Implement handoffs from the triage agent to the specialized agents.
3.  Write a prompt that requires the triage agent to hand off to one of the specialized agents.
4.  Run the system and verify that the handoff occurs correctly.

---

## ✅ Day 3 Success Checklist

-   [ ] Implemented content moderation using the Moderation API.
-   [ ] Created and tested a custom guardrail for your agent.
-   [ ] Successfully traced a multi-turn conversation and analyzed the trace.
-   [ ] Built a multi-agent system with handoffs.
-   [ ] Developed a plan for scaling, latency, and cost management in production.
