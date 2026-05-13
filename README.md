# The Gemma 4 Good Hackathon

Kaggle project workspace for a prize-oriented Gemma 4 Good submission. This is a hackathon, not a normal tabular competition: there is no provided training dataset and the deliverable is a Kaggle Writeup plus public demo assets.

## Competition Reading

- Competition: https://www.kaggle.com/competitions/gemma-4-good-hackathon
- Data: `data/raw/NOTE.md` says no dataset is provided.
- Submission: one Kaggle Writeup per team. Do not submit until the local checklist passes.
- Required assets: Kaggle Writeup, public code repository, public live demo, public video, media/gallery cover.
- Evaluation focus: impact and vision, video pitch/storytelling, technical depth/execution.
- Deadline recorded from competition page: 2026-05-18 23:59 UTC, which is 2026-05-19 07:59 in China.

## Current Product Track

Working title: **Resilience Copilot**.

Goal: a safety-first crisis-relief assistant for floods, evacuation, medication access, shelter triage, pet-compatible shelter routing, and responder handoff. The first baseline is deliberately narrow so we can prove the loop quickly, then add Gemma 4 evidence and small original improvements.

Current status: local baseline passes demo and holdout gates, and Kaggle Gemma 4 runtime evidence has been captured. The project is still not submission-ready because public video, public code repository, and public live demo URLs are missing.

## Directory Map

- `docs/实验记录.md`: every experiment and submission decision.
- `docs/学习台账.md`: beginner-friendly concepts and next learning steps.
- `docs/本地验证冲分手册.md`: how to run local checks before any public submission.
- `notebooks/public_reproduction/`: downloaded public Kaggle notebooks and review notes.
- `notebooks/experiments/`: our own Kaggle/local evidence notebooks.
- `scripts/`: local validation, baseline, evidence, and asset checks.
- `outputs/local_validation/`: generated reports and validation artifacts.

## Local Validation

Run the full local gate:

```powershell
python scripts\run_local_validation.py
```

Run only the demo-case evaluation:

```powershell
python scripts\evaluate_demo_cases.py --cases data\cases\demo_cases.jsonl --output outputs\local_validation\demo_eval.json
```

The current target is not leaderboard-style score maximization; it is a reliable evidence gate for a hackathon submission.

## Local Demo

The current project demo runs on port 7861 because port 7860 is already occupied by another local process:

```powershell
$env:PORT='7861'
python app\app.py
```

Open `http://127.0.0.1:7861`.

Temporary public demo for testing:

`https://applied-rico-impose-stated.trycloudflare.com`

This is a Cloudflare quick tunnel and should be replaced before final judging.

Video draft:

`outputs/submission_assets/resilience_copilot_caption_video_20260513.webm`

Static deployment package:

`outputs/submission_assets/public_demo_static.zip`

## Submission Policy

- No direct Kaggle submission until `scripts\run_local_validation.py` reports the required assets and evidence are ready.
- Public reproduction is capped at two online attempts per day.
- At least one original or micro-tuning branch must remain prepared for every submission round.
- Every experiment must record hypothesis, command, local result, online result if any, rank if applicable, and next action.
