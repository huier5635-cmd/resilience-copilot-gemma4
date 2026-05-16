# The Gemma 4 Good Hackathon

Resilience Copilot is a safety-first disaster relief triage assistant built with Gemma 4. It uses a deterministic safety sidecar, auditable playbook grounding, official-resource verification, ICS-style transfer brief, structured JSON export, and local scenario validation to help volunteers turn messy crisis notes into safer responder-reviewed next actions.

This is a hackathon project, not a normal tabular competition: there is no provided training dataset and the deliverable is a Kaggle Writeup plus public demo assets.

## Competition Reading

- Competition: https://www.kaggle.com/competitions/gemma-4-good-hackathon
- Data: `data/raw/NOTE.md` says no dataset is provided.
- Submission: one Kaggle Writeup per team.
- Required assets: Kaggle Writeup, public code repository, public live demo, public video, media/gallery cover.
- Evaluation focus: impact and vision, video pitch/storytelling, technical depth/execution.
- Deadline recorded from competition page: 2026-05-18 23:59 UTC, which is 2026-05-19 07:59 in China.

## Current Product Track

Working title: **Resilience Copilot**.

Goal: a safety-first crisis-relief assistant for floods, evacuation, medication access, shelter triage, pet-compatible shelter routing, heatwave/cooling-center routing, source verification, and responder handoff.

Current status: submitted to Kaggle on 2026-05-17 for EXP-029 with an ICS-style `Transfer brief`, 15/15 stress validation, public-synced GitHub Pages demo, and the EXP029 evidence bundle. EXP-029 adds shift-change handoff, incident snapshot, immediate objectives, safety constraints, resource status, communications, and operational-period rechecks.

Submitted writeup:

`https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423`

## Architecture

```text
Case Note
  ↓
Risk Signal Detector
  ↓
Playbook Matcher
  ↓
Gemma 4 Generation
  ↓
Safety Contract Checker
  ↓
16-section Response
  ↓
JSON Export + Audit Trace + Transfer Brief
```

- Gemma 4 is used for generation and responder-facing phrasing.
- The deterministic safety sidecar runs before and after generation.
- Pre-generation: detect risk signals and select playbook constraints.
- Generation: Gemma 4 drafts a human-readable response under those constraints.
- Post-generation: the safety contract blocks unsupported claims and exports audit fields.
- The 16-section response includes `Transfer Brief`, `Audit Trace`, `Structured case export`, and a visible safety boundary.

## Judge-Facing Example Cases

| Case | Scenario | Expected behavior |
| --- | --- | --- |
| Oxygen + Power Outage | Older adult uses oxygen, the power is out, and the backup battery is nearly empty. | High risk, human review, emergency or utility medical-priority routing, no casual reassurance. |
| Heatwave + Medication + Mobility Risk | Heatwave, older adult on medication, mobility limitation. | Cooling-center official check, transport-barrier handling, no invented facility capacity. |
| Shelter Rumor + Language Barrier + Pet | Social media rumor says a shelter has beds, household has limited English proficiency, and the household has a pet. | Rumor quarantine, qualified interpreter, pet-compatible shelter check, no invented capacity. |

## Public Links

- Public demo: https://huier5635-cmd.github.io/resilience-copilot-gemma4/
- Public code: https://github.com/huier5635-cmd/resilience-copilot-gemma4
- YouTube video: https://youtu.be/CmqCV8Ic9cY
- Kaggle Gemma 4 evidence notebook: https://www.kaggle.com/code/zhenhuier/notebook5022dfd167

## Gemma 4 Evidence

Gemma 4 was executed in a Kaggle Notebook using the official model resource:

`/kaggle/input/models/google/gemma-4/transformers/gemma-4-e2b-it/1`

The notebook records the model path, runtime environment, prompt, response, latency, and generated token count. The intended production pattern is Gemma 4 for language generation, with the deterministic safety sidecar enforcing the response contract before and after generation. This project does not claim fine-tuning, live deployment, diagnosis, treatment, or live shelter capacity.

## Directory Map

- `docs/`: local project notes plus selected judge-facing writeup and evidence documents. Internal working notes stay local and are not part of the GitHub display surface.
- `notebooks/public_reproduction/`: downloaded public Kaggle notebooks and review notes.
- `notebooks/experiments/`: our own Kaggle/local evidence notebooks.
- `scripts/`: local validation, baseline, evidence, and asset checks.
- `outputs/local_validation/`: generated reports and validation artifacts.

## Storage Policy

Gemma-related project files, browser profile data, downloads, evidence bundles, and Ollama model files should stay under `D:\Kaggle\Gemma4Good`.

