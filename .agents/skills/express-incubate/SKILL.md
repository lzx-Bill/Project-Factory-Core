---
name: express-incubate
description: 'Use when the user explicitly wants a fast, one-pass project incubation, such as "快速孵化", "快速出计划", "express plan", "帮我规划一下这个项目". This skill orchestrates the existing Project Factory skills with bounded multi-agent batches, dependency gates, document reviews, execution logging, a final project audit, and one implementation-kit handoff. Do not trigger it for ordinary single-stage planning or when the user requests gradual confirmation at every stage.'
argument-hint: '快速孵化、快速出计划、一气呵成、express plan、项目完整草案'
---

# Express Incubate

把一句项目想法快速推进为可审计、可交接的完整设计草案。它只负责编排，不替代各阶段 Skill。

## When to Use

- 用户明确说“快速孵化”“快速出计划”“一轮生成完整草案”
- 用户接受 AI 对可逆技术选择采用合理默认值
- 目标是设计和实现交接资料，不是直接创建产品代码

## NOT When to Use

- 用户只要求需求、架构、验收等单一阶段
- 用户要求逐阶段确认后再继续
- 关键合规、安全或商业决策尚未确认，继续会造成不可逆影响

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 项目想法、名称、目标用户、已知约束 |
| 已有项目 | 可选；HOME.md、执行 checkpoint 和已完成文档 |

## Output

- `<项目>/HOME.md` 与 `wiki/**` 项目设计文档
- `reports/stage-review/**` 阶段评审报告
- `reports/execution/express-incubate-<timestamp>/**` 执行日志与 checkpoint
- `reports/audit/**` 最终审计报告
- `implementation-kit/**` 唯一一次实现交接输出

## Orchestration Contract

使用当前运行环境实际提供的多 Agent 工具，不在文档中伪造工具调用：

| 动作 | Codex 当前语义 |
|------|----------------|
| 派发独立阶段 | `spawn_agent` |
| 等待阶段完成 | `wait_agent` |
| 补充或重试任务 | `followup_task` |
| 查看运行状态 | `list_agents` |

规则：

- 主 Agent 必须先完整读取本 Skill，以及本阶段要用的每个 Skill。
- 给子 Agent 的任务必须明确要求它完整读取对应 `.agents/skills/<name>/SKILL.md`。
- 主 Agent 占用一个并发槽；子 Agent 数不得超过当前剩余槽位。无法确定时，最多同时运行 3 个子 Agent。
- 只有输出文件互不重叠且输入依赖已完成的阶段才允许并行。
- 每个并行批次必须全部结束并完成 review，才能进入依赖它的下一阶段。
- 主 Agent顺序写 execution-log，避免多个 Agent 并发修改同一个日志文件。

## Pipeline

| Phase | 阶段 | Skill | 主要输入 | 主要输出 | Gate |
|------:|------|-------|----------|----------|------|
| 0 | 启动/恢复 | `execution-log` | 用户输入、已有 checkpoint | 执行目录、项目名 | 检查是否续跑 |
| 1 | 项目启动 | `project-bootstrap` | 用户想法 | HOME、最小 wiki 内容、目录骨架 | stage-review |
| 2 | 方向探索 | `incubation-discovery` | HOME、vision 初稿 | idea-landscape、scenario-matrix | stage-review |
| 3 | 项目定界 | `overview-framing` | Phase 2 | vision、scope、glossary | stage-review |
| 4 | 需求澄清 | `requirements-spec` + `assumptions-tracking` | Phase 3 | user-stories、constraints、assumptions、open-questions | stage-review |
| 5 | 研究验证 | `research-spikes` | 未验证的关键假设 | technical-spikes、market-notes（按需） | 关键假设有结论 |
| 6 | 架构与契约 | `architecture-decisions` → `data-api-design` | 需求、研究结论 | system-design、tech-stack、module-map、data/API 文档 | 顺序执行并 review |
| 7 | 基线一致性 | `consistency-review` | Phase 3-6 | consistency-report | 高严重度矛盾为 0 |
| 8 | 派生设计 | 见下方批次 | 已通过一致性的架构/API | UI、安全、性能、测试、对抗性场景 | 全部完成并 review |
| 9 | 设计一致性 | `consistency-review` | Phase 8 全部输出 | 更新 consistency-report | 高严重度矛盾为 0 |
| 10 | 交付与量化验收 | `delivery-planning` → `quantified-acceptance` | 所有设计文档 | task-breakdown、里程碑、quantified-checklist | 依赖闭合 |
| 11 | 交付配套 | 见下方批次 | Phase 10 | 风险、验收、运维、历史、HOME | 全部完成并 review |
| 12 | 收尾交接 | `project-audit` → `implementation-kit` | 完整项目 | 审计报告、implementation-kit | 审计无 BLOCKER |

