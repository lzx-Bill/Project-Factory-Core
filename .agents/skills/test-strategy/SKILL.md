---
name: test-strategy
description: 'Use when designing testing strategy for a project — "test strategy", "unit testing", "integration testing", "e2e testing", "test coverage", "mock strategy", "测试策略", "单元测试", "集成测试", "端到端测试". This skill defines the overall testing approach, coverage targets, test pyramid, and specific test cases for critical paths. Use after architecture-decisions and before delivery-planning.'
argument-hint: '测试策略、单元测试、集成测试、端到端测试、测试覆盖率、Mock策略'
---

# Test Strategy

用于设计项目测试策略。

## When to Use

- 需要定义测试策略和测试金字塔
- 需要设计单元测试方案
- 需要设计集成/E2E 测试方案
- 需要确定 Mock 策略和测试数据管理
- 需要建立测试覆盖率目标

## NOT When to Use

- MVP 阶段，先跑通功能
- 一次性脚本/工具，不做长期维护
- 已有完整测试策略，只需实现

## Input

| 来源 | 内容 |
|------|------|
| system-design.md | 架构和模块划分 |
| api-spec.md | API 端点和契约 |
| acceptance.md | 验收标准和成功条件 |
| tech-stack.md | 技术栈和已有测试框架 |

## Output Schema

| 文件 | 类型 | 说明 |
|------|------|------|
| `wiki/06-quality/test-strategy.md` | 测试策略 | 测试金字塔/覆盖率/用例 |
| `wiki/06-quality/unit-test-standards.md` | 单元测试规范 | 命名/结构/最佳实践 |

## Minimum Viable Output

- 测试金字塔（单元/集成/E2E 比例）
- 覆盖率目标
- 关键路径测试用例（≥5 个）
- Mock 策略概要

## Complete Output

- 完整测试策略，含：
  - 测试金字塔详细设计
  - 各层测试策略
  - 覆盖率目标
  - 测试数据管理
  - Mock 策略
  - CI/CD 集成
  - 性能测试计划（可参考 performance-design）
  - 测试用例清单

## Dependencies

| 类型 | 说明 |
|------|------|
| 前置 | `architecture-decisions`（架构已定）、`acceptance-design`（验收标准已定） |
| 后置 | `delivery-planning`（测试任务拆分） |
| 依赖读取 | system-design.md、api-spec.md、acceptance.md |

## Procedure

### Phase 1: 理解上下文

1. 读取 `system-design.md` → 确定模块边界和复杂度
2. 读取 `api-spec.md` → 确定 API 契约
3. 读取 `acceptance.md` → 确定验收标准
4. 读取 `tech-stack.md` → 确定测试框架选择

### Phase 2: 确定测试金字塔

```markdown
## 测试金字塔

        ╱ E2E Tests ╲          ← 少量，核心流程
       ╱───────────────╲
      ╱  Integration   ╲         ← 中量，模块间交互
     ╱───────────────────╲
    ╱    Unit Tests      ╲       ← 大量，单元逻辑
   ╱───────────────────────╲

### 比例建议

| 层级 | 数量占比 | 执行时间 | 维护成本 |
|------|---------|---------|---------|
| Unit | 70% | < 1s/个 | 低 |
| Integration | 20% | 1-10s/个 | 中 |
| E2E | 10% | < 30s/个 | 高 |

### 各层定义

| 层级 | 测试什么 | 不测试什么 |
|------|---------|-----------|
| Unit | 单个函数/类的逻辑 | 依赖、网络、数据库 |
| Integration | 模块间交互、API 契约 | 前端、网络抖动 |
| E2E | 完整用户流程 | 实现细节 |
```

### Phase 3: 单元测试策略

