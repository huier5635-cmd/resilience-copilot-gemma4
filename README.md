# Resilience Copilot

Resilience Copilot is a safety-first disaster relief triage assistant built with Gemma 4. It uses a deterministic safety sidecar, auditable playbook grounding, official-resource verification, ICS-style transfer brief, structured JSON export, and local scenario validation to help volunteers turn messy crisis notes into safer responder-reviewed next actions.

This project was built for **The Gemma 4 Good Hackathon**. The competition provides no official training dataset, so the work focuses on a reproducible scenario-validation workflow, a public live demo, and judge-facing evidence that explains how Gemma 4 is used safely.

## 30-Second Review

| What to check | Summary |
| --- | --- |
| Project background | Disaster-relief volunteers often receive messy notes, rumors, incomplete resource information, language-access needs, and high-risk medical-adjacent concerns. |
| Method framework | A deterministic sidecar detects risk signals, selects playbook constraints, asks Gemma 4 to produce responder-facing language, then checks the response contract before export. |
| System architecture | `Case Note -> Risk Signal Detector -> Playbook Matcher -> Gemma 4 Generation -> Safety Contract Checker -> 16-section Response -> JSON Export + Audit Trace + Transfer Brief` |
| Safety mechanism | The assistant does not replace emergency services, does not diagnose, does not invent shelter capacity or transport availability, and keeps human review explicit. |
| Validation result | Local gate passes demo 2/2, holdout 2/2, stress 15/15, with `ready_to_submit=true`. |
| Demo link | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |

## Project Background

- Competition: https://www.kaggle.com/competitions/gemma-4-good-hackathon
- Data: `data/raw/NOTE.md` says no dataset is provided.
- Submission: one Kaggle Writeup per team.
- Required assets: Kaggle Writeup, public code repository, public live demo, public video, media/gallery cover.
- Evaluation focus: impact and vision, video pitch/storytelling, technical depth/execution.
- Deadline recorded from competition page: 2026-05-18 23:59 UTC, which is 2026-05-19 07:59 in China.

Resilience Copilot targets floods, evacuation, medication access, shelter triage, pet-compatible shelter routing, heatwave/cooling-center routing, source verification, and responder handoff. EXP-029 is the submitted version, adding an ICS-style `Transfer Brief`, shift-change handoff, incident snapshot, immediate objectives, safety constraints, resource status, communications, and operational-period rechecks.

## Method Framework

- **Pre-generation:** detect risk signals such as power-dependent oxygen, heat exposure, medication continuity, shelter-capacity rumors, language access needs, pets, mobility barriers, and transport uncertainty.
- **Grounding:** match each case to auditable playbook rules and official-resource routing constraints.
- **Generation:** use Gemma 4 for responder-facing phrasing under those constraints.
- **Post-generation:** run a deterministic safety contract checker, block unsupported claims, expose audit fields, and export structured JSON.

## System Architecture

```text
Case Note
  ->
Risk Signal Detector
  ->
Playbook Matcher
  ->
Gemma 4 Generation
  ->
Safety Contract Checker
  ->
16-section Response
  ->
JSON Export + Audit Trace + Transfer Brief
```

- Gemma 4 is used for generation and responder-facing phrasing.
- The deterministic safety sidecar runs before and after generation.
- Pre-generation: detect risk signals and select playbook constraints.
- Generation: Gemma 4 composes a human-readable response under those constraints.
- Post-generation: the safety contract blocks unsupported claims and exports audit fields.
- The 16-section response includes `Transfer Brief`, `Audit Trace`, `Structured case export`, and a visible safety boundary.

## Safety Mechanism

- No emergency-service replacement: high-risk cases are routed to human review and official emergency or utility medical-priority channels.
- No medical diagnosis or treatment claims: medication, oxygen, heat, and mobility risks are handled as triage and escalation cues.
- No invented availability: shelter capacity, transport availability, road safety, and cooling-center status must be verified through official resources.
- Rumor quarantine: social-media claims are preserved as unverified until an official source confirms them.
- Auditability: every response includes playbook basis, blocked-claim categories, human-review reason, source-verification ledger, and structured export fields.

## Validation Results

Validation is scenario-based because the hackathon provides no official training dataset.

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Writeup readiness | ready |
| Judging packet | ready |
| Final local gate | `ready_to_submit=true` |

## Example Cases

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
- Submitted Kaggle writeup: https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423

## Gemma 4 Evidence

Gemma 4 was executed in a Kaggle Notebook using the official model resource:

`/kaggle/input/models/google/gemma-4/transformers/gemma-4-e2b-it/1`

The notebook records the model path, runtime environment, prompt, response, latency, and generated token count. The intended production pattern is Gemma 4 for language generation, with the deterministic safety sidecar enforcing the response contract before and after generation. This project does not claim fine-tuning, live deployment, diagnosis, treatment, or live shelter capacity.

## Project Structure and Reproducibility

The final judge-facing bundle is a compact review packet, not a full working archive.

- `docs/`: final Kaggle writeup and judging evidence matrix.
- `data/cases/`: demo, holdout, and stress scenarios used by local validation.
- `knowledge_base/`: auditable emergency playbook rules.
- `app/` and `public_demo/`: runnable local demo and static GitHub Pages demo.
- `notebooks/experiments/`: Kaggle Gemma 4 evidence script.
- `notebooks/public_reproduction/`: compact review summary only; raw public notebooks are not included.
- `scripts/`: minimal validation and bundle scripts needed to reproduce the local gate.
- `outputs/local_validation/`: final EXP-029 validation reports and evidence screenshots.

## Public Experiment Trace

- **EXP-029 final version:** submitted to Kaggle on 2026-05-17 with the 16-section response, Transfer Brief, 15/15 stress validation, public GitHub Pages demo, and EXP-029 evidence bundle.
- **Public review packet:** `resilience_copilot_submission_bundle_EXP029.zip`, 47 judge-facing files, no internal study logs or local coaching notes.
- **Evidence chain:** Kaggle writeup, public demo, public repository, video, Gemma 4 evidence notebook, scenario-validation reports, and judging evidence matrix.

## Reproduce Local Validation

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
- public evidence surface: GitHub Pages verified on 2026-05-18 with the reviewer strip, `Transfer Brief`, `Source Verification Ledger`, `Responder packet`, `Household message`, `Audit trace`, and `Structured case export`
- Kaggle checklist: 7/7
- final Kaggle submission: refreshed to EXP-029 on 2026-05-17

Validation is scenario-based because the hackathon provides no official training dataset. The current scenario gate is demo 2/2, holdout 2/2, stress 15/15, and `ready_to_submit=true`.

## Run the Local Demo

```powershell
python app\app.py
```

Open the printed local URL in a browser. If a different port is needed, set `PORT` first:

```powershell
$env:PORT='7861'
python app\app.py
```

Durable public static demo:

`https://huier5635-cmd.github.io/resilience-copilot-gemma4/`

Use the GitHub Pages link as the public demo in the Kaggle writeup. Legacy tunnel links are not part of the public review surface.

## Assets

- Video source asset: `outputs/submission_assets/resilience_copilot_caption_video_20260513.webm`
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

EXP-029 submitted version: the demo includes `Transfer Brief`, `Source Verification Ledger`, `Human Review Reason`, `Copy JSON`, `transfer_brief`, `source_verification`, and `ics-style-transfer-brief`. The local stress gate is 15/15, and the project was submitted to Kaggle on 2026-05-17 with `resilience_copilot_submission_bundle_EXP029.zip`. Literature basis: FEMA ICS 201 incident briefing structure for situation, actions, resources, communications, and prepared-by handoff.
