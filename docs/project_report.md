# Project Report: Safety-Bounded LLM Agent for High-Risk Decision Support

## 1. 项目背景

灾害救援中的一线信息经常以零散 case note 的形式出现：志愿者可能记录到老人缺氧、胰岛素断供、儿童受冷、道路中断、避难所传言、语言障碍或宠物安置等信息。大模型能够快速生成自然语言，但高风险场景真正需要的是可控、可复核、可审计的辅助系统，而不是一个只会流畅回答的聊天机器人。

Resilience Copilot 来源于 Kaggle Gemma 4 Good Hackathon，后续被整理成一个面向可信 AI 和 LLM Agent 安全的工程原型。项目目标是研究如何把风险识别、规则约束、工具沙盒、长期记忆门控、人工复核和审计追踪组合起来，让大模型在复杂任务中更可靠。

## 2. 问题定义

输入是一段混乱的灾害救援记录，输出不是直接建议用户“去哪里”或“做什么”，而是一个 responder handoff：包含风险等级、触发信号、匹配 playbook、官方资源核验路径、Transfer Brief、结构化 JSON 和 Audit Trace。

项目关注的问题是：在没有真实官方训练集的情况下，如何构建一个可复现的安全约束型 LLM Agent 原型，并用自建 benchmark 检查它是否遵守安全契约。

## 3. 系统架构

系统主流程为：

`User Case Note -> Input Normalization -> Risk Signal Detection -> Playbook Matching -> LLM / Gemma Generation -> Safety Contract Checking -> Official Resource Verification -> Memory Retrieval / Protected Invariants -> Human Review Trigger -> Structured JSON Export -> Audit Trace -> Responder Handoff`

其中生成前链路负责发现风险并限制模型输出空间；生成后链路负责检查响应结构、阻断不支持的资源声明，并把高风险案例交给人工复核。长期记忆只提供辅助检索和策略建议，不能自动修改高风险规则。

## 4. 核心模块

- Risk Signal Detection：基于确定性规则识别氧气设备、药物连续性、洪水、电力、交通、语言、宠物、谣言和避难所容量等信号。
- Playbook Matching：把风险信号映射到可审计的安全行动手册。
- Gemma Generation：在 Kaggle Notebook 中验证 Gemma 4 可用于 responder-facing phrasing；本地评测使用 deterministic fallback 保证可复现。
- Safety Sidecar：在生成前后执行规则约束和安全契约检查。
- Tool Calling Sandbox：离线模拟官方资源核验，只允许白名单类别，不允许编造实时容量或交通可用性。
- Memory Write Gate：把未经人工审核的经验隔离在 quarantine，防止 memory pollution。

## 5. 安全机制

系统显式禁止医疗诊断、编造避难所容量、编造交通可用性、保证道路安全、替代 emergency services，以及使用儿童或临时翻译处理敏感细节。高风险或资源不确定的案例必须触发 human review。Audit Trace 会记录风险等级、信号、playbook、官方核验路径、被阻断声明和复核原因。

## 6. 实验设计

由于比赛没有官方训练数据，项目使用两类评测：

1. 原 Kaggle 本地验证：demo、holdout、stress 三组场景。
2. 自建 30 条 benchmark：覆盖缺氧、胰岛素、儿童受冷、断电、洪水、交通、语言、宠物、谣言、容量未知、医疗风险和官方资源不确定。

研究化评测比较五个版本：Base LLM fallback、Risk Signal Detection、Safety Sidecar、Sidecar + Memory、Sidecar + Tool/Resource Verification。指标包括 contract pass rate、unsafe response rate、missing risk signal rate、hallucinated resource rate、human review trigger rate、structured JSON valid rate 和 audit trace complete rate。

## 7. 实验结果

当前 Kaggle 本地门禁结果为 demo 2/2、holdout 2/2、stress 15/15，`ready_to_submit=true`。新增 benchmark 结果由 `python scripts/run_eval.py` 生成，报告保存在 `docs/benchmark_eval_report.md`。这些结果只能说明系统在自建安全测试集上满足工程约束，不能外推为真实灾害救援效果。

## 8. 项目亮点

项目亮点不是模型规模，而是系统边界：用确定性 sidecar 管住 LLM 输出；用 playbook 约束生成；用 tool sandbox 管住资源声明；用 memory write gate 防止经验污染；用 structured JSON 和 Audit Trace 保证可复核；用 benchmark 和 stress suite 保证可重复检查。

## 9. 局限性

项目仍是原型系统。自建 benchmark 规模较小，没有专家标注；本地 fallback 不能代表真实 Gemma 在线推理的全部行为；官方资源核验是离线沙盒，没有连接真实应急 API；memory 机制仍需要更严格的 provenance、review workflow 和攻击测试。

## 10. 未来工作

后续可以沿三个方向深入：第一，构建专家标注的高风险 case-note benchmark；第二，研究 LLM Agent 的 memory pollution、policy drift 和 protected invariant enforcement；第三，在安全边界内扩展工具调用和多 Agent 协作，使系统能连接官方资源 API，但所有高风险策略升级仍需人工审核。

