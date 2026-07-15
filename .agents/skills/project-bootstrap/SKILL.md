---
name: project-bootstrap
description: 'Use when starting a new Project Factory project. Trigger when user says "new project", "create project", "initialize", "start a new wiki", or mentions setting up a fresh project folder with HOME.md and wiki structure. Also use when scaffolding prompts/, acceptance/, tasks/, reports/ directories for an existing project.'
argument-hint: '新项目启动、目录初始化、HOME骨架、wiki目录结构'
---

# Project Bootstrap

用于新项目启动和初始骨架建立。

## When to Use

- 用户刚提出一个新项目想法，需要建立孵化空间
- 需要创建 `HOME.md` 和基础 wiki 目录结构
- 需要初始化 `prompts/`、`acceptance/`、`tasks/`、`reports/` 等交付目录

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 项目名称（如有）、一句话想法、项目背景 |
| 已有文档 | 无（全新项目） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `<项目根>/HOME.md` | 导航首页 | 一句话定义 + 阶段 + 目标 + 下一步 + 导航 |
| `<项目根>/wiki/00-overview/vision.md` | 愿景页 | 问题、用户、价值、非目标、成功标准 |
| `<项目根>/wiki/01-requirements/user-stories.md` | 用户故事 | 核心场景的 2-3 条用户故事 |
| `<项目根>/wiki/01-requirements/assumptions.md` | 假设页 | 初始假设清单（可占位） |

## Minimum Viable Output

- HOME.md 含一句话定义、当前阶段（"启动中"）、当前目标、下一步
- 至少 1 个 wiki 页面有实质内容（不全是占位符）
- 目录结构完整，可继续扩写

## Complete Output

- HOME.md + vision.md + user-stories.md + assumptions.md 均含实质内容
- `prompts/`、`acceptance/`、`tasks/`、`reports/` 目录已创建
- `tasks/backlog.md` 含初始任务候选项

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 无（从零开始） |
| 后置 | `incubation-discovery`（方向发散）、`overview-framing`（愿景细化）、`requirements-spec`（需求细化） |
| 并行 | 无 |

## Procedure

1. 确认项目名称，固定项目根目录为 `<项目根目录>/`
2. 创建最小可运行目录结构，所有初始化文件都放在 `<项目根目录>/` 下
3. 优先写 HOME.md（一句话定义 + 阶段 + 目标 + 下一步 + 导航）
4. 再补 vision.md 和 user-stories.md 初稿
5. 不在启动阶段过早写满全部细节页

## Enriched Behavior

- 不只创建空目录，至少落下能让用户继续阅读和推进的首批内容
- 首页优先给出一句话定义、当前阶段、当前目标、下一步，而不是只放目录树
- 如果用户描述仍然模糊，用占位性的候选方向和待确认项承接，不要因为信息不全而停止产出
- 优先让新项目具备"可继续扩写"的骨架，而不是一次写满所有页面

## Target Pages

- `<项目根目录>/HOME.md`
- `<项目根目录>/wiki/00-overview/vision.md`
- `<项目根目录>/wiki/01-requirements/user-stories.md`
- `<项目根目录>/wiki/01-requirements/assumptions.md`
- `<项目根目录>/prompts/`
- `<项目根目录>/acceptance/`
- `<项目根目录>/tasks/`
- `<项目根目录>/reports/`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、Changelog | 统一 skill 结构，提升触发准确性和输出一致性 |
