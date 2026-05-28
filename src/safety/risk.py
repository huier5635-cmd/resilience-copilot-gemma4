"""Risk signal detection wrapper around the Kaggle baseline logic."""

from __future__ import annotations

from scripts.resilience_copilot_baseline import detect_risk


def detect_risk_signals(case_note: str) -> dict[str, object]:
    """Return the deterministic risk level and triggered signal labels."""

    risk_level, signals = detect_risk(case_note)
    return {"risk_level": risk_level, "signals": signals, "human_review_required": risk_level in {"high", "medium"}}