### Phase 8 派生设计批次

可并行执行，但受可用并发槽限制，超过容量时分波次：

| Skill | 输出 |
|-------|------|
| `ui-design` | `wiki/03-architecture/ui-design.md` |
| `security-design` | `wiki/03-architecture/security.md` |
| `performance-design` | `wiki/03-architecture/performance.md` |
| `test-strategy` | `wiki/06-quality/test-strategy.md` |
| `adversarial-scenarios` | `wiki/03-architecture/threat-scenarios.md` |

性能和测试必须在 `api-spec.md` 已存在后执行。Phase 9 必须等待五项设计全部完成。

### Phase 11 交付配套批次

先并行执行以下互不重叠的任务：

- `risk-register` → `wiki/02-research/risk-register.md`
- `acceptance-design` → `wiki/06-quality/acceptance-plan.md` 与 `acceptance/**`
- `operations-planning` → `wiki/07-operations/**`

全部完成后再顺序执行：

1. `history-sync` 汇总实际变更和决策。
2. `home-navigation` 更新阶段、下一步、风险和导航。
3. `project-audit standard`；有 BLOCKER 就修复并重审。
4. `implementation-kit` 只调用一次，并等待完成。

## Stage Execution

每个阶段统一执行以下最小循环：

1. 读取阶段 Skill 和已完成的上游文档。
2. 派发一个范围明确、文件所有权不重叠的子任务。
3. 等待产出完成，检查文件存在、非空、关键章节齐全。
4. 使用 `stage-review`：默认只报告；仅机械性缺口可用 `mode=fix`。
5. FAIL 时对原子阶段补充任务并重试一次；仍失败则记录 BLOCKER，不得假装完成。
6. 主 Agent 写入 stage-end 日志和 checkpoint。

## Decision Policy

| 类型 | 处理 |
|------|------|
| 不可逆业务、法律、合规、安全决策 | 暂停管线并向用户确认 |
| 会改变范围或主要成本的关键未决项 | 暂停管线并向用户确认 |
| 可逆技术选择 | 选择维护成本最低的合理默认值，记录 `[AUTO-DECISION]` |
| 信息不足但不阻塞后续 | 写入 assumptions/open-questions，继续 |
| 格式或缺字段 | `stage-review mode=fix` 自动修复 |

## Recovery

- checkpoint 唯一键为 phase ID；同一 phase 重跑时更新，不追加重复完成记录。
- 发现已有项目和 checkpoint 时，先询问用户续跑还是重新开始。
- “重新开始”只清理本次执行报告；不得删除已有 wiki 或用户内容。
- 子任务失败最多重试一次；不能证明完成的阶段必须保留为未完成。

## Minimum Viable Output

- Phase 1-10 的核心设计链完整
- 所有阶段有 review 结果与 checkpoint
- 无未处理的高严重度一致性问题
- project-audit 无 BLOCKER

## Complete Output

- Minimum Viable Output 全部满足
- Phase 11 配套文档完整
- HOME 导航、任务、Prompt、验收和报告可追踪
- implementation-kit 生成且数量与任务一致

## Dependencies

- 阶段产出：`project-bootstrap`、`incubation-discovery`、`overview-framing`、`requirements-spec`、`research-spikes`、`architecture-decisions`、`data-api-design`、`ui-design`、`security-design`、`performance-design`、`test-strategy`、`adversarial-scenarios`、`delivery-planning`、`quantified-acceptance`、`risk-register`、`acceptance-design`、`operations-planning`、`history-sync`、`home-navigation`
- 质量与追踪：`assumptions-tracking`、`consistency-review`、`stage-review`、`execution-log`、`project-audit`
- 后置：`implementation-kit`

## Target Pages

- `<项目根目录>/HOME.md`
- `<项目根目录>/wiki/**`
- `<项目根目录>/reports/**`
- `<项目根目录>/implementation-kit/**`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-07-15 | v9：改用当前 Codex 多 Agent 语义；按可用槽位分批；修复 API、设计、交付和历史阶段依赖；统一 review/提问/恢复契约；implementation-kit 改为唯一一次同步调用 | 修复 v8 工具失效、依赖倒置、并发越限、文件竞写和重复交接 |
| 2026-04-30 | v8：扩展一致性、派生设计和量化验收阶段 | 完善快速孵化覆盖面 |
