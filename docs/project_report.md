# Project Report

## 1. Background

High-risk case-note processing is a difficult setting for LLM systems. Volunteers and coordinators may receive short, incomplete, or uncertain notes about power outages, medical-device dependency, medication continuity, flood access, language barriers, pet shelter constraints, and unverified shelter rumors. A fluent chatbot can make these notes easier to read, but fluency alone is not enough. The system must avoid unsupported claims, separate known facts from unknown facts, trigger human review, and preserve an audit trail.

Resilience Copilot frames this as a safety-control problem for LLM agents. The prototype uses language generation for responder-facing phrasing, while deterministic sidecars handle risk detection, playbook constraints, official-resource checks, memory write gating, and structured export.

## 2. Problem Definition

Input: a messy disaster-relief case note.

Output: a responder handoff that includes risk level, detected signals, playbook references, official-resource checks, human-review reason, Transfer Brief, structured JSON export, and Audit Trace.

The goal is not to dispatch emergency resources, diagnose medical conditions, or promise live shelter or transport availability. The goal is to produce a bounded and auditable intermediate packet that a responder can review.

## 3. System Architecture

The system is named **Safety-Bounded LLM Agent with Deterministic Sidecar and Memory Write Gate**.

It separates three boundaries:

- **Generation boundary**: the LLM is responsible for natural-language drafting and responder-facing phrasing.
- **Policy boundary**: deterministic sidecar modules, playbooks, and response contracts determine what claims are allowed.
- **Memory boundary**: memory can retrieve reviewed experience and suggest patterns, but it cannot modify protected safety invariants.

The main flow is:

```text
User Case Note
-> Input Normalization
-> Risk Signal Detection
-> Playbook Matching
-> LLM / Gemma Generation
-> Safety Contract Checking
-> Official Resource Verification
-> Memory Retrieval / Protected Invariants
-> Human Review Trigger
-> Structured JSON Export
-> Audit Trace
-> Responder Handoff
```

## 4. Core Modules

- **Risk Signal Detection** detects oxygen or powered-device risk, medication continuity, child cold exposure, heat exposure, flood danger, language access, transport barriers, shelter rumors, and pet shelter needs.
- **Playbook Matching** maps risk signals to auditable response constraints in `knowledge_base/emergency_playbook.json`.
- **Gemma Generation Path** records Gemma 4 use in a Kaggle evidence notebook. Local evaluation uses deterministic fallback behavior so the benchmark remains reproducible.
- **Safety Contract Checking** verifies the fixed response shape, structured JSON, Audit Trace, and unsupported-claim patterns.
- **Tool/Resource Verification Sandbox** blocks unsupported capacity, transport, road-safety, and clinic-availability claims unless official channels are explicitly required.
- **Memory Write Gate** quarantines unreviewed runtime observations and allows only reviewed feedback to enter retrievable long-term memory.

## 5. Safety Mechanisms

The system explicitly blocks or quarantines:

- medical diagnosis or medication instructions
- invented shelter capacity
- invented transport availability
- road-safety guarantees
- unsupported clinic or pharmacy availability
- replacement of emergency services
- unsafe ad hoc interpretation for sensitive details

High-risk and verification-sensitive cases trigger human review. Audit Trace records risk level, signals, playbooks, official-resource routes, blocked claims, and review reason.

## 6. Evaluation Design

The project uses self-built scenario evaluation because no official training dataset was provided for this task. The evaluation has three parts:

1. Local validation gate for demo, holdout, and stress scenarios.
2. A 30-case benchmark covering oxygen, insulin, cold exposure, flood, power outage, transport barriers, language access, pet shelter, social-media rumor, unknown capacity, medical continuity, and official-resource uncertainty.
3. Stratified academic-style evaluation by risk type, uncertainty type, and safety invariant.

The ablations are:

- A. Base LLM fallback
- B. LLM + Risk Signal Detection
- C. LLM + Safety Sidecar
- D. LLM + Safety Sidecar + Memory
- E. LLM + Safety Sidecar + Tool/Resource Verification

Metrics include human-review precision/recall/F1, risk-signal recall, contract completeness, audit completeness, unsafe-claim block rate, structured JSON validity, and hallucinated-resource detection.

## 7. Results

The locked local gate previously passed demo 2/2, holdout 2/2, and stress 15/15 with `ready_to_submit=true`. The benchmark and academic reports can be regenerated with:

```powershell
python scripts\run_eval.py
python scripts\run_academic_eval.py
python scripts\run_stress_test.py
```

The reported results should be interpreted as evidence that the implemented safety controls behave consistently on a small self-built benchmark. They are not evidence of field readiness or real-world outcome improvement.

## 8. Main Contributions

The project contribution is a compact, reproducible prototype for high-risk LLM-agent safety:

- deterministic safety sidecar around generation
- explicit response contract and structured export
- official-resource-first verification logic
- bounded memory with write gate and protected invariants
- human-review trigger and Audit Trace
- benchmark protocol for safety-control regression testing

## 9. Limitations

- The benchmark is small and hand-authored.
- The local evaluation path uses deterministic fallback behavior rather than live LLM calls.
- The resource verifier is an offline sandbox, not a live official-resource API.
- Human-review labels are scenario expectations rather than expert-adjudicated operational labels.
- Memory retrieval is intentionally conservative and does not perform autonomous policy learning.

## 10. Future Work

Future work can extend the project in four directions:

- build a larger expert-reviewed benchmark for high-risk case-note processing
- compare multiple LLM backbones under the same deterministic safety contract
- add provenance-aware memory review workflows and attack tests for memory pollution
- connect approved official-resource APIs inside the tool sandbox while preserving human review for high-risk cases
