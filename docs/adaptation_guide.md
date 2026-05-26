# Adaptation Guide

Use this project as a template when an AI assistant must help a human reviewer without taking unsafe autonomous action.

## 1. Define the Review Boundary

Write down what the assistant may do and what it must never do.

Example:

```text
May do:
  classify risk, summarize facts, cite policy constraints, compose handoff text.

Must not do:
  make binding decisions, invent availability, contact external parties, bypass human review.
```

## 2. Create Risk Signals

List the details that should trigger extra caution. Keep them concrete and easy to test.

Examples:

- "oxygen equipment depends on power";
- "unverified social media claim";
- "minor or older adult involved";
- "language access barrier";
- "missing official confirmation";
- "transport or mobility barrier".

## 3. Write Playbook Constraints

Turn policy, SOP, or domain knowledge into short constraints. Each constraint should answer:

- when it applies;
- what the assistant should preserve;
- what the assistant should avoid;
- when human review is required.

## 4. Lock the Response Contract

Define the fields the reviewer always gets. Stable output makes validation and auditing possible.

For Resilience Copilot, the disaster demo uses a 16-section response with Transfer Brief, Audit Trace, and JSON export. A new domain can use a smaller contract if it keeps the same ideas: facts, risk, constraints, recommended next action, blocked claims, and reviewer notes.

## 5. Build Local Validation

Before any public demo, create a small scenario suite:

| Split | Purpose |
| --- | --- |
| Demo | known cases for visible walkthroughs |
| Holdout | cases not used while editing prompts |
| Stress | adversarial or edge cases |

Validation should check behavior, not only text similarity. Useful checks include required fields, blocked phrases, escalation flags, and audit fields.

## 6. Add Memory Carefully

Memory should improve future review quality, not silently change high-risk behavior.

Safe memory pattern:

```text
Local validation result
  -> experience record
  -> reflection note
  -> proposed skill update
  -> human review
  -> approved policy change
```

Avoid:

- automatic policy promotion;
- live memory writes from untrusted users;
- hidden online lookups;
- memory that overrides safety constraints.

## 7. Publish Like a Product

For a public repository, keep the first screen focused:

- what problem it solves;
- who it helps;
- what architecture it uses;
- what it refuses to do;
- how validation passed;
- where to try the demo.

Keep large bundles, old working notes, and private learning logs out of the root.
