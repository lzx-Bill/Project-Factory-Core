---
name: project-audit
description: 'Use when auditing a project for completeness, consistency, and readiness — "audit project", "项目审计", "check project", "verify project", "检查项目", "review project". This skill checks directory structure, file completeness, navigation consistency, cross-file coherence, traceability, standards compliance, and phase compliance. Different from stage-review (single stage) — this is a whole-project audit. Can be invoked with depth: quick/standard/deep.'
argument-hint: '项目审计、完整性检查、一致性验证、项目review'
---

# Project Audit

全项目级别的结构和内容审计。不同于 `stage-review`（单阶段文档质量），`project-audit` 检查跨文件、跨目录的全量一致性。

## 定位

| 维度 | 说明 |
|------|------|
| 目标 | 发现项目中结构不全、内容矛盾、链接断裂、规范违规、重复条目、阶段标记过期 |
| 输入 | 项目根目录 |
| 输出 | 结构化审计报告（JSON + Markdown） |
| 与 stage-review 区别 | stage-review 验单文档质量；project-audit 验整体一致性 |

## When to Use

- 快速孵化完成后（`express-incubate` 末尾）
- 阶段切换前（需求→架构、架构→交付）
- 生成 `implementation-kit` 之前
- 用户说"检查项目"、"审计"、"verify"、"review project"
- 用户说"分析孵化情况"、"看看还有什么缺的"

## Input

| 来源 | 内容 | 必读 |
|------|------|------|
| 项目目录 | `<项目根目录>/` 完整递归文件列表 | ✅ |
| 模板参考 | `PROJECT_WIKI_TEMPLATE.md`（标准结构和页面骨架） | ✅ |
| HOME.md | 首页导航、阶段标记、决策摘要、风险摘要 | ✅ |
| 所有 wiki 文件 | 逐文件读取内容 | deep 模式 ✅ |

## Output

### Output Schema

```json
{
  "project": "<项目名>",
  "timestamp": "ISO 8601",
  "depth": "quick|standard|deep",
  "score": 75,
  "verdict": "PASS|WARNING|NEEDS_FIX|BLOCKED",
  "categories": {
    "structure": {"status": "PASS|WARNING|BLOCKER", "score": 0-100, "issues": [...]},
    "files": {"status": "...", "score": 0-100, "issues": [...]},
    "navigation": {"status": "...", "score": 0-100, "issues": [...]},
    "coherence": {"status": "...", "score": 0-100, "issues": [...]},
    "traceability": {"status": "...", "score": 0-100, "issues": [...]},
    "compliance": {"status": "...", "score": 0-100, "issues": [...]},
    "phase": {"status": "...", "score": 0-100, "issues": [...]}
  },
  "findings": {
    "blockers": [{"id": "F1", "desc": "...", "fix": "..."}],
    "warnings": [{"id": "C5", "desc": "...", "fix": "..."}],
    "infos": [{"id": "N2", "desc": "...", "suggestion": "..."}]
  }
}
```

### Minimum Viable Output

最少包含：
- 7 个维度的 pass/warning/blocker 判定
- 每个异常的检查项 ID、描述、修复建议
- 总分和 verdict

### Complete Output

完整输出包含：
- Minimum Viable Output 全部内容
- 每个异常的具体文件路径和行号
- 深度模式下逐文件内容质量评定
- 修复优先级排序
- `reports/audit/<timestamp>.json` + `reports/audit/<timestamp>.md`

### 文件产出

| 文件 | 说明 |
|------|------|
| `reports/audit/<timestamp>.json` | 结构化审计数据 |
| `reports/audit/<timestamp>.md` | 人类可读审计报告 |

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 项目至少完成快速孵化（有 HOME.md + 最小文件集） |
| 后置 | 修复审计问题后可进入下一阶段 |
| 依赖读取 | `PROJECT_WIKI_TEMPLATE.md`（模板标准） |

## Procedure

### Phase 1: 确定审计深度

