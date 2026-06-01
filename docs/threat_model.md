# Threat Model

## Scope

The threat model focuses on high-risk case-note triage where an LLM-assisted system prepares responder handoffs from uncertain disaster-relief notes. The main concern is not malicious code execution. The main concern is unsafe information behavior: unsupported claims, missed escalation, polluted memory, and incomplete audit trails.

## Assets to Protect

- household safety and escalation routing
- responder trust in the handoff packet
- integrity of safety policy and playbook constraints
- integrity of memory records
- auditability of risk and routing decisions
- distinction between known facts, unknown facts, and official-resource checks

## Failure Modes

| Failure Mode | Description | Example | Control |
| --- | --- | --- | --- |
| Resource hallucination | System invents capacity, route, transport, clinic, or shelter availability. | "Beds are available" without official confirmation. | Tool/resource verification sandbox and blocked-claim checks. |
| Missed escalation | System fails to trigger human review for high-risk signals. | Oxygen concentrator outage treated as routine. | Risk signal detection and human-review trigger. |
| Memory pollution | Unreviewed runtime observations contaminate future outputs. | A rumor becomes retrievable long-term memory. | Memory write gate and quarantine status. |
| Policy drift | Reflection or memory changes protected safety rules. | Memory suggests promising transport because past case did. | Protected safety invariants and no automatic policy update. |
| Overconfident handoff | System gives definitive next steps despite uncertainty. | "Drive this road" during flooding. | Safety boundary and official-resource-first wording. |
| Audit omission | Output lacks trace fields needed for review. | No record of signals or blocked claims. | Response contract and Audit Trace completeness check. |
| Unsafe language access | System suggests using a child or unqualified person for sensitive translation. | Child interprets medical details. | Qualified interpreter rule. |
| Medical overreach | System diagnoses or gives treatment instructions. | Medication adjustment advice. | Diagnosis and medication-instruction block list. |

## Adversarial Inputs

The benchmark includes or anticipates:

- social-media rumors about shelter beds or bus routes
- vague notes with missing locations
- conflicting transport status
- medical-risk descriptions that invite diagnosis
- language barriers that invite unsafe ad hoc interpretation
- repeated observations that might pollute memory

## Safety Boundaries

The system has three boundaries:

- **Generation boundary**: language generation is allowed to phrase and organize the handoff, but not to decide safety policy.
- **Policy boundary**: sidecar modules, playbooks, and contract checks define blocked claims and review triggers.
- **Memory boundary**: memory can retrieve reviewed examples and propose updates, but it cannot apply policy changes without human review.

## Residual Risks

- The benchmark is hand-authored and may miss realistic failure modes.
- The offline tool sandbox cannot verify live resources.
- The deterministic detector may miss novel wording.
- Human-review labels are scenario expectations, not expert consensus.
- Real deployment would require governance, monitoring, user training, and official data integrations.
