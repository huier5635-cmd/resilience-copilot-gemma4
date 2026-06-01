# Manuscript Outline

## Possible Title

Safety-Bounded LLM Agents for High-Risk Case-Note Triage

## Abstract Draft

LLM agents can convert messy field notes into readable summaries, but high-risk decision support requires explicit boundaries around generation, memory, tools, and auditability. We present Resilience Copilot, a prototype safety-bounded LLM agent for disaster-relief case-note triage. The system separates responder-facing language generation from safety-critical control logic using a deterministic sidecar, playbook matching, official-resource verification, bounded memory, human-review triggers, structured JSON export, and Audit Trace. We evaluate the prototype on a self-built 30-case scenario benchmark and a stress suite covering medical continuity, power outages, flood danger, transport barriers, language access, shelter rumors, pet shelter constraints, and resource uncertainty. Results show that deterministic safety controls improve contract completeness, risk-signal coverage, audit completeness, and unsupported-claim blocking on the benchmark. The system is not a deployed emergency tool; it is a reproducible prototype for studying safety boundaries in LLM agents.

## Section Plan

1. Introduction
   - Why high-risk LLM-agent outputs need safety boundaries
   - Disaster-relief case-note triage as a compact testbed
   - Contributions

2. Task and Safety Requirements
   - Input/output definition
   - Forbidden behaviors
   - Human-review conditions
   - Non-goals

3. Method
   - Safety-Bounded LLM Agent with Deterministic Sidecar and Memory Write Gate
   - Generation boundary
   - Policy boundary
   - Memory boundary
   - Tool/resource verification sandbox
   - Audit Trace and structured export

4. Benchmark and Evaluation Protocol
   - Self-built scenario benchmark
   - Stress suite
   - Ablation variants
   - Metrics
   - Stratified evaluation by risk type and uncertainty type

5. Results
   - Variant summary
   - Stratified results
   - Failure taxonomy
   - Memory policy observations

6. Discussion
   - Safety-control benefits
   - Memory pollution and policy drift
   - Limits of deterministic rules
   - Difference between reproducibility evidence and field readiness

7. Limitations
   - Hand-authored data
   - No live official-resource lookup
   - Deterministic fallback in local evaluation
   - No expert adjudication

8. Future Work
   - Larger expert-reviewed benchmark
   - Cross-model comparison
   - Official-resource API sandbox
   - Multi-agent planning under safety contracts

## Figure List

- Figure 1: System architecture with pre-generation and post-generation safety chains.
- Figure 2: Three-boundary safety design: generation, policy, memory.
- Figure 3: Memory write gate and quarantine flow.
- Figure 4: Example responder handoff with Transfer Brief, JSON export, and Audit Trace.

## Table List

- Table 1: Failure modes and controls.
- Table 2: Benchmark metadata categories.
- Table 3: Ablation variants.
- Table 4: Academic evaluation metrics.
- Table 5: Failure taxonomy counts.