| 深度 | 检查范围 | 适用场景 |
|------|---------|---------|
| `quick` | ①结构(S1-S4) + ②文件(F1-F5) + ③导航(N1) + ⑦阶段(P1-P2) | express-incubate 后快速扫一眼 |
| `standard` | 全部 7 维度所有检查项 | 阶段切换、kit 生成前 |
| `deep` | standard + 逐文件内容质量分析 + 统一页面骨架合规 | 验收/交接前 |

### Phase 2: 7 维度逐项检查

#### ① 结构完整性（Structure）

检查实际目录结构 vs 模板结构。

| ID | 检查项 | 判定 |
|----|--------|------|
| S1 | 所有模板目录存在 | 缺失目录 = 🟡 WARNING |
| S2 | 目录中至少有一个文件 | 完全空目录 = 🟡 WARNING（除非有 README 声明跳过） |
| S3 | 无无关目录/文件 | 非模板目录 = 🟢 INFO |
| S4 | 任务 ID 无重复（task-breakdown.md 和 backlog.md） | 重复 ID = 🔴 BLOCKER |

**express-incubate 特例**：以下目录在快速模式下允许为空的（但应有 README 说明）：
- `wiki/02-research/`、`wiki/04-data-and-api/`、`wiki/06-quality/`、`wiki/07-operations/`
- `reports/` 子目录

#### ② 文件完整性（Files）

检查各目录下的文件是否齐全。

| ID | 检查项 | 判定 |
|----|--------|------|
| F1 | 最小文件集存在 | 缺失最小文件 = 🔴 BLOCKER |
| F2 | task-breakdown.md 与 backlog.md 任务 ID 一致 | 不一致 = 🔴 BLOCKER |
| F3 | implementation-kit 的 prompt 数与 task 数一致 | 不一致 = 🟡 WARNING |
| F4 | implementation-kit 的 acceptance 数与 task 数一致 | 不一致 = 🟡 WARNING |
| F5 | tasks/ 目录完整：backlog.md + in-progress.md + done.md | 缺 in-progress 或 done = 🟡 WARNING |
| F6 | 阶段相关关键交付物存在（见下表） | 缺失 = 🟡 WARNING |
| F7 | reports/ 子目录有实际内容（非空目录） | 空目录 = 🟢 INFO |

**最小文件集**（即使快速模式也应存在）：
- `HOME.md`, `wiki/00-overview/vision.md`, `wiki/00-overview/scope.md`
- `wiki/01-requirements/user-stories.md`, `wiki/01-requirements/constraints.md`
- `wiki/01-requirements/assumptions.md`, `wiki/01-requirements/open-questions.md`
- `wiki/03-architecture/system-design.md`
- `wiki/05-delivery/task-breakdown.md`, `tasks/backlog.md`

**F6 阶段-交付物映射**：

| 项目阶段 | 期望存在的关键交付物 | 缺失判定 |
|----------|---------------------|---------|
| 需求澄清后 | `user-stories.md`、`constraints.md`、`assumptions.md` | 🟡 WARNING |
| 调研验证后 | `wiki/02-research/technical-spikes.md`、`wiki/02-research/risk-register.md` | 🟡 WARNING |
| 架构设计后 | `system-design.md`（≥3 模块）、`tech-stack.md` | 🟡 WARNING |
| 一致性审查后 | `wiki/06-quality/consistency-report.md`（高严重矛盾已处理） | 🟡 WARNING |
| 设计并行批次后 | `ui-design.md`、`security.md`、`performance.md`、`test-strategy.md`、`threat-scenarios.md` | 🟡 WARNING |
| 交付规划后 | `task-breakdown.md`（≥5 任务）、`tasks/in-progress.md`、`tasks/done.md` | 🟡 WARNING |
| 设计验收后 | `wiki/06-quality/acceptance-plan.md`、`wiki/06-quality/quantified-checklist.md` | 🟡 WARNING |
| 运营规划后 | `wiki/07-operations/deployment.md` | 🟡 WARNING |
| implementation-kit 存在 | 说明至少完成架构设计，应检查上述所有阶段交付物 | 加权判定 |

#### ③ 导航一致性（Navigation）

| ID | 检查项 | 判定 |
|----|--------|------|
| N1 | HOME.md 所有链接目标文件存在 | 断裂链接 = 🔴 BLOCKER |
| N2 | HOME.md 链接覆盖所有非空 wiki 目录 | 遗漏 = 🟡 WARNING |
| N3 | wiki 间交叉引用有效 | 断裂 = 🟡 WARNING |

