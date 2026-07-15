# Project Wiki Template

本模板用于在 Project Factory 中创建新的 wiki 型项目结构。

使用方式分两层：

- 统一页面骨架：帮助 AI 默认写出更完整、可读、可继续扩写的页面
- 任务联动骨架：帮助任务、Prompt、验收、报告之间形成稳定追踪链路

## 目录模板

```text
<项目名称>/
├── HOME.md
├── wiki/
│   ├── 00-overview/
│   │   ├── vision.md
│   │   ├── scope.md
│   │   ├── glossary.md
│   │   ├── idea-landscape.md
│   │   └── scenario-matrix.md
│   ├── 01-requirements/
│   │   ├── user-stories.md
│   │   ├── constraints.md
│   │   ├── assumptions.md
│   │   └── open-questions.md
│   ├── 02-research/
│   │   ├── market-notes.md
│   │   ├── technical-spikes.md
│   │   ├── risk-register.md
│   │   └── opportunity-backlog.md
│   ├── 03-architecture/
│   │   ├── tech-stack.md
│   │   ├── system-design.md
│   │   ├── module-map.md
│   │   ├── ui-design.md
│   │   ├── security.md
│   │   ├── performance.md
│   │   ├── threat-scenarios.md
│   │   └── decisions/
│   │       └── ADR-001-template.md
│   ├── 04-data-and-api/
│   │   ├── domain-model.md
│   │   ├── schema.md
│   │   ├── api-spec.md
│   │   └── state-machine.md
│   ├── 05-delivery/
│   │   ├── task-breakdown.md
│   │   ├── milestone-plan.md
│   │   ├── dependency-map.md
│   │   └── traceability-matrix.md
│   ├── 06-quality/
│   │   ├── acceptance-plan.md
│   │   ├── test-cases.md
│   │   ├── known-gaps.md
│   │   ├── consistency-report.md
│   │   ├── quantified-checklist.md
│   │   └── test-strategy.md
│   ├── 07-operations/
│   │   ├── deployment.md
│   │   ├── monitoring.md
│   │   ├── rollback.md
│   │   └── runtime-constraints.md
│   └── 08-history/
│       ├── changelog.md
│       ├── decision-log.md
│       └── archive/
├── prompts/
│   ├── README.md
│   ├── PROMPT_TEMPLATE.md
│   └── phase-1-foundation.md
├── acceptance/
│   ├── README.md
│   ├── ACCEPTANCE_TEMPLATE.md
│   └── phase-1-foundation.md
├── tasks/
│   ├── backlog.md
│   ├── in-progress.md
│   └── done.md
├── reports/
    ├── acceptance/
    │   └── REPORT_TEMPLATE.json
    ├── stage-review/
    ├── audit/
    ├── execution/
    └── reviews/
└── implementation-kit/
```

## HOME.md 模板

```markdown
# <项目名称>

## 一句话定义

## 当前状态
- 阶段：
- 当前目标：
- 下一步：

## 导航
- 愿景：wiki/00-overview/vision.md
- 范围：wiki/00-overview/scope.md
- 用户故事：wiki/01-requirements/user-stories.md
- 假设：wiki/01-requirements/assumptions.md
- 风险：wiki/02-research/risk-register.md
- 架构：wiki/03-architecture/system-design.md
- 数据与 API：wiki/04-data-and-api/api-spec.md
- 任务拆解：wiki/05-delivery/task-breakdown.md
- Prompt：prompts/README.md
- 验收：acceptance/README.md

## 当前重点
- <本周最重要的 3 件事>

## 最新决策摘要
| 日期 | 决策 | 影响 |
|------|------|------|

## 当前风险摘要
| ID | 风险 | 状态 | 下一步 |
|----|------|------|--------|
```

## 统一页面骨架

以下骨架是推荐默认结构，用于让 AI 写出的页面更完整、更易读、更方便后续增量维护。
不是所有页面都必须逐节填满，但建议优先覆盖这些槽位。

