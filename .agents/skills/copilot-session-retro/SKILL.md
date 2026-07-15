---
name: copilot-session-retro
description: |
  Copilot Chat Session 专项复盘工具：自动读取当前 Copilot Chat session 的完整对话历史（transcript JSONL），
  多维度分析 AI 与用户在 session 中的协作表现，生成结构化复盘报告，并可将改进措施应用到项目配置文件中。
  两个模式：review（生成复盘报告）、apply（将报告中的改进措施写入配置文件）。
  触发关键词：session review、session retro、copilot retro、session复盘、对话复盘、Copilot回顾。
  **注意：本 skill 仅用于 Copilot Chat session 内部复盘，不用于项目阶段复盘。项目阶段复盘请使用 retrospective skill。**
  输入：当前 Copilot Chat session（自动获取 transcript）。
  输出：ai-gen-data/session-retro/{timestamp}/ 目录下的 report.md。
---

# Copilot Session Retrospective Skill

自动复盘当前 Copilot Chat session 的完整对话历史，多维度评估 AI 和用户协作表现，输出可执行的改进措施。

## 核心原则

1. **事实驱动**：所有评价必须基于 transcript 中的具体事件，引用具体的 turn/工具调用作为证据
2. **双向分析**：同时分析 AI 和 User 的表现，不偏袒任何一方
3. **深度归因**：不停留在"做得不好"的表面，要分析 **为什么** 做得不好、**根因** 是什么
4. **可执行**：每个改进项必须具体到可以修改哪个文件、添加什么内容
5. **不武断**：信息不足时标注"证据不充分"，不强行下结论

## 两个模式

| 模式 | 触发词 | 产出物 |
|------|--------|--------|
| **review** | `复盘`、`retro`、`retrospective`、`session review` | `report.md` |
| **apply** | `apply retro`、`应用复盘`、`apply改进` | 修改配置文件 |

---

## Review 模式

### 执行步骤

#### Step 1: 获取 Transcript

1. 定位当前 session 的 debug log 目录
   - 路径：`{{VSCODE_TARGET_SESSION_LOG}}/`
   - 主 transcript 文件：`main.jsonl`
   - 子 agent 日志：`runSubagent-{agent}-{toolId}.jsonl`（如有）
   - 或使用 conversation-summary 中指向的 transcript 路径
2. 读取 `main.jsonl`，解析 JSONL，提取关键事件（详见 [references/transcript-guide.md](references/transcript-guide.md)）：
   - `user_message` — 用户请求（`attrs.content`）
   - `agent_response` — AI 响应（`attrs.response` 含工具调用，`attrs.reasoning` 含思考过程）
   - `tool_call` — 工具调用及结果（`name` = 工具名，`attrs.args` / `attrs.result`）
   - `llm_request` — LLM 请求（`attrs.model` / `attrs.inputTokens` / `attrs.outputTokens` / `attrs.ttft`）
   - `turn_start` / `turn_end` — 每轮开始/结束（`attrs.turnId`）
3. 构建 session timeline：按 turn 聚合，标注每轮的目的、工具调用数、token 消耗

#### Step 2: 多维度分析

按以下 6 个维度分析 session，每个维度下有具体子项。

**维度 1：效率（Efficiency）**

| 子项 | 分析方法 |
|------|---------|
| 冗余操作 | 统计重复读取同一文件、重复搜索相同 pattern 的次数 |
| 工具选择效率 | 是否选了最优工具（如：应该用 grep_search 却用了 semantic_search） |
| 并行化利用 | 是否有可以并行但串行执行的独立读取操作 |
| 上下文利用 | 已获取的信息是否被充分利用，还是反复重新获取 |
| 任务拆分粒度 | todo list 管理是否合理，是否过度/不足 |

**维度 2：准确度（Accuracy）**

| 子项 | 分析方法 |
|------|---------|
| 事实正确性 | AI 陈述的代码事实（行号、方法名、逻辑）与实际代码是否一致 |
| 问题引入率 | AI 修改/生成的内容中引入了多少错误（后续需要修正） |
| 问题修复率 | 发现问题后是否及时修复，修复是否彻底 |
| 自检有效性 | 复查/验证步骤是否真正发现了问题 |

**维度 3：沟通（Communication）**

| 子项 | 分析方法 |
|------|---------|
| 提问质量 | askQuestions 的问题是否精准、有价值、不冗余 |
| 回复清晰度 | AI 的回复是否简洁、结构化、无歧义 |
| 确认及时性 | 是否在关键节点及时向用户确认 |
| 指令理解 | AI 是否正确理解了用户的意图（包括隐含意图） |

**维度 4：问题解决（Problem Solving）**

| 子项 | 分析方法 |
|------|---------|
| 分析深度 | 是否深入到根因，还是停留在表面 |
| 方案有效性 | 提出的方案是否真正解决了问题 |
| 遗漏检测 | 是否发现了隐藏的问题/遗漏（如 change party 独立路径） |
| 先例利用 | 是否有效利用代码中的 prior art 指导实现 |

**维度 5：文档质量（Documentation Quality）**

| 子项 | 分析方法 |
|------|---------|
| 结构完整性 | 产出文档是否覆盖所有要点，无遗漏 |
| 一致性 | 多份文档之间是否保持一致（如 analysis ↔ confirm ↔ plan） |
| 可追溯性 | 决策是否有来源、变更是否有 changelog |
| 排版规范 | 是否符合模板格式 |

