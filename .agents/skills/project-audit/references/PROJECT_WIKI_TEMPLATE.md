# Project Factory Wiki 模板标准

本文档定义 Project Factory 项目的标准结构和页面骨架，供 `project-audit` 审计使用。

---

## 一、标准目录结构

```
<项目根目录>/
├── HOME.md                          # 单一导航入口
├── wiki/
│   ├── 00-overview/                 # 愿景与范围
│   │   ├── vision.md                # 问题、用户、价值、非目标、成功标准
│   │   ├── scope.md                 # 范围清单（内/外）、非目标
│   │   ├── glossary.md              # 术语表
│   │   ├── idea-landscape.md        # 方向发散（画像×场景×候选）
│   │   └── scenario-matrix.md       # 场景×价值×风险矩阵
│   ├── 01-requirements/             # 需求与约束
│   │   ├── user-stories.md          # 用户故事（MVP/后续 标注）
│   │   ├── constraints.md           # 约束清单
│   │   ├── assumptions.md           # 假设清单（按风险排序）
│   │   └── open-questions.md        # 待确认问题
│   ├── 02-research/                # 调研与风险
│   │   ├── market-notes.md         # 市场/竞品调研笔记
│   │   ├── technical-spikes.md     # 技术验证记录
│   │   ├── risk-register.md         # 风险登记册
│   │   └── opportunity-backlog.md  # 机会点待办
│   ├── 03-architecture/             # 架构与设计
│   │   ├── tech-stack.md            # 技术栈选型
│   │   ├── system-design.md         # 系统设计（含模块划分、关键链路）
│   │   └── module-map.md            # 模块映射
│   ├── 04-data-and-api/            # 数据与接口
│   │   ├── domain-model.md          # 领域模型
│   │   ├── schema.md                # 数据 Schema
│   │   ├── api-spec.md              # API 规范
│   │   └── state-machine.md         # 状态机定义
│   ├── 05-delivery/                # 交付规划
│   │   ├── task-breakdown.md        # 任务拆解（含 ID/依赖/里程碑）
│   │   └── milestone-plan.md        # 里程碑计划
│   ├── 06-quality/                 # 质量与验收
│   │   ├── acceptance-plan.md      # 验收计划（任务→验收矩阵）
│   │   ├── test-cases.md           # 测试用例
│   │   └── known-gaps.md           # 已知缺口
│   ├── 07-operations/              # 运维
│   │   ├── deployment.md           # 部署说明
│   │   ├── monitoring.md           # 监控需求
│   │   └── rollback.md             # 回滚方案
│   └── 08-history/                 # 变更历史
│       ├── changelog.md            # 变更日志
│       └── decision-log.md          # 决策记录
├── prompts/                        # 逐任务实现 Prompt
│   └── README.md
├── acceptance/                     # 逐任务验收标准
│   └── README.md
├── tasks/                          # 任务面板
│   ├── backlog.md
│   ├── in-progress.md
│   └── done.md
└── reports/
    ├── reviews/                    # 阶段评审报告
    ├── audit/                      # 审计报告
    └── execution/                   # 执行追踪日志
```

---

## 二、页面标准骨架

所有 wiki 页面应遵循以下 5 节结构（`L5` 核心页面必须含全部 5 节）：

```markdown
## 本页目标
<!-- 本页面要回答的核心问题 -->

## 当前结论
<!-- 已确认的内容，含具体数据/规格/决策 -->

## 依赖与关联
<!-- 前置文档、关联页面、依赖关系 -->

## 开放问题 / 风险
<!-- 待确认项、[AUTO-ASSUMPTION] 标注、[AUTO-DECISION] 标注 -->

## 下一步
<!-- 当前阶段的下一步动作 -->
```

**简化版页面**（非核心页面）至少应含：
- 当前结论
- 依赖与关联

---

## 三、文件内容标准

### HOME.md

