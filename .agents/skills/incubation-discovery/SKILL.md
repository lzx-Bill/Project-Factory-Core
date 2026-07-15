---
name: incubation-discovery
description: >-
  Use when exploring a new project idea from many angles before writing formal
  requirements. Trigger when user says "brainstorm", "explore directions",
  "generate ideas", "opportunity map", "scenario options", "feature ideas",
  "creative direction", or when they want to "see what's possible" before
  committing to a specific scope. Only use after a project folder exists; for
  initial setup use project-bootstrap first.
argument-hint: '方向发散、机会点、创意池、场景矩阵、候选功能、脑暴'
---

# Incubation Discovery

用于围绕待孵化项目做多维度方向发散，并把结果沉淀为可阅读文档。

## When to Use

- 用户还在探索项目方向，需要先看全局可能性
- 需要围绕同一个项目穷举用户、场景、功能、商业化、技术路线等维度
- 需要先形成可阅读的创意池和机会地图，再决定哪些内容进入正式需求

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 项目名称、一句话想法、关心的维度（可选） |
| 当前项目 | 项目根目录已存在（由 project-bootstrap 建立） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/00-overview/idea-landscape.md` | 发散文档 | 用户画像、场景矩阵、痛点、差异化方向 |
| `wiki/00-overview/scenario-matrix.md` | 矩阵页 | 场景 × 价值 × 风险 三维矩阵 |
| `wiki/01-requirements/feature-ideas.md` | 功能候选 | 候选功能清单，含差异化说明 |
| `wiki/02-research/opportunity-backlog.md` | 机会backlog | 高潜力/低成本/实验型机会分类 |

## Minimum Viable Output

- idea-landscape.md 含 ≥3 个维度（用户/场景/痛点）的发散内容
- **每个方向含差异化说明**（≥1 句）
- **至少 1 个意外洞察**（看似不相关但有联系的机会点）
- feature-ideas.md 含 ≥5 条候选功能，每条含简要说明

## Complete Output

- 上述全部文件均含实质内容
- 每个方向含推荐理由、适用前提、下一步建议
- 已区分"已确认方向"、"候选方向"、"激进创意"、"暂不采纳"
- 意外洞察 ≥2 个

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `project-bootstrap`（项目目录已建立） |
| 后置 | `overview-framing`（从发散收敛到愿景）、`requirements-spec`（从功能候选到正式需求） |
| 并行 | 无 |

## Procedure

1. 确认项目名称、一句话定义和目标项目根目录 `<项目根目录>/`
2. 只在该项目目录下输出探索结果，不把项目特定想法写回仓库根目录
3. 至少从以下 10 个维度发散，每个维度→输出文件的映射关系如下：

| 维度 | 输出文件 |
|------|---------|
| 用户画像、核心场景、痛点 | idea-landscape.md |
| 差异化方向 | idea-landscape.md |
| 候选功能 | feature-ideas.md |
| 商业模式、内容来源 | idea-landscape.md（商业模式节） |
| 增长方式 | idea-landscape.md（增长策略节） |
| 技术切入点、风险假设 | opportunity-backlog.md（实验型机会） |
| 场景 × 价值 × 风险 | scenario-matrix.md |

**两套分类标准的区别**：
- "已确认 / 候选 / 激进 / 暂不采纳"是**方向成熟度**分类，用于筛选进入正式需求的内容
- "高潜力 / 低成本 / 差异化 / 实验型 / 暂缓"是**机会优先级**分类，用于 opportunity-backlog.md 中的机会排序
- 两套分类并行使用，服务不同目的
4. 【差异化要求】每个方向必须回答：
   - 这个方向与市面上现有方案的**差异化是什么**？
   - 为什么用户需要这个而不是替代品？
   - 最有可能成功的**切入点是什么**？（给出理由）
5. 【反模板化原则】
   - **禁止泛泛而谈**：如"用户画像：20-35岁年轻人"需改为具体到可辨识的群体
   - **禁止正确废话**：如"提供良好的用户体验"需改为具体什么体验、怎么提供
   - **禁止无差异描述**：每个方向必须有"为什么有意思"的说明，不能只罗列功能清单
   - **至少 1 个意外洞察**：看似不相关但实际有联系的机会点，给用户惊喜
6. 区分"已确认方向"、"候选方向"、"激进创意"、"暂不采纳方向"，不要把发散结果伪装成定稿
7. 每个维度都尽量给出推荐理由、适用前提和下一步建议，方便用户阅读后筛选

## Enriched Behavior

- 不只做发散罗列，要帮助用户比较、筛选、收敛和发现盲区
- 可以主动从产品、用户、增长、商业化、内容、技术、运营等多维度扩展视角
- 当创意很多时，优先分层：高潜力、低成本、差异化、实验型、暂缓项
- 输出应偏"给用户看"的阅读体验，避免只写成内部思维草稿

## Target Pages

- `<项目根目录>/wiki/00-overview/idea-landscape.md`（主）
- `<项目根目录>/wiki/00-overview/scenario-matrix.md`（主）
- `<项目根目录>/wiki/01-requirements/feature-ideas.md`（主）
- `<项目根目录>/wiki/02-research/opportunity-backlog.md`（主）

## 与 overview-framing 的区别

| Skill | 关注点 | 产出特征 |
|-------|--------|---------|
| `incubation-discovery` | 发散探索、穷举可能性 | 创意池、候选清单、多方向平行 |
| `overview-framing` | 收敛定位、锁定边界 | 确定范围、非目标、成功标准 |

> 当用户说"看看有哪些方向"时用 incubation-discovery；当用户说"确定这个项目具体做什么"时用 overview-framing。

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：新增 10 维度→4 文件映射表；澄清两套分类标准的区别（方向成熟度 vs 机会优先级） | 10 维度→4 文件映射不清、两套分类标准混用 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、Changelog | 统一 skill 结构，明确前置依赖关系 |
| 2026-04-26 | 增强：增加差异化洞察要求和反模板化原则，禁止泛泛而谈和正确废话 | 解决产出缺乏创意的问题 |
