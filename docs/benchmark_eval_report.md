# Benchmark Evaluation Report

This report uses a self-built scenario benchmark for safety engineering evaluation. It does not claim real-world disaster-response effectiveness.

Case count: 30

| Variant | Contract Pass | Unsafe Response | Missing Risk Signal | Hallucinated Resource | Human Review Trigger | JSON Valid | Audit Complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A_base_llm_fallback | 0.00 | 0.70 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| B_risk_signal_detection | 0.00 | 0.00 | 0.00 | 0.00 | 0.90 | 0.00 | 0.00 |
| C_safety_sidecar | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| D_sidecar_memory | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |
| E_sidecar_tool_verification | 1.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 |

## Interpretation

- A and B are deterministic fallback ablations, not measured external LLM products.
- C, D, and E reuse the locked Resilience Copilot safety contract path.
- Memory is evaluated as retrieval support only; it cannot rewrite protected safety invariants.
- Tool/resource verification is an offline sandbox that blocks unsupported capacity, transport, road-safety, and clinic-availability claims.
