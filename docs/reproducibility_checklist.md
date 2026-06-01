# Reproducibility Checklist

## Environment

- Python 3.10 or newer
- Dependencies from `requirements.txt`
- No external API key required for deterministic local evaluation
- Optional environment variables documented in `.env.example`

## Data

- Benchmark cases: `data/benchmark_cases.jsonl`
- Benchmark metadata: `data/benchmark_metadata.json`
- Demo cases: `data/cases/demo_cases.jsonl`
- Holdout cases: `data/cases/holdout_cases.jsonl`
- Stress cases: `data/cases/stress_cases.jsonl`
- Playbook rules: `knowledge_base/emergency_playbook.json`

All benchmark and stress cases are self-built scenario data. They are used for safety-control testing and do not represent an official operational dataset.

## Core Commands

```powershell
pip install -r requirements.txt
python scripts\run_demo.py --case-id bench_001_oxygen_power_outage
python scripts\run_eval.py
python scripts\run_academic_eval.py
python scripts\run_stress_test.py
python -m pytest tests
```

If the local validation wrapper is present in the checkout:

```powershell
python scripts\run_local_validation.py
```

## Expected Generated Artifacts

- `outputs/evaluation/benchmark_eval.json`
- `outputs/evaluation/academic_eval.json`
- `outputs/evaluation/stress_test_eval.json`
- `docs/benchmark_eval_report.md`
- `docs/academic_evaluation.md`
- `docs/failure_taxonomy_report.md`
- `docs/stress_test_report.md`

Generated `outputs/` files are local artifacts and do not need to be committed for the project to be reproducible.

## Model Evidence

Gemma 4 usage is documented through the Kaggle evidence notebook linked from the README. Local benchmark evaluation uses deterministic fallback behavior so that reviewers can rerun safety checks without GPU access or network dependencies.

## Known Limits

- No live official-resource API is queried.
- The benchmark is not expert-labeled.
- The local fallback does not measure open-ended model quality.
- Human-review behavior is tested against scenario expectations.
- Results should be treated as regression-test evidence for the prototype, not as deployment evidence.
