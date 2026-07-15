---
name: execution-log
description: 'Use when recording pipeline execution trace for auditability and retrospection — "log execution", "record step", "execution trace", "执行日志", "过程记录". This skill records every stage start/end, inputs, outputs, review results, decisions, and questions asked. Produces a structured execution log that can be read by retrospective or reviewed manually.'
argument-hint: '执行日志、过程记录、管线追踪、可追溯、可复盘'
---

# Execution Log

管线执行追踪。记录每一步的输入、输出、决策、评审结果，形成可追溯的执行日志。

## 定位

| 维度 | 说明 |
|------|------|
| 目标 | 让任何管线执行都可复盘（谁做了什么、结果如何） |
| 调用方 | express-incubate（每阶段前后调用）、渐进链路（每个 skill 执行前后） |
| 输出 | 结构化 JSON 日志 + 人类可读 Markdown 摘要 |
| 与 history-sync 区别 | history-sync 记设计变更；execution-log 记执行过程 |

## When to Use

- 管线开始执行时：`execution-log start --pipeline=express-incubate --project=xxx`
- 每阶段开始前：`execution-log stage-start --stage=bootstrap`
- 每阶段结束后：`execution-log stage-end --result=pass --review=<report-path>`
- 管线结束时：`execution-log end`
- 用户想查看执行历史：`execution-log show --pipeline=<name>`

## Input

| 来源 | 内容 |
|------|------|
| 调用上下文 | pipeline 名称、阶段名称、项目名称 |
| 阶段产出 | 输入文件列表、输出文件列表 |
| 评审报告 | stage-review 产出的 JSON 报告路径 |

## Output

### 日志结构

```
reports/execution/<pipeline>-<timestamp>/
├── log.json           # 结构化执行日志
├── summary.md         # 人类可读摘要（每阶段产出+评审+决策）
└── per-stage/
    ├── 01-bootstrap.md
    ├── 02-incubation.md
    └── ...
```

### log.json 结构

```json
{
  "pipeline": "express-incubate",
  "project": "发票管理工具",
  "started_at": "2026-04-26T22:00:00",
  "ended_at": "2026-04-26T22:05:00",
  "stages": [
    {
      "order": 1,
      "name": "bootstrap",
      "status": "completed",
      "started_at": "...",
      "ended_at": "...",
      "inputs": [],
      "outputs": ["HOME.md"],
      "review": {
        "result": "PASS",
        "report": "reports/stage-review/bootstrap-20260426-220000.json"
      },
      "assumptions_made": ["A-001: 目标用户为独立自由职业者"],
      "decisions": [],
      "questions_asked": [],
      "auto_fixes": []
    }
  ],
  "total_assumptions": 15,
  "total_questions_asked": 2,
  "total_auto_fixes": 4
}
```

### summary.md 结构

```markdown
# 管线执行摘要: express-incubate

- 项目: 发票管理工具
- 执行时间: 2026-04-26 22:00 - 22:05
- 总阶段: 6

## 阶段执行

| 阶段 | 状态 | 评审 | 假设 | 提问 | 修正 |
|------|------|------|------|------|------|
| ① bootstrap | ✓ | PASS | 1 | 0 | 0 |
| ② incubation | ✓ | PASS | 3 | 1 | 1 |
...

## 关键决策
- 🔴 平台: Web-only (用户确认)
- 🟡 数据库: SQLite (AI自选)

## 待用户确认
- Q1: 是否需要移动端？→ 用户回复: 不需要
- Q2: 是否需要多用户？→ 待回复
```

## Procedure

### 管线生命周期

```
start → [stage-start → stage-end] × N → end
```

### start（幂等）

1. **检查是否已存在执行记录**：
   - 检查 `reports/execution/<pipeline>-*/` 目录是否存在
   - 如果存在且包含 log.json → 读取现有记录作为基准（支持断点续传）
   - 如果存在但无 log.json → 创建新目录（覆盖空目录）

2. 创建或更新 `reports/execution/<pipeline>-<timestamp>/` 目录
3. 记录 pipeline 名称、项目名称、启动时间（追加而非覆盖已有记录）

### stage-start

1. 记录阶段名称、开始时间、输入文件列表
2. **幂等检查**：如果阶段已在 log.json 中存在，跳过（不重复记录）

### stage-end

1. 记录阶段结束时间、产出文件列表
2. 记录评审结果（引用 stage-review 报告路径）
3. 记录本阶段产生的假设、决策、提问、自动修正
4. **立即写入**：每阶段结束后立即更新 log.json（不等到 pipeline-end 才写入）
5. **Checkpoint 写入**：同时写入 `checkpoints/stage-{N}.json` 供断点续传使用

### end

1. 汇总所有阶段数据到 log.json
2. 生成 summary.md
3. 更新 HOME.md 的执行状态
4. **幂等检查**：如果 summary.md 已存在，比较内容后决定是否覆盖

---

## 幂等性与断点续传

### 幂等性保证

1. **Start 幂等**：如果目录已存在，读取现有记录而非创建新目录
2. **Stage 幂等**：每个阶段只记录一次（按 stage-order 去重）
3. **End 幂等**：summary.md 生成前检查是否已存在

### Checkpoint 机制

每个阶段完成后写入独立 checkpoint 文件：
```
reports/execution/<pipeline>-<timestamp>/
├── log.json           # 完整执行日志（累计写入）
├── summary.md         # 人类可读摘要
├── checkpoints/       # 断点续传检查点
│   ├── stage-01-bootstrap.json
│   ├── stage-02-incubation.json
│   └── ...
└── per-stage/         # 每阶段详细记录
    ├── 01-bootstrap.md
    └── ...
```

**Checkpoint 文件内容**：
```json
{
  "stage_order": 1,
  "stage_name": "bootstrap",
  "completed_at": "2026-04-27T23:00:00",
  "outputs": ["HOME.md"],
  "review_result": "PASS",
  "review_report": "reports/stage-review/bootstrap-20260427-230000.json",
  "log_updated": true
}
```

### 恢复流程

1. 检测到 `reports/execution/<pipeline>-*/checkpoints/` 目录
2. 读取最新的 checkpoint 确定最后完成的阶段
3. 在日志中标记 `[RESUMED]` 而非 `[STARTED]`

## Enriched Behavior

- **无侵入**：不改变管线逻辑，只做记录
- **可回查**：任何时间点都可以看"第 3 阶段做了什么决策"
- **供复盘用**：retrospective 可直接读取 execution log
- **决策溯源**：每个决策记录"谁做的"（AI 自选 / 用户确认）

## Target Pages

- `<项目根目录>/reports/execution/<pipeline>-<timestamp>/log.json`
- `<项目根目录>/reports/execution/<pipeline>-<timestamp>/summary.md`

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 管线已启动 |
| 后置 | `retrospective` 读取做复盘 |
| 依赖读取 | `stage-review` 的评审报告 |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-27 | v1.1: 新增幂等性保证（stage 去重、start/end 幂等）、断点续传（checkpoints/ 目录）、立即写入（stage-end 即写 log.json） | 复盘发现 session 中断导致 execution-log 缺失，增强恢复能力 |
| 2026-04-26 | v1.0 新建 skill | 实现管线执行可追溯：每步有记录、决策有溯源、复盘有数据 |
