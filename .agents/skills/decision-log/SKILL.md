---
name: decision-log
description: 'Use when documenting design decisions — "decision log", "ADR", "architecture decision", "选择A而不选B", "设计决策". This skill enforces documentation of all non-default design choices, capturing why A was chosen over B. Use within any skill that produces design outputs.'
argument-hint: '设计决策日志、ADR、架构决策记录、选择理由'
---

# Decision Log

记录所有"选 A 而不选 B"的设计决策，形成可追溯的决策链条。

## When to Use

- 架构设计时，在多个技术方案中做了选择
- 任何 skill 输出中，出现了"采用 X 而不采用 Y"的描述
- 技术选型会议后，需要记录决策依据
- Code review 时发现设计意图不清晰

## NOT When to Use

- 选择是显然的"默认值"——即业界通行做法、没有合理替代方案、不选它反而需要额外理由
  - 示例：用 UTF-8 编码（不用记录，因为 UTF-8 是业界标准）
  - 示例：用 JSON 作为 API 响应格式（不用记录，因为 JSON 是 Web API 通用格式）
  - 示例：使用 Git 管理代码（不用记录，因为这是基础工具而非设计决策）
  - 反例：用 UTF-8 而不是 GBK 编码 → 值得记录，因为有编码选择的权衡考量
- 两个选项没有本质差异（无论选哪个对系统无实质影响）
- 纯个人偏好，无客观依据（无法论证为什么 A 比 B 更好）

## Input

| 来源 | 内容 |
|------|------|
| 任何 skill 输出的设计文档 | 需要记录的决策点 |
| research-spikes 输出 | 调研结论作为决策依据 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/08-history/decision-log.md` | 决策日志 | 所有设计决策的追踪表 |

## Minimum Viable Output

- 至少 5 条决策记录
- 每条包含：决策内容、选中选项、放弃选项、选择原因

## Complete Output

- 完整决策日志（覆盖所有非平凡选择）
- 每条决策标注来源文档
- 按时间/模块/优先级排序
- 决策状态（现行/已推翻/待定）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `architecture-decisions`（架构选型） |
| 前置 | `research-spikes`（调研结论） |
| 嵌入 | 任何输出设计文档的 skill |
| 依赖读取 | 相关设计文档 |

## Procedure

### Phase 1: 识别决策点

在设计文档中，任何出现以下模式的句子都是决策点：

```
❌ 采用了 X               （没有说明为什么不选 Y）
❌ 使用 X 进行存储         （没有说明为什么不是 Y）
❌ 选择 X 架构            （没有说明为什么不是 Y）
❌ 决定支持 X             （没有说明为什么不是 Y）

✅ 决策：采用 X 而不选 Y，因为 [原因]
✅ 决策：选择 X 方案，主要考虑 [权衡因素]
```

### Phase 2: 记录决策模板

```markdown
## 决策记录模板

| 字段 | 内容 |
|------|------|
| 决策 ID | DEC-XXX（DEC-001, DEC-002...）|
| 决策时间 | YYYY-MM-DD |
| 决策者 | [角色/团队] |
| 所属阶段 | [incubation/requirements/architecture/delivery...] |
| 决策来源 | [对应的设计文档] |
| 决策类型 | 技术选型 / 架构模式 / 工具选择 / 流程决策 |

### 决策内容
[一句话描述这个决策]

### 选中方案
**[方案名称]**
[方案描述，包括关键参数/配置]

### 放弃方案
**[方案名称]**
[方案描述]

### 选择原因
[为什么要选这个？可以包含：]
- 优势 1：[具体说明]
- 优势 2：[具体说明]
- 风险缓解：[这个选择规避了什么风险]

### 风险与权衡
[这个选择引入了什么代价？有没有被刻意接受的权衡？]

### 状态变更历史
| 日期 | 状态 | 变更原因 |
|------|------|---------|
| YYYY-MM-DD | 现行 | - |

### Phase 3: 决策分类

```markdown
## 决策分类索引

### 架构类
| DEC-ID | 决策 | 日期 | 状态 |
|--------|------|------|------|
| DEC-001 | ... | 2026-04-30 | 现行 |

### 技术栈类
| DEC-ID | 决策 | 日期 | 状态 |
|--------|------|------|------|
| DEC-002 | ... | 2026-04-30 | 现行 |

### 流程类
| DEC-ID | 决策 | 日期 | 状态 |
|--------|------|------|------|
| DEC-003 | ... | 2026-04-30 | 现行 |
```

### Phase 4: 决策状态追踪

```markdown
## 决策状态

| DEC-ID | 决策 | 状态 | 变更原因 |
|--------|------|------|---------|
| DEC-001 | ... | 现行 | - |
| DEC-002 | ... | 已推翻 | 2026-05-01: 发现原假设不成立 |
```

## 决策触发规则

以下情况**必须**记录决策：

| 场景 | 示例 |
|------|------|
| 技术栈选择 | 用 SQLite 而不是 PostgreSQL |
| 架构模式 | 用模块化架构而不是微服务 |
| 通信方式 | 用 REST 而不是 GraphQL |
| 认证方式 | 用生物识别而不是 PIN |
| 存储格式 | 用 JSON 而不是 Protocol Buffers |
| 并发模型 | 用单线程事件循环而不是多线程 |
| 部署方式 | 用容器化而不是直接部署 |

## 与 ADR 的关系

decision-log 是 ADR（Architecture Decision Record）的**父集**：
- ADR 是 decision-log 的子集，专门用于架构决策
- 一个架构决策 → 一个 ADR 记录 + 一个 decision-log 条目
- 非架构决策（工具选择、流程决策）→ decision-log 条目（不必创建 ADR）

decision-log 按**时间轴**记录所有决策；ADR 侧重于**单个决策的完整文档化**。两者共同存储在 `wiki/08-history/decision-log.md`。

## 与其他 Skill 的集成

`decision-log` **不是独立运行的 skill**，而是嵌入在其他 skill 的 Procedure 中：

| 嵌入位置 | 操作 |
|---------|------|
| `architecture-decisions` Phase X | 架构选型时记录 DEC |
| `data-api-design` Phase X | API 风格选择时记录 DEC |
| `tech-stack` 选择时 | 工具选型时记录 DEC |
| `ui-design` 风格选择时 | 风格决定时记录 DEC |

集成方式：在对应 skill 的 Procedure 中，增加一条：

```
在完成 [选择] 后，立即在 decision-log 中记录：
- 选中方案：[方案]
- 放弃方案：[方案]
- 选择原因：[原因]
```

## Target Pages

- `<项目根目录>/wiki/08-history/decision-log.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 增强：NOT When 判定标准扩展，新增"默认值"判断标准（业界通行做法/无需记录 vs 有权衡考量/应记录），含正反示例 | "默认值"判定标准不够明确，导致误判 |
| 2026-04-30 | 修复：路径统一为 wiki/08-history/；新增状态变更历史字段；新增 ADR 关系说明；明确 NOT When 判定标准；MVO 阈值 3→5 | 路径冲突、状态追踪缺失、ADR 关系模糊、MVO 门槛过低 |
| 2026-04-30 | 新建 skill | 设计决策无据可查是常见问题，需要强制记录机制 |
