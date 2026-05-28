from src.safety.risk import detect_risk_signals


def test_high_risk_case_triggers_human_review():
    result = detect_risk_signals("An older adult uses oxygen and the backup battery is empty during a power outage.")
    assert result["risk_level"] == "high"
    assert "oxygen or powered medical device risk" in result["signals"]
    assert result["human_review_required"] is True


def test_low_risk_preparedness_remains_low():
    result = detect_risk_signals("A student volunteer is preparing a community preparedness checklist.")
    assert result["risk_level"] == "low"
    assert result["signals"] == ["planning or preparedness request"]

