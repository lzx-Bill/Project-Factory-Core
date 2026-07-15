---
name: consistency-review
description: 'Use when validating cross-document consistency in a project — "consistency review", "document coherence", "cross-reference check", "文档一致性", "交叉验证". This skill performs systematic cross-referencing between documents produced in the same iteration, flagging contradictions, gaps, and missing linkages. Use after architecture-decisions and before delivery-planning. Can also be used as a stage-review variant for any phase boundary.'
argument-hint: '文档一致性审查、交叉验证、矛盾检测、文档对齐'
---

# Consistency Review

用于系统性检测项目文档之间的矛盾、缺失和不一致。

## When to Use

- 架构设计完成后，需要验证各模块设计是否对齐
- 需求文档完成后，需要验证 assumptions 是否与 user stories 一致
- 任务拆分完成后，需要验证 task 是否覆盖了所有 US
- 任何阶段交接时，检查输出文档与下一阶段输入是否匹配
- 作为 `stage-review` 的加强版，专门做横向一致性检查

## NOT When to Use

- 单个文档内部的格式/语法检查（用 `stage-review`）
- 跨项目的文档对比
- 文档内容本身的质量评估（用对应领域的 skill）

## Input

| 来源 | 内容 |
|------|------|
| assumptions.md | 假设清单 |
| user-stories.md | 用户故事 |
| system-design.md | 系统架构 |
| task-breakdown.md | 任务拆分 |
| security.md | 安全设计 |
| performance.md | 性能设计 |
| api-spec.md | API 规范 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/06-quality/consistency-report.md` | 一致性报告 | 矛盾列表、严重程度、处理建议 |

## Minimum Viable Output

- 至少 6 组文档交叉比对（覆盖 2.1-2.6）
- 每组比对的结果（一致 / 矛盾 / 缺失）
- 矛盾清单（按严重程度排序）

## Complete Output

- 全量文档交叉比对矩阵
- 每个矛盾的具体位置（文件:行号）
- 每个矛盾的处理建议（接受 / 修复 / 延迟）
- 缺失项清单（某文档描述了但另一文档没提到）
- 最终签字确认（矛盾已全部处理）

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `requirements-spec`（已输出 assumptions + user stories）|
| 前置 | `architecture-decisions`（已输出 system design） |
| 前置 | `delivery-planning`（已输出 task breakdown） |
| 后置 | `delivery-planning`（一致性必须通过——高严重矛盾未处理则阻塞，中低可记录后放行但需在 open-questions.md 中标注） |
| 依赖读取 | 所有相关文档 |

## Procedure

### Phase 1: 建立文档依赖图

识别本次迭代输出的所有文档，确定哪些文档描述的是**同一件事**。

```markdown
## 文档依赖矩阵

