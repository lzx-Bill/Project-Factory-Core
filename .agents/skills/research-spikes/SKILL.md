---
name: research-spikes
description: 'Use when doing competitor analysis, feasibility analysis, technical spikes, benchmarking, option comparison, or evidence gathering. Trigger when user says "research", "spike", "feasibility", "competitor analysis", "benchmark", "compare options", "technical evaluation", "does X work for Y", or asks "should we use A or B". Also use proactively when architecture decisions depend on unverified technical assumptions.'
argument-hint: '技术调研、Spike、可行性分析、竞品对比、benchmark、方案评估'
---

# Research Spikes

用于调研和技术验证。

## When to Use

- 需要做竞品或参考方案调研
- 需要做小实验验证技术可行性
- 需要为方案选择收集证据
- 架构决策前需要验证技术假设

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 研究问题、技术选型困惑、竞品名称 |
| 当前项目 | architecture.md（如有候选方案）、assumptions.md（技术假设） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/02-research/market-notes.md` | 市场/竞品笔记 | 竞品对比、差异化机会、市场洞察 |
| `wiki/02-research/technical-spikes.md` | 技术验证 | Spike 记录：背景 + 方法 + 结果 + 结论 |

## Minimum Viable Output

- technical-spikes.md 含 ≥1 个 Spike，含背景、方法、结论
- market-notes.md 含 ≥3 个竞品或参考方案的对比要点

## Complete Output

- technical-spikes.md：每个 Spike 含置信度（高/中/低）、适用边界、下一步验证计划
- market-notes.md：完整的竞品矩阵、优缺点对比、差异化机会
- 含对 architecture-decisions 的直接推荐

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `assumptions-tracking`（识别需要验证的技术假设） |
| 后置 | `architecture-decisions`（研究结论输入架构）、`risk-register`（研究发现的风险） |
| 并行 | 无 |

## Procedure

1. 先确认目标项目根目录，并将调研与验证结果写入该项目目录
2. 优先找仓库内事实，再补外部证据
3. 对每个结论标注置信度
4. 输出时带上下一步验证动作

## Enriched Behavior

- 不只给结论，还要给证据来源、适用边界、未覆盖部分和下一步建议
- 可以并行展开竞品、技术可行性、实现成本、团队适配度等多个方向，只要最终有结构化沉淀
- 当外部信息不足时，可以先形成验证计划和假设，不必因为缺少完美证据而停住
- 输出应该帮助用户做取舍，而不是堆砌资料摘录

## Target Pages

- `<项目根目录>/wiki/02-research/market-notes.md`（主）
- `<项目根目录>/wiki/02-research/technical-spikes.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| market-notes.md | research-spikes | overview-framing（市场洞察） |
| technical-spikes.md | research-spikes | architecture-decisions（技术选型输入） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化 Spike 的结构化输出要求 |
