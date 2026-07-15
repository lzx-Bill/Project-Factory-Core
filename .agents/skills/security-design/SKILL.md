---
name: security-design
description: 'Use when designing security architecture for a project — "security design", "authentication", "authorization", "access control", "data encryption", "security audit", "安全设计", "认证授权", "数据安全". This skill designs authentication/authorization systems, defines input validation rules, specifies data encryption requirements, and identifies security risks. Use after architecture-decisions and before delivery-planning.'
argument-hint: '安全设计、认证授权、输入校验、数据加密、敏感信息、安全审计'
---

# Security Design

用于设计项目安全架构。

## When to Use

- 需要设计认证/授权系统
- 需要定义输入校验规则
- 需要考虑数据加密和敏感信息保护
- 需要识别安全风险并制定缓解措施
- 需要确保符合安全合规要求

## NOT When to Use

- 纯本地应用，无敏感数据
- CLI 工具，不涉及安全威胁
- 已有完整安全设计，只需实现

## Input

| 来源 | 内容 |
|------|------|
| system-design.md | 架构和模块划分 |
| user-stories.md | 用户角色和使用场景 |
| constraints.md | 安全相关约束 |
| scope.md | 功能范围 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/03-architecture/security.md` | 安全设计 | 认证/授权/加密/校验规范 |

## Minimum Viable Output

- 认证方案（有无认证、方式）
- 授权规则概要（角色/权限）
- 输入校验关键点（≥3 项）
- 敏感数据清单和保护措施

## Complete Output

- 完整安全设计，含：
  - 认证方案详细设计
  - 授权模型（RBAC/ABAC/其他）
  - 会话管理策略
  - 数据加密方案
  - 输入校验完整规则
  - 输出编码规范
  - 敏感信息处理
  - 安全风险登记册
  - 安全测试用例

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `architecture-decisions`（架构已定）、`requirements-spec`（用户角色已定） |
| 后置 | `data-api-design`（API 安全契约）、`delivery-planning`（安全任务拆分） |
| 依赖读取 | system-design.md、user-stories.md、constraints.md |

## Procedure

### Phase 1: 理解上下文

1. 读取 `system-design.md` → 确定模块划分和信任边界
2. 读取 `user-stories.md` → 确定用户角色和使用场景
3. 读取 `constraints.md` → 确定安全相关约束（合规要求、数据敏感性）
4. 识别资产：哪些是敏感数据需要保护

### Phase 2: 认证方案设计

```markdown
## 认证方案

| 问题 | 答案 |
|------|------|
| 是否需要认证？ | 是/否 |
| 认证方式？ | 用户名密码/OAuth/Token/API Key/生物识别 |
| MFA/2FA？ | 是否需要多因素认证（TOTP/短信/邮件/硬件令牌） |
| 会话管理？ | 无状态 JWT / 有状态 Session |
| 会话有效期？ | Access Token X 分钟，Refresh Token Y 天 |
| 会话安全属性？ | Session Fixation 防护、会话超时、并发登录限制 |

### Phase 3: 授权模型设计

```markdown
## 授权模型

### 角色定义

| 角色 | 描述 | 权限 |
|------|------|------|
| 管理员 | 系统管理 | CRUD 所有资源 |
| 用户 | 普通用户 | CRUD 自己的资源 |
| 访客 | 未认证 | 只读公开资源 |

### 权限矩阵

| 资源 | 管理员 | 用户 | 访客 |
|------|--------|------|------|
| /api/users | CRUD | R(own) | - |
| /api/posts | CRUD | CRUD(own) | R(public) |
```

### RBAC/ABAC 选择

```
RBAC: 适合角色固定、权限相对静态的场景
ABAC: 适合需要细粒度、动态权限的场景
```

### Phase 4: 输入校验规则

```markdown
## 输入校验

### 通用规则

| 字段类型 | 校验规则 |
|---------|---------|
| 字符串 | 长度限制、禁止 HTML/JS |
| 邮箱 | 格式校验、正则 |
| 密码 | 最小长度、复杂度要求 |
| 数字 | 范围限制、最大值 |
| UUID | 格式校验、存在性检查 |

### SQL 注入防护

- [ ] 使用参数化查询
- [ ] 禁止字符串拼接 SQL
- [ ] 限制特殊字符

### XSS 防护

- [ ] 输出编码（HTML/URL/JSON）
- [ ] Content-Type 正确设置
- [ ] CSP 配置

### 命令注入防护

- [ ] 不使用用户输入执行系统命令
- [ ] 如需执行，使用白名单

### CSRF 防护

- [ ] 所有状态变更请求使用 CSRF Token（POST/PUT/DELETE）
- [ ] 同源策略（Origin header 验证）
- [ ] SameSite Cookie 设置为 Strict 或 Lax

### SSRF 防护

- [ ] URL 验证：禁止内网 IP 地址（10.x.x.x, 172.16-31.x.x, 192.168.x.x）
- [ ] DNS Rebinding 防护：延迟 DNS 解析，验证解析后的 IP
- [ ] 白名单：仅允许访问预定义的外部服务域名

### IDOR 防护

- [ ] 所有资源访问使用间接引用（间接对象引用映射），禁止直接暴露数据库 ID
- [ ] 水平越权检查：用户访问资源前验证所有权
- [ ] 垂直越权检查：权限级别验证

### XXE 防护

- [ ] XML 解析禁用外部实体（`libxml_disable_entity_loader` 或等价配置）
- [ ] 使用 JSON 替代 XML 作为数据交换格式

### 业务逻辑漏洞防护

- [ ] 认证失败锁定：连续 5 次失败后锁定 30 分钟
- [ ] 验证码/OTP 有效期限制（≤ 5 分钟）
- [ ] 频率限制：单 IP/单用户操作频率上限
- [ ] 数据一致性校验：关键操作前验证业务规则
```

