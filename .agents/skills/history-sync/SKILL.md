---
name: history-sync
description: 'Use when updating changelogs, decision logs, archives, document history, or writing back requirement, research, architecture, prompt, acceptance, and task changes. Trigger when "implementation feedback" reveals a design gap, when "research结论" contradicts earlier assumptions, when "design changes" affect downstream docs, or when user asks to "update history", "log decision", "archive old version". This skill should be used proactively — do not let design changes go unlogged.'
argument-hint: '历史记录、变更日志、决策日志、归档、回写同步'
---

# History Sync

用于回写和历史留痕。

## When to Use

- 实现推翻了前期研究或设计
- 需要更新变更日志或决策日志
- 需要归档旧内容并保持当前文档清晰
- 设计变更后需要同步下游文档

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 变更内容、变更原因、影响范围 |
| 当前项目 | 所有受影响的 wiki/prompts/acceptance/tasks 页面 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/08-history/changelog.md` | 变更日志 | 日期 + 变更内容 + 原因 + 影响文档 |
| `wiki/08-history/decision-log.md` | 决策日志 | 决策 + 背景 + 结论 + 影响 |
| `wiki/08-history/archive/` | 归档目录 | 被替代的旧版本文档 |
| `HOME.md` | 首页更新 | 决策摘要同步更新 |

## Minimum Viable Output

- changelog.md 含 ≥1 条变更记录（含日期、变更内容、变更原因、影响文档）
- decision-log.md 含 ≥1 条决策记录（含决策、背景、结论）
- archive/ 含被替代文档的旧版本（按日期归档）
- 受影响文档已同步更新

## Complete Output

- changelog.md：完整变更链，含变更原因和影响分析
- decision-log.md：每条含决策背景、选项、被否方案
- archive/：含被替代文档的完整旧版本
- 含对 tasks/ 和 reports/ 的同步通知

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 无（变更随时可能发生） |
| 后置 | `home-navigation`（首页决策摘要同步） |
| 依赖读取 | 所有受影响的 wiki 页面（确定影响范围） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下回写与归档
2. 先更新当前有效文档
3. 再记录变更原因和影响范围
4. 归档旧版本，不继续堆 v2/v3 大文件

### archive/ 目录结构规范

```
archive/
├── YYYY-MM-DD/           # 按变更日期分目录
│   ├── wiki-原文件名-v原版本.旧.md   # 被替代的 wiki 文档
│   ├── prompts-原文件名-v原版本.旧.md
│   └── 其他文档类型
├── changelog-YYYY-MM-DD-备份.md    # 同步备份 changelog
└── README.md            # 归档索引（包含文件清单和归档原因）
```

> 每变更一次最多新建一个日期目录，避免目录膨胀

## Enriched Behavior

- 不只记流水账，要帮助用户理解"为什么变了、影响了哪里、下一步要同步什么"
- 可以主动联动 HOME、tasks、reports 和 wiki 对受影响部分做同步提醒
- 当实现推翻前期假设时，优先写清决策变化与影响，而不是只留一句"已更新"
- 输出既要保留历史，也要让当前有效内容保持清晰可用

## Target Pages

- `<项目根目录>/wiki/08-history/changelog.md`（主）
- `<项目根目录>/wiki/08-history/decision-log.md`（主）
- `<项目根目录>/wiki/08-history/archive/`（归档目录）
- `<项目根目录>/HOME.md`（决策摘要回写）
- `<项目根目录>/tasks/`（任务状态同步）
- `<项目根目录>/reports/`（报告归档）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| changelog.md | history-sync | 所有 skill（变更时参与补充） |
| decision-log.md | history-sync | 所有 skill（决策时参与补充） |
| archive/ | history-sync | - |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：MVO 变更记录新增"变更原因"字段；新增 archive/ 目录结构规范（按日期分目录、文件名格式、归档索引） | MVO 缺少变更原因、archive 目录结构未定义 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化变更追踪的主动性 |
