---
name: ui-design
description: 'Use when designing the user interface of a Project Factory project: page inventory, information architecture, layout, components, interaction states, responsive behavior, visual direction, or accessibility requirements. Trigger for requests such as "设计 UI", "页面布局", "组件规范", "交互设计", "wireframe", or when architecture is ready and delivery tasks need implementation-ready UI documentation. This skill produces design documents only, not frontend code.'
argument-hint: 'UI设计、页面布局、组件规范、交互设计、线框图、响应式与无障碍'
---

# UI Design

把用户故事和系统边界转换为可实现、可验收的 UI 设计文档，不生成产品代码。

## When to Use

- 需要页面清单、信息架构、导航或页面布局
- 需要组件状态、交互规则、响应式或无障碍规范
- 架构完成后，需要为交付拆解提供 UI 输入

## NOT When to Use

- 只选择技术栈或模块边界：使用 `architecture-decisions`
- 直接实现前端代码：进入实现仓库后执行
- 只制定视觉品牌或营销素材：单独处理品牌设计

## Input

| 来源 | 内容 |
|------|------|
| `vision.md`、`scope.md` | 目标用户、价值和范围 |
| `user-stories.md` | 用户目标、优先级和关键操作 |
| `system-design.md`、`api-spec.md` | 能力边界、数据和状态 |
| 用户消息 | 平台、品牌、设备、无障碍等约束 |

## Output Schema

主输出：`wiki/03-architecture/ui-design.md`

至少包含：

1. 设计目标与约束
2. 页面清单和页面间导航
3. 核心流程线框图
4. 组件及状态矩阵
5. 响应式与无障碍要求
6. 待确认问题和实现边界

## Minimum Viable Output

- 覆盖所有 P0 用户故事的页面和入口
- 至少描述正常、加载、空、错误、无权限五类状态
- 核心流程可从入口走到成功或失败结果
- 不虚构架构和 API 未支持的能力

## Complete Output

- 页面、组件、交互、视觉、响应式和无障碍规范完整
- 每个 P0 用户故事映射到页面和关键组件
- 关键交互有触发条件、反馈、失败处理和键盘行为
- UI 决策与系统设计、API 和验收条件一致

## Dependencies

| 类型 | Skill/文档 |
|------|------------|
| 前置 | `overview-framing`、`requirements-spec`、`architecture-decisions` |
| 依赖读取 | vision、scope、user-stories、system-design、api-spec（如有） |
| 后置 | `delivery-planning`、`acceptance-design` |

## Reference Routing

只在当前任务需要时读取，避免把示例当需求：

- 需要选择视觉方向时读取 `references/styles/style-presets.md`
- 需要线框图结构时读取 `references/templates/page-templates.md`
- 需要组件状态模板时读取 `references/templates/component-templates.md`

参考文件仅提供结构，所有名称、文案、状态和数据必须来自当前项目。

## Procedure

### 1. 建立 UI 覆盖矩阵

从 P0/P1 用户故事提取页面和操作：

```markdown
| US-ID | 用户目标 | 页面/入口 | 核心操作 | 成功反馈 | 失败反馈 |
|-------|----------|-----------|----------|----------|----------|
```

没有用户故事支持的页面不进入 MVP。

### 2. 定义信息架构

- 给出页面清单、层级和导航方式
- 标明公开、登录后、管理端等访问边界
- 用 Mermaid 或简洁文本表示页面流转
- 避免为单一页面创建多余导航层

### 3. 选择视觉方向

- 从参考预设中选一个最接近项目目标的方向，或明确自定义约束
- 说明选择理由、适用场景和不适用边界
- 定义颜色角色、字体层级、间距、圆角和焦点样式
- 不直接复制示例业务文案

### 4. 设计核心流程

每条 P0 流程至少覆盖：

```text
入口 → 输入/选择 → 校验 → 提交 → 成功或失败 → 可恢复动作
```

为关键页面给出 ASCII 线框图或 Mermaid 流程图；图中使用当前项目术语。

### 5. 定义组件和状态

```markdown
| 组件 | 用途 | 状态 | 输入 | 输出事件 | 无障碍要求 |
|------|------|------|------|----------|------------|
```

状态至少考虑：default、hover、focus、disabled、loading、success、error；不适用的状态明确省略。

### 6. 响应式与可访问性

- 明确主要断点或采用内容驱动的布局规则
- 所有操作必须可由键盘完成
- 焦点顺序、可见焦点、表单标签和错误关联必须明确
- 颜色不能作为唯一状态信号
- 动画遵循 reduced-motion 偏好
- 触控目标建议不小于 44×44 CSS px

### 7. 校验实现边界

- 页面字段必须能映射到 domain model/API；缺失项写入 open-questions
- 错误状态必须对应已知失败路径，不编造错误码
- UI 不替架构层决定鉴权、数据持久化或后台能力
- 复杂交互只有在用户故事明确需要时才设计

### 8. 输出与回写

1. 写入 `wiki/03-architecture/ui-design.md`
2. 将新增假设写入 `wiki/01-requirements/assumptions.md`
3. 将不可确认的业务选择写入 `open-questions.md`
4. 非默认设计选择写入 decision-log
5. 交给 `stage-review` 使用 UI 自定义 checklist 检查

## Do / Do Not

Do：

- 先覆盖核心用户流程，再补视觉细节
- 优先原生控件和常见交互，降低实现成本
- 明确加载、空、错误、权限和恢复路径
- 给出足够实现的信息，但不输出前端代码

Do not：

- 不把参考模板中的示例业务带入当前项目
- 不为“以后可能需要”设计页面或组件
- 不只提供色板而缺少流程和状态
- 不绕过用户确认做不可逆品牌或业务决策

## Target Pages

- `<项目根目录>/wiki/03-architecture/ui-design.md`
- 必要时回写 assumptions、open-questions、decision-log

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-07-15 | 重写为领域无关 UI 设计流程；增加参考文件按需路由、覆盖矩阵、状态、响应式和无障碍要求 | 移除单一业务案例污染并将主文件控制在 500 行内 |
| 2026-04-30 | 初始版本 | 建立 UI 设计文档流程 |
