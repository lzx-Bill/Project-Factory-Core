---
name: prompt-authoring
description: 'Use when writing structured implementation prompts, packaging context for AI coding, mapping prompts to tasks, or refining prompt granularity. Trigger when user says "write a prompt", "implementation prompt", "handover prompt", "context packaging", "task prompt", "decompose into prompts", or when moving from delivery-planning to actual prompt generation. The output goes into prompts/ directory. Coordinate with data-api-design for API consistency and with acceptance-design for prompt-to-acceptance mapping.'
argument-hint: 'Prompt编写、上下文打包、任务映射、粒度调整、下游交接'
---

# Prompt Authoring

用于编写可直接执行的 AI 实现 Prompt。

## When to Use

- 需要从任务生成 Prompt 文件
- 需要调整 Prompt 粒度和上下文完整性
- 需要保证 Prompt 与任务和验收一致
- 设计阶段完成，需要生成可交付给下游的 Prompt

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 任务描述、粒度要求、上下文需求 |
| 当前项目 | task-breakdown.md（任务清单）、data-api.md（如涉及API）、architecture.md |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `prompts/README.md` | Prompt 索引 | Prompt ID + 名称 + 对应任务 + 对应验收 |
| `prompts/P-NNN.md` | 单个 Prompt | 任务ID + 输入上下文 + 输出要求 + 约束 |

## Minimum Viable Output

- prompts/README.md 含 ≥1 个 Prompt 条目
- 每个 Prompt 含：任务ID、输入上下文、预期输出、文件范围

## Complete Output

- prompts/README.md：完整索引，含所有 Prompt 状态（draft/ready/deprecated）
- 每个 Prompt 文件：完整含技术约束、错误处理、验收映射、回写要求
- 含上下文打包指南（如何组装所需背景信息）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `delivery-planning`（任务已拆解）、`data-api-design`（API 契约已定） |
| 后置 | `acceptance-design`（Prompt 完成后设计验收） |
| 依赖读取 | task-breakdown.md、data-api.md、architecture.md |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下产出 Prompt
2. 一个 Prompt 对应一个完整但不过大的任务单元
3. 输入上下文必须自包含
4. 如果发现设计缺口，先回写同一项目目录下的 wiki，再继续写 Prompt

## Enriched Behavior

- 不只写一句需求说明，要提供足够上下文，让后续 AI 可以少猜测、少返工
- 可以主动补充输入、输出、依赖、文件范围、技术约束、验收映射和回写要求
- 当一个任务过大时，优先拆 Prompt，而不是把所有要求硬塞进一个文件
- Prompt 应兼顾执行效率和可验证性，不追求华丽表达

## Target Pages

- `<项目根目录>/prompts/README.md`（主）
- `<项目根目录>/prompts/`（Prompt 文件目录）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| prompts/README.md | prompt-authoring | delivery-planning（提供任务清单） |
| prompts/*.md | prompt-authoring | acceptance-design（映射到验收）、data-api-design（API 契约） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化 Prompt 与任务/验收的映射关系 |
