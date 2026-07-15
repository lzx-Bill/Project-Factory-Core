---
name: stage-review
description: 'Use when reviewing any project document against a checklist — "review this stage", "check my output", "self review", "自审", "质量检查". This is a GENERAL document review skill usable by any pipeline (express-incubate or gradual). It reads a document, runs a checklist, produces a structured review report with PASS/FAIL per item, and auto-fixes simple gaps. NOT for user-facing code review — for project factory document quality.'
argument-hint: '文档自审、质量检查、review报告、checklist验证'
---

# Stage Review

通用文档质量自审。任何阶段产出后调用，输出结构化评审报告。

## 定位

| 维度 | 说明 |
|------|------|
| 目标 | 自动验证文档质量，发现缺口，尽量自动修正 |
| 调用方 | express-incubate（每阶段后）、渐进单阶段（用户要求时） |
| 输出 | 结构化评审报告 + 自动修正（如可行） |
| 与 acceptance-design 区别 | acceptance 验的是最终交付物；stage-review 验的是中间产出 |

## When to Use

- express-incubate 每阶段产出后自动调用
- 用户说"检查一下这个文档"、"review 这个阶段"
- 渐进链路中用户要求自审当前产出

## Input

| 来源 | 内容 |
|------|------|
| 当前文档 | 待审文档的完整内容 |
| 阶段类型 | `bootstrap` / `incubation` / `overview` / `requirements` / `architecture` / `delivery`（用于选择checklist） |
| 附加checklist | 可选，用户可传入自定义检查项覆盖默认 |
| 模式 | `review`（默认，只报告）或 `fix`（仅修机械性缺口） |

## Output

### 评审报告格式

```json
{
  "stage": "overview",
  "document": "wiki/00-overview/vision.md",
  "timestamp": "2026-04-26T22:00:00",
  "result": "PASS" | "PASS_WITH_GAPS" | "FAIL",
  "items": [
    {"id": "R3.1", "check": "问题陈述", "result": "PASS", "evidence": "文档第3行..."},
    {"id": "R3.3", "check": "成功标准可量化", "result": "FAIL", "gap": "成功标准'用户体验好'不可量化", "auto_fixed": true, "fixed_to": "用户操作完成率 ≥90%"}
  ],
  "gaps_unresolved": [],
  "auto_fixes_applied": 2
}
```

### 文件产出

| 文件 | 说明 |
|------|------|
| `reports/stage-review/<stage>-<timestamp>.json` | 结构化评审报告 |
| `<原文档>` | 仅 `mode=fix` 且属于机械性缺口时允许修改 |

## Procedure

### Step 1: 加载 Checklist

根据 `stage` 类型选择对应 checklist（见下方）。如用户传入自定义 checklist，则以自定义为准（合并而非替换关键项）。

**各阶段默认 Checklist：**

#### bootstrap
| ID | 检查项 | 判定 |
|----|--------|------|
| B1 | HOME.md 存在，含项目定义 | FAIL 即阻断 |
| B2 | wiki 目录结构完整（00-08 每个目录存在） | FAIL 即阻断 |
| B3 | 阶段标记为"启动中" | FAIL 即阻断 |

#### incubation
| ID | 检查项 | 判定 |
|----|--------|------|
| I1 | idea-landscape.md 含 ≥2 用户画像 | FAIL |
| I2 | 含 ≥2 核心场景 | FAIL |
| I3 | 含 ≥3 候选方向 | FAIL |
| I4 | scenario-matrix.md 存在 | FAIL |

#### overview
| ID | 检查项 | 判定 |
|----|--------|------|
| O1 | vision.md 含：问题陈述 + 目标用户 + 核心价值 | FAIL |
| O2 | scope.md 含：范围清单 + 非目标清单 | FAIL |
| O3 | vision.md 问题陈述非空且具体 | FAIL |
| O4 | 非目标 ≥1 条 | WARNING |

#### requirements
| ID | 检查项 | 判定 |
|----|--------|------|
| R1 | user-stories.md 含 ≥3 条用户故事 | FAIL |
| R2 | 每条含"作为...我希望...以便..."格式 | FAIL |
| R3 | 含 MVP 划分（P0/P1/P2 优先级） | FAIL |
| R4 | constraints.md 含 ≥2 条约束 | FAIL |
| R5 | 假设已标注（assumptions.md 存在且非空） | WARNING |

