---
name: express-incubate
description: 'Use when the user wants a FAST, one-pass project incubation — "quick incubate", "express plan", "快速孵化", "快速出计划", "5 minute plan", "draft a project plan", "give me a quick overview", "帮我想想这个项目怎么做", "帮我规划一下". This skill ORCHESTRATES 11 phases using multi-agent parallel subagents. Five design skills (ui-design, security-design, performance-design, test-strategy, adversarial-scenarios) run simultaneously in Phase 6. Three-level quality gate: pre-check → stage-review (synchronous for critical stages, async for derived) → final consistency check. 🔴 asks user for irreversible business decisions; 🟡 AI self-decides technical choices. Output: complete project draft + execution log + review reports.'
argument-hint: '快速孵化、快速出计划、一气呵成、快速草案、express plan、项目概览、multi-agent孵化、帮我规划一下、想想这个项目怎么做'
---

# Express Incubate v8 — Codex Multi-Agent Pipeline

AI 驱动的快速项目孵化管线。一句话想法 → 完整项目草案，平均 15-20 分钟完成。

## 定位

| 维度 | 说明 |
|------|------|
| 角色 | **Multi-Agent 管线编排器**，不自己做产出、不做评审、不做日志 |
| 委托 | 阶段产出 → 按 stage 派发 `Agent(...)` subagent；评审 → `stage-review`；日志 → `execution-log` |
| 提问策略 | 🔴 不可逆业务决策 → 问用户；🟡 技术决策 → AI 自决 |
| 质量闸门 | Gate 1 预检（orchestrator 内联）→ Gate 2 正式评审（stage-review）→ Gate 3 收尾复审 |
| 输出 | 完整项目草案 + 执行日志 + 全阶段评审报告 |

## When to Use

- "快速孵化"、"5 分钟出计划"、"帮我想想这个项目"

## NOT When to Use

- 需求已确定 → 走渐进链路
- 涉及硬件、合规、安全等不可逆决策密集型领域

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 一句话项目想法、目标用户（如有）、约束（如有） |

## Output

| 类别 | 产出 |
|------|------|
| 项目文档 | HOME.md + wiki 各页面（11 阶段标准产出） |
| 评审报告 | `reports/stage-review/<stage>-<timestamp>.json`（每阶段 1 份） |
| 执行日志 | `reports/execution/express-incubate-<timestamp>/log.json` + `summary.md` |

---

## 架构：Multi-Agent 编排

```
┌────────────────────────────────────────────────────────────────────────┐
│               Express-Incubate Orchestrator                              │
│               (主 agent, 仅做编排，不产出内容)                               │
│                                                                        │
│  Phase 0: 管线启动                                                       │
│  Phase 1-5: 关键阶段 (同步 subagent + 同步 review, 阻塞通过)             │
│  Phase 5b: 一致性审查 (consistency-review gate, 阻塞)                    │
│  Phase 6:   设计并行批次 (5 design skills 并行 + 异步 review)            │
│  Phase 7:   交付规划 (delivery-planning + quantified-acceptance, 同步)   │
│  Phase 8-10: 并行批次 (5 subagent 同时跑 + 异步 review)                  │
│  Phase 11:  收尾 — 收集 review 结果, GAP 修复, implementation-kit        │
└──────┬───────┬───────┬───────┬───────┬───────────┬─────────────────────┘
       │       │       │       │       │           │
  ┌────▼──┐ ┌─▼───┐ ┌─▼───┐ ┌─▼───┐ ┌─▼───────────▼──────────────────┐
  │Stage 1│ │Stg 2│ │Stg 3│ │Stg 4│ │Stage 5b (deep, 阻塞)          │
  │quick  │ │deep  │ │deep  │ │deep  │ │  consistency-review            │
  └───┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └────┬───────────┬──────────────┘
      │        │        │        │          │           │
      └────────┴────────┴────────┴──────────┴───────────┘
                    (同步, 逐阶段通过 Gate 2 才放行)
                             │
                    ┌────────▼────────┐
                    │  Phase 6        │
                    │  设计并行批次    │
                    │  (5 并行, 异步) │
                    └───────┬─────────┘
                            │
     ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
     │Stage 6a │  │Stage 6b │  │Stage 6c │  │Stage 6d │  │Stage 6e │
     │ ui-     │  │security- │  │perfor-  │  │test-     │  │adversar-│
     │ design  │  │design    │  │mance    │  │strategy  │  │ial-scen.│
     │(deep)   │  │(deep)   │  │(deep)   │  │(deep)   │  │(deep)   │
     └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
          │             │             │             │             │
          └─────────────┴─────────────┴─────────────┴─────────────┘
                    (五个并行, run_in_background=true)
                             │
                    ┌────────▼────────┐
                    │  Phase 7       │
                    │  delivery +   │
                    │  quant-accept │
                    │  (deep, 同步) │
                    └───────┬────────┘
                            │
     ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
     │ Stage 8a │  │ Stage 8b │  │ Stage 9a │  │ Stage 9b │  │ Stage 10 │
     │ risk-reg │  │ api-spec │  │ accept-  │  │ ops-     │  │ history  │
     │ (deep)   │  │ (deep)   │  │ plan(deep)│  │ plan(deep)│  │ (quick)  │
     └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
          │             │             │             │             │
          └─────────────┴─────────────┴─────────────┴─────────────┘
                    (五个并行, run_in_background=true)
                       │
                 ┌─────▼─────┐
                 │ Phase 11  │
                 │ 收尾汇总   │
                 │ + impl-   │
                 │ kit       │
                 └───────────┘
```

