# 项目编码规范

**重要**：所有代码生成必须严格遵循以下规则文档：
- [doc/rules/coding-rule.md](doc/rules/coding-rule.md) - 完整编码标准
- [doc/rules/architecture-rule.md](doc/rules/architecture-rule.md) - 架构分层规则

本文件提供快速参考。完整细节、示例和详细说明请始终查阅上述规则文档。

---

## 0. 需求与设计文档遵循规则

**强制要求**：系统程序实现必须严格遵循需求文档和设计文档。

### 0.1 必须遵循的文档

| 文档类型 | 文档路径 | 说明 |
|---------|---------|------|
| **需求文档** | [doc/req/req-init-20260401.md](doc/req/req-init-20260401.md) | 项目需求规格说明 |
| **设计文档** | [doc/design/design-update-20260404-v1.0-init.md](doc/design/design-update-20260404-v1.0-init.md) | v1.0 MVP 技术设计 |

### 0.2 实施规则

**严格遵循：**
- ✅ 所有功能实现必须与需求文档保持一致
- ✅ 所有架构和模块设计必须遵循设计文档
- ✅ 接口定义、数据模型、配置结构必须与设计文档匹配
- ✅ 禁止留空未实现的功能（除非设计文档明确标注为后续版本）
- ✅ 禁止自行更改设计或添加未要求的功能

**变更处理：**
- ⚠️ 如果实现过程中发现需要更改设计，**必须提示用户并讨论确认**
- ⚠️ 如果发现需求不明确或有歧义，**必须提示用户并澄清**
- ⚠️ 如果设计文档存在技术可行性问题，**必须提示用户并提出替代方案**
- ❌ 禁止未经用户确认擅自修改设计或需求

### 0.3 变更确认流程

```
发现需要变更
    ↓
分析变更影响
    ↓
向用户说明变更原因和影响
    ↓
等待用户确认
    ↓
用户确认后执行变更
```

### 0.4 示例场景

**场景 1: 设计文档中的接口定义**
```python
# ✓ 正确：严格遵循设计文档
class ServiceFacade:
    """按照设计文档 3.2.2 节实现"""
    def __init__(self, config_path: Optional[str] = None):
        self._config_service = ConfigService(config_path)
        # ... 按设计文档实现
    
    def create_virtual_key(self, provider: str, name: str, 
                           expires_at: Optional[str] = None) -> Dict[str, Any]:
        """按照设计文档定义的接口实现"""
        return self._key_manager.create(provider=provider, name=name, 
                                        expires_at=expires_at)

# ✗ 错误：自行更改设计
class ServiceFacade:
    def __init__(self):  # ❌ 去掉了 config_path 参数
        self._config_service = ConfigService()
    
    def create_key(self, name: str):  # ❌ 改变了方法名和参数
        pass
```

**场景 2: 需要变更设计时**
```
❌ 错误做法：
直接修改接口设计，不通知用户

✓ 正确做法：
"⚠️ 发现设计文档中定义的 PresidioClient.analyze() 方法返回类型
与实际 Presidio API 响应不匹配。建议：
  - 方案 A: 修改返回类型为 List[DetectionResult]
  - 方案 B: 在客户端内部进行数据转换
  
请确认采用哪个方案？"
```

---

## 1. 架构分层

**重要**：所有代码必须遵循四层架构规则。

| 层级 | 路径 | 职责 | 依赖关系 |
|------|------|------|----------|
| **CLI** | `src/lpg/cli/` | 命令行交互 | → Core, Models, Utils(△) |
| **Core** | `src/lpg/core/` | 核心业务逻辑 | → Models, Utils |
| **Models** | `src/lpg/models/` | 数据模型 | → Utils |
| **Utils** | `src/lpg/utils/` | 通用工具 | (无依赖) |

**核心原则：**
- 上层可以调用下层,下层不能依赖上层
- 禁止跨层直接调用(如 CLI 直接调用 Utils)
- 禁止循环依赖
- 使用依赖注入提高可测试性

