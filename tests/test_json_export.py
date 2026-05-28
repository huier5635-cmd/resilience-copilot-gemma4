from scripts.resilience_copilot_baseline import generate_response


def test_case_export_contains_required_review_fields():
    response = generate_response("A social media rumor says a shelter has beds and a family has a dog.")
    export = response.case_export
    assert export["contract_version"] == "resilience-copilot-exp029"
    assert export["required_human_review"] is True
    assert "blocked_claims" in export
    assert "response_contract" in export

