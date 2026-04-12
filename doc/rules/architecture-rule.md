# LLM Privacy Gateway - 架构分层规则

**版本：** 1.0  
**日期：** 2026-04-05  
**适用范围：** 全项目 Python 代码  
**配套文档：** `coding-rule.md`（编码规范）

---

## 目录

1. [架构分层概述](#1-架构分层概述)
2. [各层职责定义](#2-各层职责定义)
3. [代码归属规则](#3-代码归属规则)
4. [层间依赖约束](#4-层间依赖约束)
5. [实施指南](#5-实施指南)
6. [常见错误与纠正](#6-常见错误与纠正)
7. [最佳实践](#7-最佳实践)

---

## 1. 架构分层概述

### 1.1 分层目标

| 目标 | 说明 |
|------|------|
| **职责清晰** | 每层只做自己应该做的事,职责不重叠 |
| **易于测试** | 各层可独立测试,降低测试复杂度 |
| **便于维护** | 修改某一层时,不影响其他层的实现 |
| **支持复用** | 通用组件可被多层复用,避免重复实现 |
| **降低耦合** | 层间通过明确定义的接口交互,减少依赖 |

### 1.2 项目分层架构

```
┌─────────────────────────────────────────┐
│          CLI 层 (用户交互)               │
│  src/lpg/cli/                           │
│  - 命令行参数解析                        │
│  - 用户输入输出                          │
│  - 命令路由和分发                        │
└────────────────┬────────────────────────┘
                 │ 调用
┌────────────────▼────────────────────────┐
│        Core 层 (核心业务逻辑)             │
│  src/lpg/core/                          │
│  - 业务规则和流程控制                    │
│  - 服务编排和协调                        │
│  - 外部服务集成                          │
└────────────────┬────────────────────────┘
                 │ 使用
┌────────────────▼────────────────────────┐
│       Models 层 (数据模型)               │
│  src/lpg/models/                        │
│  - 数据结构定义                          │
│  - 数据验证规则                          │
│  - 数据转换方法                          │
└────────────────┬────────────────────────┘
                 │ 依赖
┌────────────────▼────────────────────────┐
│       Utils 层 (工具函数)                │
│  src/lpg/utils/                         │
│  - 通用工具函数                          │
│  - 基础设施封装                          │
│  - 跨层共享组件                          │
└─────────────────────────────────────────┘
```

### 1.3 分层依赖规则

**单向依赖原则：**

```
CLI → Core → Models → Utils
  ↘________↓________↗
```

- **上层可以依赖下层**：CLI 可以调用 Core,Core 可以使用 Models
- **下层不能依赖上层**：Utils 不能导入 Core 或 CLI
- **同层内部可以自由依赖**：Core 内部的模块可以互相调用
- **禁止跨层直接调用**：CLI 不应该直接调用 Utils(应通过 Core 封装)

---

## 2. 各层职责定义

### 2.1 CLI 层 (`src/lpg/cli/`)

**职责范围：**
- 命令行参数解析和验证
- 用户交互(输入提示、进度显示、结果格式化)
- 命令路由和分发
- 调用 Core 层服务执行业务逻辑
- 错误信息的用户友好展示

**允许的操作：**
- 解析命令行参数(使用 Click、Argparse 等)
- 调用 Core 层的服务类和方法
- 格式化输出结果(表格、JSON、文本等)
- 捕获异常并转换为友好的错误提示
- 记录用户操作日志(INFO 级别)

**禁止的操作：**
- ❌ 直接实现业务逻辑
- ❌ 直接操作数据库或文件系统
- ❌ 直接调用外部服务 API
- ❌ 包含复杂的数据处理逻辑
- ❌ 直接实例化 Models 层对象(应通过 Core 层)

**示例：**

```python
# ✓ 正确：CLI 层只做参数解析和结果展示
import click
from lpg.core.key.manager import KeyManager

@click.command()
@click.option("--provider", required=True, help="LLM 提供商名称")
@click.option("--name", required=True, help="虚拟 Key 名称")
@click.option("--expires-at", help="过期时间 (ISO 格式)")
def create_key(provider: str, name: str, expires_at: str) -> None:
    """创建虚拟 API Key"""
    try:
        # 调用 Core 层服务
        key_manager = KeyManager(config_service)
        key = key_manager.create(
            provider=provider,
            name=name,
            expires_at=expires_at
        )
        
        # 展示结果
        click.echo(f"✓ Key created successfully")
        click.echo(f"  Key ID: {key.key_id}")
        click.echo(f"  Virtual Key: {key.virtual_key}")
        
    except Exception as e:
        click.echo(f"✗ Failed to create key: {e}", err=True)
        raise SystemExit(1)


# ✗ 错误：CLI 层包含业务逻辑
@click.command()
def create_key(provider: str, name: str) -> None:
    """创建虚拟 API Key"""
    # ❌ 不应该在这里实现密钥生成逻辑
    import secrets
    import hashlib
    virtual_key = f"lpg_{secrets.token_hex(32)}"
    hashed_key = hashlib.sha256(virtual_key.encode()).hexdigest()
    
    # ❌ 不应该直接操作文件存储
    with open("keys.json", "a") as f:
        f.write(json.dumps({...}))
```

---

### 2.2 Core 层 (`src/lpg/core/`)

**职责范围：**
- 核心业务规则和流程控制
- 服务编排和协调(组合多个底层服务)
- 外部服务集成(Presidio、LLM 提供商等)
- 数据验证和业务规则检查
- 错误处理和降级策略

**允许的操作：**
- 调用 Models 层进行数据验证和转换
- 调用 Utils 层获取工具函数支持
- 调用外部服务 API(HTTP 请求等)
- 实现复杂的业务逻辑和流程控制
- 管理资源生命周期(连接池、缓存等)
- 记录业务操作日志(DEBUG/INFO/WARNING/ERROR)

**禁止的操作：**
- ❌ 直接处理命令行参数或用户交互
- ❌ 包含 UI/CLI 相关的代码
- ❌ 绕过 Models 层直接处理原始数据
- ❌ 依赖 CLI 层的任何模块

**目录结构示例：**

```
src/lpg/core/
├── config/           # 配置管理服务
│   ├── service.py    # ConfigService
│   └── loader.py     # 配置加载器
├── key/              # 虚拟 Key 管理服务
│   ├── manager.py    # KeyManager
│   ├── store.py      # Key 存储接口
│   └── validator.py  # Key 验证规则
├── proxy/            # 代理服务
│   ├── server.py     # ProxyServer
│   ├── handler.py    # RequestHandler
│   └── stream.py     # StreamHandler
├── presidio/         # Presidio 集成
│   ├── client.py     # PresidioClient
│   ├── analyzer.py   # PII 分析器
│   └── anonymizer.py # 脱敏处理器
├── rule/             # 规则管理服务
│   ├── manager.py    # RuleManager
│   └── engine.py     # 规则引擎
└── audit/            # 审计日志服务
    ├── logger.py     # AuditLogger
    └── formatter.py  # 日志格式化
```

**示例：**

```python
# ✓ 正确：Core 层实现业务逻辑
from lpg.models.key import KeyCreateRequest, KeyResponse
from lpg.core.key.store import KeyStore
from lpg.core.key.validator import KeyValidator
from lpg.utils.crypto import generate_key, hash_key
from loguru import logger


class KeyManager:
    """虚拟 Key 管理服务"""
    
    def __init__(
        self,
        key_store: KeyStore,
        validator: KeyValidator
    ) -> None:
        self._store = key_store
        self._validator = validator
    
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        """
        创建虚拟 Key。
        
        业务流程：
        1. 验证请求参数
        2. 生成虚拟 Key
        3. 哈希存储
        4. 返回完整 Key(仅一次)
        """
        # 1. 验证请求
        self._validator.validate_create_request(request)
        
        # 2. 生成 Key
        virtual_key = generate_key()
        hashed_key = hash_key(virtual_key)
        
        # 3. 存储
        key_record = self._store.save(
            provider=request.provider,
            name=request.name,
            hashed_key=hashed_key,
            expires_at=request.expires_at
        )
        
        logger.info(
            "Key created: provider={provider}, name={name}",
            provider=request.provider,
            name=request.name
        )
        
        # 4. 返回响应
        return KeyResponse(
            key_id=key_record.key_id,
            virtual_key=virtual_key,  # 明文仅返回一次
            provider=request.provider,
            name=request.name,
            created_at=key_record.created_at
        )


# ✗ 错误：Core 层包含 CLI 交互
class KeyManager:
    def create_key(self, provider: str, name: str) -> None:
        """创建虚拟 Key"""
        # ❌ 不应该在 Core 层使用 click
        import click
        click.echo("Creating key...")
        
        # ❌ 不应该直接处理用户输入
        if not click.confirm("Continue?"):
            return
```

---

### 2.3 Models 层 (`src/lpg/models/`)

**职责范围：**
- 数据结构定义(Pydantic 模型、Dataclass)
- 数据验证规则(字段类型、范围、格式)
- 数据转换方法(序列化、反序列化)
- 领域实体和值对象
- 数据传输对象(DTO)

**允许的操作：**
- 定义数据模型和验证规则
- 实现数据转换方法(如 `from_dict()`, `to_dict()`)
- 定义业务常量
- 实现简单的数据校验方法
- 记录数据验证失败的日志(WARNING)

**禁止的操作：**
- ❌ 包含业务逻辑(如创建 Key、调用 API)
- ❌ 依赖 Core 层或 CLI 层
- ❌ 执行 I/O 操作(读写文件、网络请求)
- ❌ 包含复杂的计算逻辑

**目录结构示例：**

```
src/lpg/models/
├── key.py            # Key 相关模型
├── config.py         # 配置模型
├── provider.py       # 提供商模型
├── rule.py           # 规则模型
├── audit.py          # 审计日志模型
└── common.py         # 通用模型(分页、响应等)
```

**示例：**

```python
# ✓ 正确：Models 层只定义数据和验证
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class KeyCreateRequest(BaseModel):
    """创建 Key 请求模型"""
    
    provider: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    expires_at: Optional[datetime] = None
    permissions: Optional[dict] = None
    
    @validator("provider")
    def validate_provider(cls, v: str) -> str:
        """验证提供商名称格式"""
        if not v.islower():
            raise ValueError("Provider name must be lowercase")
        return v
    
    @validator("expires_at")
    def validate_expires_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        """验证过期时间"""
        if v and v < datetime.now():
            raise ValueError("Expires_at must be in the future")
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class KeyResponse(BaseModel):
    """Key 响应模型"""
    
    key_id: str
    virtual_key: str
    provider: str
    name: str
    created_at: datetime
    expires_at: Optional[datetime] = None


# ✗ 错误：Models 层包含业务逻辑
class KeyCreateRequest(BaseModel):
    provider: str
    
    def save_to_database(self) -> None:
        """❌ 不应该在模型中实现存储逻辑"""
        import sqlite3
        conn = sqlite3.connect("keys.db")
        conn.execute("INSERT INTO keys ...")
    
    def call_external_api(self) -> dict:
        """❌ 不应该在模型中调用外部 API"""
        import requests
        return requests.post("https://api.example.com", json={...})
```

---

### 2.4 Utils 层 (`src/lpg/utils/`)

**职责范围：**
- 通用工具函数(加密、解密、格式化)
- 基础设施封装(日志配置、异常定义)
- 跨层共享组件(常量、枚举)
- 辅助函数(时间处理、字符串处理)

**允许的操作：**
- 实现无状态的纯函数
- 封装第三方库(如日志配置、HTTP 客户端)
- 定义全局异常类和常量
- 提供通用的数据转换函数
- 记录工具函数使用日志(DEBUG)

**禁止的操作：**
- ❌ 包含业务逻辑
- ❌ 依赖 Core 层、CLI 层或 Models 层
- ❌ 维护复杂的状态
- ❌ 执行特定的业务流程

**目录结构示例：**

```
src/lpg/utils/
├── exceptions.py     # 全局异常定义
├── logging.py        # 日志配置
├── crypto.py         # 加密解密工具
├── time.py           # 时间处理工具
├── string.py         # 字符串处理工具
├── validation.py     # 通用验证函数
└── constants.py      # 全局常量
```

**示例：**

```python
# ✓ 正确：Utils 层提供通用工具
import secrets
import hashlib
from typing import Optional


def generate_key(prefix: str = "lpg", length: int = 32) -> str:
    """
    生成随机密钥。
    
    Args:
        prefix: 密钥前缀
        length: 随机字节长度
    
    Returns:
        格式化的密钥字符串
    """
    random_part = secrets.token_hex(length)
    return f"{prefix}_{random_part}"


def hash_key(key: str, algorithm: str = "sha256") -> str:
    """
    对密钥进行哈希处理。
    
    Args:
        key: 原始密钥
        algorithm: 哈希算法
    
    Returns:
        哈希后的字符串
    """
    if algorithm == "sha256":
        return hashlib.sha256(key.encode()).hexdigest()
    raise ValueError(f"Unsupported algorithm: {algorithm}")


# ✗ 错误：Utils 层包含业务逻辑
def create_and_save_key(provider: str, name: str) -> str:
    """
    ❌ 不应该在 Utils 中实现完整的业务流程
    这个函数涉及：
    - 业务验证(属于 Core)
    - 数据存储(属于 Core)
    - 日志记录(属于 Core)
    """
    from lpg.core.key.store import KeyStore  # ❌ 依赖 Core 层
    
    key = generate_key()
    store = KeyStore()
    store.save(provider, name, key)
    return key
```

---

## 3. 代码归属规则

### 3.1 功能分类决策树

```
这个功能做什么？
│
├─ 解析命令行参数/展示结果?
│   └─ YES → CLI 层
│
├─ 定义数据结构/验证规则?
│   └─ YES → Models 层
│
├─ 通用工具函数(无业务语义)?
│   └─ YES → Utils 层
│
├─ 实现业务规则/流程控制?
│   └─ YES → Core 层
│
└─ 调用外部服务/编排多个服务?
    └─ YES → Core 层
```

### 3.2 常见功能归属表

| 功能 | 归属层 | 说明 |
|------|--------|------|
| 解析 CLI 参数 | CLI | 使用 Click/Argparse |
| 展示表格结果 | CLI | 格式化输出 |
| 创建虚拟 Key | Core | 业务逻辑 |
| 验证 Key 格式 | Core | 业务规则 |
| Key 数据模型 | Models | Pydantic 模型 |
| 生成随机字符串 | Utils | 通用工具 |
| 加密/解密 | Utils | 通用工具 |
| HTTP 客户端封装 | Core | 业务集成 |
| 日志配置 | Utils | 基础设施 |
| 异常定义 | Utils | 全局共享 |
| 配置加载 | Core | 业务服务 |
| 数据验证规则 | Models | 字段验证 |
| PII 检测 | Core | 业务集成 |
| 规则引擎 | Core | 业务逻辑 |
| 审计日志 | Core | 业务流程 |

### 3.3 判断标准

**问题 1: 这个功能是否可复用?**
- YES → 考虑 Utils 或 Models
- NO → 考虑 Core 或 CLI

**问题 2: 这个功能是否包含业务语义?**
- YES → Core 层
- NO → Utils 层

**问题 3: 这个功能是否与用户交互相关?**
- YES → CLI 层
- NO → 继续判断

**问题 4: 这个功能是否定义数据结构?**
- YES → Models 层
- NO → 继续判断

---

## 4. 层间依赖约束

### 4.1 允许依赖矩阵

| 调用方 ↓ \ 被调用方 → | Utils | Models | Core | CLI |
|----------------------|-------|--------|------|-----|
| **Utils**            | ✓     | ✗      | ✗    | ✗   |
| **Models**           | ✓     | ✓      | ✗    | ✗   |
| **Core**             | ✓     | ✓      | ✓    | ✗   |
| **CLI**              | △     | ✓      | ✓    | ✓   |

**说明：**
- ✓ 允许直接依赖
- ✗ 禁止依赖
- △ 仅允许使用 Utils 中的纯工具函数,不应依赖业务相关工具

### 4.2 依赖注入规范

**原则：通过构造函数注入依赖,而非在方法内部创建**

```python
# ✓ 正确：依赖注入
class KeyManager:
    def __init__(
        self,
        key_store: KeyStore,
        validator: KeyValidator,
        config_service: ConfigService
    ) -> None:
        self._store = key_store
        self._validator = validator
        self._config = config_service
    
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        # 使用注入的依赖
        self._validator.validate(request)
        ...


# ✗ 错误：方法内部创建依赖
class KeyManager:
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        # ❌ 紧耦合,难以测试
        store = KeyStore()
        validator = KeyValidator()
        config = ConfigService()
        ...
```

### 4.3 跨层调用规范

**规则：禁止跳过中间层直接调用**

```python
# ✓ 正确：遵循分层调用
# CLI 层
@click.command()
def create_key(provider: str, name: str) -> None:
    key_manager = KeyManager(...)  # 调用 Core
    result = key_manager.create_key(request)
    click.echo(result)

# Core 层
class KeyManager:
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        self._validator.validate(request)  # 使用 Models
        key = generate_key()  # 使用 Utils
        ...

# ✗ 错误：CLI 直接调用 Utils
@click.command()
def create_key(provider: str, name: str) -> None:
    # ❌ CLI 不应该直接调用 Utils 中的业务工具
    from lpg.utils.crypto import generate_key
    key = generate_key()
    click.echo(key)
```

### 4.4 循环依赖处理

**规则：禁止任何形式的循环依赖**

```python
# ✗ 错误：循环依赖
# core/key/manager.py
from core.rule.manager import RuleManager  # ❌

# core/rule/manager.py
from core.key.manager import KeyManager  # ❌

# ✓ 正确：使用接口解耦
# core/key/manager.py
from typing import Protocol

class RuleChecker(Protocol):
    def check(self, rule: str) -> bool:
        ...

class KeyManager:
    def __init__(self, rule_checker: RuleChecker) -> None:
        self._rule_checker = rule_checker

# core/rule/manager.py
class RuleManager:
    def check(self, rule: str) -> bool:
        ...
```

---

## 5. 实施指南

### 5.1 如何判断代码归属

**步骤 1: 识别功能的主要职责**

```python
def analyze_text_for_pii(text: str) -> List[DetectionResult]:
    """这个函数的主要职责是什么?"""
    # A. 调用 Presidio API → 业务集成 → Core 层
    # B. 定义 DetectionResult 结构 → 数据模型 → Models 层
    # C. 解析命令行参数 → 用户交互 → CLI 层
    # D. 格式化文本 → 通用工具 → Utils 层
```

**步骤 2: 检查依赖关系**

```python
# 检查这个函数需要导入什么?
from lpg.core.presidio.client import PresidioClient  # ← Core 层依赖
from lpg.models.pii import DetectionResult  # ← Models 层依赖

# 结论：应该放在 Core 层
```

**步骤 3: 验证是否符合分层规则**

- 是否依赖了不允许的层?
- 是否包含了不属于该层的职责?
- 是否可以被其他层复用?

### 5.2 新建模块检查清单

创建新模块时,依次回答以下问题:

- [ ] 这个模块属于哪一层?
- [ ] 它依赖的模块是否都在允许的层?
- [ ] 它是否包含了不属于该层的职责?
- [ ] 其他层是否需要调用这个模块?
- [ ] 是否有更好的放置位置?

### 5.3 代码重构指南

**场景 1: 发现 Core 层包含 CLI 代码**

```python
# 重构前 (错误)
class KeyManager:
    def create_key(self, provider: str, name: str) -> None:
        import click
        click.echo("Creating key...")
        ...

# 重构后 (正确)
# Core 层
class KeyManager:
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        logger.info("Creating key for provider={}", request.provider)
        ...

# CLI 层
@click.command()
def create_key(provider: str, name: str) -> None:
    click.echo("Creating key...")
    manager = KeyManager(...)
    result = manager.create_key(request)
    click.echo("✓ Key created")
```

**场景 2: 发现 Utils 层包含业务逻辑**

```python
# 重构前 (错误)
# utils/key_helper.py
def create_key(provider: str) -> str:
    """❌ 包含了业务流程"""
    key = generate_key()
    save_to_database(key, provider)  # 业务逻辑
    return key

# 重构后 (正确)
# utils/crypto.py
def generate_key() -> str:
    """✓ 纯工具函数"""
    return secrets.token_hex(32)

# core/key/manager.py
class KeyManager:
    def create_key(self, provider: str) -> str:
        """✓ 业务流程"""
        key = generate_key()  # 使用 Utils
        self._store.save(key, provider)  # 业务逻辑
        return key
```

**场景 3: 发现 Models 层包含 I/O 操作**

```python
# 重构前 (错误)
class KeyModel(BaseModel):
    def save(self) -> None:
        """❌ 模型不应该直接存储"""
        with open("keys.json", "w") as f:
            json.dump(self.dict(), f)

# 重构后 (正确)
class KeyModel(BaseModel):
    """✓ 只定义数据结构"""
    key_id: str
    provider: str
    ...

class KeyStore:
    def save(self, key: KeyModel) -> None:
        """✓ Core 层负责存储"""
        ...
```

---

## 6. 常见错误与纠正

### 6.1 错误 1: "上帝类" (God Class)

**问题：** 一个类承担了太多职责

```python
# ✗ 错误：KeyManager 做了太多事
class KeyManager:
    def create_key(self, ...):
        # 解析参数 → CLI 职责
        # 验证规则 → Core 职责
        # 生成密钥 → Utils 职责
        # 存储数据 → Core 职责
        # 发送通知 → Core 职责
        # 展示结果 → CLI 职责
        ...

# ✓ 正确：职责分离
# CLI 层
@click.command()
def create_key(...) -> None:
    ...

# Core 层
class KeyManager:
    def __init__(self, validator, store, notifier):
        self._validator = validator
        self._store = store
        self._notifier = notifier
    
    def create_key(self, request: KeyCreateRequest) -> KeyResponse:
        self._validator.validate(request)
        key = generate_key()
        self._store.save(key)
        self._notifier.notify(key)
        return KeyResponse(...)

# Utils 层
def generate_key() -> str:
    ...
```

### 6.2 错误 2: 贫血模型 (Anemic Model)

**问题：** Models 层只有数据,没有验证规则

```python
# ✗ 错误：模型缺少验证
class KeyCreateRequest(BaseModel):
    provider: str
    name: str
    expires_at: str  # 没有验证格式

# ✓ 正确：包含验证规则
class KeyCreateRequest(BaseModel):
    provider: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    expires_at: Optional[datetime] = None
    
    @validator("provider")
    def validate_provider(cls, v: str) -> str:
        if not v.islower():
            raise ValueError("Provider must be lowercase")
        return v
```

### 6.3 错误 3: 循环依赖

**问题：** 模块 A 导入模块 B,模块 B 又导入模块 A

```python
# ✗ 错误：循环依赖
# core/key/manager.py
from core.rule.manager import RuleManager

# core/rule/manager.py
from core.key.manager import KeyManager

# ✓ 正确：使用接口解耦
# core/key/interfaces.py
from typing import Protocol

class RuleChecker(Protocol):
    def check(self, request) -> bool:
        ...

# core/key/manager.py
from core.key.interfaces import RuleChecker

class KeyManager:
    def __init__(self, rule_checker: RuleChecker):
        self._rule_checker = rule_checker

# core/rule/manager.py
class RuleManager:
    def check(self, request) -> bool:
        ...

# 组合层 (组装依赖)
rule_manager = RuleManager()
key_manager = KeyManager(rule_checker=rule_manager)
```

### 6.4 错误 4: 层间泄漏

**问题：** 上层直接调用下层的内部实现

```python
# ✗ 错误：CLI 直接使用 Utils 内部函数
@click.command()
def create_key(provider: str) -> None:
    from lpg.utils.crypto import generate_key, hash_key
    from lpg.utils.time import format_timestamp
    
    key = generate_key()
    hashed = hash_key(key)
    timestamp = format_timestamp(datetime.now())
    
    click.echo(f"Key: {key}, Hash: {hashed}, Time: {timestamp}")

# ✓ 正确：通过 Core 层封装
@click.command()
def create_key(provider: str) -> None:
    manager = KeyManager(...)
    result = manager.create_key(request)
    
    click.echo(f"Key: {result.virtual_key}")
    click.echo(f"Created: {result.created_at}")
```

### 6.5 错误 5: 工具函数过度耦合

**问题：** Utils 层函数依赖业务逻辑

```python
# ✗ 错误：工具函数依赖业务模型
def validate_key_format(key: KeyModel) -> bool:
    """❌ Utils 不应该依赖 Models 的具体业务模型"""
    ...

# ✓ 正确：使用通用类型
def validate_key_format(key: str) -> bool:
    """✓ 使用基础类型,保持通用性"""
    return key.startswith("lpg_") and len(key) == 69
```

---

## 7. 最佳实践

### 7.1 保持层职责单一

**原则：** 每层只关注自己的职责,不越权

```python
# CLI 层职责：用户交互
- 解析参数
- 调用 Core
- 展示结果
- 处理用户错误提示

# Core 层职责：业务逻辑
- 验证规则
- 编排流程
- 调用外部服务
- 错误处理

# Models 层职责：数据结构
- 定义模型
- 验证字段
- 数据转换

# Utils 层职责：通用工具
- 纯函数
- 基础设施
- 跨层共享
```

### 7.2 使用依赖注入

**原则：** 通过构造函数注入依赖,提高可测试性

```python
# ✓ 推荐模式
class ServiceA:
    def __init__(self, dep_b: ServiceB, dep_c: ServiceC):
        self._b = dep_b
        self._c = dep_c

# 在入口处组装依赖
def create_application():
    config = ConfigService()
    store = KeyStore(config)
    validator = KeyValidator()
    manager = KeyManager(store, validator)
    return manager
```

### 7.3 定义清晰的接口

**原则：** 使用 Protocol 定义层间接口,降低耦合

```python
from typing import Protocol

# 定义接口
class KeyStorage(Protocol):
    def save(self, key: KeyModel) -> None:
        ...
    
    def load(self, key_id: str) -> Optional[KeyModel]:
        ...

# 实现接口
class FileKeyStorage:
    def save(self, key: KeyModel) -> None:
        ...
    
    def load(self, key_id: str) -> Optional[KeyModel]:
        ...

# 使用接口
class KeyManager:
    def __init__(self, storage: KeyStorage):
        self._storage = storage
```

### 7.4 编写可测试的代码

**原则：** 每层都应该可以独立测试

```python
# ✓ Core 层可测试(使用 Mock)
@pytest.fixture
def key_manager(mock_store, mock_validator):
    return KeyManager(mock_store, mock_validator)

def test_create_key_success(key_manager):
    request = KeyCreateRequest(provider="openai", name="test")
    result = key_manager.create_key(request)
    assert result.provider == "openai"

# ✓ Utils 层可测试(纯函数)
def test_generate_key():
    key = generate_key()
    assert key.startswith("lpg_")
    assert len(key) == 69

# ✓ Models 层可测试(数据验证)
def test_key_create_request_validation():
    with pytest.raises(ValidationError):
        KeyCreateRequest(provider="", name="test")
```

### 7.5 定期重构和审查

**原则：** 定期检查代码是否符合分层规则

**代码审查检查项：**

- [ ] 新增代码是否放在了正确的层?
- [ ] 是否存在跨层直接调用?
- [ ] 是否存在循环依赖?
- [ ] 是否违反了依赖矩阵规则?
- [ ] 是否有"上帝类"需要拆分?
- [ ] Models 是否包含了不该有的逻辑?
- [ ] Utils 是否包含了业务逻辑?

### 7.6 文档化架构决策

**原则：** 重要的架构决策应该有文档记录

```markdown
# 架构决策记录 (ADR)

## ADR-001: 选择分层架构

**状态：** 已接受  
**日期：** 2026-04-05

### 背景
项目需要清晰的代码组织结构,便于团队协作和长期维护。

### 决策
采用四层架构：CLI → Core → Models → Utils

### 理由
- 职责清晰,易于理解
- 支持独立测试
- 降低模块耦合
- 便于新人上手

### 后果
- 需要严格遵守分层规则
- 初期可能需要额外抽象
- 长期收益大于成本
```

---

## 附录：快速参考

### A. 分层速查表

| 层级 | 路径 | 职责 | 允许依赖 | 典型文件 |
|------|------|------|----------|----------|
| CLI | `src/lpg/cli/` | 用户交互 | Core, Models, Utils(△) | 命令定义、参数解析 |
| Core | `src/lpg/core/` | 业务逻辑 | Models, Utils, Core 内部 | 服务类、管理器 |
| Models | `src/lpg/models/` | 数据结构 | Utils, Models 内部 | Pydantic 模型 |
| Utils | `src/lpg/utils/` | 通用工具 | Utils 内部 | 工具函数、异常 |

### B. 依赖规则口诀

```
上层调下没问题,
下层绝对不能往上指。
同层内部随便用,
跨层调用走 Core 门。
循环依赖要不得,
接口解耦是正道。
```

### C. 常用命令

```bash
# 检查循环依赖
pip install pylint
pylint --disable=all --enable=cyclic-import src/lpg/

# 检查导入依赖
pip install import-linter
import-linter  # 需要在 .import-linter 配置依赖规则

# 生成依赖图
pip install pydeps
pydeps src/lpg --max-bacon=2
```

---

**文档结束**

如有疑问或建议,请通过 Issue 或讨论区反馈。

**相关文档：**
- [编码规范](./coding-rule.md)
- [设计文档](../design/)
- [需求文档](../req/)