```markdown
# <页面标题>

## 本页目标
- 这页解决什么问题
- 这页服务于哪个阶段或决策

## 当前结论 / 当前状态
- 已确认：
- 待确认：
- 当前推荐：

## 关键内容
- <本页主体内容>

## 依赖与关联
- 上游输入：
- 下游影响：
- 相关页面：

## 开放问题 / 风险
- <尚未解决的问题、风险或边界>

## 下一步
- <建议下一步动作>
```

## 页面视觉规范

以下规范用于提升 wiki 页面的可读性和视觉层次。不是强制要求，但建议遵循。

### 标题层级

- `#` 仅用于 HOME.md 页面标题
- `##` 用于大章节（如 ## 愿景、## 用户故事）
- `###` 用于小节（如 ### 目标用户画像）
- **避免超过 4 层标题**

### 排版原则

| 规则 | 说明 | 示例 |
|------|------|------|
| 每段不超过 5 行 | 长段落降低可读性 | 将长段拆分为要点列表 |
| 列表项超过 5 项用表格 | 表格比列表更易扫读 | 风险列表 → 风险矩阵表 |
| 关键数字/术语用 **粗体** | 突出重点 | **MVP**、**3 天**、**≥90%** |
| 适当使用 emoji 增加可读性 | 但不要滥用 | 📌 重点、⚠️ 风险、✅ 完成、🔴 阻塞 |

### 可视化元素

| 元素 | 适用场景 | 示例 |
|------|---------|------|
| 表格 | 对比、列表、矩阵 | 场景×价值矩阵、技术栈对比 |
| 分隔线 `---` | 区分大章节 | 内容块之间 |
| 引用块 `>` | 突出关键结论 | > 最终推荐方案：... |
| 代码块 ``` | 命令、配置、结构 | JSON schema、API 格式 |
| Emoji | 状态、分类、强调 | 🎯 目标、⚡ 优先级 |

### 避免的写法

| 问题 | 示例 | 改进 |
|------|------|------|
| 泛泛而谈 | "用户提供良好的体验" | "用户可在 3 步内完成核心操作" |
| 无差异化描述 | "比其他产品更好" | "差异化：支持离线优先，节省 60% 网络流量" |
| 正确废话 | "提供高质量服务" | "SLA 99.9%，平均响应时间 <200ms" |
| 纯文字罗列 | 多条要点无结构 | 用表格或分隔线组织 |

### 页面结构建议

每个 wiki 页面建议遵循以下视觉节奏：

```
# 页面标题

> 一句话核心结论（可用引用块突出）

## 大章节
### 小节
内容...

---（分隔线）

## 下一个大章节
...
```

## 维度页面建议模板

### wiki/00-overview/vision.md

```markdown
# 项目愿景

## 解决的问题

## 目标用户

## 核心价值

## 非目标

## 成功标准
```

### wiki/01-requirements/user-stories.md

```markdown
# 用户故事

## MVP 用户故事
- 作为 <角色>，我希望 <能力>，以便 <目标>

## 后续迭代用户故事

## 暂不纳入范围
```

### wiki/01-requirements/assumptions.md

```markdown
# 假设清单

| ID | 假设 | 来源 | 影响范围 | 验证方式 | 状态 |
|----|------|------|----------|----------|------|
| A-001 |  |  |  |  | 待验证 |
```

### wiki/01-requirements/open-questions.md

```markdown
# 待确认问题

| ID | 问题 | 为什么重要 | 负责人 | 状态 |
|----|------|------------|--------|------|
| Q-001 |  |  |  | open |
```

### wiki/02-research/technical-spikes.md

```markdown
# 技术验证

## Spike 列表
| ID | 主题 | 目标 | 结论 | 是否影响架构 |
|----|------|------|------|--------------|

## 详细记录
### Spike X
- 背景：
- 方法：
- 结果：
- 结论：
- 后续动作：
```

### wiki/02-research/risk-register.md

```markdown
# 风险登记

