---
name: home-navigation
description: 'Use when updating or writing HOME.md in Project Factory. Trigger when user mentions "update HOME", "home page", "navigation", "project status", "current phase", "next step", "summary", "decision summary", or "risk summary". This skill owns the HOME.md as its single responsibility — do not delegate to other skills.'
argument-hint: 'HOME页更新、导航、当前状态、阶段、摘要、决策风险'
---

# Home Navigation

用于维护 `HOME.md` 作为项目单一导航入口。

## When to Use

- 需要更新首页状态或导航
- 需要补当前阶段、当前目标、下一步
- 需要汇总最新决策和风险摘要
- 项目进入新阶段（如：完成需求、进入架构设计）

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 更新指令、阶段变化、决策摘要、风险变化 |
| 当前项目 | 现有的 HOME.md 内容、各 wiki 页面的最新状态 |

## Output Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| 一句话定义 | 文本 | 项目核心定位，≤50字 |
| 当前状态 | 结构化 | 阶段 + 当前目标 + 下一步 |
| 导航链接 | 链接列表 | 各维度 wiki 页面的相对路径链接 |
| 最新决策摘要 | 表格 | 日期 + 决策 + 影响 |
| 当前风险摘要 | 表格 | ID + 风险 + 状态 + 下一步 |
| 当前重点 | 列表 | 本周最重要的 3 件事 |

## Minimum Viable Output

- 一句话定义 + 当前阶段 + 下一步存在
- 导航链接至少覆盖 wiki/00-overview、wiki/01-requirements、wiki/03-architecture

## Complete Output

- 上述全部字段均有内容
- 决策摘要和风险摘要已更新到最新
- 当前重点 ≥1 条

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `project-bootstrap`（初始 HOME 建立） |
| 后置 | 无（HOME 是所有 skill 的交汇点） |
| 依赖读取 | 所有已更新的 wiki 页面（取最新摘要） |

## Procedure

1. 确认当前维护的是哪个 `<项目根目录>/HOME.md`
2. 首页只写摘要和导航，详细内容回链到同一项目目录下的 wiki 页面
3. 决策和风险只保留最新摘要，不堆长文
4. 优先让用户在 30 秒内看懂项目当前状态、下一步和风险

## Enriched Behavior

- 优先让用户在 30 秒内看懂项目当前状态、下一步和风险，而不是把首页写成目录清单
- 对新增内容进行摘要提炼，把长文信息压缩成首页可消费的关键信号
- 当多个维度同时更新时，优先反映阶段变化、关键决策变化、风险变化和下一步变化
- 可以根据项目阶段调整首页重点，不要求每次都平均铺开所有板块

## Target Pages

- `<项目根目录>/HOME.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 增强：独立为专属 skill，新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、Changelog | 解决粒度过薄问题，明确单一职责，提升触发准确性 |
