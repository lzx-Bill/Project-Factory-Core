# GitHub 公开发布清单

本清单只记录 GitHub 远程设置和发布动作；仓库内可以自动验证的内容由 `python scripts/validate_repo.py` 负责。

## 推荐元信息

**Description**

```text
Docs-first project incubation with 34 composable AI Agent skills—from idea and requirements to architecture, acceptance, and implementation handoff.
```

**Topics**

```text
ai-agents
agent-skills
codex
docs-as-code
project-planning
product-development
software-architecture
workflow-automation
```

## 创建远程仓库后

将 `<OWNER>` 替换为 GitHub 用户名或组织名：

```powershell
git remote add origin https://github.com/<OWNER>/Project-Factory-Core.git
git push -u origin main

gh repo edit <OWNER>/Project-Factory-Core `
  --description "Docs-first project incubation with 34 composable AI Agent skills—from idea and requirements to architecture, acceptance, and implementation handoff." `
  --add-topic ai-agents `
  --add-topic agent-skills `
  --add-topic codex `
  --add-topic docs-as-code `
  --add-topic project-planning `
  --add-topic product-development `
  --add-topic software-architecture `
  --add-topic workflow-automation `
  --enable-issues `
  --enable-discussions=false `
  --enable-projects=false `
  --enable-wiki=false `
  --delete-branch-on-merge `
  --enable-squash-merge
```

保持 Discussions 关闭，直到有维护者能够持续回复；项目文档已经在仓库中，不重复启用 Wiki。

## GitHub Settings

- [ ] Visibility 设为 Public 前检查完整 Git 历史没有密钥、Cookie、个人路径或生成日志
- [ ] 默认分支为 `main`
- [ ] Actions 中 `Validate repository` 首次运行通过
- [ ] 为 `main` 设置规则：Pull Request、验证通过、禁止 force push
- [ ] 启用 Secret scanning、Push protection 和 Private vulnerability reporting
- [ ] 上传 1280×640 PNG 社交预览图
- [ ] 检查 README、License、Contributing、Security policy 在 Community Standards 中被识别
- [ ] 创建 `good first issue` 和 `help wanted` 标签，但只标记已有明确验收标准的任务

## 首次发布内容

首个 Release 建议在至少完成一次真实孵化验证后创建，避免只发布未经实战验证的模板。

发布说明至少包含：

- 解决什么问题
- 适合和不适合的用户
- 30 秒开始方式
- 已验证的真实案例
- 当前限制
- 下一步贡献入口

## Showcase 策略

真实案例放到独立的 `Project-Factory-Showcase` 仓库，Core 只保留链接和验证结论。第一个案例建议使用真实需求完整跑通：

```text
想法 → 需求 → 研究 → 架构/API → UI/安全/性能/测试 → 任务/验收 → audit → implementation-kit
```

案例必须保留执行日志、评审报告和最终审计结果，不能用手写文档冒充工作流产物。
