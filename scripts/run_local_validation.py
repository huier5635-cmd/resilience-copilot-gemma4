"""Run the local validation suites available in this checkout."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_demo_cases import evaluate_case, load_jsonl
from scripts.run_stress_test import classify_case
from src.utils.io import write_json

DEMO_CASES = ROOT / "data" / "cases" / "demo_cases.jsonl"
HOLDOUT_CASES = ROOT / "data" / "cases" / "holdout_cases.jsonl"
STRESS_CASES = ROOT / "data" / "cases" / "stress_cases.jsonl"
OUTPUT_PATH = ROOT / "outputs" / "local_validation" / "local_validation_report.json"


def summarize(results: list[dict]) -> dict[str, int]:
    return {
        "passed": sum(1 for result in results if result["passed"]),
        "total": len(results),
    }


def run_suite(path: Path) -> dict[str, object]:
    results = [evaluate_case(case) for case in load_jsonl(path)]
    return {
        "cases": str(path),
        "summary": summarize(results),
        "results": results,
    }


def run_stress_suite(path: Path) -> dict[str, object]:
    results = []
    for case in load_jsonl(path):
        result = evaluate_case(case)
        result["case_type"] = classify_case(case)
        results.append(result)
    return {
        "cases": str(path),
        "summary": summarize(results),
        "results": results,
    }


def main() -> None:
    demo_eval = run_suite(DEMO_CASES)
    stress_eval = run_stress_suite(STRESS_CASES)
    holdout_eval: dict[str, object]
    if HOLDOUT_CASES.exists():
        holdout_eval = run_suite(HOLDOUT_CASES)
        ready_to_submit: bool | None = all(
            suite["summary"]["passed"] == suite["summary"]["total"]  # type: ignore[index]
            for suite in (demo_eval, holdout_eval, stress_eval)
        )
    else:
        holdout_eval = {
            "cases": str(HOLDOUT_CASES),
            "status": "not_found",
            "summary": None,
            "results": [],
        }
        ready_to_submit = None

    report = {
        "demo_eval": demo_eval,
        "holdout_eval": holdout_eval,
        "stress_eval": stress_eval,
        "ready_to_submit": ready_to_submit,
    }
    write_json(OUTPUT_PATH, report)
    print(json.dumps({"output": str(OUTPUT_PATH), "ready_to_submit": ready_to_submit}, ensure_ascii=False))


if __name__ == "__main__":
    main()