```markdown
## 单元测试策略

### 测试结构（AAA 模式）

```kotlin
@Test
fun `should return user when id exists`() {
    // Arrange - 准备测试数据
    val userId = "123"
    val repository = mock<UserRepository>()

    // Act - 执行被测方法
    val result = userService.getUser(userId)

    // Assert - 验证结果
    assertThat(result.name).isEqualTo("Test User")
}
```

### 命名规范

| 风格 | 示例 | 说明 |
|------|------|------|
| 方法名描述 | `should_return_user_when_id_exists` | 描述性强 |
| Given-When-Then | `givenUserExists_whenGetUser_thenReturnUser` | 结构清晰 |
| 场景描述 | `获取已存在用户返回完整信息` | 中文直观 |

### 覆盖率目标

**覆盖率类型说明**：

| 类型 | 说明 | 常用工具 |
|------|------|---------|
| 行覆盖率（Line） | 代码行被执行的比例 | Jest/coverage |
| 分支覆盖率（Branch） | 每个条件分支的 true/false 都被覆盖 | Jest/coverage |
| 路径覆盖率（Path） | 每个可能的执行路径都被覆盖 | 手动分析 |

> 实践中**以分支覆盖率为主**，行覆盖率作为辅助指标。路径覆盖率成本过高，仅对核心算法要求。

| 模块类型 | 覆盖率目标（分支） | 说明 |
|---------|-------------------|------|
| 业务逻辑 | ≥ 80% | 核心算法 |
| 数据访问 | ≥ 70% | Repository |
| 工具函数 | ≥ 90% | 通用库 |
| 控制器 | ≥ 60% | API 层 |

### 测试原则

- [ ] 每个测试只测一件事
- [ ] 测试之间相互独立
- [ ] Arrange 足够简单，不含业务逻辑
- [ ] 避免 Assert 链过长
- [ ] 失败测试必须能本地复现
```

### Phase 4: 集成测试策略

```markdown
## 集成测试策略

### 测试范围

- [ ] 数据库操作（真实数据库或 Testcontainers）
- [ ] API 端点（使用真实 HTTP 客户端）
- [ ] 外部服务（WireMock / MockServer）

### API 测试示例

```kotlin
@Test
fun `POST /users should create user and return 201`() {
    // 使用真实数据库
    database.use { db ->
        val client = TestClient(db)

        val response = client.post("/users") {
            body = """{"name": "Test", "email": "test@example.com"}"""
        }

        assertThat(response.status).isEqualTo(201)
        assertThat(response.body["id"]).isNotNull()
    }
}
```

### 契约测试

```markdown
## 契约测试 (Contract Testing)

### Provider Side

```kotlin
@State("user 123 exists")
fun `should return user 123`() {
    // 验证 API 返回符合契约
}
```

### Consumer Side

```kotlin
@Test
fun `should parse user response`() {
    // 验证 Consumer 能正确解析响应
    val user = parseUser(sampleResponse)
    assertThat(user.name).isEqualTo("Test")
}
```
```

### Phase 5: E2E 测试策略

```markdown
## E2E 测试策略

### 测试范围

只测试关键用户路径：

| 优先级 | 路径 | 测试频率 |
|--------|------|---------|
| P0 | 登录 → 核心功能 → 登出 | 每次 CI |
| P1 | 注册流程 | 每次 CI |
| P1 | 支付流程 | 每次 CI |
| P2 | 复杂表单提交 | 每日 |

### 测试工具选择

| 工具 | 适用场景 | 优点 |
|------|---------|------|
| Playwright | Web 应用 | 跨浏览器、并行 |
| Detox | React Native | 原生移动端 |
| Cypress | Web 应用 | 易于调试 |
| Puppeteer | Web 应用 | 无浏览器依赖 |

### E2E 测试规范

```markdown
## E2E 规范

### 页面对象模式

```kotlin
class LoginPage {
    private val emailInput = By.cssSelector("input[name=email]")
    private val passwordInput = By.cssSelector("input[name=password]")
    private val submitButton = By.cssSelector("button[type=submit]")

    fun login(email: String, password: String) {
        find(emailInput).sendKeys(email)
        find(passwordInput).sendKeys(password)
        find(submitButton).click()
    }
}
```

### 稳定性和治理

- [ ] 测试数据在测试前准备、测试后清理
- [ ] 使用 `data-testid` 而非 CSS Selector
- [ ] 合理的 `waitFor` 替代 `Thread.sleep`
- [ ] 失败自动截图和日志
```
```

### Phase 6: Mock 策略

```markdown
## Mock 策略

### 何时 Mock

| 场景 | Mock 对象 | 原因 |
|------|-----------|------|
| 单元测试 | 外部依赖（DB/API） | 隔离被测单元 |
| 集成测试 | 第三方服务（可选） | 控制测试环境、提高稳定性 |
| E2E 测试 | 仅 Mock 不可控外部依赖 | 第三方支付/短信等不可靠服务需 Mock；核心业务逻辑不 Mock |