| 字段 | 要求 |
|------|------|
| 一句话定义 | ≤50 字，精确描述项目核心定位 |
| 当前状态 | 阶段 + 当前目标 + 下一步 |
| 导航链接 | 覆盖所有非空 wiki 目录 |
| 决策摘要 | 最新 3 条，含日期 |
| 风险摘要 | 当前 top 3 风险 |
| 链接有效性 | 所有链接目标文件必须存在 |

### vision.md

| 字段 | 要求 |
|------|------|
| 问题陈述 | 具体（非"效率问题"类泛化描述） |
| 目标用户 | 有明确定义（非"所有人"） |
| 成功标准 | ≥1 条，含数字或明确判定条件 |
| 非目标 | ≥3 条，每条具体 |
| 候选方向 | ≥2 个（孵化阶段允许） |

### user-stories.md

| 字段 | 要求 |
|------|------|
| 格式 | "作为\<角色\>，我希望\<能力\>，以便\<目标\>" |
| MVP 标注 | 每条标注 MVP 或 后续迭代 |
| 数量 | ≥3 条 |
| 可验证性 | 无"系统应该好用"类不可验证表述 |

### system-design.md

| 字段 | 要求 |
|------|------|
| 模块数 | ≥3 个，每模块有名称+职责 |
| 关键链路 | ≥1 条，含输入→处理→输出 |
| 🔴/🟡 标注 | 至少 1 条 🔴 不可逆决策 |
| 候选技术栈 | ≥2 个候选方案 |
| [AUTO-ASSUMPTION] | ≥2 条假设标注 |

### task-breakdown.md

| 字段 | 要求 |
|------|------|
| 任务数 | ≥5 条 |
| 里程碑 | ≥2 个 |
| ID 唯一性 | 无重复 ID |
| 依赖闭合 | 无孤立任务（除非是 T1） |
| MVP 标注 | MVP 范围已标明 |

### deployment.md

| 字段 | 要求 |
|------|------|
| 环境划分 | 至少 local 和 production 两种 |
| 依赖服务 | 含版本要求 |
| 部署步骤 | 可执行命令序列 |
| 回滚入口 | 明确回滚方式 |

---

## 四、快速孵化 vs 完整链路

### 快速孵化（express-incubate）允许的豁免

以下文件在快速孵化模式下允许为空或仅含占位内容（但应有 README 说明）：

| 目录/文件 | 豁免条件 |
|-----------|---------|
| `wiki/02-research/` 全目录 | 快速模式允许为空目录 |
| `wiki/04-data-and-api/` 全目录 | 无后端 API 时允许标注"本项目无后端" |
| `wiki/06-quality/` 全目录 | 快速模式允许仅含 acceptance-plan.md |
| `wiki/07-operations/` 全目录 | 快速模式允许标注"待细化" |
| `reports/` 子目录 | 允许空目录 |

### 完整链路（渐进路径）要求

所有文件必须有实质内容，不允许纯占位。

---

## 五、文件命名规范

| 类型 | 规范 |
|------|------|
| 页面文件 | `kebab-case.md`（如 `user-stories.md`） |
| 目录 | `kebab-case/` |
| 决策文件 | `ADR-NNN.md` 或 `decision-log.md` 内嵌 |
| 评审报告 | `<stage>-<timestamp>.json` |
| 审计报告 | `<timestamp>.json` / `<timestamp>.md` |

---

## 六、评审标注规范

| 标注 | 含义 |
|------|------|
| `[REVIEW: ✓ PASS]` | 文档已通过阶段评审 |
| `[REVIEW: ⚠️ GAPS: ...]` | 文档有缺口，已记录 |
| `[AUTO-ASSUMPTION: ...]` | AI 自行假设（需人工确认） |
| `[AUTO-DECISION: ...]` | AI 自行决策（已执行） |
| `[IMPL-ASSUMPTION: ...]` | 实现阶段发现的假设 |

---

*本文档由 project-audit 引用，用于审计对照。*
*更新时同步至 `.opencode/skills/project-audit/references/PROJECT_WIKI_TEMPLATE.md`*
