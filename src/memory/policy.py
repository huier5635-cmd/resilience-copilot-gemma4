"""Bounded memory write policy for high-risk decision support."""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any


PROTECTED_SAFETY_INVARIANTS = [
    "Do not diagnose medical conditions.",
    "Do not invent live shelter capacity or transport availability.",
    "Do not replace emergency services or official responders.",
    "Do not allow memory to modify high-risk safety policy without human review.",
]


@dataclass
class MemoryRecord:
    memory_id: str
    text: str
    source: str
    status: str
    tags: list[str] = field(default_factory=list)
    review_required: bool = True


class MemoryWriteGate:
    """Prevent memory pollution by quarantining unreviewed experience."""

    def __init__(self) -> None:
        self.records: list[MemoryRecord] = []
        self.protected_invariants = tuple(PROTECTED_SAFETY_INVARIANTS)

    def _stable_id(self, text: str, source: str) -> str:
        digest = sha256(f"{source}:{text}".encode("utf-8")).hexdigest()[:12]
        return f"mem-{digest}"

    def submit_runtime_observation(self, text: str, tags: list[str] | None = None) -> MemoryRecord:
        record = MemoryRecord(
            memory_id=self._stable_id(text, "runtime_observation"),
            text=text,
            source="runtime_observation",
            status="quarantined_pending_review",
            tags=tags or [],
            review_required=True,
        )
        self.records.append(record)
        return record

    def submit_validated_feedback(self, text: str, tags: list[str] | None = None, human_reviewed: bool = False) -> MemoryRecord:
        status = "approved_long_term_memory" if human_reviewed else "quarantined_pending_review"
        record = MemoryRecord(
            memory_id=self._stable_id(text, "validation_feedback"),
            text=text,
            source="validation_feedback",
            status=status,
            tags=tags or [],
            review_required=not human_reviewed,
        )
        self.records.append(record)
        return record

    def retrieve(self, query: str, limit: int = 3) -> list[dict[str, Any]]:
        query_terms = {term for term in query.lower().split() if len(term) > 2}
        scored: list[tuple[int, MemoryRecord]] = []
        for record in self.records:
            if record.status != "approved_long_term_memory":
                continue
            haystack = " ".join([record.text, *record.tags]).lower()
            score = sum(1 for term in query_terms if term in haystack)
            if score:
                scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "memory_id": record.memory_id,
                "text": record.text,
                "tags": record.tags,
                "status": record.status,
                "score": score,
            }
            for score, record in scored[:limit]
        ]

    def propose_policy_update(self, suggestion: str) -> dict[str, Any]:
        return {
            "suggestion": suggestion,
            "applied": False,
            "reason": "Protected safety invariants require human review before policy changes.",
            "protected_invariants": list(self.protected_invariants),
        }

