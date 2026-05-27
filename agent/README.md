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
- memory and strategy reflection stay human-reviewed.

The static demo in `index.html` shows the same pattern in a browser-friendly form.
