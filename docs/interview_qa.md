# Interview Q&A

This file is written for summer-camp, interview, and research discussion preparation.

## 1. 这个项目和普通 prompt engineering 有什么区别？

普通 prompt engineering 主要调整输入提示词，让模型更好回答。本项目把安全规则、风险识别、工具核验、结构化输出、人工复核和审计追踪放在模型外部，用确定性模块约束模型，而不是只相信 prompt。

## 2. Safety sidecar 具体怎么实现？

Sidecar 是模型外的一组确定性检查：生成前检测风险信号并匹配 playbook，生成后检查十六段响应契约、JSON 字段、Audit Trace 和禁止声明，例如不能编造避难所容量或交通可用性。

## 3. 为什么需要 deterministic safety sidecar？

高风险场景不能只依赖概率模型自觉遵守规则。确定性 sidecar 的好处是可复现、可测试、可审计，失败时也能定位是哪条规则没覆盖。

## 4. 16-section response contract 是什么？

它是固定输出结构，包括 risk level、case signals、human review reason、playbook references、action plan、official resource checks、source verification、Transfer Brief、questions、language support、handoff、packet、household message、audit trace、case export 和 safety boundary。

## 5. Memory system 为什么有安全风险？

记忆可能把一次错误经验、谣言或过时资源信息带入未来决策。例如“某 shelter 有床位”的传言如果进入长期记忆，就可能被系统反复错误引用。

## 6. Protected safety invariants 怎么设计？

我把不可被 memory 自动修改的规则列为 protected invariants，例如不诊断、不编造容量、不替代 emergency services、不让未审核经验改写高风险策略。

## 7. Tool calling sandbox 做了什么？

当前是离线沙盒，只允许官方资源类别检查，例如 emergency management、shelter operations、medical triage、transport desk、language access line。它会阻断“beds available”“road is safe”等未核实声明。

## 8. Audit Trace 有什么作用？

Audit Trace 记录风险等级、触发信号、playbook、官方核验路径、人工复核原因和被阻断声明。它让老师或评审能追溯系统为什么这样输出。

## 9. 怎么评价安全性？

我使用本地 demo/holdout/stress 验证和 30 条自建 benchmark。指标包括契约通过率、不安全响应率、风险信号遗漏率、资源幻觉率、人工复核触发率、JSON 合法率和审计完整率。

## 10. Benchmark 怎么构造？

根据灾害救援常见风险手工构造：缺氧、胰岛素、儿童受冷、断电、洪水、交通不可达、语言障碍、宠物避难、谣言、容量未知和医疗连续性。文档明确它不是官方真实数据集。

## 11. 这个项目有没有真实数据？

比赛没有提供官方训练集，所以我使用自建场景 benchmark 和 stress cases 做安全工程验证。真实部署需要专家标注和官方数据合作。

## 12. Hallucination 怎么检测？

我重点检测高风险资源幻觉：避难所有床位、交通可用、道路安全、诊所开放等。如果没有官方核验，系统不能把这些说成事实。

## 13. Human review trigger 怎么设计？

高风险信号、医疗连续性、资源容量不确定、交通安全、语言支持等都会触发人工复核。系统只做 responder handoff，不做最终调度决策。

## 14. 和 RAG 的关系是什么？

RAG 主要是检索外部知识帮助回答。本项目也有检索思想，但核心不是知识问答，而是安全约束、资源核验、人工复核和审计。

## 15. 和普通聊天机器人有什么区别？

普通聊天机器人直接给用户回答；本系统输出的是可复核的救援交接材料，强调未知项、官方核验、禁止声明和人工复核。

## 16. 和大模型 Agent 有什么关系？

它是安全边界内的 agent prototype：有任务流程、工具沙盒、记忆、策略反思和输出检查，但不是无限制 autonomous agent。

## 17. 项目的科研问题在哪里？

核心科研问题是高风险 LLM Agent 如何保持可控、可审计和抗记忆污染，特别是如何组合 deterministic rules、memory gate、tool sandbox 和 human-in-the-loop。

## 18. 项目的工程难点在哪里？

难点是让 demo、评测、结构化输出、审计字段、静态页面和文档都保持一致，同时不破坏已有 Kaggle 验证门禁。

## 19. 失败 case 有哪些？

早期风险主要是语言不够结构化、资源核验不够明确、容易让评审误以为系统能实时查容量。现在通过 source verification、safety boundary 和 benchmark 显式约束。

## 20. 如果模型输出冲突怎么办？

以后处理以 deterministic safety sidecar 为准。如果模型说“有床位”，但资源核验没有官方确认，post-check 会把它当作 unsupported claim。

## 21. 如何防止 memory 污染？

运行时经验默认 quarantine；只有通过验证或人工审核的反馈才能进入长期记忆；即便进入长期记忆，也只能辅助检索，不能改写 protected invariants。

## 22. 如何扩展到机器人或应急调度场景？

可以把 responder handoff 接入调度系统或机器人任务规划，但必须保留安全契约、工具白名单、人工确认和审计日志，不能让模型直接执行高风险动作。

## 23. 如何扩展到多 Agent？

可以拆成 planner、risk specialist、resource verifier、memory reviewer 和 safety checker。但 coordinator 必须受 safety sidecar 控制，不能让 agent 互相放大错误。

## 24. 如何做更严格的评测？

需要专家标注数据、更大规模 stress suite、对抗性谣言注入、跨地区资源表达、跨模型对比，以及人工评审一致性分析。

## 25. 为什么选择 Gemma？

比赛主题要求使用 Gemma 4。项目中 Gemma 4 负责 responder-facing phrasing，安全控制放在模型外部，因此框架可迁移。

## 26. 如果换成 GPT/Qwen/DeepSeek 是否能迁移？

可以。模型接口只影响语言生成层，risk detection、playbook、safety contract、tool sandbox、memory policy 和 audit trace 都可以保留。

## 27. 当前系统最大局限是什么？

最大局限是数据和工具都还停留在原型：benchmark 是自建的，官方资源核验是离线沙盒，不能直接代表真实救援部署效果。

## 28. 你本人在项目中做了什么？

我完成了项目结构、风险规则、playbook grounding、安全契约、本地验证、public demo、Kaggle 证据、memory gate、benchmark、测试和面向展示的文档整理。

## 29. 这个项目如何体现计算机能力？

它覆盖软件工程、规则系统、Agent 架构、测试评测、JSON 数据建模、前端 demo、自动化验证、文档复现和可信 AI 安全设计。

## 30. 后续如果做研究，最想深入哪个问题？

我最想研究高风险 LLM Agent 的 memory pollution 和 policy drift：系统如何从经验中学习，同时保证安全边界不被未审核记忆污染。

