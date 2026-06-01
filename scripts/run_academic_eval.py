"""Generate academic-style evaluation reports for the benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.academic_metrics import AcademicEvaluator, variant_order
from src.utils.io import load_jsonl, write_json

DEFAULT_CASES = ROOT / "data" / "benchmark_cases.jsonl"
DEFAULT_METADATA = ROOT / "data" / "benchmark_metadata.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "evaluation" / "academic_eval.json"
DEFAULT_REPORT = ROOT / "docs" / "academic_evaluation.md"
DEFAULT_FAILURE_REPORT = ROOT / "docs" / "failure_taxonomy_report.md"


def load_metadata(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_academic_report(report: dict[str, Any]) -> str:
    lines = [
        "# Academic Evaluation",
        "",
        "This report evaluates a self-built scenario benchmark. It is designed to test safety-control behavior and reproducibility, not to estimate real-world disaster-response outcomes.",
        "",
        f"System name: {report['system_name']}",
        f"Case count: {report['case_count']}",
        "",
        "## Evaluation Protocol",
        "",
        "Each case note includes expected risk signals, expected human-review behavior, forbidden behaviors, and benchmark metadata. The evaluation compares five deterministic ablations: base fallback, risk detection, safety sidecar, safety sidecar with memory retrieval, and safety sidecar with tool/resource verification.",
        "",
        "Primary metrics:",
        "",
        "- human-review precision, recall, and F1",
        "- risk-signal recall",
        "- contract completeness",
        "- audit completeness",
        "- unsafe-claim block rate",
        "- structured JSON valid rate",
        "",
        "## Variant Summary",
        "",
        "| Variant | Human Review Precision | Human Review Recall | Human Review F1 | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block | JSON Valid |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in variant_order():
        summary = report["variant_academic_summary"][variant]
        lines.append(
            "| {variant} | {precision:.2f} | {recall:.2f} | {f1:.2f} | {risk:.2f} | {contract:.2f} | {audit:.2f} | {block:.2f} | {json_valid:.2f} |".format(
                variant=variant,
                precision=summary["human_review_precision"],
                recall=summary["human_review_recall"],
                f1=summary["human_review_f1"],
                risk=summary["risk_signal_recall"],
                contract=summary["contract_completeness"],
                audit=summary["audit_completeness"],
                block=summary["unsafe_claim_block_rate"],
                json_valid=summary["structured_json_valid_rate"],
            )
        )

    final_variant = "E_sidecar_tool_verification"
    lines.extend(
        [
            "",
            "## Stratified Results",
            "",
            "The following tables report the final safety-sidecar-plus-tool-verification variant by metadata group. Groups overlap because one case can contain multiple risk or uncertainty types.",
        ]
    )
    for dimension, groups in report["stratified_metrics"].items():
        lines.extend(
            [
                "",
                f"### By {dimension}",
                "",
                "| Group | Count | Human Review Recall | Risk Signal Recall | Contract Complete | Audit Complete | Unsafe-Claim Block |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for group_name, variants in sorted(groups.items()):
            summary = variants[final_variant]
            review_value = "n/a" if summary.get("expected_human_review_cases", 0) == 0 else f"{summary.get('human_review_recall', 0):.2f}"
            lines.append(
                "| {group} | {total} | {review} | {risk:.2f} | {contract:.2f} | {audit:.2f} | {block:.2f} |".format(
                    group=group_name,
                    total=summary.get("total", 0),
                    review=review_value,
                    risk=summary.get("risk_signal_recall", 0),
                    contract=summary.get("contract_completeness", 0),
                    audit=summary.get("audit_completeness", 0),
                    block=summary.get("unsafe_claim_block_rate", 0),
                )
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The base fallback intentionally lacks the deterministic sidecar, so it is expected to fail contract, audit, and resource-hallucination checks.",
            "- The final variant is strongest on this benchmark because it combines pre-generation risk detection, post-generation contract checks, memory retrieval limits, and an offline resource-verification sandbox.",
            "- The final variant is intentionally conservative: a small number of low-risk planning cases receive human-review triggers, which lowers precision but avoids missed escalation in the high-risk subset.",
            "- These results do not prove field readiness. They show that the implemented safety controls behave consistently on a small, self-built scenario benchmark.",
            "",
            "## Limitations",
            "",
            "- Cases are hand-authored and not expert-adjudicated.",
            "- The evaluation uses deterministic fallback behavior for reproducibility.",
            "- The resource verifier is offline and category-based; it does not query live official systems.",
            "- Human-review labels are scenario expectations, not operational ground truth.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_failure_report(report: dict[str, Any]) -> str:
    lines = [
        "# Failure Taxonomy Report",
        "",
        "This taxonomy describes how benchmark failures are categorized. Passing cases are still listed as `passed`; this makes later regressions easier to locate.",
        "",
        "| Variant | passed | missed_risk_signal | unsafe_response | hallucinated_resource | human_review_mismatch | contract_incomplete | structured_json_invalid | audit_omission |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    labels = [
        "passed",
        "missed_risk_signal",
        "unsafe_response",
        "hallucinated_resource",
        "human_review_mismatch",
        "contract_incomplete",
        "structured_json_invalid",
        "audit_omission",
    ]
    for variant in variant_order():
        counts = report["failure_taxonomy"][variant]["counts"]
        values = " | ".join(str(counts.get(label, 0)) for label in labels)
        lines.append(f"| {variant} | {values} |")
    lines.extend(
        [
            "",
            "## Taxonomy Definitions",
            "",
            "- `missed_risk_signal`: expected signal was not detected.",
            "- `unsafe_response`: output matched a forbidden behavior pattern.",
            "- `hallucinated_resource`: output contained unsupported capacity, transport, route, or clinic availability claims.",
            "- `human_review_mismatch`: expected human-review behavior and actual trigger disagreed.",
            "- `contract_incomplete`: sixteen-section response or export contract failed.",
            "- `structured_json_invalid`: required export fields were missing.",
            "- `audit_omission`: audit trace did not include required decision markers.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--failure-report", type=Path, default=DEFAULT_FAILURE_REPORT)
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    metadata = load_metadata(args.metadata)
    result = AcademicEvaluator(metadata).evaluate(cases)
    write_json(args.output, result)
    args.report.write_text(build_academic_report(result), encoding="utf-8")
    args.failure_report.write_text(build_failure_report(result), encoding="utf-8")
    print(
        json.dumps(
            {
                "cases": len(cases),
                "output": str(args.output),
                "report": str(args.report),
                "failure_report": str(args.failure_report),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