---

## 阶段 → Agent 映射

| 阶段 | Agent Category | 加载 Skill | Review 模式 | 依赖 |
|------|---------------|-----------|------------|------|
| ① bootstrap | `quick` | `project-bootstrap` | **同步阻塞** | 用户输入 |
| ② incubation | `deep` | `incubation-discovery` | **同步阻塞** | ① HOME.md |
| ③ overview | `deep` | `overview-framing` | **同步阻塞** | ② idea-landscape |
| ④ requirements | `deep` | `requirements-spec` + `adversarial-scenarios` | **同步阻塞** | ③ vision+scope |
| ⑤ architecture | `deep` | `architecture-decisions` | **同步阻塞** | ④ user-stories |
| ⑤b consistency | `deep` | `consistency-review` | **同步阻塞** | ④ + ⑤ 产出 |
| ⑥a ui-design | `deep` | `ui-design` | 异步后台 | ⑤ system-design |
| ⑥b security | `deep` | `security-design` | 异步后台 | ⑤ system-design |
| ⑥c performance | `deep` | `performance-design` | 异步后台 | ⑤ system-design |
| ⑥d test-strategy | `deep` | `test-strategy` | 异步后台 | ⑤ system-design |
| ⑥e adversarial | `deep` | `adversarial-scenarios` | 异步后台 | ④ user-stories |
| ⑦ delivery | `deep` | `delivery-planning` + `quantified-acceptance` | **同步阻塞** | ⑤b 一致性通过 |
| ⑧a risk | `deep` | `risk-register` | 异步后台 | ①-⑦ 全部 |
| ⑧b api | `deep` | `data-api-design` | 异步后台 | ⑤ system-design |
| ⑨a quality | `deep` | `acceptance-design` | 异步后台 | ⑦ task-breakdown |
| ⑨b ops | `deep` | `operations-planning` | 异步后台 | ⑤ system-design |
| ⑩ history | `quick` | `history-sync` | 异步后台 | ①-⑨ 全部 |

> **⚠ Phase 6 设计批次说明**：ui-design / security-design / performance-design / test-strategy / adversarial-scenarios 五路并行。adversarial-scenarios 依赖 user-stories（④），其余依赖 system-design（⑤）。所有设计 skill 的 decision-log 记录由 orchestrator 在 Phase 11 统一汇总，不在各 subagent 中分别执行。

> **⚠ Phase 7 含两个 skill**：`delivery-planning` 和 `quantified-acceptance` 合并为同一 subagent，避免跨文档引用时序问题。

> **⚠ Phase ⑧⑨⑩ 拆分原因**：同 v7——避免单 agent 上下文过重超时。

---

## 三级质量闸门

```
Stage N subagent 产出文档
  │
  ├─ 🚦 Gate 1: 预检（orchestrator 内联, ~2s）
  │   规则：文件存在？非空？章节完整？与前一阶段矛盾？
  │   → FAIL → 重新派发本阶段 subagent（最多 1 次）
  │   → PASS → 进入 Gate 2
  │
  ├─ 🚦 Gate 2: 正式评审（Agent + stage-review skill）
  │   ● 阶段 ①-⑤: run_in_background=false, 同步等待 PASS 才放行
  │   ● 阶段 ⑥-⑨: run_in_background=true, 异步后台, 不阻塞管线
  │   → PASS → 标注 [REVIEW: ✓ PASS] → 记录 execution-log → 继续
  │   → PASS_WITH_GAPS (可自修) → auto-fix → 重审 → 继续
  │   → PASS_WITH_GAPS (不可修) → 记录 gap → 🔴 问用户 / 🟡 自决 → 继续
  │   → FAIL → 重新派发本阶段 subagent（最多 1 次）→ 重审
  │
  └─ 🚦 Gate 3: 收尾复审（Phase 10）
      收集全部异步 review 结果 → 跨阶段一致性检查(C1-C4)
      → 发现残留问题 → 重跑受影响阶段 subagent → 更新文档
```

