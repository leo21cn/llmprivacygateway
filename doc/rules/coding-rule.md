# LLM Privacy Gateway - 编码规范

**版本：** 1.0  
**日期：** 2026-04-04  
**适用范围：** 全项目 Python 代码  
**参考标准：** PEP 8, PEP 484, PEP 257, Google Python Style Guide

---

## 目录

1. [基本原则](#1-基本原则)
2. [代码格式](#2-代码格式)
3. [命名规范](#3-命名规范)
4. [类型注解](#4-类型注解)
5. [文档字符串](#5-文档字符串)
6. [导入规范](#6-导入规范)
7. [函数与方法](#7-函数与方法)
8. [类设计](#8-类设计)
9. [异步编程](#9-异步编程)
10. [错误处理](#10-错误处理)
11. [日志规范](#11-日志规范)
12. [Presidio 集成规范](#12-presidio-集成规范)
13. [测试规范](#13-测试规范)
14. [项目结构](#14-项目结构)
15. [Git 提交规范](#15-git-提交规范)
16. [代码审查清单](#16-代码审查清单)

---

## 1. 基本原则

| 原则 | 说明 |
|------|------|
| **可读性优先** | 代码是写给人看的，顺便让机器执行 |
| **显式优于隐式** | 明确表达意图，避免魔法操作 |
| **简单优于复杂** | 选择最简单的解决方案，避免过度设计 |
| **一致性** | 遵循项目已有风格，保持代码风格统一 |
| **单一职责** | 每个函数/类只做一件事，做好一件事 |

---

## 2. 代码格式

### 2.1 基础格式

- **行长度**：最大 100 字符
- **缩进**：4 个空格（禁止使用 Tab）
- **引号**：优先使用双引号 `"`，字符串内含双引号时用单引号 `'`
- **空行**：
  - 顶级定义之间：2 个空行
  - 方法定义之间：1 个空行
  - 逻辑块之间：1 个空行

### 2.2 格式化工具

```bash
# 使用 Black 进行代码格式化
black src/ tests/

# 使用 Ruff 进行 lint 检查
ruff check src/ tests/

# 使用 mypy 进行类型检查
mypy src/
```

### 2.3 pyproject.toml 配置

```toml
[tool.black]
line-length = 100
target-version = ['py310']

[tool.ruff]
line-length = 100
target-version = "py310"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "SIM", # flake8-simplify
]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### 2.4 示例

```python
# ✓ 正确
def calculate_masked_length(original: str, visible_chars: int = 4) -> int:
    """计算脱敏后的显示长度"""
    if len(original) <= visible_chars:
        return len(original)
    return visible_chars + 3  # *** 后缀


# ✗ 错误
def calculateMaskedLength(original,visibleChars=4):# 缺少空格和类型注解
    if len(original)<=visibleChars:return len(original)
    return visibleChars+3
```

---

## 3. 命名规范

### 3.1 命名风格对照表

| 类型 | 风格 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `proxy_server.py`, `presidio_client` |
| 类 | PascalCase | `ProxyServer`, `KeyManager` |
| 异常类 | PascalCase + Error | `ConfigError`, `KeyNotFoundError` |
| 函数/方法 | snake_case | `get_virtual_key()`, `process_request()` |
| 变量 | snake_case | `virtual_key`, `request_data` |
| 常量 | UPPER_SNAKE_CASE | `MAX_CONNECTIONS`, `DEFAULT_TIMEOUT` |
| 私有成员 | _leading_underscore | `_internal_state`, `_cache` |
| 受保护成员 | _single_underscore | `_protected_method()` |
| 魔术方法 | __dunder__ | `__init__`, `__str__` |

### 3.2 命名原则

```python
# ✓ 好的命名：清晰表达意图
virtual_key_manager = KeyManager()
pii_detection_result = await analyzer.detect(text)
is_valid_key = self._validate_key_format(key)

# ✗ 不好的命名：含义模糊
mgr = KeyManager()
res = await analyzer.detect(text)
flag = self._validate_key_format(key)
```

### 3.3 布尔变量命名

```python
# 使用 is_, has_, can_, should_ 前缀
is_running: bool
has_permission: bool
can_process: bool
should_retry: bool

# 否定形式使用 enable/disable 风格
enable_restoration: bool  # ✓
disable_restoration: bool  # ✓
not_enabled: bool  # ✗ 避免双重否定
```

### 3.4 Presidio 相关命名

```python
# Presidio 组件命名保持一致
presidio_client: PresidioClient
presidio_analyzer: PresidioAnalyzer
presidio_anonymizer: PresidioAnonymizer

# PII 相关命名
pii_entities: List[PIIEntity]
pii_detection_result: DetectionResult
anonymized_text: str
```

---

## 4. 类型注解

### 4.1 基本要求

**所有公共接口必须有完整的类型注解**

```python
# ✓ 正确：完整的类型注解
def create_virtual_key(
    provider: str,
    name: str,
    expires_at: Optional[str] = None,
    permissions: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """创建虚拟 Key"""
    ...

# ✗ 错误：缺少类型注解
def create_virtual_key(provider, name, expires_at=None, permissions=None):
    ...
```

### 4.2 常用类型

```python
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
    Tuple,
    Callable,
    Awaitable,
    TypeVar,
    Protocol,
)
from collections.abc import Sequence, Mapping

# 基础类型
name: str
count: int
ratio: float
is_enabled: bool

# 集合类型
items: List[str]
mapping: Dict[str, int]
data: Dict[str, Any]

# 可选类型
optional_value: Optional[str]  # 等价于 Union[str, None]

# 联合类型
value: Union[str, int]

# 回调类型
callback: Callable[[str], bool]
async_callback: Callable[[str], Awaitable[bool]]
```

### 4.3 使用 Pydantic 模型

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class ProviderConfig(BaseModel):
    """LLM 提供商配置"""
    name: str
    type: str
    base_url: str
    auth_type: str = "bearer"
    timeout: int = Field(default=60, ge=1, le=300)
    
    class Config:
        # 允许任意类型字段（向后兼容）
        extra = "allow"

class GatewayConfig(BaseModel):
    """网关主配置"""
    providers: List[ProviderConfig] = Field(default_factory=list)
    proxy_host: str = "127.0.0.1"
    proxy_port: int = Field(default=8080, ge=1024, le=65535)
```

### 4.4 Protocol 定义接口

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class KeyStore(Protocol):
    """Key 存储接口"""
    
    def get(self, key_id: str) -> Optional[Dict[str, Any]]:
        """获取 Key"""
        ...
    
    def set(self, key_id: str, data: Dict[str, Any]) -> None:
        """设置 Key"""
        ...
    
    def delete(self, key_id: str) -> bool:
        """删除 Key"""
        ...
```

---

## 5. 文档字符串

### 5.1 格式要求

使用 Google 风格的 docstring，**所有模块、类、公共函数必须有 docstring**

### 5.2 模块文档

```python
"""
Presidio 客户端模块。

提供与微软 Presidio 服务的 HTTP 交互能力，包括：
- PII 检测（Analyzer）
- 脱敏处理（Anonymizer）
- 解密还原（Decryptor）

Example:
    >>> client = PresidioClient(config)
    >>> results = await client.analyze("我的邮箱是 test@example.com")
    >>> anonymized = await client.anonymize(text, results)
"""
```

### 5.3 类文档

```python
class PresidioClient:
    """
    Presidio 服务客户端。
    
    封装与 Presidio Analyzer 和 Anonymizer 的 HTTP 交互，
    提供简化的 PII 检测和脱敏接口。
    
    Attributes:
        base_url: Presidio 服务的基础 URL
        language: 默认检测语言
        timeout: 请求超时时间（秒）
    
    Example:
        >>> client = PresidioClient(config_service)
        >>> detections = await client.analyze("包含邮箱的文本")
        >>> anonymized = await client.anonymize(text, detections)
    """
    
    def __init__(self, config_service: ConfigService) -> None:
        """
        初始化 Presidio 客户端。
        
        Args:
            config_service: 配置服务实例，用于获取 Presidio 端点配置
        """
        self._config = config_service
        self._base_url = config_service.get('presidio.endpoint')
```

### 5.4 函数文档

```python
async def analyze(
    self,
    text: str,
    language: Optional[str] = None,
    entities: Optional[List[str]] = None,
    score_threshold: float = 0.5
) -> List[DetectionResult]:
    """
    分析文本中的 PII 实体。
    
    调用 Presidio Analyzer 服务检测文本中的个人身份信息，
    返回检测到的实体列表及其位置和置信度。
    
    Args:
        text: 待分析的文本内容
        language: 语言代码，如 'zh', 'en'，默认使用配置值
        entities: 指定检测的实体类型列表，None 表示检测所有类型
        score_threshold: 最低置信度阈值，范围 0-1
    
    Returns:
        检测结果列表，每个结果包含：
        - entity_type: 实体类型（如 'EMAIL_ADDRESS'）
        - start: 起始位置
        - end: 结束位置
        - score: 置信度（0-1）
    
    Raises:
        PresidioConnectionError: 无法连接到 Presidio 服务
        PresidioTimeoutError: 请求超时
    
    Example:
        >>> results = await client.analyze(
        ...     "我的邮箱是 test@example.com",
        ...     language="zh",
        ...     score_threshold=0.7
        ... )
        >>> print(results)
        [{'entity_type': 'EMAIL_ADDRESS', 'start': 6, 'end': 24, 'score': 0.95}]
    """
```

### 5.5 简单函数文档

对于简单的函数，可以使用简短的单行 docstring：

```python
def get_key_id(self) -> str:
    """获取 Key 的唯一标识符"""
    return self._key_id

def is_expired(self) -> bool:
    """检查 Key 是否已过期"""
    return self._expires_at and datetime.now() > self._expires_at
```

---

## 6. 导入规范

### 6.1 导入顺序

1. 标准库导入
2. 第三方库导入
3. 本地模块导入

每组之间用空行分隔：

```python
# 标准库
import os
import sys
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

# 第三方库
import aiohttp
from pydantic import BaseModel, Field
from loguru import logger

# 本地模块
from lpg.core.config.service import ConfigService
from lpg.core.presidio.exceptions import PresidioError
from lpg.utils.crypto import encrypt, decrypt
```

### 6.2 导入方式

```python
# ✓ 推荐：绝对导入
from lpg.core.proxy.server import ProxyServer

# ✓ 允许：相对导入（同包内）
from .models import ConfigModel
from .exceptions import ConfigError

# ✗ 避免：模糊的通配导入
from lpg.core import *  # 禁止
```

### 6.3 条件导入

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 仅用于类型检查，运行时不导入
    from lpg.core.config.service import ConfigService

def process(config: "ConfigService") -> None:
    # 使用字符串形式的类型注解
    ...
```

---

## 7. 函数与方法

### 7.1 函数设计原则

- **单一职责**：每个函数只做一件事
- **参数数量**：尽量不超过 5 个参数
- **函数长度**：建议不超过 50 行
- **返回值**：避免返回 None 表示错误，使用异常

### 7.2 参数设计

```python
# ✓ 好的设计：使用关键字参数提高可读性
def create_proxy_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    max_connections: int = 100,
    timeout: int = 60
) -> ProxyServer:
    ...

# 调用时
server = create_proxy_server(
    host="0.0.0.0",
    port=9000,
    max_connections=200
)

# ✗ 不好的设计：过多位置参数
def create_proxy_server(host, port, max_conn, timeout, ...):
    ...

# 调用时难以理解
server = create_proxy_server("0.0.0.0", 9000, 200, 60, ...)
```

### 7.3 复杂参数使用 Dataclass/Pydantic

```python
from pydantic import BaseModel

class ServerConfig(BaseModel):
    """服务器配置"""
    host: str = "127.0.0.1"
    port: int = 8080
    max_connections: int = 100
    timeout: int = 60

def create_proxy_server(config: ServerConfig) -> ProxyServer:
    """创建代理服务器"""
    ...

# 调用时
config = ServerConfig(host="0.0.0.0", port=9000)
server = create_proxy_server(config)
```

### 7.4 私有方法

```python
class RequestHandler:
    
    def handle(self, request: Request) -> Response:
        """公共接口：处理请求"""
        self._validate_request(request)
        self._log_request(request)
        return self._process_request(request)
    
    def _validate_request(self, request: Request) -> None:
        """私有方法：验证请求"""
        ...
    
    def _log_request(self, request: Request) -> None:
        """私有方法：记录请求日志"""
        ...
    
    def _process_request(self, request: Request) -> Response:
        """私有方法：处理请求"""
        ...
```

---

## 8. 类设计

### 8.1 类组织顺序

```python
class MyClass:
    """类文档"""
    
    # 1. 类变量
    DEFAULT_TIMEOUT = 60
    
    # 2. __init__
    def __init__(self, name: str) -> None:
        self.name = name
        self._internal_state: Dict[str, Any] = {}
    
    # 3. 魔术方法
    def __str__(self) -> str:
        return f"MyClass({self.name})"
    
    def __repr__(self) -> str:
        return f"MyClass(name='{self.name}')"
    
    # 4. 公共方法
    def public_method(self) -> None:
        """公共方法"""
        ...
    
    # 5. 私有方法
    def _private_method(self) -> None:
        """私有方法"""
        ...
    
    # 6. 静态方法
    @staticmethod
    def utility_function(value: str) -> bool:
        """工具函数"""
        ...
    
    # 7. 类方法
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "MyClass":
        """从配置创建实例"""
        return cls(name=config["name"])
```

### 8.2 依赖注入

```python
# ✓ 推荐：通过构造函数注入依赖
class RequestHandler:
    def __init__(
        self,
        key_manager: KeyManager,
        rule_manager: RuleManager,
        presidio_client: PresidioClient,
        audit_service: AuditService,
        config_service: ConfigService
    ) -> None:
        self._key_manager = key_manager
        self._rule_manager = rule_manager
        self._presidio = presidio_client
        self._audit = audit_service
        self._config = config_service

# ✗ 避免：在类内部创建依赖
class RequestHandler:
    def __init__(self) -> None:
        self._key_manager = KeyManager()  # 紧耦合
        self._presidio = PresidioClient()  # 难以测试
```

### 8.3 使用 Protocol 定义接口

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Storage(Protocol):
    """存储接口协议"""
    
    def save(self, key: str, value: Any) -> None:
        ...
    
    def load(self, key: str) -> Optional[Any]:
        ...
    
    def delete(self, key: str) -> bool:
        ...

# 实现类
class FileStorage:
    def save(self, key: str, value: Any) -> None:
        ...
    
    def load(self, key: str) -> Optional[Any]:
        ...
    
    def delete(self, key: str) -> bool:
        ...

# 使用时
def process(storage: Storage) -> None:
    storage.save("key", "value")
```

---

## 9. 异步编程

### 9.1 基本原则

- I/O 密集型操作使用 `async/await`
- CPU 密集型操作考虑使用线程池
- 避免在异步函数中使用阻塞调用

### 9.2 异步函数定义

```python
# ✓ 正确：异步 I/O 操作
async def fetch_data(url: str) -> Dict[str, Any]:
    """异步获取数据"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# ✓ 正确：调用异步函数
async def process_request(request: Request) -> Response:
    data = await fetch_data(request.url)
    return Response(data=data)

# ✗ 错误：在异步函数中使用阻塞调用
async def process_request(request: Request) -> Response:
    with open("file.txt", "r") as f:  # 阻塞调用！
        data = f.read()
    return Response(data=data)

# ✓ 正确：使用 run_in_executor 处理阻塞操作
async def read_file(path: str) -> str:
    loop = asyncio.get_event_loop()
    with open(path, "r") as f:
        return await loop.run_in_executor(None, f.read)
```

### 9.3 异步上下文管理器

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_presidio_client(config: ConfigService):
    """异步上下文管理器：获取 Presidio 客户端"""
    client = PresidioClient(config)
    try:
        yield client
    finally:
        await client.close()

# 使用
async def process():
    async with get_presidio_client(config) as client:
        result = await client.analyze(text)
```

### 9.4 异步迭代

```python
async def stream_response(url: str) -> AsyncIterator[bytes]:
    """流式响应迭代器"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content:
                yield chunk

# 使用
async for chunk in stream_response(url):
    await process_chunk(chunk)
```

---

## 10. 错误处理

### 10.1 异常层次结构

```python
# lpg/core/exceptions.py

class LPGError(Exception):
    """LPG 基础异常类"""
    pass

class ConfigError(LPGError):
    """配置相关错误"""
    pass

class KeyError(LPGError):
    """Key 相关错误"""
    pass

class KeyNotFoundError(KeyError):
    """Key 未找到"""
    pass

class KeyExpiredError(KeyError):
    """Key 已过期"""
    pass

class PresidioError(LPGError):
    """Presidio 服务错误"""
    pass

class PresidioConnectionError(PresidioError):
    """Presidio 连接失败"""
    pass

class PresidioTimeoutError(PresidioError):
    """Presidio 请求超时"""
    pass

class ProxyError(LPGError):
    """代理服务错误"""
    pass

class RuleError(LPGError):
    """规则相关错误"""
    pass
```

### 10.2 异常使用原则

```python
# ✓ 正确：使用具体的异常类型
def get_key(key_id: str) -> Dict[str, Any]:
    if key_id not in self._keys:
        raise KeyNotFoundError(f"Key not found: {key_id}")
    key = self._keys[key_id]
    if self._is_expired(key):
        raise KeyExpiredError(f"Key expired: {key_id}")
    return key

# ✗ 错误：使用通用异常
def get_key(key_id: str) -> Dict[str, Any]:
    if key_id not in self._keys:
        raise Exception("Key not found")  # 太笼统
```

### 10.3 异常捕获

```python
# ✓ 正确：捕获具体异常
try:
    result = await presidio_client.analyze(text)
except PresidioConnectionError:
    logger.error("Failed to connect to Presidio service")
    raise
except PresidioTimeoutError:
    logger.warning("Presidio request timed out")
    return []  # 降级处理

# ✓ 正确：重新抛出异常时保留上下文
try:
    data = load_config(path)
except FileNotFoundError as e:
    raise ConfigError(f"Config file not found: {path}") from e

# ✗ 错误：捕获所有异常
try:
    result = await presidio_client.analyze(text)
except Exception:
    pass  # 吞掉所有异常
```

### 10.4 清理资源

```python
# 使用 async context manager
async def process_with_cleanup():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

# 手动清理（备选方案）
async def process_with_finally():
    session = None
    try:
        session = aiohttp.ClientSession()
        async with session.post(url, json=data) as response:
            return await response.json()
    finally:
        if session:
            await session.close()
```

---

## 11. 日志规范

### 11.1 日志级别使用

| 级别 | 使用场景 | 示例 |
|------|----------|------|
| DEBUG | 调试信息，详细的数据流 | "Received request: {request}" |
| INFO | 正常操作流程 | "Server started on port 8080" |
| WARNING | 潜在问题，但不影响运行 | "Key expiring soon: {key_id}" |
| ERROR | 错误，影响当前操作 | "Failed to connect to Presidio" |
| CRITICAL | 严重错误，影响整个系统 | "Database connection lost" |

### 11.2 日志使用方式

```python
from loguru import logger

# 基本日志
logger.info("Server started successfully")
logger.warning("Key expiring in 1 hour")
logger.error("Failed to process request")

# 带上下文的日志
logger.info("Processing request from {source}", source=request.source)
logger.debug("PII detected: {count} entities", count=len(detections))

# 异常日志
try:
    result = await process()
except Exception as e:
    logger.exception("Processing failed")  # 自动包含异常堆栈
    raise

# 结构化日志（用于审计）
logger.bind(
    event_type="pii_detection",
    entity_count=len(detections),
    processing_time_ms=duration
).info("PII detection completed")
```

### 11.3 日志配置

```python
# lpg/utils/logging.py

import sys
from loguru import logger

def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """配置日志系统"""
    
    # 移除默认处理器
    logger.remove()
    
    # 控制台输出
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True
    )
    
    # 文件输出（如果配置）
    if log_file:
        logger.add(
            log_file,
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            rotation="10 MB",
            retention="30 days",
            compression="gz"
        )
```

---

## 12. Presidio 集成规范

### 12.1 客户端封装原则

- 封装 Presidio HTTP API 调用细节
- 提供简化的 Python 接口
- 处理连接错误和超时
- 支持配置驱动

### 12.2 错误处理

```python
import aiohttp
from lpg.core.exceptions import PresidioConnectionError, PresidioTimeoutError

class PresidioClient:
    """Presidio 服务客户端"""
    
    async def analyze(self, text: str) -> List[Dict[str, Any]]:
        """调用 Presidio Analyzer"""
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(
                    f"{self._base_url}/analyze",
                    json={"text": text, "language": self._language}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Analyzer returned status {response.status}")
                        return []
        except aiohttp.ClientConnectionError as e:
            raise PresidioConnectionError(f"Cannot connect to Presidio: {e}") from e
        except asyncio.TimeoutError as e:
            raise PresidioTimeoutError(f"Presidio request timed out: {e}") from e
```

### 12.3 配置管理

```python
class PresidioClient:
    def __init__(self, config_service: ConfigService) -> None:
        # 从配置读取，而非硬编码
        self._base_url = config_service.get(
            'presidio.endpoint',
            'http://localhost:5001'
        )
        self._language = config_service.get('presidio.language', 'zh')
        timeout_seconds = config_service.get('presidio.timeout', 30)
        self._timeout = aiohttp.ClientTimeout(total=timeout_seconds)
```

### 12.4 响应数据转换

```python
from dataclasses import dataclass
from typing import List

@dataclass
class DetectionResult:
    """PII 检测结果"""
    entity_type: str
    start: int
    end: int
    score: float
    
    @classmethod
    def from_presidio(cls, data: Dict[str, Any]) -> "DetectionResult":
        """从 Presidio 响应创建"""
        return cls(
            entity_type=data["entity_type"],
            start=data["start"],
            end=data["end"],
            score=data["score"]
        )
    
    @classmethod
    def from_presidio_list(cls, data: List[Dict[str, Any]]) -> List["DetectionResult"]:
        """批量转换"""
        return [cls.from_presidio(item) for item in data]
```

---

## 13. 测试规范

### 13.1 测试文件组织

```
tests/
├── conftest.py              # 共享 fixtures
├── unit/
│   ├── __init__.py
│   ├── test_key_manager.py
│   └── test_rule_manager.py
├── integration/
│   ├── __init__.py
│   └── test_proxy_handler.py
└── e2e/
    ├── __init__.py
    └── test_full_workflow.py
```

### 13.2 测试命名

```python
# 测试文件：test_<module_name>.py
# 测试类：Test<ClassName>
# 测试方法：test_<method_name>_<scenario>

class TestKeyManager:
    
    def test_create_key_success(self):
        """测试成功创建 Key"""
        ...
    
    def test_create_key_with_invalid_provider(self):
        """测试使用无效提供商创建 Key"""
        ...
    
    def test_resolve_key_expired(self):
        """测试解析已过期的 Key"""
        ...
```

### 13.3 Fixtures 使用

```python
# tests/conftest.py

import pytest
from lpg.core.config.service import ConfigService
from lpg.core.key.manager import KeyManager

@pytest.fixture
def config_service(tmp_path):
    """提供测试用配置服务"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
    proxy:
      host: 127.0.0.1
      port: 8080
    providers:
      - name: openai
        type: openai
        base_url: https://api.openai.com
    """)
    return ConfigService(str(config_file))

@pytest.fixture
def key_manager(config_service):
    """提供测试用 Key 管理器"""
    return KeyManager(config_service)

@pytest.fixture
def sample_key(key_manager):
    """提供测试用虚拟 Key"""
    return key_manager.create(provider="openai", name="test")
```

### 13.4 异步测试

```python
import pytest

@pytest.mark.asyncio
async def test_presidio_analyze(presidio_client):
    """测试 Presidio 分析"""
    results = await presidio_client.analyze("我的邮箱是 test@example.com")
    assert len(results) > 0
    assert results[0]["entity_type"] == "EMAIL_ADDRESS"

@pytest.mark.asyncio
async def test_request_handler(request_handler, mock_request):
    """测试请求处理器"""
    response = await request_handler.handle(mock_request)
    assert response.status == 200
```

### 13.5 Mock 使用

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock_presidio():
    """使用 Mock 测试"""
    with patch('lpg.core.presidio.client.PresidioClient.analyze') as mock_analyze:
        mock_analyze.return_value = [
            {"entity_type": "EMAIL", "start": 0, "end": 5, "score": 0.9}
        ]
        
        client = PresidioClient(config)
        results = await client.analyze("test text")
        
        mock_analyze.assert_called_once_with("test text")
        assert len(results) == 1
```

### 13.6 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=lpg --cov-report=html --cov-report=term-missing

# 要求核心模块覆盖率 > 80%
```

---

## 14. 项目结构

### 14.1 目录结构规范

```
llm-privacy-gateway/
├── pyproject.toml           # 项目配置
├── README.md                # 项目说明
├── LICENSE                  # 许可证
├── CHANGELOG.md             # 变更日志
│
├── src/                     # 源代码目录
│   └── lpg/                 # 主包
│       ├── __init__.py
│       ├── __main__.py      # python -m lpg 入口
│       ├── cli/             # CLI 模块
│       ├── core/            # 核心业务逻辑
│       ├── models/          # 数据模型
│       └── utils/           # 工具函数
│
├── rules/                   # 内置规则文件
│   ├── pii.yaml
│   └── credentials.yaml
│
├── tests/                   # 测试代码
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                 # 辅助脚本
│   ├── install.sh
│   └── setup_presidio.sh
│
└── docs/                    # 文档
    ├── design/
    ├── rules/
    └── api/
```

### 14.2 模块文件组织

```python
# core/proxy/__init__.py
"""代理服务模块"""

from .server import ProxyServer
from .handler import RequestHandler
from .stream import StreamHandler

__all__ = ["ProxyServer", "RequestHandler", "StreamHandler"]
```

### 14.3 循环依赖处理

```python
# 避免循环导入
# 错误示例：
# module_a.py
from lpg.core.b import ClassB  # 可能导致循环导入

# 正确做法：使用 TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lpg.core.b import ClassB

def process(obj: "ClassB") -> None:  # 字符串形式的类型注解
    ...
```

---

## 15. Git 提交规范

### 15.1 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 15.2 Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构（非新功能、非修复） |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具/依赖更新 |
| ci | CI 配置 |

### 15.3 示例

```
feat(key-manager): 添加虚拟 Key 过期时间支持

- 支持为虚拟 Key 设置过期时间
- 过期 Key 自动失效
- 添加相关单元测试

Closes #123
```

```
fix(presidio): 修复连接超时未正确处理的问题

当 Presidio 服务不可用时，之前会抛出未捕获的异常。
现在会抛出 PresidioConnectionError 并正确记录日志。
```

---

## 16. 代码审查清单

### 16.1 提交前自查

- [ ] 代码格式化（Black）
- [ ] Lint 检查通过（Ruff）
- [ ] 类型检查通过（mypy）
- [ ] 单元测试通过
- [ ] 新增代码有测试覆盖
- [ ] 公共接口有文档字符串
- [ ] 提交信息符合规范

### 16.2 Code Review 检查项

| 类别 | 检查项 |
|------|--------|
| **功能** | 功能是否正确实现？边界情况是否处理？ |
| **设计** | 代码结构是否合理？是否遵循单一职责？ |
| **命名** | 变量/函数命名是否清晰？是否遵循命名规范？ |
| **注释** | 复杂逻辑是否有注释？文档是否完整？ |
| **错误处理** | 异常处理是否完善？是否有资源泄漏？ |
| **测试** | 测试覆盖是否足够？测试用例是否合理？ |
| **性能** | 是否有明显的性能问题？ |
| **安全** | 是否有安全隐患？敏感数据是否正确处理？ |

---

## 附录：快速参考

### 常用命令

```bash
# 格式化代码
black src/ tests/

# Lint 检查
ruff check src/ tests/

# 类型检查
mypy src/

# 运行测试
pytest

# 运行测试并生成覆盖率
pytest --cov=lpg --cov-report=html

# 安装开发依赖
pip install -e ".[dev]"
```

### 编辑器配置

推荐使用 VS Code，安装以下插件：
- Python
- Pylance
- Black Formatter
- Ruff

`.vscode/settings.json`:
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

---

**文档结束**

如有疑问或建议，请通过 Issue 或讨论区反馈。
