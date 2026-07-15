---
name: delivery-planning
description: 'Use when breaking work into tasks, planning milestones, mapping dependencies, sequencing implementation, or maintaining backlog and in-progress views. Trigger when user says "task breakdown", "milestone", "dependencies", "backlog", "sprint", "implementation plan", "delivery plan", or asks to "break this down into tasks". Coordinate with prompt-authoring for task-to-prompt mapping and with acceptance-design for task-to-acceptance mapping.'
argument-hint: '任务拆解、里程碑规划、依赖关系、backlog管理、执行顺序'
---

# Delivery Planning

用于把设计方案拆成可执行交付计划。

## When to Use

- 需要拆任务和里程碑
- 需要建立依赖关系和执行顺序
- 需要维护 backlog 和 in-progress
- 设计阶段完成，进入交付规划

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 交付范围、优先级偏好、里程碑要求 |
| 当前项目 | 所有已完成的 wiki 页面（从中提取可交付项） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/05-delivery/task-breakdown.md` | 任务拆解 | 任务ID + 名称 + 目标 + 前置依赖 + 输出物 |
| `wiki/05-delivery/milestone-plan.md` | 里程碑 | 阶段 + 目标日期 + 关键交付物 |
| `wiki/05-delivery/dependency-map.md` | 依赖图 | 任务间依赖关系 |
| `tasks/backlog.md` | 待办面板 | 任务ID + 名称 + 优先级 + 状态 |
| `tasks/in-progress.md` | 执行中面板 | 任务ID + 当前动作 + 阻塞点 |
| `tasks/done.md` | 完成面板 | 任务ID + 完成日期 + 产出链接 |

## Minimum Viable Output

- task-breakdown.md 含 ≥5 条任务，每条含 ID、名称、前置依赖
- milestone-plan.md 含 ≥2 个里程碑
- backlog.md 含所有未启动任务

## Complete Output

- task-breakdown.md：每条任务含 Prompt ID 映射、验收 ID 映射
- milestone-plan.md：含阶段目标和关键路径
- dependency-map.md：完整依赖图
- backlog/in-progress/done 三面板实时同步

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `requirements-spec`（需求明确）、`architecture-decisions`（方案明确） |
| 后置 | `prompt-authoring`（任务→Prompt）、`acceptance-design`（任务→验收） |
| 并行 | `history-sync`（任务状态变化同步历史） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下拆任务与维护状态
2. 每个任务都要有明确输出物
3. 每个任务都要能映射到 Prompt 和验收
4. 阻塞点和依赖必须显式记录

### task-breakdown.md 模板

```markdown
# 任务拆解

## 任务列表

| ID | 任务名称 | 前置依赖 | 估算 | 输出物 | 优先级 | 备注 |
|----|---------|---------|------|-------|-------|------|
| T1 | ... | - | 2d | ... | P0 | MVP 必需 |
| T2 | ... | T1 | 3d | ... | P0 | MVP 必需 |
| T3 | ... | T1 | 1d | ... | P1 | |
```

**估算说明**：使用人天（d）或 story points（1=1d，2=2d，3=3d）。无估算经验的团队可用相对估算（T1=T2 的 2 倍）。

**阻塞点状态定义**：

| 状态 | 含义 | 颜色 |
|------|------|------|
| 🔴 阻塞 | 依赖未完成，当前无法推进 | 阻塞 |
| 🟡 等待 | 外部依赖（等待第三方/用户回复） | 等待中 |
| 🟢 进行中 | 当前正在执行 | 正常 |
| ✅ 完成 | 任务完成 | 已完成 |

**阻塞点格式**（在 in-progress.md 中记录）：

```markdown
# 执行中

| ID | 当前动作 | 阻塞点 | 状态 | 备注 |
|----|---------|-------|------|------|
| T3 | 正在实现X | 等待 T2 完成（依赖其 API） | 🔴 阻塞 | T2 预计今天完成 |
| T5 | 设计 Y 模块 | 需要外部 API 文档 | 🟡 等待 | 已发邮件催 |
```

### 依赖闭合检查

- 无孤立任务（0 依赖且 0 被依赖），除非是 T1
- 循环依赖检测：如有循环依赖必须拆开（可用拓扑排序验证：`make deps` 或等效工具）
- MVP 任务必须有明确的优先级标注
- **task-breakdown ↔ backlog 同步机制**：task-breakdown 是设计阶段输出（稳定），backlog 是执行阶段状态（动态）。每完成一个 Task，执行者需同步更新 backlog 中的对应条目。设计者（AI）在生成 task-breakdown 时不写 backlog，执行者负责维护 backlog 状态。

## Enriched Behavior

- 不只切任务数量，要让任务既可执行又能形成里程碑节奏
- 可以同时产出任务清单、依赖图、阶段目标、执行顺序和风险阻塞说明
- 当需求尚未完全稳定时，可以先形成候选任务层级和冻结边界，而不是等待所有信息完美后再拆分
- 任务拆解要服务于后续 Prompt 生成与验收设计，而不是仅做项目管理装饰

## Target Pages

- `<项目根目录>/wiki/05-delivery/task-breakdown.md`（主）
- `<项目根目录>/wiki/05-delivery/milestone-plan.md`（主）
- `<项目根目录>/wiki/05-delivery/dependency-map.md`（辅）
- `<项目根目录>/tasks/backlog.md`（主）
- `<项目根目录>/tasks/in-progress.md`（主）
- `<项目根目录>/tasks/done.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| task-breakdown.md | delivery-planning | prompt-authoring（提供任务清单） |
| milestone-plan.md | delivery-planning | - |
| dependency-map.md | delivery-planning | - |
| tasks/*.md | delivery-planning | home-navigation（状态摘要） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：task-breakdown 模板新增估算列（工时/story points）；新增阻塞点状态定义表（🔴🟡🟢✅）；补充 task-breakdown↔backlog 同步机制说明 | 工时估算缺失、状态无定义、backlog 同步机制缺失 |
| 2026-04-29 | 新增 task-breakdown.md 模板和阻塞点格式（含状态/颜色标记） | Procedure 缺少阻塞点格式定义 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化任务与其他交付物的映射关系 |
