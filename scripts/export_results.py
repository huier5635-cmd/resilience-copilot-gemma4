"""Export a compact reproducibility summary for applications or interviews."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.io import write_json


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "evaluation" / "summer_camp_results_summary.json")
    args = parser.parse_args()

    local_validation = read_json(ROOT / "outputs" / "local_validation" / "local_validation_report.json")
    benchmark = read_json(ROOT / "outputs" / "evaluation" / "benchmark_eval.json")
    stress = read_json(ROOT / "outputs" / "evaluation" / "stress_test_eval.json")
    summary = {
        "project": "Safety-Bounded LLM Agent for High-Risk Decision Support",
        "local_validation_ready": local_validation.get("ready_to_submit"),
        "demo": local_validation.get("demo_eval", {}).get("summary"),
        "holdout": local_validation.get("holdout_eval", {}).get("summary"),
        "stress": local_validation.get("stress_eval", {}).get("summary"),
        "benchmark_case_count": benchmark.get("case_count"),
        "benchmark_variants": list(benchmark.get("variants", {}).keys()),
        "stress_report": {"passed": stress.get("passed"), "total": stress.get("total")},
        "data_limitations": "Self-built scenario benchmark; no official training dataset was provided by the hackathon.",
    }
    write_json(args.output, summary)
    print(json.dumps({"output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
