# Project Factory Core

Project Factory 的干净核心仓库，只包含 Agent 协作规范、Skills 和项目 Wiki 模板，不包含任何业务案例或产品实现。

## 内容

- `AGENTS.md`：仓库级协作规则与工作流
- `.agents/skills/`：项目孵化、设计、质量和交接 Skills
- `PROJECT_WIKI_TEMPLATE.md`：项目目录、页面骨架和任务追踪模板

## 使用

1. 在本仓库启动支持 `AGENTS.md` 与项目 Skills 的 Agent。
2. 描述项目想法；需要一轮生成完整草案时说“快速孵化”。
3. 所有产出写入新建的 `<项目名称>/` 目录。
4. 设计完成后生成 `implementation-kit/`，复制到独立实现仓库继续开发。

本仓库只负责孵化与交接，不直接承载产品代码。