**为什么基础阶段用同步 review**：阶段 ② 遗漏关键画像 → ③ 范围偏差 → ⑤ 架构对不上需求，错误**级联放大**。基础阶段必须验证通过才能进入下一阶段。

**为什么派生阶段用异步 review**：⑥⑦⑧⑨ 基于已验证的 ①-⑤ 产出，错误是**局部**的（格式不对、缺字段），不会污染其他文档。

---

## Procedure

### Phase 0: 管线启动 + 中断恢复检查

1. **检查项目是否已存在**（中断恢复）：
   - 检查 `{项目根目录}/HOME.md` 是否存在
   - 检查 `reports/execution/express-incubate-*/summary.md` 是否存在
   - 如果项目存在但无 execution-log → 记录 `[LEGACY: 无 execution-log]`，继续执行
   - 如果项目存在且有 execution-log → 检查已完成阶段

2. **中断恢复判断**：
   ```
   IF 项目已存在 AND execution-log 存在 THEN
     读取 summary.md 获取已完成阶段列表
     ASK 用户: "检测到项目 {项目名} 已存在部分孵化记录，是否要继续未完成阶段？"
     - 继续: 从最后一个未完成阶段继续（跳过已完成的阶段）
     - 重启: 删除现有项目，重新开始
   ELSE
     继续执行新孵化
   ```

3. **fire execution-log**（幂等写入，记录管线 start + skill 版本）：
   ```
   Agent(
     subagent_type="Explore",
     load_skills=["execution-log"],
     run_in_background=true,
     prompt="Log pipeline start for express-incubate. Project: {项目名}. Skill version: v8.
             If checkpoint exists, update existing log instead of creating duplicate."
   )
   ```

4. 提取用户想法、目标用户、约束
5. 创建项目目录结构（如果不存在）

### Phase 1-5: 关键基础阶段（同步 subagent + 同步阻塞 review）

每阶段执行循环，以阶段 ② 为例：

```
Step A: 派发 subagent 产出文档
  Agent(
    subagent_type="general-purpose",
    load_skills=["incubation-discovery"],
    run_in_background=false,
    prompt="
TASK: 为项目 {项目名} 产出孵化发散文档
EXPECTED OUTCOME:
  - wiki/00-overview/idea-landscape.md (≥2 用户画像 + ≥2 场景 + ≥3 候选方向)
  - wiki/00-overview/scenario-matrix.md (场景×价值×风险矩阵)
REQUIRED TOOLS: Read, Write, Edit
MUST DO: 基于 HOME.md({HOME.md内容}) 发散。用户画像具体、场景可操作、方向有差异化。
MUST NOT DO: 不写代码、不讨论技术栈、不决定最终方案（那是 overview 阶段的事）
CONTEXT: 项目根目录 {项目路径}。前一阶段产出 HOME.md 已就绪。
")

Step B: Gate 1 预检
  - 检查 idea-landscape.md 存在、非空、含 ≥2 画像 ≥2 场景 ≥3 方向
  - 失败 → 重新派发 subagent（补充: "产出不完整，请补足...")

Step C: Gate 2 正式同步评审
  Agent(
    subagent_type="general-purpose",
    load_skills=["stage-review"],
    run_in_background=false,
    prompt="
TASK: 评审阶段 ② incubation 产出
REQUIRED TOOLS: Read, Write, Edit
MUST DO: 加载 stage-review skill 的 checklist。对 idea-landscape.md 和 scenario-matrix.md 逐项检查。
  输出评审报告到 reports/stage-review/incubation-{timestamp}.json
  PASS → 在文档末尾标注 [REVIEW: ✓ PASS]
  PASS_WITH_GAPS 可自修 → auto-fix → 重审
  PASS_WITH_GAPS 不可修 → 标注 gap，返回 orchestrator 处理
  FAIL → 返回原因
")

Step D: 处理评审结果
  - PASS → 继续
  - PASS_WITH_GAPS (可自修) → subagent 已 auto-fix, 继续
  - PASS_WITH_GAPS (不可修) → 🔴 业务 → askQuestions 问用户(不阻塞), 记录 → 继续
                              🟡 技术 → AI 自决, 记录 → 继续
  - FAIL → 重新派发 subagent → 回到 Step B

Step E: 记录 execution-log stage-end
  Agent(
    subagent_type="Explore",
    load_skills=["execution-log"],
    run_in_background=true,
    prompt="Log stage-end: incubation. Result: PASS. Outputs: idea-landscape.md, scenario-matrix.md"
  )
```

