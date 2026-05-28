"""Minimal safety-first baseline for the Gemma 4 Good hackathon demo."""

from __future__ import annotations

import json
import re
from hashlib import sha256
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK_PATH = ROOT / "knowledge_base" / "emergency_playbook.json"


@dataclass
class CopilotResponse:
    risk_level: str
    case_signals: list[str]
    human_review_reason: list[str]
    playbook_references: list[str]
    action_plan: list[str]
    official_resource_checks: list[str]
    source_verification: list[str]
    transfer_brief: list[str]
    clarifying_questions: list[str]
    language_support: list[str]
    responder_handoff: list[str]
    responder_packet: list[str]
    household_message: list[str]
    audit_trace: list[str]
    case_export: dict[str, object]
    safety_boundary: str

    def to_text(self) -> str:
        sections = [
            f"Risk level: {self.risk_level}",
            "Case signals:\n" + "\n".join(f"- {item}" for item in self.case_signals),
            "Human review reason:\n" + "\n".join(f"- {item}" for item in self.human_review_reason),
            "Playbook references:\n" + "\n".join(f"- {item}" for item in self.playbook_references),
            "Action plan:\n" + "\n".join(f"{idx}. {item}" for idx, item in enumerate(self.action_plan, 1)),
            "Official resource checks:\n" + "\n".join(f"- {item}" for item in self.official_resource_checks),
            "Source verification ledger:\n" + "\n".join(f"- {item}" for item in self.source_verification),
            "Transfer brief:\n" + "\n".join(f"- {item}" for item in self.transfer_brief),
            "Clarifying questions:\n" + "\n".join(f"- {item}" for item in self.clarifying_questions),
            "Language support:\n" + "\n".join(f"- {item}" for item in self.language_support),
            "Responder handoff:\n" + "\n".join(f"- {item}" for item in self.responder_handoff),
            "Responder packet:\n" + "\n".join(f"- {item}" for item in self.responder_packet),
            "Household message:\n" + "\n".join(f"- {item}" for item in self.household_message),
            "Audit trace:\n" + "\n".join(f"- {item}" for item in self.audit_trace),
            "Structured case export:\n" + json.dumps(self.case_export, indent=2, ensure_ascii=False),
            f"Safety boundary: {self.safety_boundary}",
        ]
        return "\n\n".join(sections)


def _load_playbook() -> dict:
    return json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))


