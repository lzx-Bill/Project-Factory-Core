---
name: acceptance-design
description: 'Use when designing acceptance criteria, test cases, verification commands, acceptance reports, or traceability between tasks, prompts, and reports. Trigger when user says "acceptance criteria", "test case", "verification", "acceptance test", "how do we know this is done", "验收", "测试用例", or when moving from prompt-authoring to defining how to verify prompt outputs. Coordinate with prompt-authoring for prompt-to-acceptance mapping and with delivery-planning for task-to-acceptance mapping.'
argument-hint: '验收标准设计、测试用例、验证命令、验收报告、任务追踪'
---

# Acceptance Design

用于设计验收标准和验收记录。

## When to Use

- 需要编写验收条件和验证命令
- 需要建立任务到验收报告的追踪
- 需要补测试用例和已知缺口
- Prompt 完成后，需要设计如何验收输出

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 验收需求、验证标准 |
| 当前项目 | prompt/*.md（已完成的 Prompt）、task-breakdown.md、data-api.md |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `acceptance/README.md` | 验收索引 | 验收ID + Prompt文件 + 报告文件 + 状态 |
| `acceptance/A-NNN.md` | 单个验收 | 验收条件 + 验证命令 + 通过标准 |
| `wiki/06-quality/acceptance-plan.md` | 验收计划 | 覆盖范围 + 验收矩阵 |
| `wiki/06-quality/test-cases.md` | 测试用例 | 测试用例清单 |
| `reports/acceptance/R-NNN.json` | 验收报告 | JSON 格式的执行记录 |

## Minimum Viable Output

- acceptance/README.md 含每个 MVP Task 至少 1 个验收条目（≥3 条）
- 每个验收含：验收条件 + 通过/失败标准
- 含 acceptance-plan.md 矩阵（任务→验收映射）

## Complete Output

- acceptance/README.md：完整索引，含所有验收状态
- 每个 A-NNN.md：含验证命令、手工检查点、已知缺口
- acceptance-plan.md：完整验收矩阵（任务ID×Prompt×验收×报告）
- 含 reports/acceptance/ 下的执行报告模板

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `prompt-authoring`（Prompt 已完成）、`data-api-design`（契约已定） |
| 后置 | 无（验收是交付终点之一） |
| 依赖读取 | prompts/*.md、task-breakdown.md、data-api.md |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下写验收与报告
2. 验收条件必须量化
3. 每个任务至少对应一个验收文件
4. 报告中记录实际命令、输出、预期和结果

### 量化验收标准示例

**✅ 量化（通过）**
```
- API 响应时间 ≤200ms（P99）
- 用户操作完成率 ≥90%
- 登录失败率 <1%
- 每次搜索返回结果 ≤3s
```

**❌ 不可量化（不通过）**
```
- "系统应该快速响应" → 应改为具体 ms 数
- "用户体验应该流畅" → 应改为操作完成率或响应时间
- "错误率应该在可接受范围内" → 应改为具体百分比
```

### acceptance/A-NNN.md 模板

```markdown
# 验收: <任务ID> — <任务名称>

## 验收条件

| # | 条件 | 通过标准 | 验证方式 |
|---|------|---------|---------|
| 1 | ... | ... | 命令/手工检查 |
| 2 | ... | ... | 命令/手工检查 |

## 验证命令

```bash
<具体命令>
```
通过标准: <输出应包含的内容或数值>

## 手工检查点
- [ ] ...
- [ ] ...

## 已知缺口
- ...

## 执行记录
| 日期 | 结果 | 执行人 | 备注 |
|------|------|--------|------|
| | | | |
```

### reports/acceptance/R-NNN.json 模板

```json
{
  "id": "A-001",
  "task_id": "T1",
  "task_name": "<任务名称>",
  "executed_at": "YYYY-MM-DDTHH:mm:ss",
  "executor": "<执行人>",
  "result": "PASS | FAIL | PARTIAL",
  "checks": [
    {
      "id": 1,
      "condition": "<验收条件描述>",
      "criterion": "<通过标准>",
      "verification_method": "命令 | 手工检查",
      "actual_result": "<实际结果>",
      "passed": true
    }
  ],
  "command_output": "<如有命令，输出摘要>",
  "known_gaps": ["<缺口描述，如有>"],
  "notes": "<备注>"
}
```

## Enriched Behavior

- 不只列检查项，要形成"可执行、可重复、可回溯"的验收闭环
- 可以同时覆盖功能、结构、回写一致性、已知缺口和失败重试策略
- 当命令还无法完全自动化时，可以先给手工检查步骤和通过标准，不要放弃落文档
- 输出应直接服务于开发自检和人工复核

## Target Pages

- `<项目根目录>/acceptance/README.md`（主）
- `<项目根目录>/acceptance/`（验收文件目录）
- `<项目根目录>/wiki/06-quality/acceptance-plan.md`（主）
- `<项目根目录>/wiki/06-quality/test-cases.md`（辅）
- `<项目根目录>/reports/acceptance/`（报告目录）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| acceptance/README.md | acceptance-design | prompt-authoring（提供 Prompt 清单） |
| acceptance/*.md | acceptance-design | - |
| acceptance-plan.md | acceptance-design | delivery-planning（任务拆解） |
| test-cases.md | acceptance-design | - |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：MVO 阈值 ≥1→≥3（每个 MVP Task 至少 1 个验收）；新增 reports/acceptance/R-NNN.json 执行记录模板 | MVO 门槛过低、JSON 报告格式缺失 |
| 2026-04-29 | 新增量化验收标准示例（✅/❌对比）和 acceptance/A-NNN.md 模板 | Procedure 缺少量化示例 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化验收与 Prompt/任务的追踪关系 |
