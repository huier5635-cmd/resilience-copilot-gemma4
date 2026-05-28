"""Post-generation safety contract checks for Resilience Copilot."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


REQUIRED_RESPONSE_FIELDS = [
    "risk_level",
    "case_signals",
    "human_review_reason",
    "playbook_references",
    "action_plan",
    "official_resource_checks",
    "source_verification",
    "transfer_brief",
    "clarifying_questions",
    "language_support",
    "responder_handoff",
    "responder_packet",
    "household_message",
    "audit_trace",
    "case_export",
    "safety_boundary",
]

REQUIRED_EXPORT_FIELDS = [
    "contract_version",
    "case_fingerprint",
    "risk_level",
    "review_level",
    "signals",
    "human_review_reason",
    "playbook_ids",
    "official_routes",
    "source_verification",
    "transfer_brief",
    "required_human_review",
    "blocked_claims",
    "response_contract",
]

UNSUPPORTED_CLAIM_PATTERNS = [
    "shelter has capacity",
    "beds are available",
    "transport is available",
    "safe to drive",
    "diagnosis:",
    "you do not need emergency services",
]


class SafetyContractChecker:
    """Validate response shape, auditability, and blocked claim patterns."""

    def normalize(self, response: Any) -> dict[str, Any]:
        if is_dataclass(response):
            return asdict(response)
        if isinstance(response, dict):
            return response
        raise TypeError("response must be a dataclass or dictionary")

    def check_response(self, response: Any) -> dict[str, Any]:
        data = self.normalize(response)
        missing_fields = [field for field in REQUIRED_RESPONSE_FIELDS if field not in data or data[field] in (None, "", [])]
        case_export = data.get("case_export") if isinstance(data.get("case_export"), dict) else {}
        missing_export_fields = [field for field in REQUIRED_EXPORT_FIELDS if field not in case_export]
        text = self.response_to_text(data).lower()
        unsupported_claims = [pattern for pattern in UNSUPPORTED_CLAIM_PATTERNS if pattern in text]
        audit_complete = self.audit_trace_complete(data.get("audit_trace", []))
        return {
            "passed": not missing_fields and not missing_export_fields and not unsupported_claims and audit_complete,
            "missing_fields": missing_fields,
            "missing_export_fields": missing_export_fields,
            "unsupported_claims": unsupported_claims,
            "audit_trace_complete": audit_complete,
            "structured_json_valid": not missing_export_fields,
        }

    def response_to_text(self, data: dict[str, Any]) -> str:
        chunks: list[str] = []
        for value in data.values():
            if isinstance(value, list):
                chunks.extend(str(item) for item in value)
            elif isinstance(value, dict):
                chunks.extend(f"{key}: {item}" for key, item in value.items())
            else:
                chunks.append(str(value))
        return "\n".join(chunks)

    def audit_trace_complete(self, audit_trace: Any) -> bool:
        if not isinstance(audit_trace, list):
            return False
        joined = " ".join(str(item).lower() for item in audit_trace)
        required_markers = ["risk_level=", "signals=", "playbook_ids=", "official_routes=", "human_review_required=true"]
        return all(marker in joined for marker in required_markers)

