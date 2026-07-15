---
name: opencode-session-retro
description: |
  OpenCode Session 专项复盘工具：使用 OpenCode 原生 session 工具（session_list/session_read/session_info/session_search）
  自动读取当前或指定 session 的完整对话历史，多维度分析 AI 与用户在 session 中的协作表现，
  生成结构化复盘报告，并可将改进措施应用到 OpenCode 项目配置文件中。
  两个模式：review（生成复盘报告）、apply（将报告中的改进措施写入配置文件）。
  触发关键词：opencode retro、opencode session review、opencode复盘、session复盘、对话复盘。
  **注意：本 skill 仅用于 OpenCode session 复盘。Copilot session 复盘请使用 copilot-session-retro skill。**
  输出：reports/session-retro/{YYYYMMDD-HHmm}/ 目录下的 report.md。
argument-hint: 'opencode复盘、opencode retro、session复盘、对话复盘、session review'
---

# OpenCode Session Retrospective Skill

自动复盘当前 OpenCode session 的完整对话历史，多维度评估 AI 和用户协作表现，输出可执行的改进措施。

## 与 copilot-session-retro 的区别

| 维度 | copilot-session-retro | opencode-session-retro |
|------|----------------------|------------------------|
| 目标平台 | GitHub Copilot Chat | OpenCode |
| 数据源 | `main.jsonl` 文件 | `session_read`/`session_list`/`session_info` 工具 |
| Apply 目标 | `.github/copilot-instructions.md` | `AGENTS.md`、`opencode.json`、`.opencode/skills/` |
| 技能目录 | `.github/skills/` | `.opencode/skills/` |

## 核心原则

1. **事实驱动**：所有评价必须基于 session 中的具体事件，引用具体的消息 ID 和工具调用作为证据
2. **双向分析**：同时分析 AI 和 User 的表现，不偏袒任何一方
3. **深度归因**：不停留在"做得不好"的表面，要分析 **为什么** 做得不好、**根因** 是什么
4. **可执行**：每个改进项必须具体到可以修改哪个文件、添加什么内容
5. **不武断**：信息不足时标注"证据不充分"，不强行下结论

## 两个模式

| 模式 | 触发词 | 产出物 |
|------|--------|--------|
| **review** | `opencode retro`、`opencode复盘`、`session review` | `report.md` |
| **apply** | `apply retro`、`应用复盘`、`apply改进` | 修改配置文件 |

---

## Review 模式

### Step 1: 获取 Session 数据

使用 OpenCode 原生工具获取 session 信息：

1. **获取当前 session 列表**：
   - 使用 `session_list` 获取最近的 session 列表
   - 默认复盘当前 session；如需复盘历史 session，使用 `session_list` 查找目标 ID

2. **读取 session 元信息**：
   - 使用 `session_info(session_id="...")` 获取：消息数、日期范围、时长、使用的 agents、todos 状态

3. **读取完整对话**：
   - 使用 `session_read(session_id="...", include_todos=true, include_transcript=true)` 获取完整历史
   - 主要关注：
     - 每条消息的 role（user/assistant）、时间戳、内容
     - 工具调用（识别工具名、参数、结果）
     - todo 变化（创建、完成、取消）
     - agent 调用（subagent 的 task 调用和结果）

4. **构建 session timeline**：
   - 按消息顺序排列，标注每轮的意图、工具调用数、token 消耗（如有）

### Step 2: 多维度分析

按以下 6 个维度分析 session，每个维度下有具体子项。

**维度 1：效率（Efficiency）**

| 子项 | 分析方法 |
|------|---------|
| 冗余操作 | 是否有重复读取同一文件、重复搜索相同 pattern |
| 工具选择效率 | 是否选了最优工具（如：应用 explore agent 却手动 grep） |
| 并行化利用 | 独立操作是否并行执行（parallel tool calls） |
| 上下文利用 | 已获取的信息是否被充分利用，还是反复重新获取 |
| 任务拆分粒度 | todowrite 管理是否合理，是否过度/不足 |

**维度 2：准确度（Accuracy）**

| 子项 | 分析方法 |
|------|---------|
| 事实正确性 | AI 陈述的事实（文件路径、字段名、逻辑）与实际情况是否一致 |
| 问题引入率 | AI 修改/生成的内容中引入了多少错误 |
| 问题修复率 | 发现问题后是否及时修复，修复是否彻底 |
| 自检有效性 | lsp_diagnostics 等验证步骤是否真正发现了问题 |

**维度 3：沟通（Communication）**

| 子项 | 分析方法 |
|------|---------|
| 提问质量 | `question` 工具的问题是否精准、有价值、不冗余 |
| 回复清晰度 | AI 的回复是否简洁、结构化、无歧义 |
| 确认及时性 | 是否在关键节点及时向用户确认 |
| 指令理解 | AI 是否正确理解了用户的意图（包括隐含意图） |

**维度 4：问题解决（Problem Solving）**

| 子项 | 分析方法 |
|------|---------|
| 分析深度 | 是否深入到根因，还是停留在表面 |
| 方案有效性 | 提出的方案是否真正解决了问题 |
| 遗漏检测 | 是否发现了隐藏的问题/遗漏 |
| 先例利用 | 是否有效利用代码中的已有模式指导实现 |

**维度 5：文档质量（Documentation Quality）**