**阶段 ①(bootstrap) 差异**：用 `subagent_type="general-purpose"`, `load_skills=["project-bootstrap"]`。产出 **仅** `HOME.md` + wiki 骨架目录。

**wiki 骨架规范**（bootstrap 必须创建）：

| 目录 | bootstrap 必须创建的初始文件 |
|------|---------------------------|
| `wiki/00-overview/` | `vision.md`、`scope.md`、`glossary.md`、`idea-landscape.md`、`scenario-matrix.md`（可为空或占位内容） |
| `wiki/01-requirements/` | `user-stories.md`、`constraints.md`、`assumptions.md`、`open-questions.md` |
| `wiki/02-research/` | `market-notes.md`、`technical-spikes.md`、`risk-register.md`、`opportunity-backlog.md` |
| `wiki/03-architecture/` | `tech-stack.md`、`system-design.md`、`module-map.md`、`ui-design.md`、`security.md`、`performance.md`、`threat-scenarios.md` |
| `wiki/04-data-and-api/` | `domain-model.md`、`schema.md`、`api-spec.md`、`state-machine.md` |
| `wiki/05-delivery/` | `task-breakdown.md`、`milestone-plan.md` |
| `wiki/06-quality/` | `acceptance-plan.md`、`test-cases.md`、`known-gaps.md`、`consistency-report.md`、`quantified-checklist.md`、`test-strategy.md` |
| `wiki/07-operations/` | `deployment.md`、`monitoring.md`、`rollback.md` |
| `wiki/08-history/` | `changelog.md`、`decision-log.md` |
| `prompts/` | `README.md` |
| `acceptance/` | `README.md` |
| `tasks/` | `backlog.md`、`in-progress.md`、`done.md` |
| `reports/` | `reviews/` 目录 |

> **注意**：这些文件在 bootstrap 阶段可以是**空文件或最小占位内容**（如"待补充"），具体内容由后续阶段填充。bootstrap 的职责是**建立目录结构**，不是产出内容。

MUST NOT DO 中明确要求：**不创建 vision.md / user-stories.md / assumptions.md 等内容文件（那是后续阶段的事），不越界产出后续阶段内容。**

**阶段 ③(overview) 差异**：用 `load_skills=["overview-framing"]`。输入为 ② 的 idea-landscape。产出 `vision.md` + `scope.md` + `glossary.md`。

**阶段 ④(requirements) 差异**：用 `load_skills=["requirements-spec", "adversarial-scenarios"]`。输入为 ③ 的 vision+scope。产出 `user-stories.md` + `constraints.md`。adversarial-scenarios 在 requirements 阶段完成后立即执行，依赖 user-stories 输出。

**阶段 ⑤(architecture) 差异**：用 `load_skills=["architecture-decisions"]`。输入为 ④ 的 user-stories+constraints。产出 `system-design.md`。

### Phase 5b: 一致性审查（同步阻塞 Gate）

```
Step A: 派发 consistency-review subagent
  Agent(
    subagent_type="general-purpose",
    load_skills=["consistency-review"],
    run_in_background=false,
    prompt="
TASK: 对阶段 ④ 和 ⑤ 的产出进行一致性交叉审查
EXPECTED OUTCOME: wiki/06-quality/consistency-report.md
MUST DO:
  - 比对 assumptions.md ↔ user-stories.md（矛盾检测）
  - 比对 user-stories.md ↔ system-design.md（覆盖检测）
  - 比对 system-design.md 的模块 ↔ task-breakdown（如果 task-breakdown 已存在）
  - 所有矛盾必须处理（修复/澄清/接受/延迟）
MUST NOT DO: 不修改设计文档本身，只报告和标注矛盾
CONTEXT: 项目 {路径}
")
  注意：consistency-review 作为 Gate 运行，不自己修复矛盾——它报告问题，由 orchestrator 决定派发哪个阶段重跑。
```

