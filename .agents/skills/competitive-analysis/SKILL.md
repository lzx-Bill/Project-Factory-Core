---
name: competitive-analysis
description: 'Use when conducting structured competitor or alternative solution research with standardized comparison frameworks. Trigger when user says "competitor analysis", "compare X to Y", "alternative solutions", "market comparison", "vs competitor", "替代方案对比", "竞品分析", or when user needs a formal comparison matrix with defined criteria. This is a specialized variant of research-spikes — use research-spikes for general exploration, use this skill when a structured comparison is the primary output.'
argument-hint: '竞品分析、替代方案对比、市场对比、vs对比、竞争分析'
---

# Competitive Analysis

用于结构化竞品和替代方案对比研究。

## When to Use

- 需要系统化对比多个竞品或替代方案
- 需要建立标准对比维度和评分体系
- 选型决策前需要结构化证据
- 用户明确要求"竞品分析报告"

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 竞品列表、对比维度、选型优先级 |
| 当前项目 | 项目需求、约束条件、成功标准（用于定义对比维度） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/02-research/market-notes.md` | 市场笔记 | 竞品对比矩阵、评分表 |

## Minimum Viable Output

- 含 ≥3 个竞品或替代方案
- 含 ≥4 个对比维度
- 含每个方案在各维度的定性评估

## Complete Output

- 完整的对比矩阵（定量 + 定性）
- 每个维度含权重和评分理由
- 含推荐方案和适用场景
- 含风险和限制
- 含参考资料来源

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `overview-framing`（了解项目定位，用于定义对比维度） |
| 后置 | `architecture-decisions`（竞品分析结论输入架构选型） |
| 并行 | `research-spikes`（共享调研方法） |
| 依赖读取 | vision.md（项目定位）、requirements.md（成功标准） |

## Procedure

1. 确认对比范围和竞品列表
2. 定义对比维度（基于项目成功标准和约束）
3. 收集每个方案在各维度的信息
4. 填写对比矩阵
5. 加权评分（如适用）
6. 给出推荐和适用场景
7. 标注信息来源和置信度
8. **增量写入**：如果 `market-notes.md` 已存在（由 research-spikes 等创建），读取现有内容，在末尾追加 `## 结构化对比` section，不覆盖已有笔记

## 与 research-spikes 的区别

| Skill | 关注点 | 输出形式 |
|-------|--------|----------|
| `research-spikes` | 调研和验证，可以是任意方向 | Spike 记录、研究笔记 |
| `competitive-analysis` | 结构化对比，标准化矩阵 | 对比矩阵、评分表 |

当用户明确要求"对比 A 和 B"或"竞品分析"时，使用本 skill。当用户要求"验证 X 技术可行性"时，使用 research-spikes。

## Target Pages

- `<项目根目录>/wiki/02-research/market-notes.md`（主，与 research-spikes 共享）

## 与 research-spikes 共享 market-notes.md 的协调规则

| 规则 | 说明 |
|------|------|
| 增量写入 | 所有 skill 都**增量追加**到 market-notes.md，不覆盖已有内容 |
| 章节标识 | competitive-analysis 写入以 `## 结构化对比` 为标题的 section |
| research-spikes | 以 `## 竞品笔记` 或 `## 调研发现` 为标题的 section |
| 冲突处理 | 如发现内容矛盾，标注 `⚠️ 待确认：与 xxx 的结论存在冲突`，不直接覆盖 |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 新建 skill | 填补 skill 集合中的结构化竞品分析空白，与 research-spikes 形成互补 |
