---
name: skill-creator
description: 'Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, or optimize a skill description for better triggering accuracy. Also use when a gap in the current skill set is identified.'
argument-hint: '创建新skill、修改skill、优化skill、skill测试、skill评估'
---

# Skill Creator

用于创建新 skill 和迭代改进已有 skill。

## When to Use

- 需要从零创建一个新 skill
- 需要修改或优化已有 skill
- 需要运行测试验证 skill 效果
- 需要优化 skill description 以提升触发准确性
- 发现当前 skill 集合存在空白

## NOT When to Use

- 只需要运行已有 skill — 直接调用该 skill 即可
- 只需要编辑单页文档 — 直接用 Write/Edit 工具

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 需求描述、触发场景、目标输出 |
| 当前项目 | 现有 skill 集合（确认是否重复或冲突） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `.Codex/skills/<skill-name>/SKILL.md` | Skill 定义 | Codex 标准 skill 结构 |
| `.Codex/skills/<skill-name>/references/` | 参考文档 | 可选，包含技能相关文档 |
| `.Codex/skills/<skill-name>/scripts/` | 脚本 | 可选，包含自动化脚本 |
| `<skill-name>-workspace/` | 测试工作区 | eval 测试用例和结果 |

## Minimum Viable Output

- SKILL.md 含：name、description、argument-hint、When to Use、Procedure、Target Pages
- description 长度 ≥100 字，含具体触发场景
- 至少 1 轮用户反馈迭代

## Complete Output

- SKILL.md：完整含 Input/Output Schema、Dependencies、Min/Complete Output
- 含自测报告（测试用例执行结果）
- description 经过人工评审优化

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 无（可随时创建新 skill） |
| 后置 | 新 skill 需经过测试和用户确认后再正式加入路由 |
| 依赖读取 | 现有 skill 集合（确认无重复） |

## Procedure

### 高层流程

```
理解意图 → 访谈调研 → 写 SKILL.md 草稿 → 写测试用例 → 跑测试 → 用户评审 → 迭代改进 → 描述优化 → 交付
```

### 1. 创建 Skill

#### Capture Intent

从对话历史中提取用户意图：skill 应该做什么？何时触发？期望的输出格式？

#### Interview and Research

主动询问边界情况、输入输出格式、示例文件、成功标准。

#### Write the SKILL.md

按统一结构填写：
- **name**: Skill 标识符（kebab-case）
- **description**: 触发机制核心，包含 skill 做什么和何时使用。要"pushy"——包含具体触发场景，≥100 字
- **argument-hint**: 中文触发词提示
- **When to Use**: 触发场景清单
- **NOT When to Use**: 何时不用此 skill（避免误触发）
- **Input/Output Schema**: 输入来源和目标输出文件
- **Dependencies**: 前置/后置/并行 skill
- **Procedure**: 标准工作步骤（用 do/not-do 清单）
- **Minimum Viable Output / Complete Output**: 两级输出标准
- **Target Pages**: 产出的目标页面
- **Enriched Behavior**: 增强行为指导（可选）
- **Changelog**: 变更记录

#### Skill 写作规范

**Skill Anatomy:**
```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code
    ├── references/ - Docs loaded as needed
    └── assets/     - Templates, icons, fonts
```

**页面结构规范:**
- SKILL.md 保持在 500 行以内；超过时拆分为 SKILL.md + 子文档
- Procedure 使用 do/not-do 清单格式（如 `incubation-discovery`）
- 引用文件时明确标注何时需要读取

### 2. 编写测试用例

