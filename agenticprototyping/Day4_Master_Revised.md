# Day 4: Evaluation & Optimization

## 📝 Overview

Welcome to Day 4! This is where we transform a functional agent into a high-performing one. Today is dedicated to the science of evaluation and the art of optimization. You will learn how to systematically measure your agent's performance, design robust evaluation suites, and apply advanced techniques like RAG and fine-tuning to boost accuracy and reliability. By the end of the day, you will have a clear framework for iterating on and improving your agent.

## 🎯 Day 4 Goals

-   Understand and implement a systematic evaluation process for your agent.
-   Learn to design task-specific evals that reflect real-world use cases.
-   Master the use of the Evals API to automate testing.
-   Develop a mental model for optimization: knowing when to use Prompt Engineering, RAG, or Fine-Tuning.
-   Apply these optimization techniques to improve your agent's accuracy and consistency.

---

## 📖 Key Concepts

### 1. The Importance of Evaluation (Evals)

In the world of non-deterministic AI, traditional testing is not enough. **Evals** are structured tests that measure your agent's performance against a set of criteria. A good evaluation process is the cornerstone of building a reliable AI application.

**The Eval-Driven Development Cycle:**
1.  **Define Objective:** What does success look like for a specific task?
2.  **Collect Dataset:** Gather representative data, including common inputs, edge cases, and adversarial examples.
3.  **Define Metrics:** How will you score performance? (e.g., exact match, human review, LLM-as-a-judge).
4.  **Run & Compare:** Use the Evals API to test different prompts, models, or configurations.
5.  **Iterate:** Use the results to guide your next optimization step.

### 2. Creating and Running Evals

The Evals API allows you to programmatically define and run your tests.

**Step 1: Create an Eval Definition**
First, you define the *shape* of your test data and the *criteria* for success.

```python
from openai import OpenAI
client = OpenAI()

eval_obj = client.evals.create(
    name="IT Ticket Categorization",
    data_source_config={
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "ticket_text": {"type": "string"},       # Input for the model
                "correct_label": {"type": "string"},    # The ground truth answer
            },
            "required": ["ticket_text", "correct_label"],
        },
        "include_sample_schema": True,
    },
    testing_criteria=[
        {
            "type": "string_check",
            "name": "Match output to human label",
            "input": "{{ sample.output_text }}",  # The model's generated output
            "operation": "eq",
            "reference": "{{ item.correct_label }}", # The ground truth from our data
        }
    ],
)

eval_id = eval_obj.id
```

**Step 2: Create a Dataset and Run the Eval**
Next, you upload a dataset and run the eval against a specific prompt.

```python
# 1. Create a JSONL file (e.g., tickets.jsonl) with your test data
# {"item": {"ticket_text": "My monitor won't turn on!", "correct_label": "Hardware"}}
# {"item": {"ticket_text": "I can't quit vim!", "correct_label": "Software"}}

# 2. Upload the file
file_obj = client.files.create(file=open("tickets.jsonl", "rb"), purpose="evals")
file_id = file_obj.id

# 3. Create the eval run
run = client.evals.runs.create(
    eval_id, # The ID from Step 1
    name="Categorization Test Run v1",
    data_source={
        "type": "completions",
        "model": "gpt-4.1",
        "input_messages": {
            "type": "template",
            "template": [
                {"role": "developer", "content": "You are an expert categorizer. Classify the ticket into: Hardware, Software, or Other."},
                {"role": "user", "content": "{{ item.ticket_text }}"},
            ],
        },
        "source": {"type": "file_id", "id": file_id},
    },
)

print(f"Eval run created! View progress at: {run.report_url}")
```

### 3. The Optimization Framework: Context vs. Consistency

When your agent fails an eval, the reason usually falls into one of two categories. Your optimization strategy depends on diagnosing the problem correctly.

![Accuracy mental model diagram](images/optimizing-accuracy.png)

-   **Context Problem (Accuracy):** The agent is wrong because it **lacks knowledge**. The information wasn't in its training data, is out of date, or is proprietary.
    -   **Solution:** **Retrieval-Augmented Generation (RAG)**. Give the model the information it needs at runtime.