**N2 增强**：如果项目已生成 implementation-kit，HOME.md 导航至少应覆盖：
- `wiki/02-research/risk-register.md`（风险登记）
- `wiki/06-quality/acceptance-plan.md`（验收计划）
- `wiki/07-operations/deployment.md`（部署说明）

#### ④ 内容一致性（Coherence）

| ID | 检查项 | 判定 |
|----|--------|------|
| C1 | task-breakdown 的 ID、名称、依赖与 backlog 完全一致 | 不一致 = 🔴 BLOCKER |
| C2 | 架构模块被至少 1 条用户故事覆盖 | 未覆盖 = 🟡 WARNING |
| C3 | 交付任务覆盖所有架构模块 | 未覆盖 = 🟡 WARNING |
| C4 | 无前后矛盾假设（同一假设在不同文件中状态不同） | 矛盾 = 🟡 WARNING |
| C5 | HOME.md 风险摘要中的风险 ID 与 risk-register.md 一致 | 不一致 = 🟡 WARNING |
| C6 | task-breakdown 表中无重复行（同一任务 ID 多次出现） | 重复 = 🔴 BLOCKER |
| C7 | HOME.md 声明的阶段与文档实际成熟度一致 | 不一致 = 🟡 WARNING |

**C7 增强规则**：
- 如果 `implementation-kit/` 已存在且有内容，但 HOME.md 阶段写"架构设计中"→ WARNING（应至少为"设计验收"）
- 如果 `wiki/05-delivery/task-breakdown.md` 有完整任务拆解，但 HOME.md 阶段写"需求澄清中"→ WARNING

#### ⑤ 可追踪性（Traceability）

| ID | 检查项 | 判定 |
|----|--------|------|
| T1 | 每个任务可映射到 prompt（`prompts/` 或 `implementation-kit/prompts/`） | 无映射 = 🟡 WARNING |
| T2 | 每个任务可映射到 acceptance | 无映射 = 🟡 WARNING |
| T3 | 关键决策有记录（`HOME.md` 决策表 或 `wiki/08-history/decision-log.md`） | 无记录 = 🟡 WARNING |
| T4 | acceptance-plan.md 中的追踪矩阵完整（任务→prompt→acceptance→report 全链路） | 不完整 = 🟢 INFO |
| T5 | express-incubate 孵化项目存在 execution-log | 缺失 = 🟡 WARNING |

**T5 执行记录检查**：
- 检查 `reports/execution/express-incubate-*/summary.md` 是否存在
- 如果 implementation-kit 存在但 execution-log 缺失 → 🟡 WARNING（说明孵化被中断或 skill 版本不支持）
- 如果项目使用旧流程（无 express-incubate），检查是否有 `reports/execution/` 目录及 README 说明
- execution-log 是 express-incubate 项目的**必需产出**，缺失表明孵化流程不完整

#### ⑥ 规范合规（Compliance）

| ID | 检查项 | 判定 |
|----|--------|------|
| L1 | 所有文档使用中文 | 非中文 = 🟡 WARNING |
| L2 | 关键页面有 `[REVIEW: ...]` 标注 | 缺失 = 🟢 INFO |
| L3 | implementation-kit 含所有工具适配文件（AGENTS.md、AGENTS.md、.cursor/rules/、.github/copilot-instructions.md） | 缺失某工具 = 🟢 INFO |
| L4 | user-stories.md 使用标准格式（"作为\<角色\>，我希望\<能力\>，以便\<目标\>"） | 未使用 = 🟢 INFO |
| L5 | 核心页面遵循统一页面骨架（本页目标、当前结论、依赖与关联、开放问题/风险、下一步） | 缺失槽位 = 🟢 INFO |
| L6 | deployment.md 含最低内容：环境划分 + 依赖服务 + 部署步骤 + 回滚入口 | 缺失 = 🟡 WARNING |

**L5 核心页面清单**（deep 模式下检查）：
- `wiki/00-overview/vision.md`
- `wiki/00-overview/scope.md`
- `wiki/03-architecture/system-design.md`
- `wiki/04-data-and-api/api-spec.md`
- `wiki/07-operations/deployment.md`

