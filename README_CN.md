# Resilience Copilot 中文说明

语言版本：[README.md](README.md) | [README_EN.md](README_EN.md)

Resilience Copilot 是一个面向灾害救援场景的安全优先分诊助手，基于 Gemma 4、确定性安全侧车、可审计行动手册、官方资源核验、ICS 风格 Transfer Brief、结构化 JSON 导出和本地场景验证，帮助志愿者把混乱的危机记录转化为更安全、可复核、可交接的下一步行动建议。

项目用于 **The Gemma 4 Good Hackathon**。比赛没有提供官方训练数据，因此本项目重点放在可复现场景验证、公开在线 Demo、Gemma 4 使用证据和评委可核查的工程闭环上。

![Resilience Copilot demo preview](resilience_copilot_demo_preview.png)

## 30 秒速览

| 检查点 | 内容 |
| --- | --- |
| 项目背景 | 灾害救援志愿者常面对零散记录、谣言、资源状态不确定、语言支持需求和医疗相关高风险线索。 |
| 方法框架 | 确定性安全侧车先识别风险信号和行动约束，再让 Gemma 4 生成面向救援人员的文本，最后执行安全契约检查。 |
| 系统架构 | `Case Note -> Risk Signal Detector -> Playbook Matcher -> Gemma 4 Generation -> Safety Contract Checker -> 16-section Response -> JSON Export + Audit Trace + Transfer Brief` |
| Agent 能力 | 当前是有安全边界的学习型智能体原型，包含 LangGraph 兼容图式编排、经验账本、验证反馈记忆、长期记忆系统、策略反思、技能库和工具调用沙盒。 |
| 安全机制 | 不替代 emergency services，不诊断，不虚构避难所容量或交通可用性，关键决策保持人工复核。 |
| 验证结果 | 本地门禁通过：demo 2/2、holdout 2/2、stress 15/15，`ready_to_submit=true`。 |
| 在线 Demo | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |

## V4 救援指挥舱展示

最新版展示资产是 **Rescue Command Center** 版 PPT：

- [V4 pitch deck](resilience_copilot_pitch_v4_command_center.pptx)
- [V4 narration script](resilience_copilot_pitch_v4_narration_script.txt)

![Resilience Copilot V4 command center preview](resilience_copilot_pitch_v4_video_frame.png)

## 如何评审

1. 打开公开 Demo，运行默认 flood case 或 heatwave sample。
2. 在首屏结果区查看风险等级、行动手册数量、官方资源路径和验证状态。
3. 检查 `Transfer Brief`、`Audit Trace`、`Source Verification Ledger` 和 `Case Export`，确认安全侧车如何让输出可审计。
4. 下载 `resilience_copilot_submission_bundle_EXP029.zip`，查看最终 writeup、验证报告、证据截图、复现脚本和 Gemma 4 运行证据。

## 智能体学习侧车

EXP-029 的救援分诊运行时是 **有安全边界的 workflow agent**，不是无约束 autonomous agent，也不是完全自主的应急行动系统。项目在稳定运行时外增加了离线学习侧车，使系统能够从本地验证中积累经验并提出下一轮策略建议，但不会在真实灾害场景中自主行动。

学习侧车包含：

- **experience ledger**：记录每个本地验证案例的经验。
- **validation feedback memory**：汇总通过/失败模式、反复出现的风险信号和行动手册使用情况。
- **bounded long-term memory system**：四层长期记忆，包括情景记忆、语义记忆、程序记忆和反思记忆。
- **strategy reflection**：从验证反馈中生成只供人工审核的策略反思。
- **skill library**：沉淀可复用救援策略，如谣言隔离、语言支持交接、热浪路径规划等。
- **tool calling sandbox**：离线模拟官方资源查询，不联网、不产生真实副作用。
- **LangGraph-compatible graph orchestrator**：用规划器、协调器、专家节点、安全检查器和总结智能体组织执行流程。

```text
Planner
  ->
Coordinator
  ->
Risk Specialist
  ->
Memory Retriever
  ->
Playbook Specialist
  ->
Tool Router
  ->
Generation Specialist
  ->
Safety Contract Checker
  ->
Summary Agent
```

本地 D 盘环境已安装 LangGraph 并验证 `StateGraph` 运行成功；最终包仍保留确定性降级图执行器。这样评委机器即使不安装 LangGraph，也能离线复现同样的节点顺序和审计轨迹。

## 记忆系统

记忆系统基于本地验证反馈生成，不连接外部数据库，也不自动修改高风险策略。

| 记忆类型 | 作用 |
| --- | --- |
| episodic memory | 记录具体案例经验，例如氧气断电、热浪行动障碍、避难所谣言等。 |
| semantic memory | 从通过验证的案例中巩固稳定的安全事实和信号-策略关联。 |
| procedural memory | 保存可复用技能，例如谣言隔离、语言支持交接、热浪路径规划。 |
| reflective memory | 保存策略反思，供下一轮人工审核。 |

当前结果：53 条 memories、19 条 episodic memories、20 条 semantic memories、7 条 procedural memories、7 条 reflective memories、3 个 retrieval demos、6 条 protected safety invariants。

## 安全机制

- 高风险案例必须进入人工复核。
- 不替代 emergency services。
- 不诊断，不给治疗建议。
- 不虚构避难所容量、道路安全、交通可用性或冷却中心容量。
- 社交媒体和口头传言进入 rumor quarantine，必须等待官方渠道确认。
- 记忆系统不能自动修改高风险策略。
- 工具沙盒不能自动呼叫急救、预订避难所或执行真实外部操作。

## 验证结果

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Memory system | ready |
| Graph orchestration | ready |
| Writeup readiness | ready |
| Judging packet | ready |
| Final local gate | `ready_to_submit=true` |

## 关键产物

- `scripts/agentic_learning_loop.py`：学习侧车。
- `scripts/agent_memory_system.py`：长期记忆系统。
- `scripts/agent_graph_orchestrator.py`：LangGraph 兼容图式编排器。
- `outputs/local_validation/agent_memory_store.json`：长期记忆库。
- `outputs/local_validation/memory_retrieval_demo.json`：记忆检索演示。
- `outputs/local_validation/agent_graph_trace_demo.json`：图式执行轨迹。
- `knowledge_base/skill_library.json`：技能库。
- `resilience_copilot_submission_bundle_EXP029.zip`：评委专用最终包。

## 公开链接

- Public demo: https://huier5635-cmd.github.io/resilience-copilot-gemma4/
- Public code: https://github.com/huier5635-cmd/resilience-copilot-gemma4
- YouTube video: https://youtu.be/CmqCV8Ic9cY
- Kaggle Gemma 4 evidence notebook: https://www.kaggle.com/code/zhenhuier/notebook5022dfd167
- Submitted Kaggle writeup: https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423

## 本地复现

```powershell
python scripts\run_local_validation.py
```

只运行学习、记忆和图式编排：

```powershell
python scripts\agentic_learning_loop.py
python scripts\agent_memory_system.py
python scripts\agent_graph_orchestrator.py
```

可选 LangGraph 运行时：

```powershell
python -m pip install --target .deps\python -r requirements-agent-optional.txt
python scripts\agent_graph_orchestrator.py
```

如果安装了 `langgraph`，图式编排会走真实 `StateGraph`；如果没有安装，则使用项目内置确定性降级图执行器。
