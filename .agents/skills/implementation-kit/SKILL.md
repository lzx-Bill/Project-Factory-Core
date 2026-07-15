---
name: implementation-kit
description: 'Use when generating an AI-ready implementation package from Project Factory design docs — "generate implementation kit", "create handoff", "打包实现", "生成实现套件", "export to implementation", "交接". This skill reads ALL design documents from a project directory and compiles them into multi-tool context files (CLAUDE.md, AGENTS.md, Cursor rules, and Copilot instructions) plus per-task prompts and acceptance criteria. Output is a self-contained implementation-kit/ directory that can be copied to any new project directory and executed by any AI coding tool.'
argument-hint: '生成实现套件、打包交接、export实现、handoff、implementation kit'
---

# Implementation Kit

将 Project Factory 设计文档编译为多工具兼容的 AI 实现套件。

## 定位

| 维度 | 说明 |
|------|------|
| 目标 | 一次生成，任意 AI 工具直接可用 |
| 输入 | Project Factory 项目目录（含 wiki/、prompts/、tasks/ 等） |
| 输出 | `implementation-kit/` 自包含目录 |
| 策略 | 三层上下文：自动加载 → 实现指南 → 按需详细设计 |

## When to Use

- 设计完成，需要将项目交接给实现阶段
- 用户说"打包"、"生成实现套件"、"生成交接包"、"export"
- 用户准备在新的目录、新的 session 中开始编码

## Input