def _contains(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def detect_risk(scenario: str) -> tuple[str, list[str]]:
    text = scenario.lower()
    signals: list[str] = []

    high_patterns = {
        "child cold exposure": r"\b(child|children|kid|kids)\b.*\b(cold|hypothermia|freezing)\b|\b(cold|hypothermia|freezing)\b.*\b(child|children|kid|kids)\b",
        "older adult missing medication": r"\b(grandmother|grandfather|older adult|elderly)\b.*\b(medicine|medication|blood pressure|dialysis)\b|\b(missed|forgot|missing)\b.*\b(medicine|medication|dialysis)\b",
        "electrical hazard near floodwater": r"\b(power line|downed line|electric)\b.*\b(flood|floodwater|water)\b|\b(flood|floodwater|water)\b.*\b(power line|downed line|electric)\b",
        "immediate flood danger": r"\btrapped\b|\bfloodwater\b|\bdrive through floodwater\b",
        "pregnancy or insulin continuity risk": r"\b(pregnant|prenatal|pregnancy|insulin)\b",
        "oxygen or powered medical device risk": r"\b(oxygen concentrator|oxygen|backup battery|medical device)\b.*\b(power|battery|outage|empty)\b|\b(power|battery|outage|empty)\b.*\b(oxygen concentrator|oxygen|medical device)\b",
        "heat illness with medication or mobility risk": r"\b(heat illness|overheated|no cooling)\b.*\b(insulin|diabetes|older adult|elderly|wheelchair|mobility)\b|\b(insulin|diabetes|older adult|elderly|wheelchair|mobility)\b.*\b(heat illness|overheated|no cooling)\b",
    }
    medium_patterns = {
        "evacuation or shelter need": r"\bevacuated|evacuation|shelter\b",
        "pet-compatible shelter needed": r"\bpet|pets|dog|cat\b",
        "transport barrier": r"\b(transport|road|ride|bus|no car|drive|driving)\b",
        "care continuity concern": r"\b(dialysis|appointment|care|asthma)\b",
        "language access barrier": r"\b(spanish-speaking|interpreter|translation|language barrier|cannot understand|limited english|chinese|mandarin|cantonese|vietnamese|arabic)\b",
        "unverified shelter capacity rumor": r"\b(rumor|social media)\b.*\b(shelter|beds|capacity)\b|\b(shelter|beds|capacity)\b.*\b(rumor|social media)\b",
        "cooling center or heat safety routing": r"\b(cooling center|heat outage|no cooling|overheated|extreme heat|heat illness)\b",
    }

    for label, pattern in high_patterns.items():
        if _contains(text, pattern):
            signals.append(label)
    has_high_signal = bool(signals)

    for label, pattern in medium_patterns.items():
        if _contains(text, pattern):
            signals.append(label)
    if has_high_signal:
        return "high", signals
    if signals:
        return "medium", signals

    return "low", ["planning or preparedness request"]


def detect_preferred_language(scenario: str) -> str | None:
    language_patterns = {
        "Spanish": r"\b(spanish-speaking|spanish speaker|spanish)\b",
        "Chinese": r"\b(chinese|mandarin|cantonese)\b",
        "Vietnamese": r"\bvietnamese\b",
        "Arabic": r"\barabic\b",
        "Unknown non-English language": r"\b(limited english|does not speak english|cannot understand|language barrier|interpreter|translation)\b",
    }
    for language, pattern in language_patterns.items():
        if _contains(scenario, pattern):
            return language
    return None


def build_language_support(scenario: str) -> list[str]:
    language = detect_preferred_language(scenario)
    if not language:
        return ["Ask whether the household prefers another language, plain-language instructions, or an accessible format."]

    return [
        f"Preferred language: {language}.",
        "Use a qualified interpreter or language-access volunteer before collecting sensitive medical, registration, or shelter details.",
        "Read back the action plan in the preferred language and confirm understanding before routing the case.",
        "Do not use children as interpreters for medical or safety-critical details.",
    ]


def build_human_review_reason(scenario: str, risk: str, signals: list[str]) -> list[str]:
    lower = scenario.lower()
    reasons: list[str] = []

    if risk == "high":
        reasons.append("life-safety escalation: high-risk signals require a human responder before final routing.")
    elif risk == "medium":
        reasons.append("official resource verification: responder review is needed before sending people to a site or service.")
    else:
        reasons.append("preparedness check: human review is optional unless local conditions change.")

    if any(term in lower for term in ["insulin", "dialysis", "oxygen", "medication", "medicine", "prenatal", "asthma", "medical device"]):
        reasons.append("medical continuity: medication, device, or care timing needs official medical or clinical confirmation.")
    if any(term in lower for term in ["rumor", "capacity", "beds", "shelter can", "cooling center"]):
        reasons.append("capacity uncertainty: live shelter or cooling-center availability must come from official operations staff.")
    if any(term in lower for term in ["transport", "road", "ride", "bus", "no car"]):
        reasons.append("transport safety: route and vehicle availability need official logistics confirmation.")
    if detect_preferred_language(scenario):
        reasons.append("language-access-sensitive: qualified interpretation is needed before collecting medical, legal, or registration details.")
    if any("electrical" in signal or "floodwater" in signal or "oxygen" in signal for signal in signals):
        reasons.append("immediate hazard: emergency services or utility channels may need to act before routine shelter routing.")

    deduped: list[str] = []
    seen = set()
    for reason in reasons:
        key = reason.split(":", 1)[0]
        if key not in seen:
            deduped.append(reason)
            seen.add(key)
    return deduped


def build_official_resource_checks(scenario: str, risk: str, signals: list[str]) -> list[str]:
    lower = scenario.lower()
    checks = ["Local emergency management: verify current evacuation orders, road closures, and official shelter routing before sending people anywhere."]

    if risk == "high" or any("oxygen" in signal or "floodwater" in signal or "electrical" in signal for signal in signals):
        checks.append("Emergency services or utility emergency line: use for immediate danger, downed power lines, oxygen/powered-device failure, or life-safety escalation.")
    if "shelter" in lower or "evacuat" in lower or any("shelter" in signal for signal in signals):
        checks.append("Shelter operations desk: confirm accessibility, pet policy, intake requirements, and live capacity; do not rely on social media capacity claims.")
    if any(term in lower for term in ["medication", "medicine", "dialysis", "insulin", "prenatal", "asthma", "oxygen", "care"]):
        checks.append("Medical triage, clinic, pharmacy, or care coordinator: verify medication continuity, device power needs, dialysis/prenatal timing, and safe storage.")
    if any(term in lower for term in ["cooling center", "heat outage", "no cooling", "overheated", "extreme heat", "heat illness"]):
        checks.append("Public health heat line or cooling-center coordinator: verify cooling-center hours, accessible intake, hydration support, medication storage, and welfare-check options.")
    if any(term in lower for term in ["transport", "road", "ride", "bus", "no car"]):
        checks.append("Official transport desk or emergency management logistics: arrange accessible transport and avoid flooded roads.")
    if any(term in lower for term in ["pet", "dog", "cat"]):
        checks.append("Animal services or shelter pet desk: verify pet intake rules, carrier needs, and documentation.")
    if detect_preferred_language(scenario):
        checks.append("Language access line or qualified interpreter pool: confirm interpretation support before collecting medical or legal details.")

    return checks


def build_source_verification(scenario: str, risk: str, official_resource_checks: list[str]) -> list[str]:
    lower = scenario.lower()
    ledger = ["Known: case details are user- or volunteer-reported and must be treated as operational notes until official staff verify live conditions."]

    if any(term in lower for term in ["rumor", "social media", "heard", "probably", "may have beds", "capacity", "beds"]):
        ledger.append("Rumor quarantine: do not repeat social-media, word-of-mouth, bed-count, or capacity claims until official shelter operations confirms them.")
    if any(term in lower for term in ["shelter", "cooling center", "road", "transport", "ride", "bus", "no car"]):
        ledger.append("Freshness check: verify timestamp, current route status, facility hours, intake rules, accessibility, and transport availability before sharing directions.")
    if any(term in lower for term in ["insulin", "dialysis", "oxygen", "medication", "medicine", "prenatal", "asthma", "medical device"]):
        ledger.append("Clinical source check: route medication, oxygen, insulin, dialysis, prenatal, or device-power details through medical triage, clinic, pharmacy, or care coordinator confirmation.")
    if detect_preferred_language(scenario):
        ledger.append("Language source check: use a qualified interpreter for safety-critical details; do not treat child or ad hoc translation as verified.")
    if risk == "high":
        ledger.append("Escalation evidence: record callback, location, official route contacted, and what remains unknown before final responder decision.")

    route_labels = [item.split(":", 1)[0] for item in official_resource_checks[:3]]
    ledger.append("Official channels to verify first: " + " | ".join(route_labels) + ".")
    ledger.append("Public message rule: say what is known, what is unknown, and what is being checked; avoid unverified numbers or guarantees.")
    return ledger


def build_transfer_brief(
    scenario: str,
    risk: str,
    signals: list[str],
    human_review_reason: list[str],
    playbook_references: list[str],
    official_resource_checks: list[str],
    source_verification: list[str],
    questions: list[str],
    language_support: list[str],
) -> list[str]:
    playbook_ids = [item.split(" - ", 1)[0] for item in playbook_references]
    route_labels = [item.split(":", 1)[0] for item in official_resource_checks[:3]]
    preferred_language = detect_preferred_language(scenario) or "none"
    return [
        "ICS 201 alignment: concise transfer note for situation summary, current actions, resource status, communications, and prepared-by handoff.",
        f"Incident snapshot: risk={risk}; signals={' | '.join(signals)}; playbooks={' | '.join(playbook_ids)}.",
        "Immediate objectives: protect life safety first, verify official routes, collect callback/location/access needs, and keep final routing with a human responder.",
        "Safety constraints: do not diagnose, do not promise live capacity, do not guarantee routes or transport, and do not use child or ad hoc interpreters for sensitive details.",
        "Resource status: pending confirmation through " + " | ".join(route_labels) + "; unresolved resources stay unknown until staff confirm them.",
        "Communications: record callback, current location, preferred language=" + preferred_language + ", official channel contacted, time checked, and next owner.",
        "Unresolved questions: " + " ".join(questions[:2]),
        "Verification carryover: " + " ".join(source_verification[:2]) + " " + language_support[0],
        "Operational period check: re-verify facility hours, road status, transport ETA, welfare-check status, and capacity before each routing decision.",
    ]


def select_playbook_references(playbook: dict, risk: str, signals: list[str]) -> list[str]:
    signal_set = {risk, *signals}
    references = []
    for rule in playbook.get("playbook_rules", []):
        if signal_set.intersection(rule.get("signals", [])):
            references.append(f"{rule['id']} - {rule['title']}: {rule['summary']}")
    if not references:
        for rule in playbook.get("playbook_rules", []):
            if rule.get("id") == "PB-LOW-RISK-PREPAREDNESS":
                references.append(f"{rule['id']} - {rule['title']}: {rule['summary']}")
                break
    return references[:5]


def build_responder_handoff(
    risk: str,
    signals: list[str],
    human_review_reason: list[str],
    playbook_references: list[str],
    plan: list[str],
    official_resource_checks: list[str],
    source_verification: list[str],
    transfer_brief: list[str],
    questions: list[str],
    language_support: list[str],
) -> list[str]:
    return [
        f"Risk: {risk}.",
        "Signals: " + "; ".join(signals) + ".",
        "Human review reason: " + " ".join(human_review_reason[:2]),
        "Playbook basis: " + " ".join(item.split(":", 1)[0] for item in playbook_references[:2]) + ".",
        "Immediate routing: " + " ".join(plan[:2]),
        "Official checks: " + " ".join(official_resource_checks[:2]),
        "Source verification: " + " ".join(source_verification[:2]),
        "Transfer brief: " + " ".join(transfer_brief[1:3]),
        "Open information: " + " ".join(questions[:2]),
        "Language/access note: " + language_support[0],
    ]


def build_responder_packet(
    risk: str,
    signals: list[str],
    human_review_reason: list[str],
    playbook_references: list[str],
    official_resource_checks: list[str],
    source_verification: list[str],
    transfer_brief: list[str],
    questions: list[str],
    language_support: list[str],
) -> list[str]:
    playbook_ids = [item.split(" - ", 1)[0] for item in playbook_references]
    primary_route = official_resource_checks[0]
    if risk == "high" and len(official_resource_checks) > 1:
        primary_route = official_resource_checks[1]

    return [
        f"Case priority: {risk}.",
        "Human review reason: " + " ".join(human_review_reason[:2]),
        "Playbook IDs: " + ", ".join(playbook_ids) + ".",
        "Primary official route: " + primary_route,
        "Source verification: " + " ".join(source_verification[:2]),
        "Transfer brief: " + transfer_brief[1] + " " + transfer_brief[4],
        "Missing information: " + " ".join(questions[:2]),
        "Language/access cue: " + language_support[0],
        "Do not promise: live shelter capacity, medical conclusions, road safety, or transport availability without official confirmation.",
        "Copy packet: risk, signals, callback/location, official route, open items, and access needs.",
        "Signal summary: " + "; ".join(signals) + ".",
    ]


def build_household_message(
    scenario: str,
    risk: str,
    official_resource_checks: list[str],
    questions: list[str],
    language_support: list[str],
) -> list[str]:
    language = detect_preferred_language(scenario)
    message = [
        "Plain English holding note: we are treating this as a priority case and routing it through official local channels.",
        "Please keep the safest callback number available and tell the volunteer your current location.",
        "We cannot confirm a shelter bed, road safety, medical next steps, or transport availability until official staff verify them.",
    ]
    if risk == "high":
        message.append("If immediate danger worsens, contact emergency services or local responders now.")
    if language:
        message.append(f"Preferred language: {language}; use a qualified interpreter before collecting sensitive details.")
        message.append("This is not a full translation of medical, legal, or registration details.")
    else:
        message.append(language_support[0])
    message.append("Official channel to check first: " + official_resource_checks[0])
    message.append("Open question to answer next: " + questions[0])
    return message


def build_audit_trace(
    risk: str,
    signals: list[str],
    human_review_reason: list[str],
    playbook_references: list[str],
    official_resource_checks: list[str],
    source_verification: list[str],
    transfer_brief: list[str],
    scenario: str,
) -> list[str]:
    playbook_ids = [item.split(" - ", 1)[0] for item in playbook_references]
    language = detect_preferred_language(scenario) or "none"
    route_labels = [item.split(":", 1)[0] for item in official_resource_checks]
    source_labels = [item.split(":", 1)[0] for item in source_verification]
    return [
        f"risk_level={risk}",
        "signals=" + " | ".join(signals),
        "playbook_ids=" + " | ".join(playbook_ids),
        "official_routes=" + " | ".join(route_labels),
        "source_verification=" + " | ".join(source_labels),
        "transfer_brief=" + " | ".join(item.split(":", 1)[0] for item in transfer_brief[:6]),
        f"language={language}",
        "human_review_required=true",
        "human_review_reason=" + " | ".join(reason.split(":", 1)[0] for reason in human_review_reason),
        "blocked_claims=medical conclusions | live shelter capacity | road safety | transport availability",
        "response_contract=official-routes-first | no-invented-capacity | qualified-interpreter-when-needed",
    ]


def build_case_export(
    scenario: str,
    risk: str,
    signals: list[str],
    human_review_reason: list[str],
    playbook_references: list[str],
    official_resource_checks: list[str],
    source_verification: list[str],
    transfer_brief: list[str],
    questions: list[str],
) -> dict[str, object]:
    normalized = " ".join(scenario.lower().split())
    playbook_ids = [item.split(" - ", 1)[0] for item in playbook_references]
    route_labels = [item.split(":", 1)[0] for item in official_resource_checks]
    review_level = {
        "high": "immediate_escalation",
        "medium": "responder_review",
        "low": "preparedness_check",
    }[risk]
    return {
        "contract_version": "resilience-copilot-exp029",
        "case_fingerprint": "RC-" + sha256(normalized.encode("utf-8")).hexdigest()[:12],
        "risk_level": risk,
        "review_level": review_level,
        "signals": signals,
        "human_review_reason": human_review_reason,
        "playbook_ids": playbook_ids,
        "official_routes": route_labels,
        "source_verification": source_verification,
        "transfer_brief": transfer_brief,
        "required_human_review": True,
        "blocked_claims": [
            "medical conclusions",
            "live shelter capacity",
            "road safety",
            "transport availability",
        ],
        "language": detect_preferred_language(scenario) or "none",
        "missing_information": questions[:3],
        "response_contract": [
            "official-routes-first",
            "no-invented-capacity",
            "qualified-interpreter-when-needed",
            "human-responder-final-decision",
            "ics-style-transfer-brief",
        ],
    }


def generate_response(scenario: str) -> CopilotResponse:
    playbook = _load_playbook()
    risk, signals = detect_risk(scenario)
    human_review_reason = build_human_review_reason(scenario, risk, signals)
    playbook_references = select_playbook_references(playbook, risk, signals)
    plan = list(playbook["action_templates"][risk])
    lower = scenario.lower()

    if "pet" in lower:
        plan.append("Record pet species, size, carrier availability, and vaccination paperwork if available.")
    if "medication" in lower or "medicine" in lower or "dialysis" in lower:
        plan.append("Ask what medication or care schedule is at risk, then route through official medical or emergency channels.")
    if "transport" in lower or "road" in lower or "ride" in lower:
        plan.append("Coordinate transport only through official emergency management, clinic, or responder channels; do not drive through floodwater.")
    if "check-in" in lower or "check-ins" in lower or "live alone" in lower:
        plan.append("Set daily check-ins with a named neighbor, volunteer, or family contact, and define when to escalate if there is no response.")
    if "power line" in lower:
        plan.insert(0, "Move people away from floodwater and the downed line; contact emergency services or the utility through official channels.")
    if "pregnant" in lower or "prenatal" in lower or "insulin" in lower:
        plan.append("Route pregnancy, insulin, or prenatal-care continuity through official medical triage; record storage needs, timing, and callback details.")
    if "oxygen" in lower or "medical device" in lower or "backup battery" in lower:
        plan.insert(0, "Treat oxygen or powered medical device interruption as urgent; contact emergency services, utility medical priority channels, or clinical support.")
    if any(term in lower for term in ["cooling center", "heat outage", "no cooling", "overheated", "extreme heat", "heat illness"]):
        plan.append("Route heat exposure, cooling-center access, welfare checks, medication storage, and hydration support through public health or official emergency-management heat-response channels.")
    if "spanish" in lower or "interpreter" in lower or "cannot understand" in lower or "limited english" in lower:
        plan.append("Request a qualified interpreter or language-access volunteer before collecting sensitive medication or registration details.")
    if "rumor" in lower or "social media" in lower or "capacity" in lower or "beds" in lower:
        plan.append("Verify shelter capacity only through official emergency management or shelter operations before routing evacuees.")

    questions = [
        "What is the current location and safest callback number?",
        "Are there children, older adults, disabilities, pets, or urgent medical needs?",
        "Is there immediate danger such as floodwater, fire, electrical hazards, or severe symptoms?",
    ]
    if detect_preferred_language(scenario):
        questions.insert(1, "What is the preferred language, and is a qualified interpreter available now?")

    language_support = build_language_support(scenario)
    official_checks = build_official_resource_checks(scenario, risk, signals)
    source_verification = build_source_verification(scenario, risk, official_checks)
    transfer_brief = build_transfer_brief(scenario, risk, signals, human_review_reason, playbook_references, official_checks, source_verification, questions, language_support)
    handoff = build_responder_handoff(risk, signals, human_review_reason, playbook_references, plan, official_checks, source_verification, transfer_brief, questions, language_support)
    packet = build_responder_packet(risk, signals, human_review_reason, playbook_references, official_checks, source_verification, transfer_brief, questions, language_support)
    household_message = build_household_message(scenario, risk, official_checks, questions, language_support)
    audit_trace = build_audit_trace(risk, signals, human_review_reason, playbook_references, official_checks, source_verification, transfer_brief, scenario)
    case_export = build_case_export(scenario, risk, signals, human_review_reason, playbook_references, official_checks, source_verification, transfer_brief, questions)
    boundary = "Do not diagnose or invent real-time shelter capacity; use official local emergency channels for availability and urgent escalation."
    return CopilotResponse(
        risk,
        signals,
        human_review_reason,
        playbook_references,
        plan,
        official_checks,
        source_verification,
        transfer_brief,
        questions,
        language_support,
        handoff,
        packet,
        household_message,
        audit_trace,
        case_export,
        boundary,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", nargs="*", help="Scenario text")
    args = parser.parse_args()
    scenario = " ".join(args.scenario) or "A family was evacuated after a flood and needs shelter."
    print(generate_response(scenario).to_text())


if __name__ == "__main__":
    main()
