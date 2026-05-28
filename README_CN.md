# Resilience Copilot 中文说明

本仓库的主说明以 [README.md](README.md) 为准。

## 项目定位

Resilience Copilot 是一个面向高风险场景的大模型安全智能体系统原型。项目研究如何在灾害救援 case note 处理中，用风险识别、规则约束、工具核验、长期记忆门控、人工复核和审计追踪提升 LLM Agent 的可靠性与可控性。

## 核心链路

`User Case Note -> Risk Signal Detection -> Playbook Matching -> LLM / Gemma Generation -> Safety Contract Checking -> Official Resource Verification -> Memory Retrieval / Protected Invariants -> Human Review Trigger -> Structured JSON Export -> Audit Trace -> Responder Handoff`

系统不是自动救援调度工具，也不替代 emergency services。它只把混乱、不确定的救援记录整理成可复核、可交接、可审计的 responder handoff。

## 快速运行

```powershell
pip install -r requirements.txt
python scripts\run_demo.py
python scripts\run_eval.py
python scripts\run_stress_test.py
python -m pytest tests
```

## 当前验证

- demo 2/2
- holdout 2/2
- stress 15/15
- original Kaggle local gate: `ready_to_submit=true`
- self-built benchmark: 30 条安全工程场景
- pytest: 8 个核心测试

## 适合展示的材料

- [docs/architecture.md](docs/architecture.md)
- [docs/project_report.md](docs/project_report.md)
- [docs/memory_eval.md](docs/memory_eval.md)
- [docs/interview_qa.md](docs/interview_qa.md)
- [docs/summer_camp_summary.md](docs/summer_camp_summary.md)