> E2E "不 Mock"指不 Mock 被测系统自身组件。第三方不可控服务（如支付网关、短信 API）在 E2E 中必须 Mock，以保证测试稳定性。

### Mock 工具选择

| 环境 | 工具 | 场景 |
|------|------|------|
| Kotlin/Java | MockK / Mockito | 单元测试 |
| Python | unittest.mock / pytest-mock | 单元测试 |
| JavaScript | jest.mock | 单元测试（Mock 函数/模块） |
| JavaScript | msw (Mock Service Worker) | 集成/E2E 层（Mock HTTP 请求） |
| 外部服务 | WireMock / MockServer | 集成测试（Mock HTTP 第三方服务） |
| 外部 API | WireMock / MockServer | 集成测试 |

### Mock 原则

```markdown
### 正确的 Mock

```kotlin
// ✅ Mock 外部依赖，不 Mock 内部实现
val userRepository = mock<UserRepository>()
val service = UserService(userRepository)
```

### 错误的 Mock

```kotlin
// ❌ Mock 被测类的内部方法
val service = mock<UserService>(UserService::class.java)
```
```

### 测试数据管理

```markdown
## 测试数据管理

### 策略 1: 工厂方法

```kotlin
fun createUser(name: String = "Test User") = User(
    id = UUID.randomUUID().toString(),
    name = name,
    email = "test@example.com"
)
```

### 策略 2: Fixture 文件

```
test/fixtures/
├── users.json
├── posts.json
└── tokens.json
```

### 策略 3: Test Database

- 使用独立测试数据库（每次测试回滚）
- 或使用 Transaction 测试模式（测试结束回滚）
```
```

### Phase 7: CI/CD 集成

```markdown
## CI/CD 集成

### 测试执行时机

| 阶段 | 运行测试 | 阻塞条件 |
|------|---------|---------|
| PR 检查 | 单元测试 + Lint | 任意失败 |
| Merge 检查 | 单元 + 集成 | 任意失败 |
| 部署前 | 单元 + 集成 + E2E | E2E 失败阻塞部署，不阻塞代码合并 |
| 定时任务 | 稳定性 E2E | 任意失败 |

### 测试报告

- [ ] 单元测试覆盖率上传到 Codecov / Coveralls
- [ ] 集成测试报告上传到 CI 产物
- [ ] E2E 测试视频/截图存档

### 性能回归

- [ ] 每次 PR 运行基准测试
- [ ] P99 退化 > 20% 阻塞合并
```

### Phase 8: 测试用例清单

```markdown
## 关键路径测试用例

### 用户模块

| ID | 测试用例 | 优先级 | 测试类型 |
|----|---------|--------|---------|
| TC-U1 | 注册 - 正常流程 | P0 | E2E |
| TC-U2 | 注册 - 邮箱已存在 | P1 | Integration |
| TC-U3 | 登录 - 正确凭证 | P0 | E2E |
| TC-U4 | 登录 - 错误密码 | P1 | Integration |
| TC-U5 | 密码强度校验 | P1 | Unit |

### 业务模块

| ID | 测试用例 | 优先级 | 测试类型 |
|----|---------|--------|---------|
| TC-B1 | 核心业务逻辑 - 正常 | P0 | Unit |
| TC-B2 | 核心业务逻辑 - 边界条件 | P1 | Unit |
| TC-B3 | 业务逻辑 - 异常处理 | P1 | Unit |
```

## Target Pages

- `<项目根目录>/wiki/06-quality/test-strategy.md`
- `<项目根目录>/wiki/06-quality/unit-test-standards.md`

## Changelog

| 日期 | 变更 | 原因 |
|------|------|------|
| 2026-04-30 | 修复：金字塔 E2E 时间 10s-1min→<30s；覆盖率目标新增分支覆盖率类型定义（明确为主指标）；Mock 策略明确 E2E 可 Mock 第三方不可控服务，区分 jest.mock（单元）/ msw（集成/E2E HTTP）/ WireMock（第三方服务）；CI/CD E2E 失败语义澄清（阻塞部署不阻塞合并） | E2E 时间过严、覆盖率类型未定义、Mock 策略自相矛盾、CI/CD 语义模糊 |
| 2026-04-30 | 新建 skill | 测试策略是质量保障重要维度，之前缺失 |
