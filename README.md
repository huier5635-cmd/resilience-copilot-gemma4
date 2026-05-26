# Resilience Copilot

**A safety-bounded agent template for high-risk human-review workflows.**

[![Live Demo](https://img.shields.io/badge/demo-GitHub%20Pages-1f6feb)](https://huier5635-cmd.github.io/resilience-copilot-gemma4/)
[![Validation](https://img.shields.io/badge/validation-demo%202%2F2%20%7C%20holdout%202%2F2%20%7C%20stress%2015%2F15-brightgreen)](#validation)
[![Gemma 4](https://img.shields.io/badge/model-Gemma%204-7c3aed)](https://www.kaggle.com/code/zhenhuier/notebook5022dfd167)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Resilience Copilot turns messy disaster-relief notes into responder-reviewed next actions. The broader goal is a reusable pattern for safer agents in domains where unchecked autonomy is risky: disaster response, public-service intake, campus safety, elder-care support, insurance triage, and compliance-heavy support desks.

![Resilience Copilot demo preview](resilience_copilot_demo_preview.png)

## Why Star This

- **Safety-first agent pattern**: LLM generation is wrapped by deterministic constraints, validation gates, audit traces, and human review.
- **Agentic without overclaiming**: graph orchestration, bounded memory, experience ledger, strategy reflection, skill library, and tool sandbox are implemented offline and review-first.
- **Reusable template**: the disaster-relief demo is the flagship example, but the architecture can be adapted to other high-risk workflows.
- **Judge-ready evidence**: live demo, V4 pitch deck, Gemma 4 evidence notebook, local validation reports, and a reproducible final bundle are included.

## Quick Links

| Resource | Link |
| --- | --- |
| Live demo | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |
| English docs | [README_EN.md](README_EN.md) |
| Chinese docs | [README_CN.md](README_CN.md) |
| V4 pitch deck | [resilience_copilot_pitch_v4_command_center.pptx](resilience_copilot_pitch_v4_command_center.pptx) |
| V4 narration script | [resilience_copilot_pitch_v4_narration_script.txt](resilience_copilot_pitch_v4_narration_script.txt) |
| Kaggle writeup | https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423 |
| Gemma 4 evidence notebook | https://www.kaggle.com/code/zhenhuier/notebook5022dfd167 |
| Final evidence bundle | [resilience_copilot_submission_bundle_EXP029.zip](resilience_copilot_submission_bundle_EXP029.zip) |

## 30-Second Architecture

```text
Case Note
  -> Risk Signal Detector
  -> Playbook Matcher
  -> Gemma 4 Generation
  -> Safety Contract Checker
  -> 16-section Response
  -> JSON Export + Audit Trace + Transfer Brief
```

Agentic learning sidecar:

```text
Validation Feedback
  -> Experience Ledger
  -> Bounded Long-Term Memory
  -> Strategy Reflection
  -> Human-Reviewed Skill Library
  -> Next-Round Policy Suggestions
```

The system is not an unrestricted autonomous agent. It does not call emergency services, diagnose conditions, book shelters, or promise live capacity. The learning loop proposes improvements for human review.

## Validation

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Memory system | ready |
| Graph orchestration | ready |
| Final local gate | `ready_to_submit=true` |

Run the reproducibility gate from the final bundle:

```powershell
python scripts\run_local_validation.py
```

## Demo Story

The V4 Rescue Command Center deck shows the user flow as a short incident handoff:

1. Incoming call / messy case note.
2. Risk signal detection.
3. Memory and skill retrieval.
4. Playbook constraints and tool sandbox.
5. Transfer Brief, Audit Trace, and JSON export.

![Resilience Copilot V4 command center preview](resilience_copilot_pitch_v4_video_frame.png)

## Reuse Ideas

This repository is easiest to adapt when your workflow has three properties:

- high-risk or regulated outputs;
- a human reviewer remains accountable;
- local scenarios can be written as validation cases.

Good next templates: campus safety intake, elder-care hotline triage, public-service request routing, insurance claim intake, NGO volunteer coordination, and compliance support.

## Project Status

Resilience Copilot was built for **The Gemma 4 Good Hackathon** and submitted as EXP-029. The Kaggle submission remains locked; this repository is the clean public surface for reviewers, teachers, interviewers, and open-source readers.

See [ROADMAP.md](ROADMAP.md) for the path from competition prototype to reusable safety-bounded agent toolkit.

## Contributing

Small, reviewable contributions are welcome: new validation scenarios, safer playbook constraints, clearer demo examples, adapter templates, and documentation improvements. Start with [CONTRIBUTING.md](CONTRIBUTING.md).