| ID | 风险 | 概率 | 影响 | 触发条件 | 应对策略 | 状态 |
|----|------|------|------|----------|----------|------|
```

### wiki/03-architecture/system-design.md

```markdown
# 系统设计

## 上下文图

## 模块划分

## 关键链路

## 失败路径

## 需要进一步验证的点
```

### wiki/03-architecture/decisions/ADR-001-template.md

```markdown
# ADR-001: <决策标题>

## 背景

## 选项

## 决策

## 后果

## 回滚条件
```

### wiki/04-data-and-api/api-spec.md

```markdown
# API 规格

## 接口目录
| 方法 | 路径 | 说明 | 调用方 |
|------|------|------|--------|

## 接口详情
### GET /api/example
- 请求参数：
- 响应结构：
- 错误码：
- 验收点：
```

### wiki/05-delivery/task-breakdown.md

```markdown
# 任务拆解

## 里程碑

## 任务列表
| 任务 ID | 名称 | 目标 | 前置依赖 | 输出物 | Prompt ID | 验收 ID | 报告 ID | 状态 |
|---------|------|------|----------|--------|-----------|---------|---------|------|
```

### wiki/05-delivery/traceability-matrix.md

```markdown
# 追踪矩阵

| 任务 ID | 任务名称 | Prompt 文件 | 验收文件 | 验收报告 | 当前状态 | 备注 |
|---------|----------|-------------|----------|----------|----------|------|
| T-001 |  | prompts/<file>.md | acceptance/<file>.md | reports/acceptance/<file>.json | backlog |  |
```

### wiki/06-quality/acceptance-plan.md

```markdown
# 验收计划

## 覆盖范围

## 验收矩阵
| 任务 ID | Prompt 文件 | 验收文件 | 报告文件 | 验证命令 | 通过标准 |
|---------|-------------|----------|----------|----------|----------|
```

### wiki/07-operations/deployment.md

```markdown
# 部署说明

## 环境划分

## 依赖服务

## 部署步骤

## 回滚入口
```

### wiki/08-history/changelog.md

```markdown
# 变更日志

| 日期 | 变更 | 原因 | 影响文档 |
|------|------|------|----------|
```

## prompts/README.md 模板

```markdown
# Prompt 索引

| Prompt ID | 名称 | 对应任务 | 对应验收 | 文件 | 状态 |
|-----------|------|----------|----------|------|------|
```

### prompts/PROMPT_TEMPLATE.md

```markdown
# Prompt <Prompt ID>：<任务名称>

**对应任务**：wiki/05-delivery/task-breakdown.md 中的 <任务 ID>
**对应验收**：acceptance/<文件名>.md
**回写页面**：wiki/...、tasks/...、reports/...

## 输入上下文
- 技术栈：
- 相关文档：
- 前置依赖：
- 当前已知限制：

## 输出
- 文件：
- 模块：
- 不应修改：

## 实现要求
- 功能要求：
- 技术约束：
- 错误处理：
- 数据/API 一致性要求：

## 验收映射
- 对应验收文件：
- 关键通过标准：

## 回写要求
- 如果发现设计缺口，先更新 wiki 再继续实现
- 完成后同步 tasks / acceptance / reports
```

单个 Prompt 文件建议格式：

```markdown
# Prompt <Prompt ID>：<任务名称>

**对应任务**：wiki/05-delivery/task-breakdown.md 中的 <任务 ID>
**对应验收**：acceptance/<文件名>.md
**回写页面**：wiki/...、tasks/...、reports/...

### 输入上下文
- 技术栈：
- 相关文档：
- 前置依赖：

### 输出
- 文件：
- 模块：

### 要求
- 功能要求：
- 技术约束：
- 错误处理：
- 验收映射：
- 回写要求：如果发现设计缺口，先更新 wiki 再继续实现
```

## acceptance/README.md 模板

```markdown
# 验收索引

