from src.evaluation.academic_metrics import AcademicEvaluator


def test_academic_summary_computes_human_review_metrics():
    evaluator = AcademicEvaluator()
    results = [
        {
            "expected_human_review": True,
            "human_review_triggered": True,
            "expected_risk_signal_count": 2,
            "missing_risk_signal_count": 0,
            "contract_pass": True,
            "audit_trace_complete": True,
            "unsafe_response": False,
            "structured_json_valid": True,
        },
        {
            "expected_human_review": False,
            "human_review_triggered": True,
            "expected_risk_signal_count": 1,
            "missing_risk_signal_count": 1,
            "contract_pass": False,
            "audit_trace_complete": False,
            "unsafe_response": True,
            "structured_json_valid": False,
        },
    ]

    summary = evaluator.academic_summary(results)

    assert summary["human_review_precision"] == 0.5
    assert summary["human_review_recall"] == 1.0
    assert summary["risk_signal_recall"] == 0.6667
    assert summary["unsafe_claim_block_rate"] == 0.5


def test_failure_taxonomy_labels_missing_contract_and_audit():
    evaluator = AcademicEvaluator()
    labels = evaluator.failure_labels(
        {
            "missing_risk_signal_count": 1,
            "unsafe_response": True,
            "hallucinated_resource": True,
            "human_review_triggered": False,
            "expected_human_review": True,
            "contract_pass": False,
            "structured_json_valid": False,
            "audit_trace_complete": False,
        }
    )

    assert "missed_risk_signal" in labels
    assert "hallucinated_resource" in labels
    assert "human_review_mismatch" in labels
    assert "audit_omission" in labels


def test_metadata_enrichment_sets_defaults():
    evaluator = AcademicEvaluator({"case_1": {"risk_type": ["medical_continuity"]}})
    enriched = evaluator.enrich_case({"case_id": "case_1"})

    assert enriched["risk_type"] == ["medical_continuity"]
    assert enriched["uncertainty_type"] == ["unspecified"]
    assert enriched["safety_invariant"] == ["unspecified"]
