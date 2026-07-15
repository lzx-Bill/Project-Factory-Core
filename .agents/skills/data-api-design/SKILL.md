---
name: data-api-design
description: 'Use when modeling entities, writing schema docs, designing APIs, defining state machines, or keeping data and API contracts consistent. Trigger when user says "data model", "schema", "API design", "state machine", "entity relationship", "database schema", "API contract", "endpoint", or when moving from architecture to implementation-ready data contracts. Coordinate with architecture-decisions for module boundaries and with prompt-authoring for API consistency.'
argument-hint: '数据模型设计、Schema编写、API规格、状态机、实体关系、契约一致性'
---

# Data API Design

用于数据模型与接口规格设计。

## When to Use

- 需要定义领域模型或 schema
- 需要设计 API 规格和错误码
- 需要定义状态机和契约一致性
- 从架构阶段进入数据/API 详细设计

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 数据建模需求、API 设计需求、状态机需求 |
| 当前项目 | architecture.md（模块边界）、system-design.md（数据流） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/04-data-and-api/domain-model.md` | 领域模型 | 实体、关系、关键属性 |
| `wiki/04-data-and-api/schema.md` | Schema | 表/集合结构、字段类型、约束 |
| `wiki/04-data-and-api/api-spec.md` | API 规格 | 路径、方法、参数、响应、错误码 |
| `wiki/04-data-and-api/state-machine.md` | 状态机 | 状态流转图、触发条件 |

## Minimum Viable Output

- domain-model.md 含：≥3 个核心实体及关系
- api-spec.md 含：≥3 个 API 端点，含路径、方法、响应结构
- schema.md 或 state-machine.md 至少一个含实质内容

## Complete Output

- domain-model.md：完整实体关系图、聚合根、值对象
- schema.md：完整字段、索引、约束
- api-spec.md：全部端点，含请求/响应示例、错误码、验收点
- state-machine.md：完整状态流转、异常状态

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `architecture-decisions`（模块边界已定） |
| 后置 | `prompt-authoring`（API 契约输入 Prompt）、`acceptance-design`（API 契约输入验收） |
| 并行 | `architecture-decisions`（数据流反馈架构） |

## Procedure

1. 先确认目标项目根目录，并只更新该项目目录下的数据/API 文档
2. 先定义模型和边界，再落接口
3. API、Prompt、验收三处必须可映射
4. 修改数字、路径、名称时同步全局检查

### Phase 1: API 错误码规范

每个 API 端点必须定义错误码结构：

```markdown
## 错误码规范

### 标准结构
{
  "code": "ERR_XXX_YYYY",
  "message": "人类可读的错误描述",
  "details": {} // 可选，额外上下文
}

### 错误码分层
| 层级 | 范围 | 含义 |
|------|------|------|
| 4xx | 1000-1999 | 客户端错误（参数错误、权限不足等） |
| 5xx | 2000-2999 | 服务端错误（系统故障、外部依赖等） |

### 按模块分码
| 模块 | 错误码前缀 | 示例 |
|------|----------|------|
| 认证 | AUTH_ | AUTH_1001: Token 过期 |
| 用户 | USER_ | USER_2001: 用户不存在 |
| 习惯 | HABIT_ | HABIT_1001: 习惯不存在 |
```

### 分页响应规范（如适用）

```markdown
## 分页响应格式（Cursor-based）

{
  "data": [...],
  "pagination": {
    "next_cursor": "opaque_cursor_string",
    "has_more": true,
    "total_count": 100 // 可选
  }
}

说明：使用 Cursor 分页而非 Offset，避免大偏移量性能问题。
```

### API 版本策略

| 版本策略 | 适用场景 | 说明 |
|---------|---------|------|
| 路径版本 | 重大不兼容变更 | `GET /api/v1/users` |
| Header 版本 | 轻微不兼容 | `API-Version: 2024-01-01` |

不兼容变更**必须**升版本；兼容变更（如新增字段）不需升版本。

### Schema 索引设计（如适用）

```markdown
## 索引设计

| 表/集合 | 索引类型 | 字段 | 说明 |
|---------|---------|------|------|
| users | UNIQUE | email | 唯一约束 |
| habits | BTREE | user_id, created_at | 复合索引 |
| checkins | BTREE | habit_id, checkin_date | 支持按习惯查打卡 |

说明：
- 主键索引由数据库自动创建
- 外键字段建索引以加速 JOIN
- 复合索引字段顺序遵循最左前缀原则
```

## Enriched Behavior

- 不只给表结构或接口清单，要形成一套能支撑实现、测试、文档同步的契约描述
- 可以主动补充错误码、状态流转、实体关系、示例请求响应等高价值细节
- 当接口或数据模型仍未定时，优先给候选契约和影响范围，不要把未确认设计伪装成稳定规范
- 输出要尽量减少后续实现阶段的歧义

## Target Pages

- `<项目根目录>/wiki/04-data-and-api/domain-model.md`（主）
- `<项目根目录>/wiki/04-data-and-api/schema.md`（主）
- `<项目根目录>/wiki/04-data-and-api/api-spec.md`（主）
- `<项目根目录>/wiki/04-data-and-api/state-machine.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| domain-model.md | data-api-design | architecture-decisions（模块边界） |
| schema.md | data-api-design | - |
| api-spec.md | data-api-design | prompt-authoring（映射到实现 Prompt）、acceptance-design（映射到验收） |
| state-machine.md | data-api-design | - |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：Phase 1 新增 API 错误码规范（分层结构 + 按模块分码）、分页响应规范（Cursor-based）、API 版本策略、Schema 索引设计指引 | 错误码规范缺失、分页规范缺失、API 版本策略缺失、Schema 索引策略缺失 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化 API 与 Prompt/验收的映射关系 |
