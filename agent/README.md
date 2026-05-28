# Agent Core

This folder contains the reusable public core behind the Resilience Copilot demo.

```python
from agent import ResilienceAgent

agent = ResilienceAgent()
result = agent.run(
    "Older adult uses oxygen. Power is out and backup battery is nearly empty."
)
print(result["risk_level"])
print(result["transfer_brief"])
```

The agent is intentionally bounded:

- no live external API calls;
- no emergency-service replacement;
- no medical diagnosis;
- no shelter-capacity or transport-availability promises;
- runtime input is ledger-only until validated;
- long-term memory promotion requires local validation, confidence, and human review;
- memory and strategy reflection stay human-reviewed.

## Memory Write Gate

```python
agent = ResilienceAgent()

runtime = agent.run("A social media rumor says the shelter has beds.")
print(runtime["memory_write_gate"]["promotion_status"])
# quarantined_pending_review

validated = agent.run_validated_case(
    "A social media rumor says the shelter has beds and the family needs a pet-compatible shelter."
)
print(validated["memory_write_gate"]["promotion_status"])
# approved_long_term_memory
```

Protected invariants cannot be rewritten by memory:

- do not replace emergency services;
- do not provide medical diagnosis;
- do not invent live shelter capacity;
- do not invent transport availability;
- do not execute external actions;
- require human review before policy updates.

The static demo in `index.html` shows the same pattern in a browser-friendly form.
