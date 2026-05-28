# Resilience Copilot English Note

The canonical project description is maintained in [README.md](README.md).

## Positioning

Resilience Copilot is a safety-bounded LLM agent prototype for high-risk decision support. It studies how risk detection, deterministic constraints, tool/resource verification, bounded long-term memory, human review, and audit traces can make LLM-assisted disaster-relief case-note processing more reliable and controllable.

## Core Pipeline

`User Case Note -> Risk Signal Detection -> Playbook Matching -> LLM / Gemma Generation -> Safety Contract Checking -> Official Resource Verification -> Memory Retrieval / Protected Invariants -> Human Review Trigger -> Structured JSON Export -> Audit Trace -> Responder Handoff`

The system is not an autonomous emergency responder and does not replace emergency services. It converts messy and uncertain notes into reviewable, handoff-ready, and auditable responder packets.

## Quick Start

```powershell
pip install -r requirements.txt
python scripts\run_demo.py
python scripts\run_eval.py
python scripts\run_stress_test.py
python -m pytest tests
```

## Current Validation

- demo 2/2
- holdout 2/2
- stress 15/15
- original Kaggle local gate: `ready_to_submit=true`
- self-built benchmark: 30 safety-engineering scenarios
- pytest: 8 core tests

## Review Materials

- [docs/architecture.md](docs/architecture.md)
- [docs/project_report.md](docs/project_report.md)
- [docs/memory_eval.md](docs/memory_eval.md)
- [docs/interview_qa.md](docs/interview_qa.md)
- [docs/summer_camp_summary.md](docs/summer_camp_summary.md)