| 任务 ID | Prompt 文件 | 验收文件 | 报告文件 | 主要验证方式 | 当前状态 |
|---------|-------------|----------|----------|--------------|----------|
```

### acceptance/ACCEPTANCE_TEMPLATE.md

```markdown
# 验收 <Acceptance ID>：<任务名称>

**对应任务**：<任务 ID>
**对应 Prompt**：prompts/<文件名>.md
**报告输出**：reports/acceptance/<文件名>.json

## 验收前提
- 前置环境：
- 依赖数据：
- 版本/分支要求：

## 验收条件
1. <条件>
   ```bash
   <命令>
   ```
   通过标准：<标准>

2. 文档回写完成
   检查项：相关 wiki / prompts / acceptance / tasks / reports 已同步更新

## 手工检查项
- <当命令无法覆盖时的人工核对点>

## 已知缺口
- <暂不覆盖或需后续补齐的点>
```

单个验收文件建议格式：

```markdown
# 验收 <Acceptance ID>：<任务名称>

**对应任务**：<任务 ID>
**对应 Prompt**：prompts/<文件名>.md
**报告输出**：reports/acceptance/<文件名>.json

### 验收条件
1. <条件>
   ```bash
   <命令>
   ```
   通过标准：<标准>

2. 文档回写完成
    检查项：相关 wiki / prompts / acceptance / tasks / reports 已同步更新
```

## reports/acceptance/REPORT_TEMPLATE.json 模板

```json
{
   "任务ID": "T-001",
   "PromptID": "P-001",
   "AcceptanceID": "A-001",
   "任务名称": "示例任务",
   "验收时间": "YYYY-MM-DD HH:MM:SS",
   "执行命令数": 0,
   "通过数": 0,
   "失败数": 0,
   "结果": "PASS 或 FAIL",
   "检查记录": [
      {
         "条件": "条件描述",
         "命令": "实际执行的命令",
         "实际输出": "命令输出",
         "预期": "预期结果",
         "结果": "PASS 或 FAIL"
      }
   ],
   "文档回写": {
      "wiki": [],
      "prompts": [],
      "acceptance": [],
      "tasks": [],
      "reports": []
   },
   "循环次数": "N/3"
}
```

## tasks/ 模板

### backlog.md

```markdown
# Backlog

| 任务 ID | 名称 | 优先级 | 依赖 | Prompt 状态 | 验收状态 | 备注 |
|---------|------|--------|------|-------------|----------|------|
```

### in-progress.md

```markdown
# In Progress

| 任务 ID | 名称 | 当前动作 | 对应 Prompt | 对应验收 | 阻塞点 | 下一步 |
|---------|------|----------|-------------|----------|--------|--------|
```

### done.md

```markdown
# Done

| 任务 ID | 名称 | 完成日期 | Prompt 文件 | 验收文件 | 验收报告 | 备注 |
|---------|------|----------|-------------|----------|----------|------|
```

## 任务联动规则

推荐至少维持下面这条链路完整：

`任务 ID` -> `Prompt 文件` -> `验收文件` -> `验收报告`

建议的最小命名约定：

- 任务：`T-001`
- Prompt：`P-001`
- 验收：`A-001`
- 报告：`R-001` 或直接沿用任务 ID

如果项目规模较小，也可以直接用同一个任务 ID 贯穿任务、Prompt、验收、报告文件名。

## 使用规则

1. 首页只放导航、摘要、状态，不把所有内容塞进 `HOME.md`。
2. 维度页面优先写结论，再补证据和细节。
3. 研究未证实的内容必须写入假设、问题、风险，不得伪装成最终设计。
4. 任务、Prompt、验收必须通过任务 ID 互相映射。
5. 实现阶段推翻前期研究时，先更新 wiki，再更新 prompts、acceptance、tasks、reports。
6. 统一页面骨架是默认推荐结构，允许按项目阶段裁剪，但不要只留空标题。
7. 本文件是项目结构的唯一标准；Skill 不维护独立模板副本，审计和生成流程均引用本文件。