### Phase 6: 设计并行批次（五路同时 + 异步 review）

**五路同时派发**：

```
// ⑥a ui-design
Agent(
  subagent_type="general-purpose",
  load_skills=["ui-design"],
  run_in_background=true,
  prompt="
TASK: 为项目设计 UI 界面方案
EXPECTED OUTCOME: wiki/03-architecture/ui-design.md
MUST DO: 读取 system-design.md 确定组件结构。风格从 Modern Minimal/Soft Elegant/Neo-Brutalism/Premium Dark/Playful Colorful 中选择，给出选择理由。
MUST NOT DO: 不写前端代码，只输出设计方案
CONTEXT: 项目 {路径}, system-design.md 已就绪。
")

// ⑥b security-design
Agent(
  subagent_type="general-purpose",
  load_skills=["security-design"],
  run_in_background=true,
  prompt="
TASK: 为项目设计安全方案
EXPECTED OUTCOME: wiki/03-architecture/security.md
MUST DO: 读取 system-design.md + user-stories.md。覆盖认证/授权/数据加密/输入校验。识别安全风险并登记。
MUST NOT DO: 不写安全实现代码，只输出设计方案
CONTEXT: 项目 {路径}
")

// ⑥c performance-design
Agent(
  subagent_type="general-purpose",
  load_skills=["performance-design"],
  run_in_background=true,
  prompt="
TASK: 为项目设计性能方案
EXPECTED OUTCOME: wiki/03-architecture/performance.md
MUST DO: 读取 system-design.md + api-spec.md。定义性能目标、关键链路分析、缓存策略。
MUST NOT DO: 不写性能优化代码，只输出设计方案
CONTEXT: 项目 {路径}
")

// ⑥d test-strategy
Agent(
  subagent_type="general-purpose",
  load_skills=["test-strategy"],
  run_in_background=true,
  prompt="
TASK: 为项目设计测试策略
EXPECTED OUTCOME: wiki/06-quality/test-strategy.md
MUST DO: 读取 system-design.md + api-spec.md。定义测试金字塔、覆盖率目标、关键路径测试用例。
MUST NOT DO: 不写测试代码，只输出测试策略
CONTEXT: 项目 {路径}
")

// ⑥e adversarial-scenarios（如果阶段 ④ 未执行）
Agent(
  subagent_type="general-purpose",
  load_skills=["adversarial-scenarios"],
  run_in_background=true,
  prompt="
TASK: 从用户故事推导对抗性场景
EXPECTED OUTCOME: wiki/03-architecture/threat-scenarios.md
MUST DO: 读取 user-stories.md + assumptions.md。对每个 US 推导失效路径、影响程度、架构响应。
MUST NOT DO: 不写实现代码，只输出场景
CONTEXT: 项目 {路径}
")
```

**每一路 fire 异步 review**：
```
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑥a ui-design 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑥b security 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑥c performance 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑥d test-strategy 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑥e adversarial 产出...")
```

### Phase 7: 交付规划 + 量化验收（同步阻塞）

```
Step A: 派发 subagent
  Agent(
    subagent_type="general-purpose",
    load_skills=["delivery-planning", "quantified-acceptance"],
    run_in_background=false,
    prompt="
TASK: 产出任务拆分 + 量化验收清单
EXPECTED OUTCOME:
  - wiki/05-delivery/task-breakdown.md (≥5 任务 + ≥2 里程碑)
  - wiki/06-quality/quantified-checklist.md (每条验收标准可测量)
MUST DO:
  - 基于 system-design.md 拆解任务
  - 每条验收标准必须量化（指标+目标值+测量方法）
  - 引用 consistency-report.md 中的矛盾处理结果
MUST NOT DO: 不写实现代码
CONTEXT: 项目 {路径}
")
```

### Phase 8-10: 并行批次（功能文档 + 异步 review）

**五路同时派发**：

