---
name: assumptions-tracking
description: 'Use when recording assumptions, open questions, unresolved dependencies, decision blockers, or items awaiting confirmation. Trigger when user says "assumption", "we assume", "unconfirmed", "open question", "blocker", "pending decision", "TBD", "depends on", or when a requirement or design decision cannot be finalized due to missing information. This skill should be used proactively — do not wait for the user to ask.'
argument-hint: '假设记录、开放问题、待确认项、阻塞依赖、TBD'
---

# Assumptions Tracking

用于显式记录未确认内容。

## When to Use

- 有判断还没被验证
- 有关键问题需要用户或后续实现确认
- 需要把阻塞项与依赖写清楚
- 在其他 skill 工作时发现依赖未确认的内容

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 提及的假设、问题、阻塞点 |
| 当前项目 | 所有已写的 wiki 页面（扫描其中标注的"未确认"内容） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/01-requirements/assumptions.md` | 假设清单 | ID + 假设 + 来源 + 影响范围 + 验证方式 + 状态 |
| `wiki/01-requirements/open-questions.md` | 开放问题 | ID + 问题 + 为什么重要 + 负责人 + 状态 |

## Minimum Viable Output

- assumptions.md 含 ≥1 条假设（即使项目刚开始）
- 每条假设含：假设内容、来源、影响范围
- open-questions.md 含 ≥1 条待确认问题

## Complete Output

- assumptions.md 每条含完整字段：验证方式、状态（待验证/已证实/已推翻）
- open-questions.md 每条含：为什么重要、负责人、确认截止建议
- 已按影响面和紧急度排序

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 无（可随时使用，即使项目刚开始） |
| 后置 | `research-spikes`（假设需要验证时）、`architecture-decisions`（假设影响架构时） |
| 依赖读取 | 所有其他 skill 的输出（从中提取未确认内容） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下记录假设与问题
2. 将"猜测"与"事实"分开
3. 每条假设写清来源、影响范围和验证方式
4. 每条问题写清为什么重要和当前负责人

## Enriched Behavior

- 不只记录"还不确定"，还要说明这些不确定性为什么会影响项目推进
- 可以主动把模糊需求、外部依赖、资源不足、技术未知数转化为结构化假设或开放问题
- 当问题较多时，优先按影响面和紧急度排序，帮助用户先看关键阻塞
- 输出要支持后续 research、risk、architecture 跟进，而不是只做备忘录

## Target Pages

- `<项目根目录>/wiki/01-requirements/assumptions.md`（主）
- `<项目根目录>/wiki/01-requirements/open-questions.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| assumptions.md | assumptions-tracking | 所有 skill（发现未确认内容时参与补充） |
| open-questions.md | assumptions-tracking | 所有 skill |

## 与 risk-register 的区别

| Skill | 关注点 | 标记对象 |
|-------|--------|---------|
| `assumptions-tracking` | 未经验证的猜测和前提 | "我们假设X"、"需要确认Y" |
| `risk-register` | 已识别的潜在威胁 | "如果Z发生，会导致..." |

> assumptions 是"还不确定的事"，risk 是"可能出错的事"。当假设被验证为"可能出问题"时，应转为 risk 登记。

### 假设状态机

```markdown
## 假设状态定义

| 状态 | 含义 | 后续动作 |
|------|------|---------|
| 待验证 | 初始状态，假设尚未验证 | 执行验证或等待外部确认 |
| 已证实 | 假设经验证成立 | 通知相关方，可关闭跟踪 |
| 已推翻 | 假设经验证不成立 | 通知相关方，需调整设计或计划 |
| 转风险 | 假设成立但存在负面风险 | 转入 risk-register |

## 假设状态转换规则

```
待验证 ──[验证: 成立且无显著风险]──→ 已证实
待验证 ──[验证: 不成立]────────────→ 已推翻
待验证 ──[验证: 成立但有负面影响]──→ 转风险 → risk-register
待验证 ──[长期无进展]─────────────→ 提升为 open-questions
```

### 开放问题状态机

```markdown
## 开放问题状态定义

| 状态 | 含义 | 后续动作 |
|------|------|---------|
| 待确认 | 初始状态，问题已提出但未分配 | 分配负责人，设置截止建议 |
| 确认中 | 正在与相关方确认 | 记录当前进展 |
| 已确认 | 问题已有明确答案 | 更新相关文档，关闭问题 |
| 已取消 | 问题不再相关或无法回答 | 记录原因，关闭跟踪 |

## 开放问题转换规则

```
待确认 ──[分配负责人]────────────→ 确认中
确认中 ──[获得明确答案]───────────→ 已确认
确认中 ──[问题不再相关]───────────→ 已取消
待确认 ──[长期无响应]─────────────→ 提升为 blocker，通知项目负责人
```


## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 增强：将"假设→风险转换规则"扩展为完整的假设状态机（待验证/已证实/已推翻/转风险）和开放问题状态机（待确认/确认中/已确认/已取消），含状态定义和转换规则 | 状态转换规则不完整，仅有假设→风险转换，缺少整体状态机定义 |
| 2026-04-29 | 新增假设→风险转换规则和示例 | 明确假设状态变化时的处理流程 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化主动使用意识 |
