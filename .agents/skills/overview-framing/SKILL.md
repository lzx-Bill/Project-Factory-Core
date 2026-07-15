---
name: overview-framing
description: 'Use when defining project vision, problem statement, target users, scope boundaries, glossary, non-goals, or success criteria. Trigger when user says "vision", "define scope", "target users", "non-goals", "success metrics", "glossary", or asks to clarify what the project is and is not. This skill primarily owns wiki/00-overview/ — coordinate with incubation-discovery if ideas are still fuzzy.'
argument-hint: '愿景定义、问题陈述、目标用户、范围边界、术语表、非目标、成功标准'
---

# Overview Framing

用于定义项目的全局问题域和边界。

## When to Use

- 需要写项目愿景和范围
- 需要定义目标用户、术语、非目标
- 需要明确成功标准和边界条件
- 项目从发散阶段进入收敛，需要明确定位

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 项目想法、已确认的边界、用户类型 |
| 当前项目 | idea-landscape.md（如已发散）、assumptions.md（如有初始假设） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/00-overview/vision.md` | 愿景页 | 问题、用户、价值、非目标、成功标准 |
| `wiki/00-overview/scope.md` | 范围页 | 范围内/外、MVP边界 |
| `wiki/00-overview/glossary.md` | 术语页 | 关键术语定义，≥3条 |

## Minimum Viable Output

- vision.md 含：问题陈述、目标用户、核心价值、≥3条非目标
- scope.md 含：范围内/外清单
- glossary.md 含：≥3 条术语定义

## Complete Output

- vision.md 全部字段饱满，非目标 ≥3 条
- scope.md 含 MVP 与未来迭代的边界描述
- glossary.md 覆盖所有可能混淆的概念
- 可选：scenario-matrix.md（场景地图）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `incubation-discovery`（建议但非必须，如想法已收敛可直接使用） |
| 后置 | `requirements-spec`（愿景确定后进入需求）、`architecture-decisions`（范围确定后进入架构） |
| 并行 | `assumptions-tracking`（并行记录约束和假设） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下写概览文档
2. 先写问题、用户、价值
3. 明确范围内与范围外
4. 把易混淆概念沉淀为术语表

## Enriched Behavior

- 不只回答"这是个什么项目"，还要帮助用户看清为什么值得做、边界在哪里、怎么避免跑偏
- 可以主动补充相邻维度，例如成功标准、非目标、边界条件，只要仍然服务于项目定位
- 当用户想法跨度很大时，优先把不同方向拆开描述，而不是混成一个含糊的大目标
- 输出应帮助后续需求、调研、架构继续展开，而不是停留在宣传语层面

## Target Pages

- `<项目根目录>/wiki/00-overview/vision.md`（主）
- `<项目根目录>/wiki/00-overview/scope.md`（主）
- `<项目根目录>/wiki/00-overview/glossary.md`（主）
- `<项目根目录>/wiki/00-overview/scenario-matrix.md`（辅，可选）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| vision.md | overview-framing | incubation-discovery |
| scope.md | overview-framing | - |
| glossary.md | overview-framing | 所有涉及术语的 skill |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：MVO 非目标数量 ≥1→≥3，与 Complete Output 保持一致 | 非目标数量前后矛盾 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，明确主/辅归属 |
