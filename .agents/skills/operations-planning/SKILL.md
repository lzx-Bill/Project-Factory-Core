---
name: operations-planning
description: 'Use when documenting deployment, environment layout, monitoring, alerting, rollback, runtime constraints, or operational dependencies. Trigger when user says "deployment", "operations", "monitoring", "rollback", "runtime", "environment", "infrastructure", "SLA", or when preparing for production launch. Coordinate with architecture-decisions for deployment topology and with delivery-planning for operational tasks.'
argument-hint: '部署规划、环境配置、监控告警、回滚策略、运行约束、运维'
---

# Operations Planning

用于记录部署和运行约束。

## When to Use

- 需要补部署说明和环境约束
- 需要设计监控、告警、回滚
- 需要记录运行时依赖和操作边界
- 准备进入生产环境或交付运维

## Input

| 来源 | 内容 |
|------|------|
| 用户消息 | 运维需求、部署环境、监控要求 |
| 当前项目 | architecture.md（部署拓扑）、system-design.md（组件依赖） |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/07-operations/deployment.md` | 部署说明 | 环境矩阵、依赖服务、部署步骤 |
| `wiki/07-operations/monitoring.md` | 监控告警 | 监控指标、告警规则、日志 |
| `wiki/07-operations/rollback.md` | 回滚策略 | 回滚入口、触发条件、操作步骤 |

## Minimum Viable Output

- deployment.md 含：环境划分（dev/staging/prod）、依赖服务列表、部署步骤 ≥3 步
- monitoring.md 含：≥3 个关键监控指标
- rollback.md 含：回滚触发条件 + 操作步骤

## Complete Output

- deployment.md：完整配置项清单、端口映射、计划任务、资源需求
- monitoring.md：完整 SLA/SLO、告警阈值、日志规范
- rollback.md：完整故障处理入口、风险点清单
- 含与 architecture、data-api 的一致性检查

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `architecture-decisions`（部署拓扑已定） |
| 后置 | `delivery-planning`（运维任务入任务清单） |
| 依赖读取 | architecture.md（组件依赖）、data-api.md（服务端口） |

## Procedure

1. 先确认目标项目根目录，并只在该项目目录下写运维文档
2. 写清环境、依赖、部署步骤
3. 监控和回滚不能缺席
4. 与架构文档中的端口、服务名、计划任务保持一致

### 部署关键步骤检查清单

每次部署必须逐项确认：

```markdown
## 部署前检查

- [ ] 代码已通过所有 CI 检查（单元测试、集成测试）
- [ ] 已在预发布环境验证通过
- [ ] 数据库迁移脚本已准备并测试
- [ ] 配置文件（环境变量、密钥）已更新
- [ ] 回滚方案已确认可用
- [ ] 相关团队（运维/测试/产品）已通知
- [ ] 部署时间窗口已确认

## 部署中执行

- [ ] 按顺序执行部署步骤（参照 deployment.md）
- [ ] 每步执行后验证健康检查通过
- [ ] 关键指标监控开启（CPU/内存/错误率/延迟）
- [ ] 记录部署时间线和每步结果

## 部署后验证

- [ ] 核心功能冒烟测试通过
- [ ] 监控指标无异常
- [ ] 旧版本包/镜像保留至少 24 小时（用于回滚）
- [ ] 部署完成通知已发送
```

### 监控指标框架

```markdown
## 监控指标体系

| 类别 | 指标 | 告警阈值 | 数据来源 |
|------|------|---------|---------|
| 可用性 | 服务 uptime | < 99.9% 告警 | 健康检查 |
| 性能 | API P99 延迟 | > 2s 告警 | APM |
| 性能 | API 错误率 | > 1% 告警 | 日志 |
| 资源 | CPU 使用率 | > 80% 持续 5min | 监控 |
| 资源 | 内存使用率 | > 85% 告警 | 监控 |
| 业务 | 日活用户 | 较昨日跌 > 20% 告警 | 数据平台 |
```

## Enriched Behavior

- 不只写上线步骤，要让后续运行、监控、故障处理都有抓手
- 可以主动补充环境矩阵、配置项、资源需求、SLA/SLO、值班关注点等信息
- 如果运维方案尚未定型，可以先写候选方案和运行约束，供用户评估
- 输出应尽量减少部署落地时的隐性知识依赖

## Target Pages

- `<项目根目录>/wiki/07-operations/deployment.md`（主）
- `<项目根目录>/wiki/07-operations/monitoring.md`（主）
- `<项目根目录>/wiki/07-operations/rollback.md`（主）

## 页面归属说明

| 页面 | 主负责 | 辅参与 |
|------|--------|--------|
| deployment.md | operations-planning | architecture-decisions（部署拓扑） |
| monitoring.md | operations-planning | - |
| rollback.md | operations-planning | - |

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：新增部署关键步骤检查清单（部署前/部署中/部署后三阶段）；新增监控指标框架表（可用性/性能/资源/业务，含告警阈值和数据来源） | 部署步骤缺少检查清单、监控指标框架不完整 |
| 2026-04-26 | 增强：新增 Input/Output Schema、Dependencies、Min/Complete Output 两级标准、页面归属表、Changelog | 统一 skill 结构，强化运维文档的完整性要求 |