| 子项 | 分析方法 |
|------|---------|
| 结构完整性 | 产出文档是否覆盖所有要点 |
| 一致性 | 多份文档之间是否保持一致 |
| 可追溯性 | 决策是否有来源、变更是否有 changelog |
| 排版规范 | 是否符合 Project Factory 模板格式 |

**维度 6：协作模式（Collaboration Pattern）**

| 子项 | 分析方法 |
|------|---------|
| 主动性 | AI 是否主动发现问题而非被动等待用户指出 |
| 迭代效率 | 用户反馈 → AI 修正的循环是否高效 |
| 上下文保持 | 长 session 中是否丢失了早期上下文 |
| 角色边界 | AI 是否适当在"执行"和"确认"之间切换 |

### Step 3: 事件提取与归因

对每个维度：
1. 从 session 中提取 **具体事件**（引用消息序号或时间戳）
2. 标记为 ✅ Good Practice 或 ❌ Issue
3. 对每个 Issue 进行 **根因分析**（Why-Why 链）
4. 提出 **改进措施**（具体到文件和内容）

### Step 4: 生成报告

1. 创建输出目录 `reports/session-retro/{YYYYMMDD-HHmm}/`
2. 生成 `report.md`，结构：
   - **元信息**：session ID、时长、消息数、使用的 agents、主题
   - **6 维度评分**（1-5 分 + 关键证据）
   - **Top Issues**（按影响程度排序）
   - **Top Wins**（做得好的地方）
   - **改进措施清单**（含目标文件和建议内容）
   - **Agent/SubAgent/Skill 调用分析**：调用合理性、时机、效果、缺失的调用
   - **经验教训提炼**
   - **发散观察与洞察**
   - **可执行建议**（分四类：AI 使用优化 / 用户协作优化 / 流程设计优化 / 工具链优化）

### Step 5: 确认

使用 `question` 工具向用户确认报告内容，收集 feedback。

### 评分标准

| 分数 | 含义 |
|------|------|
| 5 | 卓越 — 超出预期，可作为 best practice |
| 4 | 良好 — 基本无问题，偶有小瑕疵 |
| 3 | 合格 — 完成任务但有明显改进空间 |
| 2 | 不足 — 有较大问题影响产出质量 |
| 1 | 严重 — 关键失误导致返工或错误 |

### 分析指导

#### 常见 AI 问题模式 (OpenCode 特有)

- **过度搜索**：已有足够信息仍继续搜索
- **假设性陈述**：未经验证就声称代码行为
- **遗漏验证**：修改后不运行 lsp_diagnostics
- **串行执行冗余**：独立操作未并行（如同时读 3 个文件却分 3 次调）
- **上下文遗忘**：忘记 session 早期讨论的结论
- **Subagent 滥用**：简单任务不必要地 spawn subagent
- **Subagent 不用**：复杂任务应该 spawn subagent 却手动执行

#### 常见 User 问题模式

- **需求模糊**：请求描述不够具体
- **延迟反馈**：在多步操作后才指出方向偏差
- **隐含假设**：假设 AI 知道某些背景知识
- **频繁变更**：反复修改需求导致返工

#### 根因分析框架

对每个 Issue，追问：
1. **What** — 具体发生了什么？
2. **When** — 在哪个消息/阶段发生？
3. **Impact** — 造成了什么影响（时间浪费/错误引入/返工）？
4. **Why** — 为什么会发生？（至少追问 2 层 Why）
5. **How to prevent** — 如何在系统层面预防？

---

## Apply 模式

### 前置条件

必须先有一份复盘报告（`report.md`），apply 模式基于报告中的改进措施执行。

### 执行步骤

#### Step 1: 读取报告

读取最新的 `reports/session-retro/` 下的 `report.md`；如果有多份，使用 `question` 让用户选择。

#### Step 2: 分类改进措施

按目标文件分类：

| 目标 | 文件路径 | 典型改进 |
|------|---------|---------|
| OpenCode 指令 | `AGENTS.md` | 新增约束、流程规范 |
| OpenCode 配置 | `opencode.json` | 调整 skill 加载、工具权限 |
| Skills | `.opencode/skills/*/SKILL.md` | 改进 skill 工作流 |
| 项目 Wiki | `<项目>/wiki/**` | 补充项目知识 |

#### Step 3: 逐项应用

对每个改进措施：
1. 读取目标文件当前内容
2. 展示改动预览（before → after）
3. 使用 `question` 逐项确认
4. 用户确认后执行修改

#### Step 4: 汇总

输出修改汇总，标注每项改进的来源（report.md 中的哪个 Issue）。

---

## 注意事项

- 使用 `session_list` 时，可用 `limit` 控制返回数量
- `session_read` 支持 `include_todos` 和 `include_transcript` 参数
- 长 session 分析时用 `message_limit` 控制消息量，或用 `session_search` 搜索关键事件
- 分析时区分 **系统性问题**（需要修改配置文件）和 **偶发问题**（无需系统性修复）
- 评分应有区分度，不要所有维度都给 3-4 分
- 改进措施要具体到 **可执行**，不要写"提高沟通效率"这样的空话

## Target Pages

- `<项目根目录>/reports/session-retro/{YYYYMMDD-HHmm}/report.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 新建 skill | OpenCode 专属 session 复盘工具，使用原生 session 工具替代文件读取 |
