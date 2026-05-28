"""Evaluate baseline behavior on demo or holdout JSONL cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from resilience_copilot_baseline import generate_response


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def evaluate_case(case: dict) -> dict:
    response = generate_response(case["scenario"])
    text = response.to_text()
    lower = text.lower()
    must_include = case.get("must_include", [])
    must_not_include = case.get("must_not_include", [])
    include_hits = {item: item.lower() in lower for item in must_include}
    forbidden_hits = {item: item.lower() in lower for item in must_not_include}
    risk_ok = response.risk_level == case.get("expected_risk")
    passed = risk_ok and all(include_hits.values()) and not any(forbidden_hits.values())
    return {
        "id": case["id"],
        "expected_risk": case.get("expected_risk"),
        "actual_risk": response.risk_level,
        "risk_ok": risk_ok,
        "include_hits": include_hits,
        "forbidden_hits": forbidden_hits,
        "passed": passed,
        "response": text,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    results = [evaluate_case(case) for case in load_jsonl(args.cases)]
    summary = {
        "cases": str(args.cases),
        "passed": sum(1 for result in results if result["passed"]),
        "total": len(results),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"passed": summary["passed"], "total": summary["total"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
