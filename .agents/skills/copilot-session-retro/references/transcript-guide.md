# Transcript 分析指南

## JSONL 文件结构

VS Code Copilot Chat 的 debug log 位于 `{{VSCODE_TARGET_SESSION_LOG}}/` 目录下，包含多个文件：

| 文件 | 内容 |
|------|------|
| `main.jsonl` | **主 transcript** — 所有主对话事件 |
| `runSubagent-{agent}-{toolId}.jsonl` | 子 agent 独立 session 日志 |
| `title-{id}.jsonl` | 对话标题生成日志 |
| `system_prompt_0.json` | System prompt 快照 |
| `tools_0.json` | 可用工具列表快照 |
| `models.json` | 可用模型列表 |

分析时以 `main.jsonl` 为主，如需深入子 agent 行为则读取对应 `runSubagent-*.jsonl`。

## JSONL 事件格式

每行是一个 JSON 对象，通用字段结构：

```json
{
  "v": 1,                    // 格式版本（仅 session_start）
  "ts": 1776909567912,       // 毫秒时间戳
  "dur": 0,                  // 持续时间（毫秒）
  "sid": "session-uuid",     // Session ID
  "type": "event_type",      // 事件类型（下划线分隔）
  "name": "event_name",      // 事件名称（更具体）
  "spanId": "span-id",       // Span ID（用于关联事件）
  "parentSpanId": "parent",  // 父 Span ID
  "status": "ok",            // 状态
  "attrs": { ... }           // 事件属性（各类型不同）
}
```

### 关键事件类型

| type | name 示例 | 含义 | attrs 关键字段 |
|------|-----------|------|---------------|
| `session_start` | `session_start` | Session 开始 | `copilotVersion`, `vscodeVersion` |
| `user_message` | `user_message` | 用户消息 | `content`（用户输入的完整文本） |
| `turn_start` | `turn_start:0` | AI 新 turn 开始 | `turnId`（字符串："0", "1", ...） |
| `turn_end` | `turn_end:0` | AI turn 结束 | `turnId` |
| `tool_call` | `read_file` / `grep_search` | 工具调用（含请求和结果） | `args`（参数 JSON 字符串）, `result`（结果 JSON 字符串） |
| `llm_request` | `chat:claude-opus-4.6` | LLM 请求（含 token 统计） | `model`, `inputTokens`, `outputTokens`, `ttft`（首 token 延迟 ms） |
| `agent_response` | `agent_response` | AI 完整回复 | `response`（含工具调用），`reasoning`（思考过程） |
| `discovery` | `Agent Discovery` | 发现 agents/skills/instructions | `details`（解析结果） |
| `child_session_ref` | `title` | 子 session 引用 | `childSessionId`, `childLogFile` |

### Turn 编号规则

- `turnId` 从 `"0"` 开始递增（字符串类型）
- 一个 `user_message` 触发一个或多个连续 turn（工具调用链产生多 turn）
- Turn 包含范围：`turn_start` → 多个 `tool_call` → `llm_request` → `agent_response` → `turn_end`
- `spanId` 和 `parentSpanId` 用于关联同一 turn 内的事件

### 重要字段说明

| 字段 | 位置 | 说明 |
|------|------|------|
| 用户输入文本 | `user_message.attrs.content` | 可能包含 XML 标签（`<attachments>` 等） |
| AI 思考过程 | `agent_response.attrs.reasoning` | 内部推理，关键分析材料 |
| AI 回复内容 | `agent_response.attrs.response` | JSON 数组，含文本和工具调用 |
| 工具名称 | `tool_call.name` | 根级 `name` 字段 |
| 工具参数 | `tool_call.attrs.args` | JSON 字符串 |
| 工具结果 | `tool_call.attrs.result` | JSON 字符串（可能很长，会被截断） |
| Token 使用 | `llm_request.attrs.inputTokens/outputTokens` | 用于效率分析 |
| 首 token 延迟 | `llm_request.attrs.ttft` | 毫秒，反映模型响应速度 |
| 模型 | `llm_request.attrs.model` | 如 `claude-opus-4.6` |

## 高效分析策略

### 策略 1: 先概览再深入

```
1. 统计 main.jsonl 总行数 → 估算 session 规模
2. grep "user_message" → 获取所有用户请求（从 attrs.content 提取）
3. grep "agent_response" → 获取 AI 回复（从 attrs.reasoning 了解决策过程）
4. grep '"type":"tool_call"' → 统计工具使用情况（从 name 字段获取工具名）
5. grep "llm_request" → 提取 token 统计和模型信息
6. 针对发现的问题深入读取具体 turn（用 spanId/parentSpanId 关联）
```

### 策略 2: 关注关键模式

搜索以下 pattern 来快速定位问题：

| 模式 | grep pattern | 说明 |
|------|-------------|------|
| 重复文件读取 | `"name":"read_file"` 配合 args 中同一文件名 | 效率问题 |
| 错误修复 | `"name":"replace_string_in_file"` 多次出现且 args 含同一位置 | 准确度问题 |
| 用户纠正 | `user_message` 的 content 含"不对"、"错了"、"不是" | 沟通/准确度问题 |
| 长思考短输出 | `agent_response` 的 reasoning 很长但 response 简短 | 效率问题 |
| 提问密度 | `"name":"vscode_askQuestions"` 出现频率 | 沟通模式 |
| Token 消耗 | `llm_request` 的 `inputTokens` 和 `outputTokens` | 效率/成本分析 |
| 子 agent 调用 | `"name":"runSubagent"` | 复杂度指标 |
| 上下文压缩 | `child_session_ref` 或 conversation-summary 出现 | 长 session 标记 |

### 策略 3: 时间线重建

```
1. 提取所有事件的 ts 字段（毫秒时间戳）
2. 按 turn_start/turn_end 分组计算每轮耗时
3. 识别用户消息间的长间隔（可能在思考/不满意）
4. 识别 tool_call 密集区（AI 连续多次工具调用 = 复杂任务）
5. 从 llm_request.attrs.ttft 分析响应延迟
```

## 常见问题模式检测

### AI 侧

1. **循环搜索**：3+ 次 `tool_call` 中 `name` 为搜索类工具且 args 相似
2. **过度读取**：`read_file` 的行范围远超实际需要
3. **假设性错误**：`agent_response.attrs.reasoning` 中假设了事实，后续被推翻
4. **遗漏检查**：`replace_string_in_file` 后未跟 `get_errors` 验证
5. **模板机械套用**：输出与模板格式差异但未调整
6. **Token 浪费**：`llm_request.attrs.inputTokens` 异常高（重复塞入大量上下文）

### User 侧

1. **需求后置**：先让 AI 做完再提出额外要求
2. **模糊指令**：使用"调整一下"、"改改"等不具体的描述
3. **跨 turn 要求变更**：同一任务的要求在多个 turn 中逐步展开
4. **隐含标准**：有未明说的质量标准
