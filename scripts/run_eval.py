"""Run the self-built safety benchmark across agent ablations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.metrics import BenchmarkEvaluator
from src.utils.io import load_jsonl, write_json

DEFAULT_CASES = ROOT / "data" / "benchmark_cases.jsonl"
DEFAULT_OUTPUT = ROOT / "outputs" / "evaluation" / "benchmark_eval.json"
DEFAULT_REPORT = ROOT / "docs" / "benchmark_eval_report.md"


def build_markdown_report(report: dict) -> str:
    lines = [
        "# Benchmark Evaluation Report",
        "",
        "This report uses a self-built scenario benchmark for safety engineering evaluation. It does not claim real-world disaster-response effectiveness.",
        "",
        f"Case count: {report['case_count']}",
        "",
        "| Variant | Contract Pass | Unsafe Response | Missing Risk Signal | Hallucinated Resource | Human Review Trigger | JSON Valid | Audit Complete |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, payload in report["variants"].items():
        summary = payload["summary"]
        lines.append(
            "| {name} | {contract:.2f} | {unsafe:.2f} | {missing:.2f} | {hallucinated:.2f} | {review:.2f} | {json_valid:.2f} | {audit:.2f} |".format(
                name=name,
                contract=summary["contract_pass_rate"],
                unsafe=summary["unsafe_response_rate"],
                missing=summary["missing_risk_signal_rate"],
                hallucinated=summary["hallucinated_resource_rate"],
                review=summary["human_review_trigger_rate"],
                json_valid=summary["structured_json_valid_rate"],
                audit=summary["audit_trace_complete_rate"],
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A and B are deterministic fallback ablations, not measured external LLM products.",
            "- C, D, and E reuse the locked Resilience Copilot safety contract path.",
            "- Memory is evaluated as retrieval support only; it cannot rewrite protected safety invariants.",
            "- Tool/resource verification is an offline sandbox that blocks unsupported capacity, transport, road-safety, and clinic-availability claims.",
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
    result = BenchmarkEvaluator().evaluate(cases)
    write_json(args.output, result)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(build_markdown_report(result), encoding="utf-8")
    print(json.dumps({"cases": len(cases), "output": str(args.output), "report": str(args.report)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
