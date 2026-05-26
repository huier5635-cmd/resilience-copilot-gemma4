# Resilience Copilot 中文说明

[English README](../README.md)

Resilience Copilot 是一个面向高风险人工复核场景的安全边界智能体。当前展示场景是灾害救援分诊：它把志愿者收到的混乱求助记录，转成更安全、可审计、可交接的下一步行动建议。

![Resilience Copilot demo preview](../resilience_copilot_demo_preview.png)

## 快速链接

| 内容 | 链接 |
| --- | --- |
| 在线 Demo | https://huier5635-cmd.github.io/resilience-copilot-gemma4/ |
| 架构说明 | [architecture.md](architecture.md) |
| 示例案例 | [examples.md](examples.md) |
| 复用指南 | [adaptation_guide.md](adaptation_guide.md) |
| 路线图 | [roadmap.md](roadmap.md) |
| Kaggle Writeup | https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778665719423 |

## 核心方法

```text
Case Note
  -> Risk Signal Detector
  -> Playbook Matcher
  -> Gemma 4 Response
  -> Safety Contract Checker
  -> Transfer Brief + Audit Trace + JSON Export
```

系统使用 Gemma 4 生成面向救援人员的自然语言响应，同时用确定性安全侧车做风险识别、行动手册约束、官方资源核验、16 段响应契约、Transfer Brief、Audit Trace 和结构化 JSON 导出。

## Agent 能力边界

当前版本是 safety-bounded learning agent：它有经验账本、验证反馈记忆、长期记忆、策略反思、技能库和工具沙盒，但策略升级必须人工复核。

它不是无限制自主智能体：

- 不替代 emergency services。
- 不做医疗诊断。
- 不承诺避难所容量、交通可用性或道路安全。
- 不把社交媒体传言当作已核实事实。
- 不自动联系机构或执行真实外部操作。

## 验证结果

| Gate | Result |
| --- | --- |
| Demo cases | 2/2 |
| Holdout cases | 2/2 |
| Stress cases | 15/15 |
| Local gate | `ready_to_submit=true` |

验证证据已在 Kaggle Writeup 和 Gemma 4 evidence notebook 中汇总。公开仓库只保留给评委、老师和面试官看的 Demo 与说明页面。

## 适合复用的场景

这个项目适合迁移到“模型可以辅助生成，但最终责任必须由人承担”的场景，例如校园安全、养老热线、公益救助、政务工单、保险理赔初筛和合规客服。
