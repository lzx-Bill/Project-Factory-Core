---
name: plain-language-handoff
description: 'Use when generating a plain-language project summary that anyone can understand — "generate plain summary", "create readable handoff", "non-technical summary", "全员可读概要", "通俗交接文档". This skill compiles a comprehensive yet accessible document from project design docs, written in everyday language that serves both human stakeholders (no technical background needed) and AI agents (complete enough for full design and implementation). Output: implementation-kit/PLAIN-LANGUAGE-SUMMARY.md'
argument-hint: '生成通俗文档、全员可读概要、plain language、non-technical summary、通用语言交接'
---

# Plain-Language Handoff Summary

将 Project Factory 设计文档编译为**全员可读的交接概要**，同时具备 AI 完整执行力。

## 定位

| 维度 | 说明 |
|------|------|
| 目标读者 A | 非技术背景的利益相关者（产品、运营、管理层） |
| 目标读者 B | AI 代理（能基于此文档完整 design + implement） |
| 输出位置 | `implementation-kit/PLAIN-LANGUAGE-SUMMARY.md` |
| 语言风格 | 通俗易懂，无行话，无缩写，附通俗解释 |
| 与 AGENTS.md 区别 | AGENTS.md 给 AI 技术开发者；这个给人类非技术读者 + AI 执行者 |

## 双重设计原则

| 受众 | 需求 |
|------|------|
| 人类（非技术） | 理解项目是什么、为什么、怎么做、无障碍沟通 |
| AI 执行者 | 获得足够上下文，完整设计 + 实现，不需额外追问 |

## When to Use

- `implementation-kit` 执行后自动触发（或独立调用）
- 用户说"生成通俗概要"、"生成全员可读文档"、"create plain summary"
- 需要向非技术利益相关者展示项目时
- 需要 AI 接手项目但不想读技术文档时

## Input

| 来源 | 内容 |
|------|------|
| 项目目录 | `<项目根目录>/` 下的所有 wiki 设计文档 |
| 优先级 | HOME.md → vision.md → scope.md → user-stories.md → system-design.md → task-breakdown.md |

## Output

```
<项目根目录>/implementation-kit/
└── PLAIN-LANGUAGE-SUMMARY.md   ← 本 skill 产出
```

## 内容结构（10 + 1 附录）

### 1. 一句话说清楚

**模板**：`这是个 [什么东西]，用来 [做什么]。

**要求**：8-15 个字，任何人能读懂。

---

### 2. 为什么需要它

**内容**：
- 背景故事：什么情况下产生这个需求
- 现有问题：人们现在怎么凑合，为什么不满意
- 解决承诺：用上这个会带来什么改善

**通俗写法**：假设在向朋友解释"这个东西是干嘛的"

---

### 3. 谁会用，怎么用

**内容**：
- 目标用户：什么人会用这个（用身份 + 日常场景描述，不要"用户"两个字）
- 使用时机：什么时候会用
- 核心动作：用户进来后主要做哪几件事

**通俗写法**：用"小王是个[职业]，他每天要[做什么]"的叙事

---

### 4. 它能做什么

**内容**：功能清单，每条用 `[用户] 可以 [做什么]` 描述。

**格式**：
```
- 你可以 [功能1]
- 你可以 [功能2]
- ...
```

**禁止**：
- ❌ 技术术语（如"API调用"、"数据库同步"）
- ❌ 产品黑话（如"赋能"、"闭环"）
- ❌ 模糊描述（如"高效管理"）

---

### 5. 它不能做什么

**内容**：明确排除的范围。

**格式**：
```
- 这个工具做不到 [排除项1]
- 这个工具不会 [排除项2]
```

---

### 6. 用户怎么做每一步

**内容**：操作流程，用自然顺序描述。

**格式**：
```
第一步：你先 [做什么]
第二步：然后 [做什么]
第三步：最后 [做什么]
```

**要求**：3-7 步，覆盖主要使用场景。

---

### 7. 做完之后变成什么样

**内容**：输入→输出的具体例子。

**格式**：
```
例子：假设 [输入场景]，工具会 [输出结果]

