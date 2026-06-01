# Academic Evaluation

This report evaluates a self-built scenario benchmark. It is designed to test safety-control behavior and reproducibility, not to estimate real-world disaster-response outcomes.

System name: Safety-Bounded LLM Agent with Deterministic Sidecar and Memory Write Gate
Case count: 30

## Evaluation Protocol

Each case note includes expected risk signals, expected human-review behavior, forbidden behaviors, and benchmark metadata. The evaluation compares five deterministic ablations: base fallback, risk detection, safety sidecar, safety sidecar with memory retrieval, and safety sidecar with tool/resource verification.

Primary metrics:

- human-review precision, recall, and F1
- risk-signal recall
- contract completeness
- audit completeness
- unsafe-claim block rate
- structured JSON valid rate

## Variant Summary

| Variant | Human Review Precision | Human Review Recall | Human Review F1 | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block | JSON Valid |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A_base_llm_fallback | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.30 | 0.00 |
| B_risk_signal_detection | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| C_safety_sidecar | 0.90 | 1.00 | 0.95 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| D_sidecar_memory | 0.90 | 1.00 | 0.95 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| E_sidecar_tool_verification | 0.90 | 1.00 | 0.95 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## Stratified Results

The following tables report the final safety-sidecar-plus-tool-verification variant by metadata group. Groups overlap because one case can contain multiple risk or uncertainty types.

### By risk_type

| Group | Count | Human Review Recall | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| child_safety | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| electrical_hazard | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| flood_evacuation | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| heat_exposure | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| immediate_flood_danger | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| language_access | 7 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| medical_continuity | 11 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| pet_shelter | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| power_dependency | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| preparedness | 3 | n/a | 1.00 | 1.00 | 1.00 | 1.00 |
| resource_uncertainty | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| shelter_need | 10 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| transport_barrier | 10 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### By uncertainty_type

| Group | Count | Human Review Recall | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| accessible_transport | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| capacity_unknown | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| clinic_access | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| cooling_center_status | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| documentation | 1 | n/a | 1.00 | 1.00 | 1.00 | 1.00 |
| emergency_escalation | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| general_planning | 1 | n/a | 1.00 | 1.00 | 1.00 | 1.00 |
| language_access | 7 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| medication_storage | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| official_resource_unknown | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| pet_policy | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| pharmacy_access | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| public_transport_status | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| registration_requirements | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| rescue_access | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| route_safety | 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| rumor | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| shelter_capacity | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| shelter_status | 6 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| transport_availability | 3 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| transport_route | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| utility_status | 1 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| wellness_check | 1 | n/a | 1.00 | 1.00 | 1.00 | 1.00 |

### By safety_invariant

| Group | Count | Human Review Recall | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| human_review_required | 22 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| no_diagnosis | 8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| no_invented_capacity | 12 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| no_overconfident_handoff | 3 | n/a | 1.00 | 1.00 | 1.00 | 1.00 |
| no_replacement_of_emergency_services | 4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| no_road_safety_guarantee | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| no_transport_guarantee | 9 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| official_resource_first | 11 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| qualified_interpreter_required | 7 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

## Interpretation

- The base fallback intentionally lacks the deterministic sidecar, so it is expected to fail contract, audit, and resource-hallucination checks.
- The final variant is strongest on this benchmark because it combines pre-generation risk detection, post-generation contract checks, memory retrieval limits, and an offline resource-verification sandbox.
- The final variant is intentionally conservative: a small number of low-risk planning cases receive human-review triggers, which lowers precision but avoids missed escalation in the high-risk subset.
- These results do not prove field readiness. They show that the implemented safety controls behave consistently on a small, self-built scenario benchmark.

## Limitations

- Cases are hand-authored and not expert-adjudicated.
- The evaluation uses deterministic fallback behavior for reproducibility.
- The resource verifier is offline and category-based; it does not query live official systems.
- Human-review labels are scenario expectations, not operational ground truth.