-   **Behavior Problem (Consistency):** The agent **knows** what to do but does it **unreliably**. It fails to follow instructions, uses the wrong format, or has an inconsistent tone.
    -   **Solution:** **Fine-Tuning**. Show the model 50-100+ examples of the task being performed correctly to ingrain the desired behavior.

**Key Takeaway:** Don't jump to fine-tuning if the problem is a lack of context. RAG is often faster, cheaper, and more effective for knowledge-based issues.

### 4. Evaluation Design for Agentic Architectures

As your agent becomes more complex (e.g., using tools and handoffs), your evaluation strategy must also evolve.

| Architecture      | Key Evaluation Questions                                                                                             |
|-------------------|----------------------------------------------------------------------------------------------------------------------|
| **Single Agent**  | **Tool Selection:** Does it choose the right tool for the job? <br> **Data Precision:** Does it call the tool with the correct arguments? |
| **Multi-Agent**   | **Handoff Accuracy:** Does the triage agent route the query to the correct specialist? Does a specialist hand back control when appropriate? |

---

## 🚀 Activities

### Activity 1: Create and Run Your First Eval

1.  **Define the Task:** Choose a simple, core task your agent performs (e.g., classifying an email, summarizing a paragraph, extracting a specific piece of information).
2.  **Create a Dataset:** Create a small `evals.jsonl` file with at least 5-10 examples. Each line should contain an `item` with the input for the model and the `correct_label` (the ground truth).
3.  **Define the Eval:** Write the Python code to create an eval definition using `client.evals.create`. For a classification task, a `string_check` with the `eq` (equals) operation is a good start.
4.  **Run the Eval:** Write the code to upload your dataset and create an eval run using `client.evals.runs.create`. Test the prompt you are currently using for your agent.
5.  **Analyze the Report:** Open the `report_url` from the run response. Review the results. Where did the agent fail? Where did it succeed?

### Activity 2: The Optimization Challenge

1.  **Diagnose the Failures:** Look at the failed cases from Activity 1. As a team, diagnose the root cause. Is it a **context problem** (the agent didn't know something) or a **behavior problem** (the agent didn't follow instructions)?
2.  **Form a Hypothesis:** Based on your diagnosis, propose an optimization strategy.
    *   *"If we provide the product return policy in the prompt (simple RAG), the agent will answer policy questions correctly."*
    *   *"If we show the agent three examples of correctly formatted JSON (few-shot prompting), it will stop making formatting errors."*
3.  **Implement the Fix:** Modify your prompt or agent logic based on your hypothesis.
4.  **Re-run the Eval:** Create a new eval run with your improved prompt/agent.
5.  **Compare Results:** Did your pass rate improve? Discuss why or why not.

### Activity 3: Design an Eval for a Multi-Agent System

1.  **Map the Flow:** Look at the multi-agent system you designed on Day 2. Identify the key decision points.
    *   The initial triage decision.
    *   A specialist agent's decision to use a tool.
    *   A specialist agent's decision to hand back to triage.
2.  **Design the Evals:** For each decision point, describe an eval you would create. What would the `item_schema` look like? What `testing_criteria` would you use?
    *   **Example (Triage Handoff):**
        *   `item_schema`: `{"user_query": "...", "correct_handoff_agent_name": "..."}`
        *   `testing_criteria`: An LLM-as-a-judge eval that checks if the `last_agent.name` in the run result matches the `correct_handoff_agent_name`.
3.  **Discuss:** Share your evaluation designs with the group. How would you test for incorrect tool use or circular handoffs?

---

## ✅ Day 4 Success Checklist

-   [ ] You have successfully created and run an automated eval for your agent.
-   [ ] You can articulate the difference between a context problem and a behavior problem.
-   [ ] You have applied at least one optimization technique (improving the prompt, adding context) and measured its impact.
-   [ ] You have designed a comprehensive evaluation plan for a multi-agent system, covering handoffs and tool use.
-   [ ] You are prepared to use an eval-driven approach to systematically improve your agent.