```
// ⑧a risk — 从已有文档提取风险
Agent(
  subagent_type="general-purpose",
  load_skills=["risk-register"],
  run_in_background=true,
  prompt="
TASK: 从项目文档提取并格式化风险登记册
EXPECTED OUTCOME: wiki/02-research/risk-register.md (分类: 交付/产品/技术/运维)
MUST DO: 读入 HOME.md + task-breakdown.md + system-design.md。提取而非编造——每条风险必须来自已有文档的引用。
MUST NOT DO: 不添加文档中未出现的风险
CONTEXT: 项目 {路径}
")

// ⑧b api — 从架构提取 API 契约
Agent(
  subagent_type="general-purpose",
  load_skills=["data-api-design"],
  run_in_background=true,
  prompt="
TASK: 从系统架构提取 API 端点定义
EXPECTED OUTCOME: wiki/04-data-and-api/api-spec.md (method+path+描述+请求/响应)
MUST DO: 只读 system-design.md。提取显式端点；隐含端点标注来源但不过度推断。无 API 则标注'本项目无后端 API'。
MUST NOT DO: 不编造文档中未出现的端点
CONTEXT: ⑤ architecture 已就绪。
")

// ⑨a quality — 从交付计划提取验收矩阵
Agent(
  subagent_type="general-purpose",
  load_skills=["acceptance-design"],
  run_in_background=true,
  prompt="
TASK: 从交付文档提取验收计划
EXPECTED OUTCOME: wiki/06-quality/acceptance-plan.md (任务→验收标准映射矩阵 + 测试策略)
MUST DO: 基于 task-breakdown.md 逐条提取验收标准。
MUST NOT DO: 不编造任务中未涉及的验收项
CONTEXT: ⑦ delivery 已就绪。
")

// ⑨b ops — 从架构提取部署说明
Agent(
  subagent_type="general-purpose",
  load_skills=["operations-planning"],
  run_in_background=true,
  prompt="
TASK: 从架构文档提取部署说明
EXPECTED OUTCOME: wiki/07-operations/deployment.md (环境+步骤≤5+回滚)
MUST DO: 基于 system-design.md 的部署拓扑提取。无信息则标注'待细化'。
MUST NOT DO: 不编造架构未提及的部署细节
CONTEXT: ⑤ architecture 已就绪。
")

// ⑩ history — 项目变更日志
Agent(
  subagent_type="general-purpose",
  load_skills=["history-sync"],
  run_in_background=true,
  prompt="
TASK: 创建项目变更日志
EXPECTED OUTCOME: wiki/08-history/changelog.md (至少'项目创建(express-incubate v7)'一条)
MUST DO: 记录所有已创建文档的摘要
CONTEXT: 项目 {路径}
")
```

**每一路 fire 异步 review**：
```
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑧a risk 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑧b api 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑨a quality 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑨b ops 产出...")
Agent(load_skills=["stage-review"], run_in_background=true, prompt="评审 ⑩ history 产出...")
```

### Phase 11: 管线收尾 + Implementation Kit

1. **收集全部后台结果**：使用 `TaskOutput(task_id, block=false)` 逐个收集 ⑧a-⑩ subagent 结果和所有异步 review 结果

2. **Gate 3 跨阶段一致性检查 (C1-C4)**：

   | ID | 检查项 | 处理 |
   |----|--------|------|
   | C1 | HOME.md 的模块数 = system-design.md 的模块数？ | 不一致 → 重跑 ⑤ subagent |
   | C2 | user-stories 的优先级 = task-breakdown 的任务数？ | 遗漏 → 重跑 ⑦ subagent |
   | C3 | risk-register 中的风险是否在 task-breakdown 中有缓解措施？ | 无缓解 → 补充 |
   | C4 | scope.md 的非目标与 architecture 决策矛盾？ | 矛盾 → 标注 gap, 🔴 问用户 |

3. **异步 review GAP 修复**：检查 ⑥a-⑥e, ⑧a-⑧b, ⑨a-⑨b 的异步 review 是否有未解决的 GAP。有则重跑对应 subagent

4. **汇总决策日志**：
   - 从各设计阶段（⑥a-⑥e）收集所有设计决策 → `wiki/08-history/decision-log.md`
   - 汇总 🔴 未回复提问 → `wiki/01-requirements/open-questions.md`

5. **收尾日志**：
   ```
   Agent(
     subagent_type="Explore",
     load_skills=["execution-log"],
     run_in_background=true,
     prompt="Log pipeline end for express-incubate. All stages complete.
             Total assumptions: N. Questions asked: N. Auto-fixes: N."
   )
   ```

6. **呈现待确认清单给用户**（完整表格：阶段 | 评审结果 | 假设数 | 待确认问题）

7. **生成 Implementation Kit**：
   ```
   Agent(
     subagent_type="general-purpose",
     load_skills=["implementation-kit"],
     run_in_background=true,
     prompt="
TASK: 为项目 {项目名} 生成 implementation-kit
INPUT: 项目目录 {项目路径}，包含完整的 wiki 设计文档
OUTPUT: implementation-kit/ 目录（含 AGENTS.md, prompts/, acceptance/, PLAIN-LANGUAGE-SUMMARY.md）
MUST DO:
  - 读取所有 wiki 文档
  - 生成 Tier 1 上下文文件（CLAUDE.md, AGENTS.md, 等）
  - 生成 START_HERE.md 实现指南
  - 生成逐任务 prompts/ 和 acceptance/
  - 调用 plain-language-handoff 生成 PLAIN-LANGUAGE-SUMMARY.md
"
   )
   ```

