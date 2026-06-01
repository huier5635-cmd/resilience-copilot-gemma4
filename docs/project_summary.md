# Project Summary

## Safety-Bounded LLM Agent for High-Risk Decision Support

Resilience Copilot is a prototype LLM-agent system for high-risk disaster-relief case-note triage. The project studies how to combine deterministic rules, risk recognition, tool/resource verification, bounded long-term memory, human review, and audit traces so that LLM-assisted outputs remain useful, reproducible, and constrained.

The system processes messy case notes such as power outages affecting oxygen concentrators, medication continuity during heat waves, flood evacuation barriers, language-access needs, pet shelter constraints, and unverified shelter rumors. Instead of giving a direct unverified answer, the system produces a responder handoff: risk level, detected signals, matched playbooks, official-resource checks, human-review reason, Transfer Brief, structured JSON export, and Audit Trace.

The core design is a **Safety-Bounded LLM Agent with Deterministic Sidecar and Memory Write Gate**. The LLM is used for responder-facing phrasing. The deterministic sidecar enforces safety policy before and after generation. The tool sandbox blocks unsupported claims about capacity, transport, roads, and clinics. The memory module retrieves reviewed experience but quarantines unreviewed runtime observations, preventing memory from rewriting protected safety invariants.

Evaluation is based on a self-built 30-case scenario benchmark and a stress suite. The benchmark covers medical continuity, power dependency, flood danger, transport barriers, language access, pet shelter, resource uncertainty, and social-media rumors. Metrics include human-review precision/recall/F1, risk-signal recall, contract completeness, audit completeness, unsafe-claim block rate, and structured JSON validity. The results are intended as reproducible safety-control tests, not as real-world deployment claims.

The project demonstrates an engineering path for trustworthy LLM agents in high-risk settings: separate generation from policy, keep memory bounded, make tool use auditable, require human review for high-risk cases, and preserve structured evidence for every handoff.