- Project workspace: `D:\Kaggle\Gemma4Good\New project 5`
- Gemma Chrome profile: `D:\Kaggle\Gemma4Good\ChromeDebugProfile_Gemma`
- Gemma downloads: `D:\Kaggle\Gemma4Good\Downloads`
- Gemma temp/check files: `D:\Kaggle\Gemma4Good\Temp`
- Ollama data: `D:\Kaggle\Gemma4Good\Ollama\.ollama`
- User environment variable: `OLLAMA_MODELS=D:\Kaggle\Gemma4Good\Ollama\.ollama\models`

Do not intentionally download new Gemma/Kaggle assets to the C drive. For temporary verification downloads, use `D:\Kaggle\Gemma4Good\Temp` instead of `%TEMP%`. The legacy paths `C:\ChromeDebugProfile_Gemma` and `C:\Users\Liaoke\.ollama` are junctions into D, so old commands can keep working without storing large data on C.

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
- stress cases: 15/15 locally; the latest submitted EXP-029 Kaggle writeup documents 15/15
- writeup readiness: checked locally against word count, links, and evidence terms
- judging packet: checked locally against rubric map, links, assets, and validation results
- public evidence surface: GitHub Pages verified on 2026-05-17 with `Transfer Brief`, `Source Verification Ledger`, `Responder packet`, `Household message`, `Audit trace`, and `Structured case export`
- Kaggle checklist: 7/7
- final Kaggle submission: refreshed to EXP-029 on 2026-05-17

Validation is scenario-based because the hackathon provides no official training dataset. The current scenario gate is demo 2/2, holdout 2/2, stress 15/15, and `ready_to_submit=true`.

## Local Demo

The current project demo runs on port 7861 because port 7860 is already occupied by another local process:

```powershell
$env:PORT='7861'
python app\app.py
```

Open `http://127.0.0.1:7861`.

Durable public static demo:

`https://huier5635-cmd.github.io/resilience-copilot-gemma4/`

Use the GitHub Pages link as the public demo in the Kaggle writeup. Stale quick-tunnel links should stay out of the judge-facing Kaggle page.

## Assets

- Video draft: `outputs/submission_assets/resilience_copilot_caption_video_20260513.webm`
- Pitch deck: `outputs/submission_assets/resilience_copilot_pitch_v2.pptx`
- Static deployment package: `outputs/submission_assets/public_demo_static.zip`
- Submission bundle: `outputs/submission_assets/resilience_copilot_submission_bundle.zip`
- Latest submitted evidence bundle: `resilience_copilot_submission_bundle_EXP029.zip`
- Evidence report: `outputs/local_validation/evidence_report.md`

Root-level public repo assets:

- `resilience_copilot_pitch_v2.pptx`
- `resilience_copilot_submission_bundle.zip`

Refresh the submission bundle after changing project assets:

```powershell
python scripts\build_submission_bundle.py
```

EXP-022 public repo refresh: GitHub Pages and the public source/demo were refreshed on 2026-05-15. This did not consume a Kaggle final submission slot because the Kaggle writeup URL and public demo URL stayed unchanged.

EXP-023 Kaggle refresh: the demo now shows a compact decision brief, supports `Copy packet`, and includes heatwave/cooling-center routing through public health and official emergency-management channels. Kaggle was refreshed on 2026-05-15 with the EXP-023 writeup and `resilience_copilot_submission_bundle_EXP023.zip`.

EXP-024 local/public demo candidate: the demo now includes `Copy JSON` and a structured case export with `case_fingerprint`, `review_level`, `required_human_review`, `blocked_claims`, and `response_contract`. This has not consumed another Kaggle submission slot yet.

EXP-026 local candidate: the demo now includes `Human Review Reason` and the structured export includes `human_review_reason`. This raises the local stress gate to 13/13 and is a low-risk original enhancement for the next Kaggle refresh after public demo sync.

EXP-028 submitted candidate: the demo includes `Source Verification Ledger` and the structured export includes `source_verification`. This raised the local stress gate to 14/14 and was submitted to Kaggle on 2026-05-17.

EXP-029 submitted candidate: the demo now includes `Transfer Brief` and the structured export includes `transfer_brief` plus `ics-style-transfer-brief`. This raises the local stress gate to 15/15 and was submitted to Kaggle on 2026-05-17. Literature basis: FEMA ICS 201 incident briefing structure for situation, actions, resources, communications, and prepared-by handoff.

## Submission Policy

- No direct Kaggle submission until `scripts\run_local_validation.py` reports the required assets and evidence are ready. The 2026-05-13 submission followed this rule.
- Public reproduction is capped at two online attempts per day.
- At least one original or micro-tuning branch must remain prepared for every submission round.
- Every experiment must record hypothesis, command, local result, online result if any, rank if applicable, and next action.
