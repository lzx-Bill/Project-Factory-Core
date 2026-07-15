# 贡献指南

感谢你帮助改进 Project Factory Core。这个仓库以文档和 Skill 为核心，最有价值的贡献是可复现的问题、最小修复和真实项目验证。

## 适合贡献的内容

- Skill 触发不准确、阶段依赖错误或输出契约冲突
- 模板、导航、任务、Prompt、验收之间的追踪缺口
- 去除特定业务污染，让示例更通用
- 能由真实项目或最小测试证明有效的流程改进

不建议提交：

- 没有实际需求的新 Skill 或抽象层
- 产品实现代码、框架脚手架或示例应用
- 只增加篇幅、不改善执行结果的大段说明

## 提交流程

1. 先搜索已有 Issue；没有再创建新 Issue。
2. Fork 仓库并从 `main` 创建短生命周期分支。
3. 修改前阅读 `AGENTS.md` 和涉及的每个 `SKILL.md`。
4. 保持改动聚焦；跨 Skill 变更需说明共同根因。
5. 运行验证：

   ```powershell
   python scripts/validate_repo.py
   ```

6. 在 Pull Request 中说明问题、根因、改动和验证结果。

## Skill 修改要求

- Frontmatter 至少包含 `name` 和可准确触发的 `description`。
- `SKILL.md` 不超过 500 行；大段参考内容放入 `references/` 并明确读取时机。
- 示例必须是领域无关的结构示例，不能变成隐含项目需求。
- 修改编排 Skill 时，必须验证依赖顺序、文件所有权、并发上限和失败路径。
- 新增 Skill 前先证明现有 Skill 无法承接。

## Commit 与 Pull Request

- 使用简洁、可读的提交信息，例如 `fix: align express incubation dependencies`。
- 一个 PR 解决一个清晰问题。
- 不提交临时报告、日志、生成缓存或个人编辑器配置。
- 如果改动影响公开行为，请同步更新 README 或对应 Changelog。
