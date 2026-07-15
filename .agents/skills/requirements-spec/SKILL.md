---
name: requirements-spec
description: 'Use when writing formal functional requirements, non-functional requirements, MVP scope, user stories, constraints, or priorities. Trigger when user says "requirements", "user story", "MVP", "constraints", "priorities", "feature list", "functional specs", or asks to "organize features into backlogs or phases". Coordinate with assumptions-tracking if requirements depend on unconfirmed assumptions.'
argument-hint: '功能需求、非功能需求、MVP范围、用户故事、约束条件、优先级'
---

# Requirements Spec

用于编写正式需求和用户故事。

## When to Use

- 需要整理功能需求或非功能需求
- 需要梳理 MVP 与后续迭代
- 需要明确约束和优先级
- 从模糊想法进入正式需求文档

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 需求片段、功能想法、业务目标 |
| 当前项目 | vision.md（如已确定）、feature-ideas.md（如经incubation发散过）、assumptions.md |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/01-requirements/user-stories.md` | 用户故事 | 角色|能力|目标 表格 + MVP/后续迭代划分 |
| `wiki/01-requirements/constraints.md` | 约束页 | 约束条件清单，带来源和影响 |

## Minimum Viable Output

- user-stories.md 含 ≥3 条用户故事，格式为"作为...我希望...以便..."
- 每条用户故事含优先级（高/中/低）
- 已区分 MVP 和后续迭代
- constraints.md 含 ≥2 条约束

## Complete Output

- user-stories.md 全部字段饱满：触发场景、验收关注点、依赖
- constraints.md 含技术约束、时间约束、资源约束、监管约束
- 已标注每条需求依赖哪些假设（回链 assumptions.md）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `overview-framing`（愿景和范围已定） |
| 后置 | `architecture-decisions`（需求明确后进入架构）、`delivery-planning`（需求稳定后可拆任务） |
| 并行 | `assumptions-tracking`（并行记录未验证的依赖） |

## Procedure

1. 先确认目标项目根目录，并只更新该项目目录下的需求页
2. 用用户故事或能力清单表达需求
3. 区分 MVP、后续迭代、非目标
4. 把约束写成明确条目，避免散落在正文里

### 用户故事字段说明

每条用户故事应含以下字段：

```markdown
| 字段 | 说明 | 示例 |
|------|------|------|
| ID | 唯一标识 | US-001 |
| 角色 | 谁（As a...） | 习惯追踪者 |
| 能力 | 能做什么（I want to...） | 设定每日习惯 |
| 目标 | 为什么（So that...） | 追踪坚持进度 |
| 优先级 | 高/中/低 | P0 |
| 所属阶段 | MVP / 后续迭代 | MVP |
| 验收条件 | 可验证的完成标准 | ≥1 条 |
| 触发场景 | 何时会使用 | 早晨起床后 |
| 依赖 | 依赖哪些假设/其他 US | assumptions: A-001 |
```

### MVP 划分标准

| 标准 | 说明 |
|------|------|
| 核心价值 | 直接支撑产品核心价值的 US 必须 MVP |
| 闭环完整性 | 能独立完成一个用户任务的 US 优先 MVP |
| 技术风险 | 技术未验证或依赖不清晰的 US 延后 |
| 优先级 | P0 必须 MVP，P1/P2 可放入后续迭代 |

### 验收条件格式

每条 US 必须含 ≥1 条验收条件，格式如下：

```
✅ 验收条件 = [条件描述] + [通过标准]

示例：
- 验收条件：习惯创建后立即显示在列表顶部
- 通过标准：数据库 insert 成功 + 列表 API 返回新记录在首位
```

## Enriched Behavior

- 不只罗列功能点，要把需求组织成用户可理解、开发可执行、验收可映射的结构
- 可以同时给出用户故事、能力清单、优先级分层，避免单一表达方式信息密度不足
- 当用户需求含糊时，优先拆成可讨论的候选需求组，而不是直接武断定稿
- 对明显依赖前置设计的问题，主动回链到概览、假设或调研页面

## Target Pages

- `<项目根目录>/wiki/01-requirements/user-stories.md`（主）
- `<项目根目录>/wiki/01-requirements/constraints.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| user-stories.md | requirements-spec | incubation-discovery（提供功能候选） |
| constraints.md | requirements-spec | architecture-decisions（提供技术约束） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：新增用户故事字段说明表（含 ID/角色/能力/目标/优先级/所属阶段/验收条件/触发场景/依赖）；新增 MVP 划分标准表；新增验收条件格式说明 | US 字段缺失、验收条件格式未定义、MVP 划分标准缺失 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，明确与其他 skill 的协作关系 |