### Phase 5: 数据安全

```markdown
## 数据安全

### 敏感数据清单

| 数据类型 | 示例 | 敏感等级 | 保护措施 |
|---------|------|---------|---------|
| 密码 | 用户密码 | 🔴 高 | Bcrypt/Argon2 哈希 |
| API Key | 第三方密钥 | 🔴 高 | 加密存储、环境变量 |
| 个人隐私 | 邮箱、手机号 | 🟡 中 | 脱敏展示、访问控制 |
| 公开数据 | 文章内容 | 🟢 低 | 无需特殊保护 |

### 加密方案

| 场景 | 算法 | 说明 |
|------|------|------|
| 密码存储 | Argon2id（首选）/ Bcrypt（备选） | 慢哈希，防 GPU/ASIC 暴力破解 |
| 传输加密 | TLS 1.3（强制），TLS 1.2（最小兼容） | 禁止 TLS 1.0/1.1 |
| 敏感文件 | AES-256-GCM | 本地加密存储 |
```

### Phase 6: 安全风险登记

```markdown
## 安全风险登记

| ID | 风险描述 | 威胁来源 | 可能性 | 影响 | 缓解措施 |
|----|---------|---------|--------|------|---------|
| S1 | SQL 注入 | 用户输入 | 高 | 高 | 参数化查询 |
| S2 | 密码泄露 | 攻击者 | 中 | 高 | 强哈希、2FA |
| S3 | XSS 攻击 | 恶意脚本 | 高 | 中 | 输出编码、CSP |
```

### Phase 7: 安全测试用例

```markdown
## 安全测试用例

| ID | 测试场景 | 预期结果 |
|----|---------|---------|
| ST1 | SQL 注入 payload `' OR '1'='1` | 被拦截或转义 |
| ST2 | XSS payload `<script>alert(1)</script>` | 被转义，不执行 |
| ST3 | CSRF Token 缺失或无效提交状态变更 | 请求被拒绝 |
| ST4 | JWT Token 过期后访问受保护 API | 返回 401 |
| ST5 | JWT Token 刷新流程（过期前刷新） | 返回新 Token |
| ST6 | 低权限用户访问高权限接口（垂直越权） | 返回 403 |
| ST7 | 用户 A 访问用户 B 的私有资源（水平越权） | 返回 403 或 404 |
| ST8 | 密码连续 5 次错误 | 账户锁定 30 分钟 |
| ST9 | API 请求超过频率限制 | 返回 429，触发限流 |
| ST10 | SSRF payload `http://169.254.169.254/` | 请求被拒绝或超时 |
```

### Phase 8: 隐私合规（如适用）

```markdown
## 隐私合规

| 法规 | 适用场景 | 关键要求 |
|------|---------|---------|
| GDPR（欧盟） | 处理欧盟用户数据 | 数据删除权、数据保留期限、跨境传输限制 |
| CCPA（加州） | 处理加州居民数据 | 知情权、删除权、不歧视 |
| PIPL（中国） | 处理中国用户数据 | 数据本地化、同意授权、跨境传输安全评估 |

**数据保留策略**：
- 用户数据：保留至用户主动删除
- 日志数据：保留 ≤ 90 天（可配置）
- 审计日志：保留 ≥ 1 年
```

## Target Pages

- `<项目根目录>/wiki/03-architecture/security.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：Phase 2 认证方案新增 MFA/2FA 和会话安全属性；Phase 3 加密方案标注 Argon2id 首选/Bcrypt 备选，TLS 1.3 强制 + 1.2 最小兼容；Phase 4 输入校验新增 CSRF/SSRF/IDOR/XXE/业务逻辑防护；Phase 7 测试用例新增 ST3-ST10（CSRF/JWT/越权/限流/SSRF）；Phase 8 新增隐私合规章节（GDPR/CCPA/PIPL） | OWASP Top 10 覆盖不完整、密码哈希优先级未标注、TLS 版本策略缺失、认证缺 MFA、会话管理缺安全属性、测试用例不足 |
| 2026-04-30 | 新建 skill | 安全设计是架构重要维度，之前缺失 |
