"""Generate a readable stress-test report from existing stress cases."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_demo_cases import evaluate_case, load_jsonl
from src.utils.io import write_json

DEFAULT_CASES = ROOT / "data" / "cases" / "stress_cases.jsonl"
DEFAULT_OUTPUT = ROOT / "outputs" / "evaluation" / "stress_test_eval.json"
DEFAULT_REPORT = ROOT / "docs" / "stress_test_report.md"


def classify_case(case: dict) -> str:
    text = (case.get("scenario") or case.get("case_note") or "").lower()
    if "oxygen" in text or "power" in text or "battery" in text:
        return "oxygen_power_or_utility"
    if "heat" in text or "cooling" in text:
        return "heat_and_cooling"
    if "rumor" in text or "capacity" in text or "beds" in text:
        return "rumor_or_capacity"
    if "spanish" in text or "language" in text or "interpreter" in text or "limited english" in text:
        return "language_access"
    if "pet" in text or "dog" in text or "cat" in text:
        return "pet_shelter"
    if "transport" in text or "road" in text or "ride" in text or "bus" in text:
        return "transport_barrier"
    if "insulin" in text or "dialysis" in text or "medication" in text:
        return "medical_continuity"
    return "general_disaster_triage"


def build_report(results: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for result in results:
        grouped[result["case_type"]].append(result)
    lines = [
        "# Stress Test Report",
        "",
        "The stress suite is scenario-based because the hackathon did not provide an official training dataset. It checks whether the deterministic safety sidecar preserves the response contract under high-risk case-note variations.",
        "",
        "| Case Type | Count | Pass | Fail | Main Risk | Fix |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    risk_map = {
        "oxygen_power_or_utility": "powered medical device outage",
        "heat_and_cooling": "heat illness and capacity uncertainty",
        "rumor_or_capacity": "unverified shelter capacity",
        "language_access": "unsafe ad hoc interpretation",
        "pet_shelter": "invented pet-compatible shelter routing",
        "transport_barrier": "unsafe route or transport assumptions",
        "medical_continuity": "medical continuity without diagnosis",
        "general_disaster_triage": "generic overconfidence",
    }
    fix_map = {
        "oxygen_power_or_utility": "Emergency/utility medical-priority routing plus human review.",
        "heat_and_cooling": "Cooling-center official check and no capacity promise.",
        "rumor_or_capacity": "Rumor quarantine and shelter operations confirmation.",
        "language_access": "Qualified interpreter requirement.",
        "pet_shelter": "Animal services or shelter pet desk verification.",
        "transport_barrier": "Official logistics routing and flooded-road avoidance.",
        "medical_continuity": "Medical triage/pharmacy/care coordinator route.",
        "general_disaster_triage": "Keep official-resource-first response contract.",
    }
    for case_type in sorted(grouped):
        items = grouped[case_type]
        passed = sum(1 for item in items if item["passed"])
        failed = len(items) - passed
        lines.append(f"| {case_type} | {len(items)} | {passed} | {failed} | {risk_map[case_type]} | {fix_map[case_type]} |")
    lines.extend(
        [
            "",
            "## Current Result",
            "",
            f"Passed {sum(1 for item in results if item['passed'])}/{len(results)} stress cases.",
            "",
            "## Follow-up",
            "",
            "Future work should replace these hand-authored stress cases with larger multi-region benchmarks and expert-reviewed annotations.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    results = []
    for case in cases:
        result = evaluate_case(case)
        result["case_type"] = classify_case(case)
        results.append(result)
    summary = {"cases": str(args.cases), "passed": sum(1 for item in results if item["passed"]), "total": len(results), "results": results}
    write_json(args.output, summary)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(build_report(results), encoding="utf-8")
    print(json.dumps({"passed": summary["passed"], "total": summary["total"], "report": str(args.report)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
