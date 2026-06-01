# Related Work

This project sits at the intersection of LLM agents, tool use, memory systems, human-in-the-loop safety, auditability, and disaster informatics.

## LLM Agents and Tool Use

ReAct-style agents combine reasoning traces with tool actions, showing that language models can interleave analysis and external operations. Toolformer studies how models can learn to call tools, while later agent systems use planners, executors, and tool routers to decompose tasks. Resilience Copilot uses the agent idea more conservatively: the system may call an offline verification sandbox, but tool use is white-listed and cannot override safety rules.

## Reflection and Skill Accumulation

Reflexion and Voyager show that agents can improve through feedback, reflection, and accumulated skills. This project adopts that direction only inside a bounded loop. Runtime observations are quarantined; only reviewed validation feedback can become retrievable memory. Skills can inform future suggestions, but they cannot update protected safety invariants automatically.

## Long-Term Memory

Generative Agents and MemGPT motivate persistent memory, retrieval, and memory management for LLM systems. In high-risk settings, memory is also an attack surface: stale, biased, adversarial, or unreviewed memory can contaminate later outputs. Resilience Copilot therefore treats memory as advisory retrieval with a write gate, not as a source of automatic policy change.

## Retrieval-Augmented Generation

RAG systems ground generation in retrieved documents or knowledge bases. Resilience Copilot is related but narrower: it retrieves playbook constraints and reviewed memory, while official-resource claims remain blocked unless a permitted verification path is available. The goal is not maximum recall of documents; it is controlled handoff generation under explicit constraints.

## Human-in-the-Loop Safety

High-risk decision support often requires escalation, review, and explicit responsibility boundaries. This project uses human-review triggers for cases involving medical continuity, powered devices, flood danger, language access, transport barriers, and uncertain resource availability. Human review is part of the system contract rather than an optional afterthought.

## Auditability and Safety Contracts

Safety contracts make outputs inspectable by requiring structured sections, blocked-claim records, and trace fields. Resilience Copilot uses a fixed response contract and Audit Trace so downstream reviewers can inspect why a risk level, playbook, official route, or review reason appeared.

## Disaster Informatics

Disaster informatics studies how crisis information appears in social media, volunteer reports, and emergency coordination channels. These sources are often incomplete, noisy, multilingual, and rumor-prone. This project uses disaster-relief case notes as a compact testbed for high-risk LLM-agent safety because the domain naturally combines uncertainty, urgency, resource constraints, and human review.

## Positioning

The project differs from unrestricted autonomous agents in three ways:

1. The LLM handles responder-facing phrasing, not safety policy.
2. The deterministic sidecar enforces risk detection, playbook constraints, resource checks, and response-contract validation.
3. Memory is retrieval-only unless reviewed; it cannot rewrite protected safety invariants.