| 文档 | 描述对象 | 依赖文档 | 被依赖文档 |
|------|---------|---------|-----------|
| assumptions.md | 项目假设 | - | user-stories.md |
| user-stories.md | 用户需求 | assumptions.md | task-breakdown.md |
| system-design.md | 系统架构 | user-stories.md | task-breakdown.md |
| task-breakdown.md | 任务拆分 | user-stories.md, system-design.md | - |
| security.md | 安全设计 | system-design.md | - |
| performance.md | 性能设计 | system-design.md | - |
| api-spec.md | API 契约 | system-design.md | task-breakdown.md |
```

### Phase 2: 强制交叉比对清单

以下每一项都必须检查，不能跳过：

#### 2.1 assumptions ↔ user-stories

```
检查规则：
- 每条 AS 是否被至少一个 US 覆盖
- 每条 AS 的风险等级是否与对应 US 的优先级匹配
- 矛盾的假设和 US 必须标记（假设说"用户每天一次"，US 说"一天多次"）
```

#### 2.2 user-stories ↔ task-breakdown

```
检查规则：
- 每个 US 是否有对应的 Task（US-001 → T?）
- 每个 Task 是否明确标注了覆盖的 US
- 优先级为 P0 的 US 是否对应了最早完成的任务
```

#### 2.3 system-design ↔ task-breakdown

```
检查规则：
- 每个 Module 是否都有对应的 Task
- 模块间的依赖关系是否与 Task 的依赖链一致
- 数据流是否在 Task 中有对应的实现步骤
```

#### 2.4 system-design ↔ security

```
检查规则：
- 安全方案覆盖的威胁是否在 threat model 中列出
- 每个敏感数据是否有对应的保护措施
- 安全测试用例是否覆盖了所有高风险威胁
```

#### 2.5 user-stories ↔ api-spec

```
检查规则：
- 每个 US 的操作是否都有对应的 API 端点
- API 错误码是否覆盖了所有 US 的异常路径
- API 的输入校验是否与 US 的约束条件一致
```

#### 2.6 assumptions ↔ system-design

```
检查规则：
- 每条 AS 中的技术假设是否在 system-design 中有对应实现
- system-design 的架构决策是否与 AS 中的约束条件一致
```

#### 2.7 assumptions ↔ task-breakdown

```
检查规则：
- 每条 AS 中的假设是否在某 Task 中被验证或实现
- 有风险的 AS 是否有对应的缓解 Task
```

#### 2.8 system-design ↔ performance

```
检查规则：
- 性能目标中的关键链路是否在 system-design 中有对应模块
- 缓存策略是否与 system-design 的数据流一致
```

#### 2.9 security ↔ task-breakdown

```
检查规则：
- 每个安全措施是否在 task-breakdown 中有对应实现任务
- 安全测试用例是否对应了具体的 Task
```

#### 2.10 api-spec ↔ task-breakdown

```
检查规则：
- 每个 API 端点是否在 task-breakdown 中有对应实现任务
- API 版本策略是否在 Task 中有体现
```

#### 2.11 performance ↔ api-spec

```
检查规则：
- API 响应时间目标是否与 performance.md 中的性能目标一致
- API 吞吐量是否满足性能设计中的 QPS 要求
```

### Phase 3: 生成矛盾清单 + 严重程度判定

**严重程度判定标准：**

| 等级 | 判定条件 | 例子 |
|------|---------|------|
| 🔴 高 | 矛盾会导致系统无法运行、数据损坏、安全隐患 | AS 说单用户，US 说多用户；安全方案完全未覆盖某敏感数据 |
| 🟡 中 | 矛盾影响功能正确性但有 workaround | 缓存策略与 API 设计不一致；性能目标与资源预算不匹配 |
| 🟢 低 | 矛盾仅影响可维护性/可读性，不影响功能 | 文档格式不一致；命名不统一 |

**澄清与接受的边界**：
- **澄清**：两份文档描述的是同一事实的不同方面，互补而非矛盾 → 加解释
- **接受**：已知设计权衡，有意接受矛盾，收益大于风险 → 记录风险，继续

```markdown
## 矛盾清单

| ID | 矛盾描述 | 涉及文档 | 严重程度 | 处理建议 |
|----|---------|---------|---------|---------|
| C1 | AS-006 说"每天只打一次卡"，US-003 允许"一天多次补卡" | assumptions.md:AS-006, user-stories.md:US-003 | 🔴 高 | 修复 |
| C2 | AS-004 说"固定时间使用"，US-004 说"随机提醒时间" | assumptions.md:AS-004, user-stories.md:US-004 | 🟡 中 | 澄清 |
```

```markdown
## 矛盾清单

| ID | 矛盾描述 | 涉及文档 | 严重程度 | 处理建议 |
|----|---------|---------|---------|---------|
| C1 | AS-006 说"每天只打一次卡"，US-003 允许"一天多次补卡" | assumptions.md:AS-006, user-stories.md:US-003 | 🔴 高 | 修复 |
| C2 | AS-004 说"固定时间使用"，US-004 说"随机提醒时间" | assumptions.md:AS-004, user-stories.md:US-004 | 🟡 中 | 澄清 |
```

### Phase 4: 矛盾处理

对于每个矛盾，选择以下处理方式之一：

| 处理方式 | 适用场景 |
|---------|---------|
| **修复** | 明显错误，更新文档消除矛盾 |
| **澄清** | 两个描述其实不矛盾，是视角不同，加入解释 |
| **接受** | 已知矛盾，有意为之，记录风险后放行 |
| **延迟** | 不影响当前阶段，移入 backlog |

### Phase 5: 签字确认

```markdown
## 一致性确认

| 检查项 | 状态 |
|-------|------|
| assumptions ↔ user-stories | ✅ 无矛盾 |
| user-stories ↔ task-breakdown | ✅ 全覆盖 |
| system-design ↔ task-breakdown | ✅ 依赖一致 |
| system-design ↔ security | ✅ 覆盖完整 |
| user-stories ↔ api-spec | ✅ 端点完备 |

**结论**：✅ 可以进入 delivery-planning 阶段
**签字**：_________________ 日期：_________
```

## Target Pages

- `<项目根目录>/wiki/06-quality/consistency-report.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：补充 performance.md 至依赖矩阵；新增 2.6-2.11 共 6 组比对；新增严重程度判定标准；明确 Gate 为强制（高严重矛盾阻塞）；MVO 阈值 3→6 | 比对矩阵不完整、严重程度无标准、Gate 机制模糊、MVO 门槛过低 |
| 2026-04-30 | 新建 skill | 文档间矛盾是常见问题，需要强制交叉验证机制 |
