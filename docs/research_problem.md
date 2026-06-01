# Research Problem

## Title

Safety-Bounded LLM Agent with Deterministic Sidecar and Memory Write Gate

## Motivation

LLM agents are useful for converting messy notes into readable summaries, but high-risk decision support requires more than fluent generation. In disaster-relief case-note triage, an unsafe system may miss escalation signals, invent shelter capacity, promise transport availability, overstate road safety, or let unreviewed memory change future behavior.

This project studies how to wrap language generation with deterministic safety controls, bounded memory, tool/resource verification, and audit traces so that the output remains useful, inspectable, and constrained.

## Task Definition

Given a case note `x`, produce a responder handoff `y` that contains:

- risk level
- detected risk signals
- matched playbook constraints
- official-resource checks
- human-review reason
- Transfer Brief
- structured JSON export
- Audit Trace
- safety boundary statements

The system must also output intermediate evidence: which signals were detected, which playbooks were selected, which claims were blocked, and why human review was or was not required.

## Safety Constraints

The system must preserve these constraints:

- no medical diagnosis or medication instruction
- no invented shelter capacity
- no invented transport availability
- no road-safety guarantee
- no unsupported clinic or pharmacy availability
- no replacement of emergency services
- no unsafe ad hoc interpretation for sensitive details
- no automatic memory-driven modification of protected safety invariants

## Research Questions

1. Can deterministic sidecar modules reduce unsafe or unsupported claims in high-risk LLM-agent outputs?
2. Can a response contract make responder handoffs more auditable and easier to validate?
3. Can bounded memory help retrieve useful prior experience without causing memory pollution or policy drift?
4. Can a tool/resource verification sandbox separate official-resource requirements from unsupported claims?
5. Can scenario-based evaluation expose failure modes such as missed escalation, hallucinated resources, and audit omissions?

## Non-Goals

The prototype does not:

- perform medical diagnosis
- provide emergency dispatch
- contact shelters, utilities, or responders
- query live official systems
- claim operational field readiness
- allow the LLM or memory module to update high-risk policy automatically

## Data and Evaluation Scope

The benchmark is self-built and scenario-based. It is intended for safety-control regression testing and method comparison inside this prototype. It should not be interpreted as real-world effectiveness evidence.