**L6 最低内容判定**：
- 环境划分：至少有 local 和 production/docker 两种环境的说明
- 依赖服务：列出运行时依赖（含版本要求）
- 部署步骤：可执行的命令序列
- 回滚入口：明确的回滚方式

#### ⑦ 阶段合规（Phase）

| ID | 检查项 | 判定 |
|----|--------|------|
| P1 | HOME.md 声明的阶段与实际文档状态匹配（参见 C7） | 不一致 = 🟡 WARNING |
| P2 | 如果声明"设计完成"，所有最小文件有实质内容 | 空文件或仅占位 = 🔴 BLOCKER |
| P3 | 已存在的页面有实质内容（非仅骨架/TODO/待补充占位） | 空洞页面较多 = 🟡 WARNING |
| P4 | 无矛盾状态信号（如 "当前目标：实现 PoW 求解器" 但 implementation-kit 已存在） | 矛盾 = 🟡 WARNING |

**P3 实质内容判定**：
- 页面非空
- 至少有一节具体内容（不只是"待补充"或"TODO"）
- 无大面积空白表格

### Phase 3: 输出报告

1. 汇总每个维度的 PASS/WARNING/BLOCKER/INFO
2. 计算总分（每个 WARNING -5，BLOCKER -15）
3. 对每个异常给出：检查项 ID、描述、具体文件路径/行号、修复建议
4. 按严重性排序：BLOCKER → WARNING → INFO
5. 生成 `reports/audit/<timestamp>.json` 和 `.md`
6. 呈现给用户，用 `question` 收集反馈

## 评分计算

```
总分 = 100
- BLOCKER × 15
- WARNING × 5
- INFO × 0
最低 0 分
```

| 分数 | 判定 |
|------|------|
| 90-100 | ✅ PASS — 可以进入下一阶段 |
| 70-89 | ⚠️ WARNING — 有改进空间，不阻塞 |
| 40-69 | 🔴 NEEDS FIX — 建议修复后再推进 |
| 0-39 | 🚫 BLOCKED — 必须修复 |

## 检查项密度矩阵

| 深度 | 包含检查项 | 检查项数量 |
|------|-----------|-----------|
| quick | S1-S4, F1-F5, N1, P1-P2 | 11 项 |
| standard | 全部 S/F/N/C/T/L/P | 32 项（T5 新增） |
| deep | standard + L5 逐文件 | 32+ 项 |

## Target Pages

- `<项目根目录>/reports/audit/<timestamp>.json`
- `<项目根目录>/reports/audit/<timestamp>.md`

## Enriched Behavior

### 执行前环境检查

执行审计前，必读以下文件以获取基准：
1. `PROJECT_WIKI_TEMPLATE.md` — 获取标准结构定义
2. `<项目>/HOME.md` — 获取项目当前阶段声明
3. 根据深度决定是否读取所有 wiki 文件

### 自检机制

完成审计后，对照本 skill 的检查项清单自查：是否每一项都实际执行了（而非仅凭印象判断）。

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | v2.2 更新 F6 阶段映射表：新增一致性审查、设计并行批次（ui/security/performance/test/threat-scenarios）、量化验收等新阶段 | express-incubate v8 新增阶段，旧映射表已过时 |
| 2026-04-27 | v2.1 新增 T5 检查项：express-incubate 孵化项目必须存在 execution-log | 复盘发现多个项目因 session 中断或 skill bug 导致 execution-log 缺失，影响孵化追溯性 |
| 2026-04-26 | v2.0 重大增强：新增 11 项检查（S4/F5-F7/C5-C7/L4-L6/P3-P4/T4），补充 Input/Output Schema、Minimum/Complete Output、Enriched Behavior | 对 deepseek-web-proxy 审计发现原有 skill 遗漏了重复 ID、面板不完整、阶段标记过期、文档格式合规等 6 类问题 |
| 2026-04-26 | 新建 skill | 全项目级别审计：7维度×3深度×4严重级别，填补 stage-review 无法覆盖的跨文件一致性问题 |
