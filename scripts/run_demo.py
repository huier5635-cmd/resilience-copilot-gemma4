"""Run a single Resilience Copilot case from the command line."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agent import ResilienceAgent
from src.utils.io import load_jsonl

DEFAULT_CASES = ROOT / "data" / "benchmark_cases.jsonl"


def pick_case(case_id: str | None) -> str:
    cases = load_jsonl(DEFAULT_CASES)
    if case_id:
        for case in cases:
            if case["case_id"] == case_id:
                return case["case_note"]
        raise SystemExit(f"Unknown case_id: {case_id}")
    return cases[0]["case_note"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", help="Benchmark case id to run")
    parser.add_argument("--scenario", help="Raw case note text")
    args = parser.parse_args()

    case_note = args.scenario or pick_case(args.case_id)
    result = ResilienceAgent().run(case_note)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
