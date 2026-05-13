# The Gemma 4 Good Hackathon

Kaggle project workspace for a prize-oriented Gemma 4 Good submission. This is a hackathon, not a normal tabular competition: there is no provided training dataset and the deliverable is a Kaggle Writeup plus public demo assets.

## Competition Reading

- Competition: https://www.kaggle.com/competitions/gemma-4-good-hackathon
- Data: `data/raw/NOTE.md` says no dataset is provided.
- Submission: one Kaggle Writeup per team.
- Required assets: Kaggle Writeup, public code repository, public live demo, public video, media/gallery cover.
- Evaluation focus: impact and vision, video pitch/storytelling, technical depth/execution.
- Deadline recorded from competition page: 2026-05-18 23:59 UTC, which is 2026-05-19 07:59 in China.

## Current Product Track

Working title: **Resilience Copilot**.

Goal: a safety-first crisis-relief assistant for floods, evacuation, medication access, shelter triage, pet-compatible shelter routing, and responder handoff. The first baseline is deliberately narrow so we can prove the loop quickly, then add Gemma 4 evidence and small original improvements.

Current status: submitted to Kaggle on 2026-05-13. The local baseline passes demo, holdout, and stress gates; Kaggle Gemma 4 runtime evidence has been captured; the public GitHub repo is live; the durable GitHub Pages static demo is available; the YouTube video is uploaded as unlisted; and the polished pitch deck plus refreshed submission bundle are published in the repository.

Submitted writeup:

`https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423`

## Public Links

- Public demo: https://huier5635-cmd.github.io/resilience-copilot-gemma4/
- Public code: https://github.com/huier5635-cmd/resilience-copilot-gemma4
- YouTube video: https://youtu.be/CmqCV8Ic9cY
- Kaggle Gemma 4 evidence notebook: https://www.kaggle.com/code/zhenhuier/notebook5022dfd167

## Directory Map

- `docs/`: Chinese experiment log, learning ledger, local validation manual, public notebook review, writeup draft, deployment notes, and pitch-deck evidence notes.
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

Current final gate:

- `ready_to_submit=true`
- demo cases: 2/2
- holdout cases: 2/2
- stress cases: 4/4
- Kaggle checklist: 7/7
- final Kaggle submission: created

## Local Demo

The current project demo runs on port 7861 because port 7860 is already occupied by another local process:

```powershell
$env:PORT='7861'
python app\app.py
```

Open `http://127.0.0.1:7861`.

Temporary public demo backup:

`https://applied-rico-impose-stated.trycloudflare.com`

Durable public static demo:

`https://huier5635-cmd.github.io/resilience-copilot-gemma4/`

The Cloudflare link is a quick tunnel backup. Use the GitHub Pages link as the public demo in the Kaggle writeup.

## Assets

- Video draft: `outputs/submission_assets/resilience_copilot_caption_video_20260513.webm`
- Pitch deck: `outputs/submission_assets/resilience_copilot_pitch_v2.pptx`
- Static deployment package: `outputs/submission_assets/public_demo_static.zip`
- Submission bundle: `outputs/submission_assets/resilience_copilot_submission_bundle.zip`
- Evidence report: `outputs/local_validation/evidence_report.md`

Root-level public repo assets:

- `resilience_copilot_pitch_v2.pptx`
- `resilience_copilot_submission_bundle.zip`

Refresh the submission bundle after changing project assets:

```powershell
python scripts\build_submission_bundle.py
```

## Submission Policy

- No direct Kaggle submission until `scripts\run_local_validation.py` reports the required assets and evidence are ready. The 2026-05-13 submission followed this rule.
- Public reproduction is capped at two online attempts per day.
- At least one original or micro-tuning branch must remain prepared for every submission round.
- Every experiment must record hypothesis, command, local result, online result if any, rank if applicable, and next action.