[输入]
→
[输出]
```

**要求**：至少 2 个具体例子，让 AI 理解预期效果。

---

### 8. 什么地方需要特别注意

**内容**：
- 异常处理：遇到问题时怎么办
- 已知限制：有什么已知的局限
- 注意事项：用户需要知道的前提条件

---

### 9. 我们做了哪些重要决定

**内容**：关键设计决策。

**格式**：
```
我们选择了 [方案A] 而不是 [方案B]
原因：[简短解释]
```

**数量**：3-5 条最重要的决策。

---

### 附录：完整功能规格表

**内容**：每行对应一个功能，包含：功能描述 | 怎么做算完成 | 有什么限制。

**格式**：
```
| 功能 | 完成标准 | 限制条件 |
|------|----------|----------|
| [功能1] | [可验证的完成标准] | [限制] |
```

---

## 翻译规则

### 术语对照表

| 技术术语 | 通俗解释 |
|---------|---------|
| API | 数据接口（类似"服务员"：你点单，他帮你拿到东西） |
| 数据库 | 数据的仓库（类似"档案室"） |
| 前端 | 你看到的界面（网站的"脸"） |
| 后端 | 幕后的处理程序（在后台帮你做事的东西） |
| 部署 | 让产品正式上线运行（类似"开店"） |
| 爬虫 | 自动抓取网页内容的程序（类似"复制粘贴机器人"） |
| 缓存 | 临时存放的数据（类似"口袋"，用完就走） |
| 日志 | 记录发生事情的日记（类似"流水账"） |

### 禁止用语

| 禁止 | 替换 |
|------|------|
| 用户 | 你 / 人们 |
| 调用 | 发送请求 / 请求 |
| 部署 | 上线 / 推出 |
| 异常 | 出错 / 问题 |
| 缓存 | 临时存储 |
| 集成 | 打通 / 联通 |

---

## Procedure

### Phase 1: 收集上下文

读取以下文件（按优先级）：
1. `HOME.md` → 项目一句话 + 当前状态
2. `wiki/00-overview/vision.md` → 背景和愿景
3. `wiki/00-overview/scope.md` → 范围和非目标
4. `wiki/01-requirements/user-stories.md` → 用户故事
5. `wiki/01-requirements/constraints.md` → 约束条件
6. `wiki/03-architecture/system-design.md` → 架构设计
7. `wiki/04-data-and-api/*.md` → 数据模型
8. `wiki/05-delivery/task-breakdown.md` → 任务列表

### Phase 2: 提炼核心信息

从每个文档提取关键信息：

| 文档 | 提取什么 |
|------|---------|
| HOME.md | 项目定义、阶段、决策 |
| vision.md | 背景故事、问题、价值 |
| scope.md | 范围边界、非目标 |
| user-stories.md | 用户画像、功能需求 |
| constraints.md | 硬约束、限制 |
| system-design.md | 模块划分、数据流 |
| task-breakdown.md | 任务列表、里程碑 |

### Phase 3: 编写各 Section

按内容结构逐节编写：

**Section 1（说清楚）**：
- 从 vision.md 提取一句话
- 检查：8-15 字？任何人都懂？

**Section 2-3（背景和用户）**：
- 从 vision.md + user-stories.md 提炼
- 用具体场景代替抽象描述

**Section 4-5（功能）**：
- 从 user-stories.md + scope.md 提取
- 用"你可以..."格式重写

**Section 6（流程）**：
- 从 system-design.md 的关键流程提取
- 确保 3-7 步，顺序正确

**Section 7（例子）**：
- 构造具体输入输出场景
- 至少 2 个，覆盖主要功能

**Section 8（注意）**：
- 从 constraints.md + assumptions.md 提取
- 标注已知限制

**Section 9（决策）**：
- 从 HOME.md 决策表 + decision-log.md 提取
- 选择 3-5 条最重要的

**附录（规格表）**：
- 从 task-breakdown.md + acceptance-plan.md 提取
- 每行：功能 | 完成标准 | 限制

**禁止包含**：
- ❌ 项目文件结构（如 "implementation-kit/", "prompts/"）
- ❌ 实现指导（如 "How to Start", "Questions to Clarify"）
- ❌ 项目状态信息（如 "现在进展到哪"）
- ❌ 指向其他设计文档的引用

### Phase 4: 术语检查

- 全文搜索技术术语
- 用通俗表达替换
- 检查比喻是否恰当

### Phase 5: 受众测试

快速自检：
- 能否用一句话向朋友解释这个项目？
- AI 能否基于此文档知道要做什么？

---

## 质量标准

| 标准 | 要求 |
|------|------|
| 完整性 | 10 个 section + 附录全部填写 |
| 可读性 | 初中生能读懂（无专业术语） |
| 可执行性 | AI 能基于文档完整实现 |
| 具体性 | 有具体例子，不是抽象描述 |
| 简洁性 | 无废话，每句都有信息 |

---

## Target Pages

- `<项目根目录>/implementation-kit/PLAIN-LANGUAGE-SUMMARY.md`

---

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 项目已完成孵化（HOME.md + wiki + task-breakdown.md） |
| 并行 | implementation-kit（同一批设计文档的不同产出） |
| 后置 | 利益相关者沟通 / AI 接手实现 |

---

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-28 | 删除 Section 10（项目状态） | PLAIN-LANGUAGE-SUMMARY 应该是纯产品说明书，不含项目状态/文件结构信息 |
| 2026-04-27 | 新建 skill | 满足双重需求：人类可读 + AI 可执行的全员可懂交接文档 |
