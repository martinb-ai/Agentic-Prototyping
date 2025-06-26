## 📋 Agent Product Requirements Document (PRD)

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

## 🧮 LLM Model Selection Worksheet

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

## 🧪 Prompt Engineering Starter Table

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