#### architecture
| ID | 检查项 | 判定 |
|----|--------|------|
| A1 | system-design.md 含 ≥3 模块 | FAIL |
| A2 | 含关键链路描述 | FAIL |
| A3 | 含技术栈选择及选型理由 | FAIL |
| A4 | 模块间依赖关系清晰 | WARNING |

#### delivery
| ID | 检查项 | 判定 |
|----|--------|------|
| D1 | task-breakdown.md 含 ≥5 任务 | FAIL |
| D2 | 含 ≥2 里程碑 | FAIL |
| D3 | 每个任务含验收标准（非空） | FAIL |
| D4 | 任务依赖关系无循环 | FAIL |
| D5 | 估算工时已标注（天或 story points） | WARNING |

### Step 2: 逐项检查

对每个检查项：
1. 读取文档中对应部分
2. 根据判定标准给出 PASS / FAIL
3. 记录 evidence（PASS 的证据行号或 FAIL 的具体缺口）

### Step 3: 聚合判定

整体 result 按以下规则聚合：

| 关键项 FAIL | 非关键项 FAIL | 整体 result |
|------------|--------------|-------------|
| 任意 1 项 | 任意数量 | FAIL |
| 0 项 | 0 项 | PASS |
| 0 项 | ≥1 项 | PASS_WITH_GAPS |

**关键项定义**：判定列为 `FAIL` 或 `FAIL 即阻断` 的检查项。判定列为 `WARNING` 的检查项只产生 `PASS_WITH_GAPS`。

### Step 4: 可选修正

默认 `mode=review`，不修改原文档。只有调用方明确传入 `mode=fix` 时，才判断缺口能否自动修正：

| 可自动修正 | 须报告（不擅自改） |
|-----------|-------------------|
| 缺数量不足（如只有2条场景，需加到3） | 内容方向错误（如"目标用户"写成"所有人"但无法推断正确用户） |
| 格式不规范（如用户故事缺少"以便..."） | 业务决策缺口（如缺少不可逆决策分级，AI不能替用户决定） |
| 缺失必要字段（如缺少导航链接） | 矛盾内容（需要用户拍板的方向性矛盾） |

**冲突处理原则**：当一项操作同时满足"可自动修正"和"涉业务方向"时，**须报告**，不擅自修正。

自动修正后，在报告中标注 `auto_fixed: true` 和修正内容；修改后必须重新执行对应检查项。

无法自动修正的，标注到 `gaps_unresolved`。

### Step 5: 输出报告

1. 将评审报告写入 `reports/stage-review/<stage>-<timestamp>.json`
2. 不向原文档追加 `[REVIEW: ...]` 标记；评审报告是唯一状态来源
3. `mode=review` 不修改原文；`mode=fix` 只保留已通过重审的机械性修正
4. 返回评审结果摘要

## Enriched Behavior

- **修正优先**：能自动修的先修好，不把简单问题留给用户
- **不越界**：涉及业务方向、用户意图的判断，只报告不修改
- **证据可查**：每条 PASS/FAIL 都记录具体位置
- **报告可追溯**：所有评审报告存入 `reports/stage-review/`，供复盘使用

## Target Pages

- `<项目根目录>/reports/stage-review/<stage>-<timestamp>.json`

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | 被评审的文档已产出 |
| 后置 | 评审报告供 `execution-log` 记录、供 `retrospective` 回查 |
| 并行 | 无 |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-07-15 | 明确 `review/fix` 两种模式；统一 FAIL 聚合规则；评审报告作为唯一状态来源 | 消除“自动改原文”与“不修改原文”的契约冲突 |
| 2026-04-30 | 修复：内嵌各阶段 checklist（移除外部引用）；新增聚合判定规则（关键项 FAIL→整体 FAIL）；修复冲突处理（涉业务方向不自动修正）；移除原文档追加标注（评审结果不入原文档） | 检查项引用文件不存在、聚合规则缺失、修正权限边界模糊、评审标注污染原文档 |
| 2026-04-26 | 新建 skill | 从 express-incubate 中抽取自审逻辑为独立技能，实现关注分离 |
