---
name: architecture-decisions
description: 'Use when choosing architecture, comparing tech stack options, defining module boundaries, writing ADRs, documenting system design, or explaining major technical tradeoffs. Trigger when user says "architecture", "tech stack", "module", "ADR", "system design", "technical decision", "choose between A and B", "microservices vs monolith", or when moving from requirements to implementation design. Coordinate with research-spikes for unverified technical assumptions.'
argument-hint: '架构设计、技术选型、模块边界、ADR决策、系统设计、技术取舍'
---

# Architecture Decisions

用于系统设计和技术决策。

## When to Use

- 需要做技术选型
- 需要定义模块划分和关键链路
- 需要记录 ADR 和架构取舍
- 从需求阶段进入方案设计阶段

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 技术选型需求、架构问题、模块划分需求 |
| 当前项目 | requirements.md、technical-spikes.md（如有）、assumptions.md（技术假设） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/03-architecture/system-design.md` | 系统设计 | 上下文图、模块划分、关键链路、失败路径 |
| `wiki/03-architecture/tech-stack.md` | 技术栈 | 候选方案对比、最终选择及理由 |
| `wiki/03-architecture/module-map.md` | 模块地图 | 模块边界、依赖关系、接口约定 |
| `wiki/03-architecture/decisions/ADR-NNN.md` | ADR | 决策背景、选项、决策、后果 |

## Minimum Viable Output

- system-design.md 含：模块划分、关键链路 1-2 条
- tech-stack.md 含：≥2 个候选方案对比
- ADR ≥1 篇（针对关键决策）

## Complete Output

- system-design.md：完整含上下文图、失败路径、部署拓扑
- tech-stack.md：完整含候选/选择/代价/改版条件
- module-map.md：完整含所有模块的边界和依赖
- ADR ≥3 篇，覆盖所有高风险决策

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `requirements-spec`（需求明确）、`research-spikes`（技术可行性已验证） |
| 后置 | `data-api-design`（模块划分后进入数据/API设计）、`operations-planning`（架构影响部署） |
| 并行 | `risk-register`（架构风险同步识别） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下写架构资料
2. 设计必须能追溯到需求和研究
3. 明确写出取舍与备选方案
4. 不稳定决策要标为待验证

### ADR 模板

每篇 ADR 保存为 `wiki/03-architecture/decisions/ADR-NNN.md`：

```markdown
# ADR-NNN: <决策标题>

## 状态
提议中 | 已接受 | 已废弃 | 已替代

## 决策日期
YYYY-MM-DD

## 背景
<触发决策的问题或上下文>

## 决策
<核心决策内容>

## 选项对比

| 选项 | 优点 | 缺点 | 适用条件 |
|------|------|------|---------|
| A: ... | ... | ... | ... |
| B: ... | ... | ... | ... |

## 后果

### 正面
- ...

### 负面
- ...

### 待验证假设
- [AUTO-ASSUMPTION: ...]

## 改版条件
如果 <条件> 发生，重新评审此决策。
```

**ADR 编号规则**：`ADR-001`, `ADR-002`...，每项目顺增。

### module-map.md 模板

```markdown
# 模块地图

## 模块列表

| 模块名 | 职责 | 边界（输入/输出） | 依赖模块 | 备注 |
|--------|------|-----------------|---------|------|
| auth | 用户认证与会话管理 | 输入: 凭证；输出: JWT | users, cache | |
| users | 用户数据管理 | 输入: user_id；输出: User实体 | db | |
| records | 核心业务记录管理 | 输入: record_id；输出: Record 实体 | users, db | |
```

## 模块依赖图

```
auth ──→ users
auth ──→ cache
habits ──→ users
habits ──→ db
```

## 接口约定

| 模块 | 接口 | 协议 | 数据格式 |
|------|------|------|---------|
| auth | POST /auth/login | HTTP | JSON |
| users | GET /users/:id | HTTP | JSON |
| habits | CRUD /habits | HTTP | JSON |
```

> 模块划分原则：高内聚低耦合，每个模块有明确职责和边界；跨模块调用通过定义好的接口，不直接访问对方内部状态。

## Enriched Behavior

- 不只写"选了什么"，还要写"为什么这样选、代价是什么、什么情况下可能要改"
- 可以同时输出模块边界、关键链路、部署拓扑、数据流，只要仍服务于主要架构决策
- 当项目还早期时，可以先给候选架构和比较框架，不必强行定稿
- 输出应为后续任务拆解、数据设计和运维规划提供清晰接口

## Target Pages

- `<项目根目录>/wiki/03-architecture/system-design.md`（主）
- `<项目根目录>/wiki/03-architecture/tech-stack.md`（主）
- `<项目根目录>/wiki/03-architecture/module-map.md`（主）
- `<项目根目录>/wiki/03-architecture/decisions/`（ADR 存放目录）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| system-design.md | architecture-decisions | data-api-design（接口契约） |
| tech-stack.md | architecture-decisions | operations-planning（部署约束） |
| module-map.md | architecture-decisions | data-api-design（模块接口） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-07-15 | 模块示例改为领域无关资源 | 避免单一业务案例污染 |
| 2026-04-30 | 修复：ADR 模板新增"决策日期"字段；新增 module-map.md 模板（含模块列表表、依赖图、接口约定） | ADR 缺少决策日期、module-map 无模板 |
| 2026-04-29 | 新增 ADR 模板（背景/决策/选项对比/后果/改版条件） | Procedure 缺少格式规范 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化 ADR 的结构化输出 |
