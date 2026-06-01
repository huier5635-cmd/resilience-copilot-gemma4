# Discussion Q&A

## 1. How is this different from prompt engineering?

Prompt engineering changes the model instruction. This project moves safety-critical logic outside the prompt: deterministic risk detection, playbook constraints, resource verification, memory write gating, response-contract checks, and audit traces.

## 2. What is the deterministic safety sidecar?

It is the rule-based control layer around generation. Before generation it detects risk signals and selects playbook constraints. After generation it checks the response contract, structured JSON, Audit Trace, and unsupported-claim patterns.

## 3. Why use deterministic controls?

High-risk systems need repeatable behavior. Deterministic controls are testable, auditable, and easier to debug when a safety case fails.

## 4. What is the sixteen-section response contract?

It is a fixed output structure containing risk level, case signals, human-review reason, playbook references, action plan, official-resource checks, source verification, Transfer Brief, clarifying questions, language support, responder handoff, responder packet, household message, Audit Trace, case export, and safety boundary.

## 5. Why is memory risky?

Memory can preserve wrong, stale, or adversarial information. A rumor about shelter beds could contaminate future cases if it becomes long-term memory without review.

## 6. How does the memory write gate work?

Runtime observations are quarantined by default. Only reviewed validation feedback can enter retrievable long-term memory. Even approved memory is advisory and cannot rewrite protected safety invariants.

## 7. What are protected safety invariants?

They are rules that memory and reflection cannot modify automatically: no diagnosis, no invented capacity, no transport guarantees, no replacement of emergency services, and human review for high-risk cases.

## 8. What does the tool/resource verification sandbox do?

It blocks unsupported resource claims and keeps the system offline and auditable. It can require official categories such as emergency management, shelter operations, medical triage, transport desk, animal services, or language access line.

## 9. What is Audit Trace used for?

Audit Trace records risk level, detected signals, playbook ids, official routes, blocked claims, and human-review reason. It makes the handoff reviewable after generation.

## 10. How do you evaluate safety?

The project uses local validation, a 30-case self-built benchmark, a stress suite, and unit tests. Metrics include human-review precision/recall/F1, risk-signal recall, contract completeness, audit completeness, unsafe-claim block rate, and structured JSON validity.

## 11. Is the benchmark real operational data?

No. It is self-built scenario data for safety-control regression testing. Real deployment would require expert-labeled data and official operational partnerships.

## 12. How do you detect hallucination?

The benchmark focuses on high-risk hallucinations: invented shelter capacity, transport availability, route safety, clinic status, and medical claims. The resource sandbox and contract checker block these patterns.

## 13. How is human review triggered?

Human review is triggered for high-risk or verification-sensitive cases, including powered medical devices, medication continuity, flood danger, language access, transport barriers, and uncertain resource availability.

## 14. How is this related to RAG?

It uses retrieval-like components for playbooks and reviewed memory, but the core goal is not open-ended knowledge retrieval. The core goal is constrained, auditable handoff generation under safety rules.

## 15. How is this different from a chatbot?

A chatbot gives a direct answer. This system prepares a responder handoff with known facts, unknowns, official-resource checks, blocked claims, review reasons, and structured export.

## 16. Is this an autonomous agent?

It is a safety-bounded agent prototype, not an unrestricted autonomous agent. It has workflow, memory, tool sandbox, reflection hooks, and validation feedback, but high-risk policy remains deterministic and human-reviewed.

## 17. Where is the research question?

The research question is how to keep LLM-agent behavior useful while preserving safety boundaries, auditability, memory integrity, and human review in high-risk tasks.

## 18. What is the main engineering challenge?

The challenge is consistency: the demo, CLI, tests, JSON export, Audit Trace, response contract, benchmark, and documentation all need to describe the same system behavior.

## 19. What failure cases are most important?

The most important failures are missed escalation, resource hallucination, unsafe medical overreach, memory pollution, policy drift, and missing audit fields.

## 20. What if the model output conflicts with the safety sidecar?

The sidecar wins. If generated text claims shelter capacity or transport availability without verification, the post-generation check blocks or flags that claim.

## 21. How do you prevent memory pollution?

Unreviewed runtime observations remain quarantined. Approved memory is retrievable context only. Policy updates are proposed but never applied automatically.

## 22. Could this extend to robotics or emergency logistics?

Yes, but only if tool actions are white-listed, audited, and human-reviewed. The current project produces a handoff packet; it does not execute physical or dispatch actions.

## 23. Could this become a multi-agent system?

Yes. A planner, risk specialist, resource verifier, memory reviewer, and safety checker could collaborate, but the coordinator should still be governed by deterministic safety contracts.

## 24. How would you make evaluation stricter?

Add expert annotations, adversarial rumor injection, multi-region resource phrasing, cross-model comparisons, larger stress suites, and inter-rater agreement for review labels.

## 25. Why Gemma?

The original challenge focused on Gemma. In this architecture, Gemma is used for responder-facing phrasing, while the sidecar holds the safety policy. That makes the architecture model-portable.

## 26. Can this transfer to GPT, Qwen, or DeepSeek?

Yes. The generation boundary can swap model backends while keeping risk detection, playbooks, contract checking, memory policy, tool sandbox, and audit trace intact.

## 27. What is the biggest limitation?

The benchmark and resource checks are prototype-scale. They do not prove real-world readiness or operational impact.

## 28. What part is most technically meaningful?

The memory boundary is the most interesting part: the system can learn from reviewed feedback while preventing unreviewed memory from changing high-risk policy.

## 29. How does the project show computer-science ability?

It combines software architecture, rule systems, agent design, structured data modeling, safety evaluation, unit tests, static demo engineering, and reproducible experiment scripts.

## 30. What would be the next deep research direction?

The next direction is memory pollution and policy drift in high-risk LLM agents: how an agent can use experience without allowing experience to weaken protected safety rules.
