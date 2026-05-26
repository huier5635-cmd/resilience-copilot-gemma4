# v0.1.0 Release Notes

Resilience Copilot v0.1.0 is the first public template release after the Gemma 4 Good Hackathon submission.

## What This Release Is

- A safety-bounded agent template for high-risk human-review workflows.
- A disaster-relief triage demo built with Gemma 4, deterministic safety checks, audit traces, and local scenario validation.
- A reusable pattern for teams that need AI assistance without unchecked autonomy.

## What This Release Includes

- Static GitHub Pages demo.
- Architecture guide.
- Example cases.
- Adaptation guide.
- Roadmap.
- Contribution guide.
- Safety/security policy.
- Issue templates for validation scenarios, safety improvements, and adapter requests.

## Validation Snapshot

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Final local gate | `ready_to_submit=true` |

## Best First Uses

- Review the live demo.
- Read `docs/architecture.md`.
- Copy the scenario format from `docs/examples.md`.
- Use `docs/adaptation_guide.md` to adapt the pattern to a new high-risk workflow.

## Non-Goals

- No emergency-service replacement.
- No medical diagnosis.
- No live resource booking.
- No invented capacity or transport availability.
- No automatic policy promotion from memory.
