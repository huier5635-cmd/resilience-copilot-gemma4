"""Reusable agent wrapper for disaster-relief case-note triage."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from scripts.resilience_copilot_baseline import CopilotResponse, generate_response
from src.memory.policy import MemoryWriteGate
from src.safety.contract import SafetyContractChecker
from src.tools.resource_verification import ResourceVerificationSandbox


class ResilienceAgent:
    """Safety-bounded LLM-agent prototype backed by deterministic sidecars."""

    def __init__(self, memory: MemoryWriteGate | None = None) -> None:
        self.memory = memory or MemoryWriteGate()
        self.contract_checker = SafetyContractChecker()
        self.resource_sandbox = ResourceVerificationSandbox()

    def run(self, case_note: str, use_memory: bool = True) -> dict[str, Any]:
        response: CopilotResponse = generate_response(case_note)
        response_data = asdict(response)
        retrieved_memory = self.memory.retrieve(case_note) if use_memory else []
        contract = self.contract_checker.check_response(response)
        resource_check = self.resource_sandbox.verify_claims(response.to_text())
        return {
            "case_note": case_note,
            "response": response_data,
            "retrieved_memory": retrieved_memory,
            "safety_contract": contract,
            "resource_verification": resource_check,
            "memory_policy": {
                "memory_can_modify_policy": False,
                "write_gate": "human_review_required_for_long_term_promotion",
            },
        }

