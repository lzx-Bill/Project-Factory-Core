# Component Templates

组件模板只定义需要说明的字段，不指定业务名称或视觉品牌。

## Component Spec

```markdown
### <组件名称>

| 字段 | 内容 |
|------|------|
| 用途 | 解决什么交互问题 |
| 变体 | primary / secondary / destructive（按需） |
| 状态 | default / hover / focus / disabled / loading / error |
| 输入 | props、数据或用户输入 |
| 输出 | 事件与结果 |
| 键盘 | Tab、Enter、Space、Escape、方向键（按需） |
| 语义 | 原生元素或 ARIA 角色 |
| 响应式 | 小屏和大屏差异 |
```

## Button

- 使用原生 `button` 语义
- loading 时避免重复提交并保留可理解的名称
- destructive 操作需要风险清晰的确认步骤
- 只有一个主要操作时才使用 primary 强调

## Form Field

- label 与控件明确关联
- 帮助文本和错误文本使用稳定 ID 关联
- 错误同时提供文字说明，不只改变颜色
- 校验时机说明为提交时、失焦时或实时校验

## List Item / Card

- 明确整项是否可点击，避免嵌套冲突操作
- 主要信息、次要信息、状态和操作层级清晰
- 列表大量数据时说明分页或虚拟化条件，不默认引入

## Dialog / Drawer

- 打开后焦点进入容器，关闭后返回触发元素
- Escape 行为和遮罩点击行为明确
- 重要操作不能只依赖弹窗承载，移动端需评估整页替代

## Feedback

| 类型 | 何时使用 | 必须包含 |
|------|----------|----------|
| inline | 字段或局部错误 | 原因、修复方式 |
| toast | 非阻塞结果 | 简短结果、必要的撤销入口 |
| banner | 页面级持续状态 | 影响范围、下一步 |
| progress | 可感知等待 | 当前状态；可取消时给取消入口 |

## Navigation

- 当前页面状态对视觉和辅助技术都可识别
- 移动端折叠不能隐藏唯一关键操作
- 导航项来自信息架构，不根据模板自行增加
