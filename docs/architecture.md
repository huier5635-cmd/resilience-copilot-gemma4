# Architecture

Resilience Copilot is a safety-bounded agent pattern for high-risk workflows where a human reviewer remains accountable. The disaster-relief demo is the reference implementation.

## Runtime Flow

```text
Case Note
  -> Risk Signal Detector
  -> Playbook Matcher
  -> Gemma 4 Generation
  -> Safety Contract Checker
  -> 16-section Response
  -> JSON Export + Audit Trace + Transfer Brief
```

## Learning Sidecar

The learning sidecar is offline and review-first. It does not change runtime policy automatically.

```text
Validation Feedback
  -> Experience Ledger
  -> Memory Write Gate
  -> Bounded Long-Term Memory
  -> Strategy Reflection
  -> Human-Reviewed Skill Library
  -> Next-Round Policy Suggestions
```

## Memory Pollution Controls

Runtime case notes are not trusted as long-term memory. The public agent core uses a Memory Write Gate:

- raw runtime input is ledger-only;
- failed or unvalidated feedback is quarantined;
- long-term memory promotion requires local validation, confidence, and human review;
- protected invariants cannot be changed by memory;
- strategy reflection can propose future improvements but cannot update runtime policy automatically.

Protected invariants include no emergency-service replacement, no medical diagnosis, no invented live capacity, no invented transport availability, no external actions, and human review before policy updates.

## Safety Contract

The safety contract blocks common failure modes before an answer becomes reviewer-facing:

- no medical diagnosis or treatment instruction;
- no invented shelter capacity, road status, transport availability, or official confirmation;
- no unsupported reassurance when power, oxygen, heat, medication, mobility, language access, or rumor risk appears;
- no replacement for emergency services;
- no automatic action outside the review boundary.

## Why This Is Not a Free-Running Agent

The project is agentic in orchestration and feedback use, but bounded in authority. The system can detect risk, retrieve relevant playbook constraints, compose a structured response, export an audit trace, and propose future strategy improvements. It cannot contact responders, book resources, promote new policies, or treat unverified claims as facts.

## Adaptation Points

To adapt the pattern to another domain, replace these components:

| Component | Disaster demo | Other high-risk workflow |
| --- | --- | --- |
| Risk signals | oxygen, heat, rumors, shelter, mobility | domain-specific red flags |
| Playbooks | emergency routing constraints | policy or SOP constraints |
| Response contract | 16 disaster triage sections | reviewer-facing checklist |
| Validation cases | demo, holdout, stress scenarios | local scenario suite |
| Safety sidecar | no diagnosis, no invented capacity | domain-specific blocked claims |

Keep these components stable:

- human review;
- deterministic safety checks;
- audit trace;
- local validation gate;
- no hidden online dependency for review.