**维度 6：协作模式（Collaboration Pattern）**

| 子项 | 分析方法 |
|------|---------|
| 主动性 | AI 是否主动发现问题而非被动等待用户指出 |
| 迭代效率 | 用户反馈 → AI 修正的循环是否高效 |
| 上下文保持 | 长 session 中是否丢失了早期上下文 |
| 角色边界 | AI 是否适当地在"执行"和"确认"之间切换 |

#### Step 3: 事件提取与归因

对每个维度：
1. 从 transcript 中提取 **具体事件**（引用 turn 号或时间戳）
2. 标记为 ✅ Good Practice 或 ❌ Issue
3. 对每个 Issue 进行 **根因分析**（Why-Why 链）
4. 提出 **改进措施**（具体到文件和内容）

#### Step 4: 生成报告

1. 创建输出目录 `ai-gen-data/session-retro/{YYYYMMDD-HHmm}/`
2. 按模板 [references/report-template.md](references/report-template.md) 生成 `report.md`
3. 报告结构：
   - 元信息（session ID、时长、主题）
   - 6 维度评分（1-5 分 + 关键证据）
   - Top Issues（按影响程度排序）
   - Top Wins（做得好的地方）
   - 改进措施清单（含目标文件和建议内容）
   - Agent/SubAgent/Skill 调用分析（调用合理性、时机、效果、缺失的调用）
   - 经验教训提炼
   - 发散观察与洞察（session 中发现的有趣现象、方法论洞察、意外发现）
   - 可执行建议（分四类：AI 使用优化 / 用户协作优化 / 流程设计优化 / 工具链优化，每条必须具体到做什么、怎么做、预期效果）

#### Step 5: 确认

使用 askQuestions 向用户确认报告内容，收集 feedback。

### 评分标准

每个维度 1-5 分：

| 分数 | 含义 |
|------|------|
| 5 | 卓越 — 超出预期，可作为 best practice |
| 4 | 良好 — 基本无问题，偶有小瑕疵 |
| 3 | 合格 — 完成任务但有明显改进空间 |
| 2 | 不足 — 有较大问题影响产出质量 |
| 1 | 严重 — 关键失误导致返工或错误 |

### 分析指导

#### 常见 AI 问题模式

- **过度搜索**：已有足够信息仍继续搜索
- **假设性陈述**：未经验证就声称代码行为
- **遗漏验证**：修改后不验证正确性
- **模板套用**：机械地套用模板而非根据实际情况调整
- **上下文遗忘**：忘记 session 早期讨论的结论

#### 常见 User 问题模式

- **需求模糊**：请求描述不够具体
- **延迟反馈**：在多步操作后才指出方向偏差
- **隐含假设**：假设 AI 知道某些背景知识
- **频繁变更**：反复修改需求导致返工

#### 根因分析框架

对每个 Issue，追问：
1. **What** — 具体发生了什么？
2. **When** — 在哪个 turn/阶段发生？
3. **Impact** — 造成了什么影响（时间浪费/错误引入/返工）？
4. **Why** — 为什么会发生？（至少追问 2 层 Why）
5. **How to prevent** — 如何在系统层面预防？

---

## Apply 模式

### 前置条件

必须先有一份复盘报告（`report.md`），apply 模式基于报告中的改进措施执行。

### 执行步骤

#### Step 1: 读取报告

1. 读取最新的 `ai-gen-data/session-retro/` 下的 `report.md`
   - 如果有多份，使用 askQuestions 让用户选择
2. 提取报告中的 **改进措施清单**

#### Step 2: 分类改进措施

按目标文件分类：

| 目标 | 文件路径 | 典型改进 |
|------|---------|---------|
| Copilot Instructions | `.github/copilot-instructions.md` | 新增约束、流程规范 |
| Agent 定义 | `.github/agents/*.md` | 调整 agent 行为指令 |
| Wiki | `ai-gen-data/wiki/**` | 补充项目知识 |
| Skills | `.github/skills/*/SKILL.md` | 改进 skill 工作流 |
| User Memory | `/memories/*.md` | 记录用户偏好和经验 |
| Repo Memory | `/memories/repo/*.md` | 记录项目级经验 |

#### Step 3: 逐项应用

对每个改进措施：
1. 读取目标文件当前内容
2. 展示改动预览（before → after）
3. 使用 askQuestions 逐项确认
4. 用户确认后执行修改

#### Step 4: 汇总

输出修改汇总，标注每项改进的来源（report.md 中的哪个 Issue）。

---

## 注意事项

- `{{VSCODE_TARGET_SESSION_LOG}}` 是目录路径，主 transcript 文件为其中的 `main.jsonl`
- Transcript JSONL 可能很大（数千行），优先使用 grep_search 定位关键事件，避免全量读取
- 子 agent 日志在独立文件中（`runSubagent-*.jsonl`），需要时单独分析
- 分析时区分 **系统性问题**（需要修改配置）和 **偶发问题**（无需系统性修复）
- 评分应有区分度，不要所有维度都给 3-4 分
- 改进措施要具体到 **可执行**，不要写"提高沟通效率"这样的空话
- 每次复盘都是独立的，不依赖之前的复盘报告

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 新建 skill | 填补 Codex 专属 session 复盘工具空白，使用原生 transcript 文件分析