孵化完成后，调用 `implementation-kit` skill 生成 AI 实现套件（含全员可读概要）：

```
1. **调用 implementation-kit**：
   Agent(
     subagent_type="general-purpose",
     load_skills=["implementation-kit"],
     run_in_background=false,
     prompt="
TASK: 为项目 {项目名} 生成 implementation-kit
INPUT: 项目目录 {项目路径}，包含完整的 wiki 设计文档
OUTPUT: implementation-kit/ 目录（含 AGENTS.md, prompts/, acceptance/, PLAIN-LANGUAGE-SUMMARY.md）
MUST DO:
  - 读取所有 wiki 文档
  - 生成 Tier 1 上下文文件（CLAUDE.md, AGENTS.md, 等）
  - 生成 START_HERE.md 实现指南
  - 生成逐任务 prompts/ 和 acceptance/
  - 调用 plain-language-handoff 生成 PLAIN-LANGUAGE-SUMMARY.md
"
   )
```

### Gate 1 预检规则速查

| 阶段 | 检查项 |
|------|--------|
| ① bootstrap | HOME.md 存在? 含项目定义+阶段+导航? |
| ② incubation | idea-landscape.md ≥2 画像 ≥2 场景 ≥3 方向? |
| ③ overview | vision.md 有问题+用户+价值? scope.md 有范围+非目标? |
| ④ requirements | user-stories.md ≥3 条(含 MVP 划分)? constraints.md ≥2 约束? adversarial-scenarios 产出 threat-scenarios.md? |
| ⑤ architecture | system-design.md ≥3 模块? 含关键链路+技术栈? |
| ⑤b consistency | consistency-report.md 存在? 无未处理的高严重矛盾? |
| ⑥a ui-design | ui-design.md 存在? 含风格选择+理由? |
| ⑥b security | security.md 存在? 含认证+加密+风险登记? |
| ⑥c performance | performance.md 存在? 含性能目标+缓存策略? |
| ⑥d test-strategy | test-strategy.md 存在? 含测试金字塔+关键用例? |
| ⑥e adversarial | threat-scenarios.md 存在? ≥5 场景? |
| ⑦ delivery | task-breakdown.md ≥5 任务 ≥2 里程碑? quantified-checklist.md 每条可测量? |
| ⑧a risk | risk-register.md 存在? 非空? 风险来源可追溯? |
| ⑧b api | api-spec.md 存在? 含端点定义? |
| ⑨a quality | acceptance-plan.md 存在? 任务→验收映射? |
| ⑨b ops | deployment.md 存在? 含环境+步骤? |
| ⑩ history | changelog.md 存在? 含"项目创建"记录? |

### 提问判断逻辑

| 缺口类型 | 举例 | 处理方式 |
|---------|------|---------|
| 🔴 业务决策 | "Web-only还是移动端？"、"单用户还是多用户？" | **askQuestions 工具问用户**（全管线最多 5 题, 不阻塞） |
| 🟡 技术决策 | "SQLite还是PostgreSQL？"、"React还是Vue？" | **AI 自决**（选最合理默认值, 标注 `[AUTO-DECISION]`） |
| 🟢 格式/数量 | 缺少导航链接、场景不够 3 个 | **自动修正**（补足缺失） |

### 重试和容错

| 场景 | 策略 |
|------|------|
| Subagent 返回 error/空 | 重新派发 1 次。仍失败 → 记录到日志, 标注 `[SKIPPED: reason]`, 继续管线 |
| stage-review 返回 FAIL | Gate 1 预检不过 → 重跑 subagent。Gate 2 FAIL → 记录 gap, 继续(不阻塞管线) |
| 🔴 用户未回复 | 不等待。记录到 open-questions.md, 标注"待回复"。管线不阻塞 |
| 并行批次(⑥a-⑥e)某个超时 | 收集已有结果, 超时的标记 `[TIMEOUT: stage N]`, 用窄 scope retry(单 skill,单文件)补缺, 继续收尾 |
| 并行批次(⑧a-⑩)某个超时 | 同上策略 |
| ⑤b consistency 高严重矛盾 | 阻塞管线, 派发对应阶段重跑, 完成后重新执行 consistency-review |

