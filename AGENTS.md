# Project Factory Core

文档优先的项目孵化工作区。输入想法，沉淀需求、研究、架构、数据/API、任务、验收和实现交接资料。

## 核心规则

- 默认使用中文交流和编写文档。
- 默认只产出文档，不创建 `src/`、`package.json`、`Dockerfile` 等产品实现文件。
- 项目内容必须写入 `<项目名称>/`，不得散落在仓库根目录。
- 信息不足时主动提问；暂时无法确认的内容写入假设、开放问题或风险登记。
- 修改采用增量更新，优先更新对应维度页面，不把内容堆回单一文件。
- 阶段切换、不可逆决策或关键未决项必须请用户确认。
- 每次完成包含文件改动的任务后执行必要验证；仓库已使用 Git 管理时及时提交。

## 工作流

```text
想法 → 需求澄清 → 研究验证 → 架构设计 → 数据/API与关键流程 → 任务拆解 → 设计验收 → 实现交接
```

用户说“快速孵化”时，使用 `express-incubate` skill；渐进推进时，按问题维度选择对应 skill。

## Skill 使用

- Skill 目录：`.agents/skills/`
- 使用前完整读取对应 `<skill-name>/SKILL.md`。
- 仅加载当前任务需要的 skill；多个 skill 同时适用时，明确执行顺序。
- `express-incubate` 是多 Agent 编排器；只有用户要求快速孵化时才启动其并行流程。
- 全项目检查使用 `project-audit`，单阶段文档检查使用 `stage-review`。
- 设计完成后使用 `implementation-kit` 生成独立实现套件。

## 项目目录

```text
<项目名称>/
├── HOME.md
├── wiki/
│   ├── 00-overview/
│   ├── 01-requirements/
│   ├── 02-research/
│   ├── 03-architecture/
│   ├── 04-data-and-api/
│   ├── 05-delivery/
│   ├── 06-quality/
│   ├── 07-operations/
│   └── 08-history/
├── prompts/
├── acceptance/
├── tasks/
├── reports/
└── implementation-kit/
```

完整页面骨架与追踪约定见 `PROJECT_WIKI_TEMPLATE.md`。
