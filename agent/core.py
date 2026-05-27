"""Small reusable safety-bounded agent core.

The public demo is static, but this module shows the reusable agent pattern:
case note -> risk signals -> memory/skills -> tool sandbox -> safety check ->
human-reviewed transfer brief.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import re
from typing import Iterable


@dataclass
class Skill:
    skill_id: str
    triggers: tuple[str, ...]
    safe_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]


@dataclass
class Experience:
    case_id: str
    signals: list[str]
    outcome: str
    reflection: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResilienceAgent:
    """Safety-bounded learning agent for responder-reviewed triage.

    The agent can retrieve skills and propose strategy improvements, but it
    never performs external actions or updates high-risk policy automatically.
    """

    def __init__(self) -> None:
        self.experience_ledger: list[Experience] = []
        self.skills = [
            Skill(
                "life-safety-escalation",
                ("oxygen", "power outage", "battery", "floodwater", "downed line"),
                (
                    "route urgent hazards through emergency services or official utility channels",
                    "collect location, callback, device needs, and mobility constraints",
                ),
                ("wait-and-see reassurance", "medical diagnosis", "capacity guarantee"),
            ),
            Skill(
                "rumor-quarantine",
                ("rumor", "social media", "beds", "capacity"),
                (
                    "label unverified claims as unconfirmed",
                    "route capacity checks through official shelter operations",
                ),
                ("repeat unverified bed counts", "promise live shelter capacity"),
            ),
            Skill(
                "language-access-handoff",
                ("limited english", "interpreter", "spanish", "translation"),
                (
                    "request qualified interpretation for safety-critical details",
                    "record preferred language in the transfer brief",
                ),
                ("use children as interpreters for medical or legal details",),
            ),
            Skill(
                "heatwave-routing",
                ("heatwave", "no cooling", "cooling center", "medication", "mobility"),
                (
                    "verify cooling-center hours and accessible intake through official channels",
                    "carry transport barriers into responder handoff",
                ),
                ("invent cooling-center capacity", "claim clinical safety without confirmation"),
            ),
        ]

    def run(self, case_note: str) -> dict:
        signals = self.detect_signals(case_note)
        high_signals = {"oxygen", "power outage", "battery", "downed line"}
        risk_level = "high" if high_signals & set(signals) else "medium" if signals else "low"
        skills = self.retrieve_skills(signals)
        sandbox_calls = self.plan_tool_sandbox(skills)
        safety_contract = self.check_safety_contract(case_note, skills)
        transfer_brief = self.build_transfer_brief(case_note, risk_level, signals, skills)
        audit_trace = {
            "risk_level": risk_level,
            "signals": signals,
            "skill_ids": [skill.skill_id for skill in skills],
            "sandbox_only": True,
            "human_review_required": risk_level in {"high", "medium"},
            "blocked_claims": safety_contract["blocked_claims"],
        }
        result = {
            "risk_level": risk_level,
            "signals": signals,
            "skills": [skill.skill_id for skill in skills],
            "tool_sandbox": sandbox_calls,
            "transfer_brief": transfer_brief,
            "audit_trace": audit_trace,
            "safety_contract": safety_contract,
        }
        self.record_experience(result)
        return result

    def detect_signals(self, case_note: str) -> list[str]:
        text = case_note.lower()
        patterns = {
            "oxygen": r"\boxygen\b",
            "power outage": r"\b(power outage|power is out|no power)\b",
            "battery": r"\b(battery|backup)\b",
            "downed line": r"\b(downed line|power line)\b",
            "rumor": r"\b(rumor|social media|heard online)\b",
            "capacity": r"\b(capacity|beds?|room)\b",
            "limited english": r"\b(limited english|interpreter|spanish|translation)\b",
            "heatwave": r"\b(heatwave|extreme heat|no cooling|cooling center)\b",
            "mobility": r"\b(mobility|wheelchair|no car|transport)\b",
            "medication": r"\b(medication|medicine|insulin|dialysis)\b",
            "pet": r"\b(pet|dog|cat)\b",
        }
        return [label for label, pattern in patterns.items() if re.search(pattern, text)]

    def retrieve_skills(self, signals: Iterable[str]) -> list[Skill]:
        signal_text = " ".join(signals).lower()
        return [skill for skill in self.skills if any(trigger in signal_text for trigger in skill.triggers)]

    def plan_tool_sandbox(self, skills: Iterable[Skill]) -> list[dict]:
        return [
            {
                "skill_id": skill.skill_id,
                "mode": "offline sandbox",
                "external_side_effects": "none",
                "allowed": "prepare official-resource verification question for a human responder",
            }
            for skill in skills
        ]

    def check_safety_contract(self, case_note: str, skills: Iterable[Skill]) -> dict:
        blocked = sorted({action for skill in skills for action in skill.blocked_actions})
        if re.search(r"\b(shelter|cooling center|transport|road)\b", case_note.lower()):
            blocked.extend(["invent live facility status", "invent transport availability"])
        return {
            "passed": True,
            "human_review_required": True,
            "blocked_claims": sorted(set(blocked)),
            "no_external_actions": True,
            "no_medical_diagnosis": True,
        }

    def build_transfer_brief(self, case_note: str, risk_level: str, signals: list[str], skills: list[Skill]) -> list[str]:
        return [
            f"Risk level: {risk_level}.",
            "Case note summary: " + case_note.strip(),
            "Signals: " + (", ".join(signals) if signals else "none detected"),
            "Skills retrieved: " + (", ".join(skill.skill_id for skill in skills) if skills else "none"),
            "Responder action: verify official resources and keep final decision with a human reviewer.",
        ]

    def record_experience(self, result: dict) -> None:
        case_id = f"case-{len(self.experience_ledger) + 1:04d}"
        self.experience_ledger.append(
            Experience(
                case_id=case_id,
                signals=result["signals"],
                outcome=result["risk_level"],
                reflection="Preserve safety contract; propose skill changes only after human review.",
            )
        )

    def reflect_strategy(self) -> dict:
        signal_counts: dict[str, int] = {}
        for item in self.experience_ledger:
            for signal in item.signals:
                signal_counts[signal] = signal_counts.get(signal, 0) + 1
        return {
            "experience_count": len(self.experience_ledger),
            "recurrent_signals": sorted(signal_counts.items(), key=lambda item: (-item[1], item[0])),
            "policy_update": "human review required",
            "auto_apply": False,
        }


if __name__ == "__main__":
    agent = ResilienceAgent()
    output = agent.run("Older adult uses oxygen. Power is out and backup battery is nearly empty.")
    print(json.dumps(output, indent=2))
