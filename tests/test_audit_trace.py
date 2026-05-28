from scripts.resilience_copilot_baseline import generate_response


def test_audit_trace_records_key_steps():
    response = generate_response("A Spanish-speaking family needs shelter registration help and has asthma medication.")
    trace = "\n".join(response.audit_trace)
    assert "risk_level=" in trace
    assert "signals=" in trace
    assert "playbook_ids=" in trace
    assert "official_routes=" in trace
    assert "human_review_required=true" in trace

