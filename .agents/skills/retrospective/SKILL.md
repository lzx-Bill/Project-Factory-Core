---
name: retrospective
description: 'Use when conducting project phase retrospectives, lessons learned sessions, or after implementation feedback reveals recurring issues. Trigger when user says "project retro", "lessons learned", "what went well", "what could be better", "project review", "phase review", "post-mortem", "项目复盘", "阶段回顾", "经验总结", or when a project phase completes. NOT for Copilot Chat session analysis — use copilot-session-retro for that.'
argument-hint: '项目阶段复盘、经验教训、做得好的、可以改进的、post-mortem'
---

# Retrospective

用于项目阶段复盘和经验总结。

## When to Use

- 项目某个阶段完成，需要做复盘
- 实现反馈揭示了反复出现的问题
- 用户要求回顾"做得好的"和"可以改进的"
- 项目遇到重大挫折需要总结
- 里程碑达成或未达成后的回顾

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 复盘范围（全部还是某个维度）、参与者反馈 |
| 当前项目 | 所有已完成阶段的相关文档、受影响 wiki 页面 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/08-history/decision-log.md` | 决策回顾 | 决策效果评估、是否需要回滚 |
| `wiki/06-quality/known-gaps.md` | 缺口追踪 | 本次复盘发现的新缺口 |
| `HOME.md` | 状态更新 | 如复盘影响项目方向则更新首页 |
| `reports/stage-review/R-NNN.md` | 复盘报告 | 结构化复盘记录 |

## Minimum Viable Output

- 含做得好的 ≥2 条
- 含可以改进的 ≥2 条
- 含下次避免问题的具体行动 ≥2 条

## Complete Output

- 完整 4 象限分析：做得好的/可以改进的/问题根因/行动项
- 含量化指标（时间偏差、返工次数等）
- 含对后续阶段的具体建议
- 含决策回顾（之前的决策效果如何）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 项目有实际执行记录（任务、Prompt 执行结果等） |
| 后置 | `history-sync`（复盘结论同步到历史）、`home-navigation`（首页状态更新） |
| 依赖读取 | tasks/done.md、reports/acceptance/*.json、HOME.md |

## Procedure

1. 确认复盘范围（全部/某个维度/某次迭代）
2. 收集事实：任务完成情况、返工次数、时间偏差、反馈
3. 分析根因：区分"做得好的"和"问题"
4. 形成行动项：具体、可执行、有负责人
5. 更新已知缺口（known-gaps.md）
6. 同步到历史记录和首页

### 4 象限分析模板

```markdown
# 复盘报告: <阶段名称> — <日期>

## 做得好的 ✅

| # | 事项 | 根因分析 |
|---|------|---------|
| 1 | ... | 因为... |
| 2 | ... | 因为... |

## 可以改进的 🔧

| # | 事项 | 根因分析 |
|---|------|---------|
| 1 | ... | 因为... |
| 2 | ... | 因为... |

## 问题根因 🔴

| # | 问题 | 根因 | 影响 |
|---|------|------|------|
| 1 | ... | ... | ... |

## 行动项 📋

| # | 行动 | 负责人 | 截止日期 | 状态 |
|---|------|--------|---------|------|
| 1 | ... | ... | ... | 待启动 |
```

**复盘报告保存到**: `reports/stage-review/R-NNN.md`

## Enriched Behavior

- 不只做感性的"好/不好"总结，要找根因和模式
- 可以主动发现反复出现的问题，提出系统性改进建议
- 行动项要具体可执行，不是"多沟通"这种无效建议
- 区分个人问题 vs 系统问题，系统问题优先解决

## Target Pages

- `<项目根目录>/wiki/06-quality/known-gaps.md`（主）
- `<项目根目录>/wiki/08-history/decision-log.md`（决策回顾）
- `<项目根目录>/reports/reviews/`（复盘报告目录）
- `<项目根目录>/HOME.md`（状态更新）

## 与相近 skill 的区别

| Skill | 关注点 | 时机 | 触发关键词 |
|-------|--------|------|-----------|
| `history-sync` | 变更追踪、决策记录、文档归档 | 任何变更发生时 | 变更日志、决策日志、归档 |
| `copilot-session-retro` | Copilot Chat session 协作分析 | session 结束后 | session review、session复盘、对话复盘 |
| `retrospective` | 项目阶段复盘、经验总结、行动改进 | 项目阶段完成或重大事件后 | 项目复盘、阶段回顾、经验教训 |

> **区分原则**：Copilot 对话复盘 → `copilot-session-retro`；项目阶段复盘 → `retrospective`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：输出路径从 reports/reviews/ 改为 reports/stage-review/（与 express-incubate 结构对齐） | 路径与实际不符 |
| 2026-04-29 | 新增 4 象限分析模板（做得好的/可以改进的/问题根因/行动项） | Procedure 缺少格式定义 |
| 2026-04-26 | 新建 skill | 填补 skill 集合中的复盘空白，完善项目闭环 |
