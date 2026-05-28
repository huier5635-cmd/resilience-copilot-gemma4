from scripts.resilience_copilot_baseline import generate_response
from src.safety.contract import SafetyContractChecker


def test_safety_contract_accepts_complete_response():
    response = generate_response("An older adult uses oxygen and the backup battery is empty during a power outage.")
    result = SafetyContractChecker().check_response(response)
    assert result["passed"] is True
    assert result["missing_fields"] == []


def test_safety_contract_detects_missing_fields():
    incomplete = {"risk_level": "high", "case_signals": ["oxygen or powered medical device risk"]}
    result = SafetyContractChecker().check_response(incomplete)
    assert result["passed"] is False
    assert "case_export" in result["missing_fields"]