写 2-3 个真实测试 prompt，保存到 `evals/evals.json`：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的任务描述",
      "expected_output": "期望产出的描述",
      "files": []
    }
  ]
}
```

**测试用例原则：**
- 每个测试用例代表一个真实触发场景
- 避免过于简单或过于复杂的边界 case
- 含期望产出描述，用于后续判定是否通过

### 3. 执行测试

#### Codex 执行方式（无 Python 工具链）

按以下步骤手动执行测试：

**Step 1: 读取被测 skill**
读取待测 skill 的 SKILL.md，理解其预期行为。

**Step 2: 逐个执行测试用例**

对每个测试用例：
1. 构造符合 `prompt` 字段的输入
2. 带着 skill 上下文执行（读取 skill 文件）
3. 记录实际产出

**Step 3: 人工判定**

对每个测试用例：
1. 对照 `expected_output` 判定 PASS/FAIL
2. 记录具体差异（PASS 的证据或 FAIL 的原因）
3. 将结果写入 `grading.json`：

```json
{
  "eval_id": 1,
  "result": "PASS|FAIL",
  "evidence": "具体证据",
  "gap": "如果 FAIL，描述差距"
}
```

**Step 4: 汇总报告**

生成 `<workspace>/iteration-1/report.md`：
```markdown
# Skill Eval Report: <skill-name>

## 测试结果

| 测试用例 | 结果 | 证据 |
|---------|------|------|
| eval-1 | PASS | 成功产出预期文件 |
| eval-2 | FAIL | 缺少 X 字段 |

## 改进建议

- 问题 1: ...
- 问题 2: ...
```

#### 有 Python 工具链的环境（可选）

如果有 `scripts/` 目录，可选地使用自动化工具：

```bash
# 聚合评分
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>

# 启动评测查看器
python <skill-creator-path>/eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "my-skill"
```

> ⚠️ Codex 默认没有这些 Python 工具链。使用上方的手动评测流程。

### 4. 迭代改进

根据测试结果改进 skill：

1. **不要过度拟合** — 从具体反馈中提炼通用规律
2. **保持 prompt 精简** — 删除没有实际作用的描述
3. **解释 WHY** — 用"因为..."替代生硬的 MUST 规则
4. **寻找重复工作** — 如果所有测试用例都写了同一个辅助函数，考虑 bundling

**迭代循环：**
```
应用改进 → 重新跑测试 → 用户评审 → 继续迭代
```

停止条件：用户满意、反馈为空、或无明显改进空间。

### 5. Description 优化

优化 description 字段以提升触发准确性：

**Step 1: 生成测试查询**

创建 20 个测试查询 — 包含应触发和不应触发的场景。重点关注模糊边界。

**Step 2: 手动对比**

对每个测试查询，对比原 description 和候选 description 的触发效果。选出在准确性和覆盖面间平衡最好的版本。

**Step 3: 用户评审**

呈现候选 description 给用户，选择或进一步修改。

### 6. 打包交付

完成所有迭代后：

1. 确认 `.Codex/skills/<skill-name>/SKILL.md` 结构完整
2. 确认 `Changelog` 已更新
3. 将 skill 目录复制到目标位置
4. 向用户说明 skill 的触发词和使用方式

---

## Codex 评测工作流（总结）

```markdown
1. 读取 skill SKILL.md
2. 构造测试输入
3. 带 skill 上下文执行
4. 对照 expected_output 判定 PASS/FAIL
5. 记录到 grading.json
6. 汇总到 report.md
7. 根据反馈迭代改进
```

**无需 Python 脚本、无需 subagent、无需浏览器。全部手动完成。**

---

## Reference Files（人工参考）

以下文件可在人工评测时阅读参考：

| 文件 | 用途 |
|------|------|
| `agents/grader.md` | 如何对输出做 assertion 判定 |
| `agents/comparator.md` | 如何做 A/B 盲测对比 |
| `agents/analyzer.md` | 如何分析评测结果模式 |
| `references/schemas.md` | evals.json、grading.json 的 JSON 结构规范 |

> 这些文件是给人工参考的概念指南，不需要自动化工具即可理解和使用。

## Target Pages

- `.Codex/skills/<skill-name>/SKILL.md`
- `.Codex/skills/<skill-name>/references/`
- `.Codex/skills/<skill-name>/scripts/`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-29 | v2.0: 移除 Python 工具链依赖，重写为 Codex 兼容的手动评测流程；新增 NOT When to Use；Procedure 改为 do/not-do 清单风格 | Codex 无 Python eval 脚本，需手动评测 |
| 2026-04-26 | 统一结构增强（Input/Output/Dependencies/Min-Complete/Changelog）+ 保留完整工作流 | 修复首次增强时意外裁剪核心流程的问题 |