完整规则请查阅 [架构分层规则](doc/rules/architecture-rule.md)。

---

## 2. 基本原则

| 原则 | 说明 |
|------|------|
| **可读性优先** | 代码是写给人看的，顺便让机器执行 |
| **显式优于隐式** | 明确表达意图，避免魔法操作 |
| **简单优于复杂** | 选择最简单的解决方案，避免过度设计 |
| **一致性** | 遵循项目已有风格，保持代码风格统一 |
| **单一职责** | 每个函数/类只做一件事，做好一件事 |

> 📖 详细说明：[coding-rule.md - 基本原则](doc/rules/coding-rule.md#1-基本原则)

---

## 3. 代码格式

### 核心规则

- **行长度**：最大 100 字符
- **缩进**：4 个空格（禁止使用 Tab）
- **引号**：优先使用双引号 `"`
- **空行**：顶级定义 2 行，方法定义 1 行，逻辑块 1 行

### 工具命令

```bash
black src/ tests/       # 格式化
ruff check src/ tests/  # Lint
mypy src/               # 类型检查
```

> 📖 详细说明和示例：[coding-rule.md - 代码格式](doc/rules/coding-rule.md#2-代码格式)

---

## 4. 命名规范

### 命名风格

| 类型 | 风格 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `proxy_server.py` |
| 类 | PascalCase | `ProxyServer`, `KeyManager` |
| 异常类 | PascalCase + Error | `ConfigError` |
| 函数/方法 | snake_case | `get_virtual_key()` |
| 变量 | snake_case | `virtual_key` |
| 常量 | UPPER_SNAKE_CASE | `MAX_CONNECTIONS` |
| 私有成员 | `_leading_underscore` | `_internal_state` |

### 布尔变量

使用 `is_`, `has_`, `can_`, `should_` 前缀，避免双重否定。

> 📖 详细说明和示例：[coding-rule.md - 命名规范](doc/rules/coding-rule.md#3-命名规范)

---

## 5. 类型注解

### 核心规则

- **所有公共接口必须有完整的类型注解**
- 使用 `Optional[T]` 表示可选类型
- 使用 `Union[A, B]` 表示联合类型
- 复杂参数使用 Pydantic 模型

### 常用类型

```python
from typing import Any, Dict, List, Optional, Union, Callable, Awaitable, Protocol
```

> 📖 详细说明和示例：[coding-rule.md - 类型注解](doc/rules/coding-rule.md#4-类型注解)

---

## 6. 文档字符串

- 使用 **Google 风格**的 docstring
- **所有模块、类、公共函数必须有 docstring**
- 包含：功能描述、Args、Returns、Raises、Example

> 📖 详细说明和示例：[coding-rule.md - 文档字符串](doc/rules/coding-rule.md#5-文档字符串)

---

## 7. 导入规范

### 导入顺序

1. 标准库
2. 第三方库
3. 本地模块

每组之间用空行分隔，禁止使用通配导入(`from xxx import *`)。

> 📖 详细说明和示例：[coding-rule.md - 导入规范](doc/rules/coding-rule.md#6-导入规范)

---

## 8. 函数与方法

- **单一职责**：每个函数只做一件事
- **参数数量**：不超过 5 个
- **函数长度**：建议不超过 50 行
- **返回值**：使用异常而非返回 None 表示错误
- 复杂参数使用 Pydantic 模型

> 📖 详细说明和示例：[coding-rule.md - 函数与方法](doc/rules/coding-rule.md#7-函数与方法)

---

## 9. 类设计

### 类组织顺序

1. 类变量 → 2. `__init__` → 3. 魔术方法 → 4. 公共方法 → 5. 私有方法 → 6. 静态方法 → 7. 类方法

### 依赖注入

**通过构造函数注入依赖，禁止在类内部创建依赖。**

> 📖 详细说明和示例：[coding-rule.md - 类设计](doc/rules/coding-rule.md#8-类设计)

---

## 10. 异步编程

- I/O 密集型使用 `async/await`
- CPU 密集型使用线程池
- 避免在异步函数中使用阻塞调用
- 使用 `async with` 管理资源

> 📖 详细说明和示例：[coding-rule.md - 异步编程](doc/rules/coding-rule.md#9-异步编程)

---

## 11. 错误处理

### 异常层次

```
LPGError
├── ConfigError
├── KeyError
│   ├── KeyNotFoundError
│   └── KeyExpiredError
├── PresidioError
│   ├── PresidioConnectionError
│   └── PresidioTimeoutError
├── ProxyError
└── RuleError
```

### 原则

- 使用具体异常类型，避免使用通用 `Exception`
- 捕获具体异常，禁止 `except Exception: pass`
- 重新抛出时保留上下文：`raise NewError(...) from e`
- 使用 `async with` 自动清理资源

> 📖 详细说明和示例：[coding-rule.md - 错误处理](doc/rules/coding-rule.md#10-错误处理)

---

## 12. 日志规范

### 日志级别

| 级别 | 场景 | 示例 |
|------|------|------|
| DEBUG | 调试信息 | 详细数据流 |
| INFO | 正常操作 | 服务启动 |
| WARNING | 潜在问题 | Key 即将过期 |
| ERROR | 错误 | 连接失败 |
| CRITICAL | 严重错误 | 数据库断开 |

使用 `loguru`，异常日志使用 `logger.exception()` 自动包含堆栈。

> 📖 详细说明和示例：[coding-rule.md - 日志规范](doc/rules/coding-rule.md#11-日志规范)

---

## 13. Presidio 集成规范

- 封装 HTTP API 调用细节
- 处理连接错误和超时
- 从配置读取端点，禁止硬编码
- 使用自定义异常（`PresidioConnectionError`, `PresidioTimeoutError`）

> 📖 详细说明和示例：[coding-rule.md - Presidio 集成规范](doc/rules/coding-rule.md#12-presidio-集成规范)

---

## 14. 测试规范

### 组织

```
tests/
├── conftest.py          # 共享 fixtures
├── unit/                # 单元测试
├── integration/         # 集成测试
└── e2e/                 # 端到端测试
```

### 命名

- 文件：`test_<module>.py`
- 类：`Test<ClassName>`
- 方法：`test_<method>_<scenario>`

### 要求

- 使用 `@pytest.mark.asyncio` 标记异步测试
- 核心模块覆盖率 > 80%
- 使用 Mock 隔离外部依赖

> 📖 详细说明和示例：[coding-rule.md - 测试规范](doc/rules/coding-rule.md#13-测试规范)

---

## 15. 项目结构

```
llm-privacy-gateway/
├── src/lpg/
│   ├── cli/             # CLI 模块
│   ├── core/            # 核心业务逻辑
│   ├── models/          # 数据模型
│   └── utils/           # 工具函数
├── tests/               # 测试代码
└── doc/                 # 文档
```

> 📖 完整结构：[coding-rule.md - 项目结构](doc/rules/coding-rule.md#14-项目结构)

---

## 16. Git 提交规范

### 格式

```
<type>(<scope>): <subject>
```

### Type 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档 |
| refactor | 重构 |
| test | 测试 |
| chore | 构建/依赖 |

> 📖 详细说明和示例：[coding-rule.md - Git 提交规范](doc/rules/coding-rule.md#15-git-提交规范)

---

## 17. 代码审查清单

### 提交前自查

- [ ] 代码格式化（Black）
- [ ] Lint 检查（Ruff）
- [ ] 类型检查（mypy）
- [ ] 单元测试通过
- [ ] 新增代码有测试覆盖
- [ ] 公共接口有文档字符串
- [ ] 提交信息符合规范

> 📖 完整清单：[coding-rule.md - 代码审查清单](doc/rules/coding-rule.md#16-代码审查清单)

---

## 参考文档

详细规则请查阅：
- [doc/rules/coding-rule.md](doc/rules/coding-rule.md) - 完整编码标准
- [doc/rules/architecture-rule.md](doc/rules/architecture-rule.md) - 架构分层规则
