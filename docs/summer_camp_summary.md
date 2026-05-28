# 面向高风险场景的大模型安全智能体系统

本项目源于 Kaggle Gemma 4 Good Hackathon，后续被整理为一个面向可信 AI 与大模型智能体安全的工程研究项目。项目关注灾害救援场景中的 case note 处理：志愿者接收到的信息往往混乱、缺失且包含不确定传言，例如老人氧气设备断电、胰岛素保存风险、儿童受冷、避难所容量未知、交通不可达和语言障碍。普通聊天机器人可以生成流畅回答，但在高风险任务中，更重要的是保证回答可控、可复核、可审计。

我的工作是构建 Resilience Copilot，一个 safety-bounded LLM agent 原型。系统采用“LLM 生成 + 确定性安全侧车”的架构：先进行风险信号识别和 playbook 匹配，再让 Gemma 4 或本地 fallback 生成面向救援人员的自然语言响应，随后执行 safety contract checking、official resource verification、human review trigger、structured JSON export 和 Audit Trace。系统显式禁止医疗诊断、编造避难所容量、编造交通可用性和替代应急服务。

为提升可复现性，我保留了 Kaggle 本地验证闭环，并新增 30 条自建 benchmark，覆盖缺氧、断电、洪水、药物连续性、语言支持、宠物避难、谣言隔离等场景；评测指标包括契约通过率、不安全响应率、风险信号遗漏率、资源幻觉率、人工复核触发率、JSON 合法率和审计追踪完整率。同时设计了 bounded long-term memory 与 Memory Write Gate：未经人工审核的经验只能进入隔离区，不能修改 protected safety invariants，从而降低 memory pollution 风险。

该项目体现了我对大模型 Agent 系统、安全工程、可复现评测和复杂任务规划的综合训练。未来希望继续研究高风险场景中 LLM Agent 的工具调用边界、长期记忆污染、策略漂移和人机协同评测方法。