| 来源 | 内容 |
|------|------|
| 项目目录 | `<项目根目录>/` 下的 HOME.md、wiki/*、tasks/*、prompts/* |
| 用户消息 | 可选：目标实现目录路径 |

## Output

```
<项目根目录>/implementation-kit/
├── CLAUDE.md                       ← Tier 1: Claude Code 自动加载
├── AGENTS.md                       ← Tier 1: Codex + OpenCode 自动加载
├── .cursor/rules/project.mdc       ← Tier 1: Cursor 专用规则
├── .github/
│   └── copilot-instructions.md     ← Tier 1: Copilot 指令
├── START_HERE.md                   ← Tier 2: AI+人类 实现指南（含工具兼容表）
├── IMPLEMENT_PROMPT.md             ← 可选: 单一母 Prompt (复制粘贴)
├── context/                        ← Tier 3: 压缩设计文档
│   ├── overview.md
│   ├── architecture.md
│   ├── tasks.md
│   ├── assumptions.md
│   └── open-questions.md
├── prompts/                        ← 逐任务实现 prompt
│   ├── T1-xxx.md
│   ├── T2-xxx.md
│   └── ...
└── acceptance/                     ← 逐任务验收标准
    ├── T1-xxx.md
    ├── T2-xxx.md
    └── ...
```

**AI 工具自动加载机制**：
| 工具 | 自动读取的文件 |
|------|---------------|
| Claude Code | `CLAUDE.md`（session 启动时自动加载） |
| OpenCode | `AGENTS.md`（session 启动时自动加载） |
| Codex | `AGENTS.md`（session 启动时自动加载） |
| Cursor | `.cursor/rules/project.mdc`（alwaysApply: true） |
| GitHub Copilot | `.github/copilot-instructions.md` |

各工具读取自己的 Tier 1 文件，无需复制粘贴公共上下文。

## Procedure

### Phase 1: 收集设计上下文

读取项目目录下的所有设计文档：
1. `HOME.md` → 项目概览、决策、风险
2. `wiki/00-overview/vision.md`、`scope.md` → 愿景和范围
3. `wiki/01-requirements/user-stories.md`、`constraints.md` → 需求和约束
4. `wiki/01-requirements/assumptions.md`、`open-questions.md` → 假设和待确认
5. `wiki/03-architecture/system-design.md` → 架构设计
6. `wiki/04-data-and-api/*.md` → 数据/API（如有）
7. `wiki/05-delivery/task-breakdown.md` → 任务拆解
8. `tasks/backlog.md` → 任务状态

### Phase 2: 编译 Tier 1 上下文文件

#### CLAUDE.md

```markdown
# <项目名称>
<一句话定义>

## Tech Stack
- <从架构提取>

## Architecture
<模块划分 + 关键链路>

## Key Decisions
- 🔴 <不可逆决策>
- 🟡 <可逆决策>

## Conventions
- <从约束提取>

## Build & Run
- <从部署提取>

## References
- context/*.md for detailed design docs
- prompts/ for per-task implementation instructions
```

#### AGENTS.md

跨工具标准，内容与 CLAUDE.md 相同，格式适配 AGENTS.md 规范。

#### .cursor/rules/project.mdc

```yaml
---
alwaysApply: true
---
# <项目名称> Project Rules
<从 AGENTS.md 提取关键规则>
```

#### .github/copilot-instructions.md

```markdown
# <项目名称>
<从 AGENTS.md 提取，格式适配 Copilot>
```

### Phase 3: 编译 Tier 2 实现指南

#### START_HERE.md

```markdown
# <项目名称> — 实现指南

## 你要构建什么
<3 句总结：项目 + 技术栈 + 核心功能>

## 实现顺序
| 顺序 | 任务 | 输入 Prompt | 验收 |
|------|------|------------|------|
| 1 | <T1名称> | prompts/T1-xxx.md | acceptance/T1-xxx.md |
| ...

## 规则
- 所有设计决策参考 context/*.md
- 每完成一个任务，用 acceptance/ 做自检
- 发现设计缺口：合理推断 + 标注 [IMPL-ASSUMPTION]
- 不要问我实现细节（上下文已给足）
```

#### IMPLEMENT_PROMPT.md（可选）

将全部上下文压缩为一份 3000 字以内的超级 prompt，用于复制粘贴到任意 AI 对话中。

### Phase 4: 编译 Tier 3 详细上下文

#### context/*.md

将 wiki 中的原始文档压缩为 1-2 页的精华版本：
- `context/overview.md` ← vision.md + scope.md（1 页）
- `context/architecture.md` ← system-design.md（2 页）
- `context/tasks.md` ← task-breakdown.md（1 页）
- `context/assumptions.md` ← assumptions.md + open-questions.md（1 页）

### Phase 5: 生成逐任务 prompts

为 task-breakdown.md 中每个任务生成实现 prompt：

```markdown
# <任务ID>: <任务名称>

**依赖**: <前置任务>
**产出**: <输出文件列表>

## 目标
<任务目标>

## 输入上下文
- 参考 context/architecture.md 中的 <相关模块>
- 参考 context/overview.md 中的 <相关约束>

## 实现要求
<具体功能要求和技术约束>

## 不应修改
- <明确排除的文件或模块>

## 验收
- 对照 acceptance/<任务ID>.md
```

### Phase 6: 生成逐任务验收

为每个任务生成验收标准：

```markdown
# 验收: <任务ID>

## 验证步骤
1. <检查项>
   ```bash
   <验证命令>
   ```
   通过标准: <标准>

## 文档一致性
- [ ] context/ 中的设计意图已满足
- [ ] 与前后任务的接口一致
```

### Phase 7: 生成 PLAIN-LANGUAGE-SUMMARY.md

主 Agent 完整读取 `../plain-language-handoff/SKILL.md`，按其规则同步生成
`implementation-kit/PLAIN-LANGUAGE-SUMMARY.md`。不要再派发嵌套 Agent；这样可避免并发写入 kit 和无法确认子任务完成的问题。

### Phase 8: 最终检查

1. 确认所有 Tier 1 文件格式正确
2. 确认 START_HERE.md 覆盖所有任务
3. 确认 prompt 和 acceptance 数量与 task-breakdown 一致
4. 确认 PLAIN-LANGUAGE-SUMMARY.md 存在且完整
5. 在 HOME.md 中记录 kit 生成完成

## Enriched Behavior

- **自动检测**：如果 wiki 文件不完整，标注缺失项，但仍生成 kit
- **工具适配**：生成全部 Tier 1 文件（至少 CLAUDE.md + AGENTS.md）
- **压缩原则**：上下文文件 ≤ 2 页，避免 token 超限
- **可追溯**：每个生成的文件标注来源（从哪个设计文档编译）

## Target Pages

- `<项目根目录>/implementation-kit/*`

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 项目设计文档已产出（至少 HOME.md + wiki + tasks） |
| 并行 | `plain-language-handoff`（生成全员可读概要） |
| 后置 | 用户在实现目录中使用 kit |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-07-15 | 移除失效的子任务调用示例，改为主 Agent 同步读取并执行 plain-language-handoff | 适配当前 Codex 工具并避免嵌套任务竞写 |
| 2026-04-29 | v1.2：适配当时的 Codex 子任务语法 | 工具接口变化 |
| 2026-04-27 | v1.1: 新增 Phase 7 调用 plain-language-handoff skill | implementation-kit 生成后自动产出全员可读概要 |
| 2026-04-26 | v1.0 新建 skill | 桥接设计与实现：自动编译设计文档为多工具 AI 上下文文件 |
