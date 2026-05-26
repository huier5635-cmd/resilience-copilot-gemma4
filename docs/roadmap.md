# Roadmap

Resilience Copilot is moving from a competition prototype toward a reusable safety-bounded agent toolkit.

## Current

- Disaster-relief triage flagship demo.
- Gemma 4 responder-facing generation.
- Deterministic safety sidecar.
- Playbook grounding.
- 16-section response contract.
- Transfer Brief, Audit Trace, JSON export.
- Scenario validation: demo 2/2, holdout 2/2, stress 15/15.
- Offline memory and graph-orchestration evidence.

## Near Term

- Add more reusable examples beyond disaster response.
- Split safety checks into a smaller `safety_contract_checker` module.
- Split playbook matching into a portable `playbook_grounding` module.
- Add a minimal CLI for running a case note through the pipeline.
- Add Docker support for easier reproducibility.
- Add more validation cases from campus safety, elder-care intake, and public-service routing.

## Mid Term

- Add adapter templates for:
  - campus safety report triage;
  - elder-care hotline triage;
  - public-service request routing;
  - insurance claim intake;
  - NGO volunteer coordination.
- Add structured scenario authoring docs.
- Add a reviewer dashboard for comparing audit traces.
- Add a no-network local demo mode and an optional model-backed generation mode.

## Long Term

- Turn the sidecar into a reusable safety-bounded agent framework.
- Add official-resource tool adapters with strict whitelist rules.
- Add human-reviewed promotion from validation feedback to skill library.
- Add benchmark packs for high-risk human-review workflows.
- Support LangGraph as the main graph runtime while keeping a deterministic fallback runner.

## Non-Goals

- No autonomous emergency calls.
- No medical diagnosis.
- No invented shelter, transport, road, or resource availability.
- No automatic policy upgrade in high-risk workflows.
- No hidden online dependency for the static demo or validation gate.