**核心原则：完成管线, 不因单点失败停滞。问题留痕, 事后可修。**

## Target Pages

- 项目文档：`<项目根目录>/HOME.md`、`wiki/**`
- 评审报告：`<项目根目录>/reports/stage-review/`
- 执行日志：`<项目根目录>/reports/execution/express-incubate-<timestamp>/`

## Dependencies

| 类型 | Skill |
|------|-------|
| 前置 | 无 |
| 派发 subagent | `project-bootstrap`, `incubation-discovery`, `overview-framing`, `requirements-spec`, `adversarial-scenarios`, `architecture-decisions`, `consistency-review`, `ui-design`, `security-design`, `performance-design`, `test-strategy`, `delivery-planning`, `quantified-acceptance`, `risk-register`, `data-api-design`, `acceptance-design`, `operations-planning`, `history-sync` |
| 调用评审 | `stage-review`（三级闸门） |
| 调用日志 | `execution-log`（全管线追踪） |
| 并行加载 | `assumptions-tracking`（阶段 ④ 同步加载） |
| 后置 | `implementation-kit`（Phase 11 生成 AI 实现套件 + 全员可读概要） |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | v8: 阶段扩展至 11 个——新增 ⑤b consistency-review gate、⑥ 设计并行批次(5路)、⑦ delivery+quantified-acceptance；更新 wiki 骨架目录（新增 consistency-report.md, threat-scenarios.md, decision-log.md, quantified-checklist.md）；更新容错策略（design batch 超时处理 + consistency 高严重矛盾阻塞） | 将 design skills、adversarial-scenarios、consistency-review、decision-log、quantified-acceptance 五个新 skill 纳入标准孵化流程 |
| 2026-04-29 | v7: Codex 适配 + 精简 — `task()` → `Agent()`, `background_output()` → `TaskOutput()`；移除 ultrabrain category；删除委托关系表（Procedure 已说明）；删除阶段产出速查（与 Agent 映射表重复）；幂等性章节从 30 行压缩至 15 行 | Codex 适配 + 内容精简 |
| 2026-04-27 | v6.3: 新增 Phase 11 调用 implementation-kit，孵化完成后自动生成 AI 实现套件（含 PLAIN-LANGUAGE-SUMMARY.md） | 确保每个快速孵化项目都能产出全员可读概要 |
| 2026-04-27 | v6.2: 新增中断恢复机制（Phase 0 resume check）、幂等执行日志（每个阶段独立 checkpoint）、execution-log 缺失检测 | 复盘发现多个项目因 session 中断或 skill bug 导致 execution-log 缺失，影响孵化追溯性 |
| 2026-04-26 | v6.1: 拆分 Stage ⑦⑧ 为 4 个独立 subagent（⑦a risk-register + ⑦b data-api-design + ⑧a acceptance-design + ⑧b operations-planning），并行批次 3→5 路；收紧 Stage ① bootstrap 边界（只产出 HOME.md+骨架，不越界写后续内容）；容错策略增加窄 scope retry | 测试发现双 skill 同 agent 超时（34min）；bootstrap 越界产出导致重复内容 |
| 2026-04-26 | v5: 6阶段→9阶段；新增 ⑦Risk+API、⑧Quality+Ops、⑨History | 审计发现快速模式产出不完整 |
| 2026-04-26 | v4: 重构为编排器 — 自审委托 stage-review、日志委托 execution-log；🔴问/🟡自决/🟢自修 | 关注分离 |
| 2026-04-26 | v3: 新增自审机制(27项checklist)+跨阶段一致性 | 用户反馈无review |
| 2026-04-26 | v2: 内联假设+决策分级+风险简报 | 深度审查 |
| 2026-04-26 | v1: 新建 | 填补快速孵化空白 |

---

## 幂等性与断点续传

### 幂等性

- **Execution-log**：每次 stage-end 只追加，用 stage-ID 作唯一键避免重复
- **Stage 产出**：文件已存在则更新，Gate 1 检查"已存在且内容充分"

### 断点续传

1. 每阶段完成后写入 `reports/execution/.../checkpoints/stage-{N}.json`（含阶段号、完成时间、产出文件、评审结果）
2. Phase 0 检测到 checkpoints → 询问用户：继续（跳过已完成）或重启
3. Restart 删除 `reports/execution/` 和 `reports/stage-review/`，保留 `wiki/` 和 `HOME.md`
