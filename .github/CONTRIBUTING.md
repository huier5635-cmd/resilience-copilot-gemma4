# Contributing

Thanks for helping improve Resilience Copilot.

This project is intentionally conservative because it targets high-risk human-review workflows. Small, well-scoped changes are preferred.

## Good First Contributions

- Add a new validation scenario.
- Improve wording in README or demo examples.
- Add a new playbook constraint with a clear safety reason.
- Improve local reproducibility instructions.
- Add an adapter sketch for another high-risk intake workflow.
- Improve the V4 pitch or screenshot assets.

## Safety Rules

- Do not add claims that the system replaces emergency services.
- Do not add medical diagnosis or treatment advice.
- Do not invent live shelter capacity, transport availability, road safety, or facility status.
- Do not add automatic external actions such as calling, booking, dispatching, or messaging.
- Keep human review explicit for high-risk outputs.

## Suggested Workflow

1. Open an issue describing the scenario or safety improvement.
2. Keep the pull request narrow.
3. If you are working from the full source bundle, run the local validation gate before submitting a code or scenario change.
4. Include the validation result, or explain why the change is documentation-only.

## Issue Labels To Use

- `scenario`
- `safety`
- `documentation`
- `agentic-memory`
- `playbook`
- `demo`
- `good-first-issue`
