---
name: risk-register
description: 'Use when identifying, updating, prioritizing, or mitigating delivery risks, product risks, technical risks, and operational risks. Trigger when user says "risk", "mitigation", "contingency", "what could go wrong", "blocker", or when new information reveals a potential problem. Also use proactively after research spikes or architecture decisions that have open questions — risks should be logged before they become blockers.'
argument-hint: '风险识别、风险登记、缓解策略、触发条件、应急预案'
---

# Risk Register

用于风险识别和风险管理。

## When to Use

- 需要补风险清单
- 需要更新风险状态或缓解方案
- 需要把研究或实现发现的问题转成风险项
- 在其他 skill 工作时发现潜在风险

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 提及的风险、担忧、潜在问题 |
| 当前项目 | 所有 wiki 页面（扫描未完成项、依赖不稳项、外部依赖） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/02-research/risk-register.md` | 风险登记 | ID + 风险 + 概率 + 影响 + 状态 + 触发条件 + 应对策略 |

## Minimum Viable Output

- risk-register.md 含 ≥1 条风险
- 每条含：风险描述、概率（高/中/低）、影响（高/中/低）、触发条件

### 风险量化标准

| 维度 | 🔴 高 | 🟡 中 | 🟢 低 |
|------|-------|-------|-------|
| **概率** | 项目生命周期内很可能发生（>60%） | 有可能发生（20%-60%） | 不太可能发生（<20%） |
| **影响** | 造成项目目标无法达成、严重数据损失或合规违规 | 造成显著延迟、质量下降或用户体验受损 | 影响有限，可快速恢复，不影响核心目标 |

### 风险优先级矩阵

| 概率 × 影响 | 优先级 | 处理策略 |
|-------------|--------|---------|
| 🔴高 × 🔴高 | **P0**：立即处理 | 必须有缓解方案和应急预案 |
| 🔴高 × 🟡中 | **P1**：优先处理 | 2 周内有缓解方案 |
| 🟡中 × 🔴中 | **P1**：优先处理 | 2 周内有缓解方案 |
| 🟡中 × 🟡中 | **P2**：持续关注 | 纳入迭代计划 |
| 🔴低 × 🔴高 | **P1**：观察并准备预案 | 确保有应急预案 |
| 其他组合 | **P3**：低优先级 | 记录并监控 |

## Complete Output

- 覆盖产品、技术、交付、运营四类风险
- 每条含：缓解动作、应急预案、负责人、下一步
- 已关闭风险含结论与经验

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `requirements-spec`（需求不清是风险源）、`research-spikes`（技术未验证是风险源） |
| 后置 | `delivery-planning`（高风险任务优先拆出）、`operations-planning`（运营风险输入运维规划） |
| 依赖读取 | 所有 wiki 页面（从中识别风险信号） |

## Procedure

1. 先确认目标项目根目录，并只更新该项目目录下的风险登记
2. 风险必须写清触发条件和影响
3. 区分已发生问题与潜在风险
4. 明确下一步缓解动作和负责人

## Enriched Behavior

- 不只罗列风险名词，要帮助用户判断哪些风险最值得现在处理
- 可以主动把需求不清、研究未完成、依赖不稳、资源不足等信号转写为风险项
- 高风险事项优先写清触发条件、预警信号、缓解动作和兜底方案
- 对首页摘要只保留高价值信号，详细细节沉淀到风险页

## Target Pages

- `<项目根目录>/wiki/02-research/risk-register.md`（主）
- `<项目根目录>/HOME.md`（风险摘要回写）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| risk-register.md | risk-register | 所有 skill（识别到风险时参与补充） |
| HOME.md 风险摘要 | risk-register | home-navigation（负责更新格式） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：新增风险量化标准表（概率/影响的高/中/低定义）；新增风险优先级矩阵（P0-P3 划分及对应处理策略） | 概率/影响无量化标准，风险优先级判定无依据 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化风险识别的主动性 |
