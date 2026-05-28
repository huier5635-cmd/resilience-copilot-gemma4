# Resilience Copilot

**Safety-bounded agent for disaster-relief triage, built with Gemma 4.**

[![Demo](https://img.shields.io/badge/demo-live-1f6feb)](https://huier5635-cmd.github.io/resilience-copilot-gemma4/)
[![Validation](https://img.shields.io/badge/validation-2%2F2%20%7C%202%2F2%20%7C%2015%2F15-brightgreen)](#validation)
[![Gemma 4](https://img.shields.io/badge/model-Gemma%204-7c3aed)](https://www.kaggle.com/code/zhenhuier/notebook5022dfd167)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Resilience Copilot turns messy crisis notes into responder-reviewed next actions. It combines Gemma 4 generation with a deterministic safety sidecar, official-resource checks, a Transfer Brief, an Audit Trace, structured JSON export, and an offline learning loop that keeps strategy updates human-reviewed.

![Resilience Copilot demo preview](resilience_copilot_demo_preview.png)

## Quick Start

```bash
git clone https://github.com/huier5635-cmd/resilience-copilot-gemma4.git
cd resilience-copilot-gemma4
python -m agent.core
```

Or import the reusable core directly:

```python
from agent import ResilienceAgent

agent = ResilienceAgent()
result = agent.run("Older adult uses oxygen. Power is out and backup battery is nearly empty.")
print(result["risk_level"])
print(result["transfer_brief"])
```

## Why This Repo Is Worth Reusing

- Small public surface: reusable `agent/` core, static demo, and focused docs.
- Safety-bounded pattern: deterministic checks, Memory Write Gate, audit trace, transfer brief, and human review.
- Fast evaluation path: live demo, preview image, architecture notes, examples, and a tagged release.

## Start Here

| If you want to... | Open |
| --- | --- |
| Try the public static demo | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |
| Understand the workflow and boundaries | [docs/architecture.md](docs/architecture.md) |
| Review scenario behavior | [docs/examples.md](docs/examples.md) |
| See release scope | [docs/release_notes_v0.1.0.md](docs/release_notes_v0.1.0.md) |
| Read the competition writeup | https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423 |

## Links

| Resource | URL |
| --- | --- |
| Live demo | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |
| Architecture | [docs/architecture.md](docs/architecture.md) |
| Examples | [docs/examples.md](docs/examples.md) |
| Adaptation guide | [docs/adaptation_guide.md](docs/adaptation_guide.md) |
| Release notes | [docs/release_notes_v0.1.0.md](docs/release_notes_v0.1.0.md) |
| Security notes | [docs/security.md](docs/security.md) |
| Roadmap | [docs/roadmap.md](docs/roadmap.md) |
| Chinese README | [docs/README_CN.md](docs/README_CN.md) |
| Kaggle writeup | https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423 |

## Public Surface At A Glance

- Static GitHub Pages demo with sample cases and copyable responder outputs.
- Documentation for architecture, examples, release scope, adaptation, and security notes.
- Public validation snapshot: demo `2/2`, holdout `2/2`, stress `15/15`, local gate `ready_to_submit=true`.
- Deliberately excludes internal logs, competition bundles, and local-only audit artifacts.

## Method

```text
Case Note
  -> Risk Signal Detector
  -> Playbook Matcher
  -> Gemma 4 Response
  -> Safety Contract Checker
  -> Transfer Brief + Audit Trace + JSON Export
```

```text
Validation Feedback
  -> Experience Ledger
  -> Memory Write Gate
  -> Bounded Memory
  -> Strategy Reflection
  -> Human-Reviewed Skill Library
```

The system is not an unrestricted autonomous responder. It does not call emergency services, diagnose conditions, book shelters, invent live capacity, present rumors as verified facts, or promote raw runtime input into long-term memory.

## Validation

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Local gate | `ready_to_submit=true` |

Validation evidence is summarized in the Kaggle writeup and the Gemma 4 evidence notebook. The public site keeps only the judge-facing demo and documentation surface.

## Repository Layout

```text
agent/    reusable safety-bounded agent core
assets/   static demo code
docs/     architecture, examples, roadmap, reuse notes
index.html
README.md
LICENSE
resilience_copilot_demo_preview.png
```

The public root is intentionally small. Full competition logs, learning notes, old bundles, and local audit files are kept out of this repository surface.
