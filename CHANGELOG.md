# Changelog

All notable public changes are recorded here.

## v0.1.0 - Public Template Release

This release turns the original Gemma 4 Good Hackathon submission into a cleaner reusable open-source template.

### Added

- Safety-bounded agent positioning for high-risk human-review workflows.
- Public architecture guide in `docs/architecture.md`.
- Reusable case examples in `docs/examples.md`.
- Adaptation guide for new domains in `docs/adaptation_guide.md`.
- Contribution guide, issue templates, MIT license, and roadmap.
- GitHub Pages demo with validation badge, Transfer Brief, Audit Trace, structured JSON export, and explicit safety boundary.

### Validation

- Demo cases: 2/2.
- Holdout cases: 2/2.
- Stress cases: 15/15.
- Final local gate: `ready_to_submit=true`.

### Safety Boundaries

- Does not replace emergency services.
- Does not diagnose or provide treatment instructions.
- Does not invent shelter capacity, transport availability, or official confirmation.
- Does not automatically promote learned strategies without human review.
