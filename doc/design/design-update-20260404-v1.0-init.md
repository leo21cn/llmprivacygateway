# LLM API 隐私保护网关 - v1.0 MVP 技术设计文档

**版本：** 1.0  
**日期：** 2026-04-04  
**状态：** 设计评审中  
**依赖：** req-init-20260401.md (v0.4)

---

## 目录

1. [设计概述](#1-设计概述)
2. [架构设计](#2-架构设计)
3. [模块详细设计](#3-模块详细设计)
4. [接口设计](#4-接口设计)
5. [数据模型设计](#5-数据模型设计)
6. [配置系统设计](#6-配置系统设计)
7. [扩展性设计](#7-扩展性设计)
8. [测试策略](#8-测试策略)
9. [实现计划](#9-实现计划)
10. [附录](#10-附录)

---

## 1. 设计概述

### 1.1 设计目标

v1.0 MVP 版本的核心目标是实现一个**可用的 CLI 隐私保护代理**，具备以下能力：

| 目标 | 说明 | 验收标准 |
|------|------|----------|
| **核心代理功能** | 本地 HTTP 代理，支持 OpenAI API 格式 | 能成功转发请求并返回响应 |
| **PII 检测脱敏** | 基于 Presidio 的敏感信息处理 | 检测率 > 90%，误报 < 10% |
| **虚拟 Key 管理** | 虚拟 Key 生成、映射、验证 | 支持多 Key 管理 |
| **基础规则管理** | 预设规则加载、自定义规则导入 | 支持 YAML 规则配置 |
| **审计日志** | 请求处理记录 | 支持日志查询和导出 |

### 1.2 设计原则

| 原则 | 说明 | 实现方式 |
|------|------|----------|
| **简单优先** | MVP 聚焦核心价值，避免过度设计 | 仅实现必要功能，预留扩展点 |
| **接口稳定** | 核心接口面向后续版本兼容 | 使用协议/接口定义，依赖注入 |
| **配置驱动** | 行为通过配置控制，便于扩展 | YAML 配置 + 环境变量 |
| **可测试性** | 模块化设计，便于单元测试 | 接口抽象 + 依赖注入 |
| **渐进增强** | v1.0 基础功能，后续版本增量增强 | 预留扩展点和钩子 |

### 1.3 v1.0 范围边界

**包含功能：**
- CLI 命令行工具（start/stop/status/config/key/rule/log）
- 本地 HTTP 代理服务器（支持 OpenAI API 格式）
- Presidio 本地服务集成（PII 检测 + 脱敏）
- 虚拟 Key 管理（配置文件方式）
- 基础规则管理（本地 YAML 文件）
- 审计日志（文件输出）
- 基础配置管理（YAML 配置文件）

**不包含功能（v1.1+）：**
- ❌ 规则库订阅服务
- ❌ 规则云端同步
- ❌ 自然语言创建规则
- ❌ 可视化配置界面
- ❌ macOS GUI 应用
- ❌ 团队协作功能

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CLI Application (lpg)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          CLI Layer (Click)                              │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │ │
│  │  │  start  │ │  stop   │ │ status  │ │ config  │ │   key   │  ...    │ │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘         │ │
│  │       │           │           │           │           │               │ │
│  │       └───────────┴───────────┴───────────┴───────────┘               │ │
│  │                              │                                        │ │
│  │                    Service Facade (统一服务门面)                       │ │
│  └──────────────────────────────│────────────────────────────────────────┘ │
│                                 │                                           │
│  ┌──────────────────────────────│────────────────────────────────────────┐ │
│  │                    Core Service Layer                                  │ │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐             │ │
│  │  │ ProxyService  │  │ KeyService    │  │ RuleService   │             │ │
│  │  │ (代理服务)     │  │ (Key管理)     │  │ (规则管理)     │             │ │
│  │  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘             │ │
│  │          │                  │                  │                      │ │
│  │  ┌───────┴───────┐  ┌───────┴───────┐  ┌───────┴───────┐             │ │
│  │  │ AuditService  │  │ ConfigService │  │ PresidioClient│             │ │
│  │  │ (审计服务)     │  │ (配置服务)     │  │ (Presidio客户端)│            │ │
│  │  └───────────────┘  └───────────────┘  └───────────────┘             │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                          Infrastructure Layer                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │ │
│  │  │ YAML Config │  │ File Logger │  │ HTTP Client │  │   Crypto    │  │ │
│  │  │ (配置存储)   │  │ (日志存储)   │  │ (HTTP客户端) │  │   (加密)    │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      External Presidio Service                               │
│  ┌─────────────────────────────────┐ ┌─────────────────────────────────────┐│
│  │ presidio-analyzer (port 5001)   │ │ presidio-anonymizer (port 5001)    ││
│  │ POST /analyze                   │ │ POST /anonymize                    ││
│  └─────────────────────────────────┘ └─────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 模块依赖关系

```
                    ┌─────────────────┐
                    │   CLI Entry     │
                    │   (main.py)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  CLI Commands   │
                    │  (commands/)    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Service Facade  │
                    │  (facade.py)    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  ProxyService   │ │   KeyService    │ │   RuleService   │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  Shared Components                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ConfigService│  │AuditService │  │PresidioClient│    │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 数据流设计

#### 2.3.1 请求处理流程

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            请求处理完整流程                                   │
└──────────────────────────────────────────────────────────────────────────────┘

外部应用请求（使用虚拟 Key）
     │
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1: 接收请求 & 虚拟 Key 验证                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ HTTP Server │───▶│ KeyResolver │───▶│ KeyMapping  │                      │
│  │ 接收请求     │    │ 解析虚拟Key │    │ 查询真实Key │                      │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
│                          │ 验证失败返回 401                                   │
└──────────────────────────│──────────────────────────────────────────────────┘
                           │ 验证通过
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 2: Presidio Analyzer - PII 检测                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ RequestBuilder                                                        │  │
│  │   │                                                                   │  │
│  │   ├── 提取消息内容（user/assistant messages）                          │  │
│  │   ├── 构建 analyze 请求                                               │  │
│  │   │                                                                   │  │
│  │   ▼                                                                   │  │
│  │ PresidioClient.post("/analyze", {text, language, recognizers})        │  │
│  │   │                                                                   │  │
│  │   ▼                                                                   │  │
│  │ 返回: [{"entity_type": "EMAIL", "start": 10, "end": 25, "score": 0.9}]│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 3: Presidio Anonymizer - PII 脱敏                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ AnonymizeBuilder                                                      │  │
│  │   │                                                                   │  │
│  │   ├── 根据检测结果构建脱敏请求                                          │  │
│  │   ├── 应用默认脱敏策略（可配置）                                        │  │
│  │   │                                                                   │  │
│  │   ▼                                                                   │  │
│  │ PresidioClient.post("/anonymize", {text, anonymizers})                │  │
│  │   │                                                                   │  │
│  │   ▼                                                                   │  │
│  │ 返回: {"text": "脱敏后文本", "items": [...]}                           │  │
│  │ 同时: 保存加密映射表到 request context                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 4: 转发请求到 LLM API                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ 替换真实Key │───▶│ 构建请求体  │───▶│ HTTP Client │                      │
│  │             │    │ (脱敏内容)  │    │ 发送请求     │                      │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 5: 响应处理                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ 接收响应    │───▶│ 内容还原    │───▶│ 返回客户端  │                      │
│  │ (SSE/JSON)  │    │ (可选)      │    │             │                      │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 6: 审计日志记录                                                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ AuditEntry {                                                          │  │
│  │   timestamp, source_app, provider, endpoint,                          │  │
│  │   detections: [...], masking_actions: [...],                          │  │
│  │   duration, status                                                    │  │
│  │ }                                                                     │  │
│  │   │                                                                   │  │
│  │   ▼                                                                   │  │
│  │ AuditService.log(entry) → 写入日志文件                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 模块详细设计

### 3.1 CLI 模块 (cli/)

#### 3.1.1 目录结构

```
cli/
├── __init__.py
├── main.py              # CLI 入口，Click 应用定义
├── commands/
│   ├── __init__.py
│   ├── start.py         # 启动代理服务器
│   ├── stop.py          # 停止代理服务器
│   ├── status.py        # 查看服务状态
│   ├── config.py        # 配置管理
│   ├── key.py           # 虚拟 Key 管理
│   ├── rule.py          # 规则管理
│   ├── provider.py      # LLM 提供商管理
│   └── log.py           # 日志查看
└── utils/
    ├── __init__.py
    ├── output.py        # 输出格式化（Rich）
    └── interactive.py   # 交互式输入
```

#### 3.1.2 主入口设计 (main.py)

```python
# main.py - CLI 入口
import click
from lpg.core.service_facade import ServiceFacade
from lpg.cli.commands import start, stop, status, config, key, rule, provider, log

@click.group()
@click.version_option(version="1.0.0")
@click.option('-c', '--config', 'config_path', help='配置文件路径')
@click.option('-v', '--verbose', is_flag=True, help='详细输出模式')
@click.option('-q', '--quiet', is_flag=True, help='静默模式')
@click.option('-j', '--json', 'json_output', is_flag=True, help='JSON 格式输出')
@click.pass_context
def cli(ctx, config_path, verbose, quiet, json_output):
    """LLM Privacy Gateway - 本地隐私保护代理"""
    ctx.ensure_object(dict)
    ctx.obj['facade'] = ServiceFacade(config_path)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['json_output'] = json_output

cli.add_command(start.start)
cli.add_command(stop.stop)
cli.add_command(status.status)
cli.add_command(config.config)
cli.add_command(key.key)
cli.add_command(rule.rule)
cli.add_command(provider.provider)
cli.add_command(log.log)
```

#### 3.1.3 命令设计 (start.py 示例)

```python
# commands/start.py
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('-p', '--port', default=8080, help='代理端口')
@click.option('-h', '--host', default='127.0.0.1', help='监听地址')
@click.option('-d', '--daemon', is_flag=True, help='后台运行模式')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warn', 'error']), 
              default='info', help='日志级别')
@click.option('--log-file', help='日志文件路径')
@click.pass_context
def start(ctx, port, host, daemon, log_level, log_file):
    """启动代理服务器"""
    facade = ctx.obj['facade']
    
    # 检查是否已运行
    if facade.is_running():
        console.print("[yellow]代理服务器已在运行[/yellow]")
        return
    
    # 启动服务
    try:
        facade.start_service(host=host, port=port, daemon=daemon, 
                            log_level=log_level, log_file=log_file)
        _print_startup_info(facade)
    except Exception as e:
        console.print(f"[red]启动失败: {e}[/red]")
        raise SystemExit(1)

def _print_startup_info(facade):
    """打印启动信息"""
    status = facade.get_status()
    console.print(f"""
[bold green]╔═══════════════════════════════════════════════════════════╗
║         LLM Privacy Gateway v1.0.0                        ║
║         Your AI Privacy Shield                            ║
╚═══════════════════════════════════════════════════════════╝[/bold green]

  ✓ Configuration loaded
  ✓ Rules loaded: {status['rules_count']} active rules
  ✓ Virtual keys loaded: {status['keys_count']} active keys

  ┌─────────────────────────────────────────────────────────────┐
  │  Proxy Server Running                                       │
  │  ─────────────────────────────────────────────────────────  │
  │  Address:     http://{status['host']}:{status['port']}                        
  │  PID:         {status['pid']}                                         
  └─────────────────────────────────────────────────────────────┘

  Press Ctrl+C to stop
""")
```

### 3.2 核心服务层 (core/)

#### 3.2.1 目录结构

```
core/
├── __init__.py
├── service_facade.py    # 服务门面（统一入口）
├── proxy/
│   ├── __init__.py
│   ├── server.py        # HTTP 代理服务器
│   ├── handler.py       # 请求处理器
│   ├── stream.py        # SSE 流式处理
│   └── models.py        # 代理相关数据模型
├── key/
│   ├── __init__.py
│   ├── manager.py       # Key 管理器
│   ├── resolver.py      # Key 解析器
│   └── store.py         # Key 存储
├── rule/
│   ├── __init__.py
│   ├── manager.py       # 规则管理器
│   ├── loader.py        # 规则加载器
│   └── models.py        # 规则数据模型
├── presidio/
│   ├── __init__.py
│   ├── client.py        # Presidio HTTP 客户端
│   ├── analyzer.py      # 分析器封装
│   └── anonymizer.py    # 脱敏器封装
├── audit/
│   ├── __init__.py
│   ├── service.py       # 审计服务
│   └── models.py        # 审计数据模型
└── config/
    ├── __init__.py
    ├── service.py       # 配置服务
    └── models.py        # 配置数据模型
```

#### 3.2.2 服务门面设计 (service_facade.py)

服务门面是 CLI 命令与核心服务的统一接口，**确保后续版本扩展时 CLI 层代码最小改动**。

```python
# core/service_facade.py
from typing import Optional, Dict, Any, List
from lpg.core.config.service import ConfigService
from lpg.core.proxy.server import ProxyServer
from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.audit.service import AuditService
from lpg.core.presidio.client import PresidioClient

class ServiceFacade:
    """
    服务门面 - 统一服务入口
    
    设计原则:
    1. CLI 命令通过门面访问核心服务
    2. 门面隐藏服务间依赖关系
    3. 便于后续版本添加新服务（如订阅服务）
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self._config_service = ConfigService(config_path)
        self._presidio_client = PresidioClient(self._config_service)
        self._audit_service = AuditService(self._config_service)
        self._key_manager = KeyManager(self._config_service)
        self._rule_manager = RuleManager(self._config_service)
        self._proxy_server: Optional[ProxyServer] = None
    
    # ========== 代理服务 ==========
    
    def start_service(self, host: str = '127.0.0.1', port: int = 8080, 
                      daemon: bool = False, log_level: str = 'info',
                      log_file: Optional[str] = None) -> None:
        """启动代理服务"""
        self._proxy_server = ProxyServer(
            config_service=self._config_service,
            key_manager=self._key_manager,
            rule_manager=self._rule_manager,
            presidio_client=self._presidio_client,
            audit_service=self._audit_service
        )
        self._proxy_server.start(host=host, port=port, daemon=daemon,
                                 log_level=log_level, log_file=log_file)
    
    def stop_service(self, force: bool = False) -> None:
        """停止代理服务"""
        if self._proxy_server:
            self._proxy_server.stop(force=force)
    
    def is_running(self) -> bool:
        """检查服务是否运行"""
        return self._proxy_server is not None and self._proxy_server.is_running()
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            'running': self.is_running(),
            'host': self._config_service.get('proxy.host', '127.0.0.1'),
            'port': self._config_service.get('proxy.port', 8080),
            'pid': self._proxy_server.pid if self._proxy_server else None,
            'uptime': self._proxy_server.uptime if self._proxy_server else 0,
            'rules_count': self._rule_manager.count(),
            'keys_count': self._key_manager.count(),
            'stats': self._proxy_server.stats if self._proxy_server else {}
        }
    
    # ========== Key 管理 ==========
    
    def create_virtual_key(self, provider: str, name: str, 
                           expires_at: Optional[str] = None) -> Dict[str, Any]:
        """创建虚拟 Key"""
        return self._key_manager.create(provider=provider, name=name, 
                                        expires_at=expires_at)
    
    def list_virtual_keys(self) -> List[Dict[str, Any]]:
        """列出所有虚拟 Key"""
        return self._key_manager.list_all()
    
    def revoke_virtual_key(self, key_id: str) -> bool:
        """吊销虚拟 Key"""
        return self._key_manager.revoke(key_id)
    
    def get_key_info(self, key_id: str) -> Optional[Dict[str, Any]]:
        """获取 Key 详情"""
        return self._key_manager.get_info(key_id)
    
    # ========== 规则管理 ==========
    
    def list_rules(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出规则"""
        return self._rule_manager.list_all(category=category)
    
    def enable_rule(self, rule_id: str) -> bool:
        """启用规则"""
        return self._rule_manager.enable(rule_id)
    
    def disable_rule(self, rule_id: str) -> bool:
        """禁用规则"""
        return self._rule_manager.disable(rule_id)
    
    def import_rules(self, file_path: str) -> int:
        """导入规则文件"""
        return self._rule_manager.import_from_file(file_path)
    
    def test_rule(self, rule_config: Dict[str, Any], text: str) -> Dict[str, Any]:
        """测试规则"""
        return self._rule_manager.test_rule(rule_config, text)
    
    # ========== 配置管理 ==========
    
    def get_config(self, key: Optional[str] = None) -> Any:
        """获取配置"""
        return self._config_service.get(key)
    
    def set_config(self, key: str, value: Any) -> None:
        """设置配置"""
        self._config_service.set(key, value)
    
    def init_config(self, interactive: bool = True) -> None:
        """初始化配置"""
        self._config_service.init(interactive=interactive)
    
    # ========== 提供商管理 ==========
    
    def list_providers(self) -> List[Dict[str, Any]]:
        """列出提供商"""
        return self._config_service.get_providers()
    
    def add_provider(self, provider_type: str, name: str, **kwargs) -> Dict[str, Any]:
        """添加提供商"""
        return self._config_service.add_provider(provider_type, name, **kwargs)
    
    def test_provider(self, name: str) -> bool:
        """测试提供商连接"""
        provider = self._config_service.get_provider(name)
        if not provider:
            return False
        return self._presidio_client.test_connection(provider)
    
    # ========== 日志管理 ==========
    
    def get_logs(self, lines: int = 50, level: Optional[str] = None,
                 since: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取日志"""
        return self._audit_service.get_logs(lines=lines, level=level, since=since)
    
    def get_log_stats(self, since: Optional[str] = None) -> Dict[str, Any]:
        """获取日志统计"""
        return self._audit_service.get_stats(since=since)
    
    def export_logs(self, output_path: str, since: Optional[str] = None) -> int:
        """导出日志"""
        return self._audit_service.export(output_path, since=since)
```

#### 3.2.3 代理服务器设计 (proxy/server.py)

```python
# core/proxy/server.py
import asyncio
from typing import Optional, Dict, Any
from aiohttp import web
import logging

from lpg.core.config.service import ConfigService
from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.presidio.client import PresidioClient
from lpg.core.audit.service import AuditService
from lpg.core.proxy.handler import RequestHandler

logger = logging.getLogger(__name__)

class ProxyServer:
    """
    HTTP 代理服务器
    
    职责:
    1. 监听本地端口，接收 API 请求
    2. 委托 RequestHandler 处理请求
    3. 管理服务器生命周期
    """
    
    def __init__(self, config_service: ConfigService, key_manager: KeyManager,
                 rule_manager: RuleManager, presidio_client: PresidioClient,
                 audit_service: AuditService):
        self._config = config_service
        self._handler = RequestHandler(
            key_manager=key_manager,
            rule_manager=rule_manager,
            presidio_client=presidio_client,
            audit_service=audit_service,
            config_service=config_service
        )
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._pid: Optional[int] = None
        self._start_time: Optional[float] = None
        self._stats = {
            'total_requests': 0,
            'success_requests': 0,
            'failed_requests': 0,
            'pii_detected': 0,
            'total_latency_ms': 0
        }
    
    @property
    def pid(self) -> Optional[int]:
        return self._pid
    
    @property
    def uptime(self) -> float:
        if self._start_time:
            import time
            return time.time() - self._start_time
        return 0
    
    @property
    def stats(self) -> Dict[str, Any]:
        return self._stats.copy()
    
    def is_running(self) -> bool:
        return self._runner is not None and self._runner.server is not None
    
    async def start_async(self, host: str = '127.0.0.1', port: int = 8080,
                          log_level: str = 'info', log_file: Optional[str] = None):
        """异步启动服务器"""
        import os
        import time
        
        self._app = web.Application()
        self._setup_routes()
        
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        
        site = web.TCPSite(self._runner, host, port)
        await site.start()
        
        self._pid = os.getpid()
        self._start_time = time.time()
        
        logger.info(f"Proxy server started at http://{host}:{port}")
    
    def start(self, host: str = '127.0.0.1', port: int = 8080, 
              daemon: bool = False, log_level: str = 'info',
              log_file: Optional[str] = None):
        """启动服务器（同步接口）"""
        if daemon:
            self._start_daemon(host, port, log_level, log_file)
        else:
            asyncio.run(self._run_forever(host, port, log_level, log_file))
    
    async def _run_forever(self, host: str, port: int, log_level: str, 
                           log_file: Optional[str]):
        """持续运行"""
        await self.start_async(host, port, log_level, log_file)
        try:
            await asyncio.Event().wait()  # 永久等待
        except KeyboardInterrupt:
            await self.stop_async()
    
    def _start_daemon(self, host: str, port: int, log_level: str, 
                      log_file: Optional[str]):
        """后台守护进程模式"""
        import subprocess
        import sys
        
        # 启动子进程
        cmd = [sys.executable, '-m', 'lpg', 'start', '-h', host, '-p', str(port)]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    async def stop_async(self, force: bool = False):
        """异步停止服务器"""
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
            logger.info("Proxy server stopped")
    
    def stop(self, force: bool = False):
        """停止服务器（同步接口）"""
        asyncio.run(self.stop_async(force))
    
    def _setup_routes(self):
        """设置路由"""
        # OpenAI API 兼容端点
        self._app.router.add_post('/v1/chat/completions', self._handle_request)
        self._app.router.add_post('/v1/completions', self._handle_request)
        self._app.router.add_post('/v1/embeddings', self._handle_request)
        
        # 通用端点（转发到配置的提供商）
        self._app.router.add_post('/{path:.*}', self._handle_request)
        self._app.router.add_get('/{path:.*}', self._handle_request)
        
        # 健康检查
        self._app.router.add_get('/health', self._handle_health)
    
    async def _handle_request(self, request: web.Request) -> web.Response:
        """处理 API 请求"""
        import time
        start_time = time.time()
        
        self._stats['total_requests'] += 1
        
        try:
            response = await self._handler.handle(request)
            self._stats['success_requests'] += 1
            return response
        except Exception as e:
            self._stats['failed_requests'] += 1
            logger.error(f"Request failed: {e}")
            return web.json_response(
                {'error': {'message': str(e), 'type': 'internal_error'}},
                status=500
            )
        finally:
            elapsed = (time.time() - start_time) * 1000
            self._stats['total_latency_ms'] += elapsed
    
    async def _handle_health(self, request: web.Request) -> web.Response:
        """健康检查端点"""
        return web.json_response({
            'status': 'ok',
            'version': '1.0.0',
            'uptime': self.uptime
        })
```

#### 3.2.4 请求处理器设计 (proxy/handler.py)

```python
# core/proxy/handler.py
import json
import logging
from typing import Dict, Any, List, Optional
from aiohttp import web
import time

from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.presidio.client import PresidioClient
from lpg.core.audit.service import AuditService
from lpg.core.config.service import ConfigService
from lpg.core.proxy.stream import StreamHandler

logger = logging.getLogger(__name__)

class RequestHandler:
    """
    请求处理器
    
    职责:
    1. 验证虚拟 Key
    2. 提取并检测 PII
    3. 执行脱敏处理
    4. 转发请求到 LLM API
    5. 处理响应（含流式响应）
    6. 记录审计日志
    """
    
    def __init__(self, key_manager: KeyManager, rule_manager: RuleManager,
                 presidio_client: PresidioClient, audit_service: AuditService,
                 config_service: ConfigService):
        self._key_manager = key_manager
        self._rule_manager = rule_manager
        self._presidio = presidio_client
        self._audit = audit_service
        self._config = config_service
        self._stream_handler = StreamHandler()
    
    async def handle(self, request: web.Request) -> web.Response:
        """处理请求主流程"""
        start_time = time.time()
        
        # Step 1: 验证虚拟 Key
        virtual_key = self._extract_api_key(request)
        if not virtual_key:
            return self._error_response(401, "Missing API key")
        
        key_mapping = self._key_manager.resolve(virtual_key)
        if not key_mapping:
            return self._error_response(401, "Invalid API key")
        
        # Step 2: 获取提供商配置
        provider = self._config.get_provider(key_mapping['provider'])
        if not provider:
            return self._error_response(500, "Provider not configured")
        
        # Step 3: 读取请求体
        body = await request.read()
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            return self._error_response(400, "Invalid JSON body")
        
        # Step 4: PII 检测与脱敏
        detection_results = []
        anonymized_data = request_data
        
        if self._should_process(request_data):
            messages = self._extract_messages(request_data)
            for msg in messages:
                content = msg.get('content', '')
                if content:
                    # 检测 PII
                    detections = await self._presidio.analyze(content)
                    if detections:
                        detection_results.extend(detections)
                        
                        # 脱敏处理
                        anonymized_content = await self._presidio.anonymize(
                            content, detections
                        )
                        msg['content'] = anonymized_content
            
            anonymized_data = request_data
        
        # Step 5: 转发请求
        target_url = self._build_target_url(provider, request.path)
        headers = self._build_headers(provider, key_mapping['real_key'], request.headers)
        
        is_stream = request_data.get('stream', False)
        
        if is_stream:
            # 流式响应
            return await self._handle_stream_response(
                target_url, headers, anonymized_data, start_time, detection_results
            )
        else:
            # 普通响应
            return await self._handle_normal_response(
                target_url, headers, anonymized_data, start_time, detection_results
            )
    
    def _extract_api_key(self, request: web.Request) -> Optional[str]:
        """从请求头提取 API Key"""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]
        return request.headers.get('x-api-key')
    
    def _should_process(self, request_data: Dict) -> bool:
        """判断是否需要进行 PII 处理"""
        # 仅处理包含 messages 的请求
        return 'messages' in request_data
    
    def _extract_messages(self, request_data: Dict) -> List[Dict]:
        """提取消息内容"""
        return request_data.get('messages', [])
    
    def _build_target_url(self, provider: Dict, path: str) -> str:
        """构建目标 URL"""
        base_url = provider.get('base_url', '').rstrip('/')
        return f"{base_url}{path}"
    
    def _build_headers(self, provider: Dict, real_key: str, 
                       original_headers: Dict) -> Dict:
        """构建请求头"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'LLM-Privacy-Gateway/1.0'
        }
        
        # 根据提供商类型设置认证头
        auth_type = provider.get('auth_type', 'bearer')
        if auth_type == 'bearer':
            headers['Authorization'] = f'Bearer {real_key}'
        elif auth_type == 'x-api-key':
            headers['x-api-key'] = real_key
        elif auth_type == 'api-key':
            headers['api-key'] = real_key
        
        return headers
    
    async def _handle_normal_response(self, url: str, headers: Dict,
                                       data: Dict, start_time: float,
                                       detections: List) -> web.Response:
        """处理普通响应"""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                response_data = await resp.json()
                
                # 记录审计日志
                self._audit.log_request(
                    url=url,
                    method='POST',
                    status=resp.status,
                    duration_ms=(time.time() - start_time) * 1000,
                    detections=detections
                )
                
                return web.json_response(response_data, status=resp.status)
    
    async def _handle_stream_response(self, url: str, headers: Dict,
                                       data: Dict, start_time: float,
                                       detections: List) -> web.StreamResponse:
        """处理流式响应（SSE）"""
        import aiohttp
        
        response = web.StreamResponse()
        response.headers['Content-Type'] = 'text/event-stream'
        response.headers['Cache-Control'] = 'no-cache'
        await response.prepare(self._current_request)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                async for chunk in resp.content:
                    await response.write(chunk)
        
        # 记录审计日志
        self._audit.log_request(
            url=url,
            method='POST',
            status=200,
            duration_ms=(time.time() - start_time) * 1000,
            detections=detections,
            is_stream=True
        )
        
        return response
    
    def _error_response(self, status: int, message: str) -> web.Response:
        """错误响应"""
        return web.json_response(
            {'error': {'message': message, 'type': 'invalid_request_error'}},
            status=status
        )
```

#### 3.2.5 Presidio 客户端设计 (presidio/client.py)

```python
# core/presidio/client.py
import aiohttp
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PresidioClient:
    """
    Presidio 服务客户端
    
    职责:
    1. 调用 presidio-analyzer 进行 PII 检测
    2. 调用 presidio-anonymizer 进行脱敏处理
    3. 管理服务连接和健康检查
    """
    
    def __init__(self, config_service):
        self._config = config_service
        self._base_url = config_service.get('presidio.endpoint', 'http://localhost:5001')
        self._language = config_service.get('presidio.language', 'zh')
        self._timeout = aiohttp.ClientTimeout(total=30)
    
    async def analyze(self, text: str, 
                      language: Optional[str] = None,
                      entities: Optional[List[str]] = None,
                      score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        调用 Presidio Analyzer 检测 PII
        
        Args:
            text: 待检测文本
            language: 语言代码（默认使用配置）
            entities: 指定检测的实体类型（None 表示全部）
            score_threshold: 置信度阈值
            
        Returns:
            检测结果列表 [{"entity_type": str, "start": int, "end": int, "score": float}]
        """
        url = f"{self._base_url}/analyze"
        
        payload = {
            "text": text,
            "language": language or self._language,
            "score_threshold": score_threshold
        }
        
        if entities:
            payload["entities"] = entities
        
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Analyzer failed: {resp.status}")
                        return []
        except Exception as e:
            logger.error(f"Analyzer error: {e}")
            return []
    
    async def anonymize(self, text: str, 
                        analyzer_results: List[Dict[str, Any]],
                        operators: Optional[Dict[str, Dict]] = None) -> str:
        """
        调用 Presidio Anonymizer 进行脱敏
        
        Args:
            text: 原始文本
            analyzer_results: Analyzer 返回的检测结果
            operators: 自定义脱敏操作符配置
            
        Returns:
            脱敏后的文本
        """
        url = f"{self._base_url}/anonymize"
        
        # 构建默认脱敏策略
        default_operators = self._get_default_operators()
        if operators:
            default_operators.update(operators)
        
        payload = {
            "text": text,
            "analyzer_results": analyzer_results,
            "operators": default_operators
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("text", text)
                    else:
                        logger.error(f"Anonymizer failed: {resp.status}")
                        return text
        except Exception as e:
            logger.error(f"Anonymizer error: {e}")
            return text
    
    async def decrypt(self, text: str, 
                      items: List[Dict[str, Any]],
                      key: str) -> str:
        """
        调用 Presidio 解密还原（用于响应处理）
        
        Args:
            text: 脱敏后的文本
            items: 脱敏项列表
            key: 解密密钥
            
        Returns:
            还原后的文本
        """
        url = f"{self._base_url}/decrypt"
        
        payload = {
            "text": text,
            "items": items,
            "key": key
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("text", text)
                    else:
                        return text
        except Exception as e:
            logger.error(f"Decrypt error: {e}")
            return text
    
    def _get_default_operators(self) -> Dict[str, Dict]:
        """获取默认脱敏策略"""
        return {
            "DEFAULT": {"type": "replace", "new_value": "<REDACTED>"},
            "EMAIL_ADDRESS": {"type": "mask", "masking_char": "*", 
                             "chars_to_mask": 4, "from_end": False},
            "PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"},
            "CREDIT_CARD": {"type": "mask", "masking_char": "*",
                           "chars_to_mask": 12, "from_end": False},
            "PERSON": {"type": "replace", "new_value": "<PERSON>"},
            "LOCATION": {"type": "replace", "new_value": "<LOCATION>"},
            "IP_ADDRESS": {"type": "replace", "new_value": "<IP>"},
            "URL": {"type": "mask", "masking_char": "*",
                    "chars_to_mask": 10, "from_end": False},
            # 中国特定实体
            "CN_PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"},
            "CN_ID_CARD": {"type": "replace", "new_value": "<ID_CARD>"},
            "CN_BANK_CARD": {"type": "replace", "new_value": "<BANK_CARD>"}
        }
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.get(f"{self._base_url}/health") as resp:
                    return resp.status == 200
        except:
            return False
```

#### 3.2.6 Key 管理器设计 (key/manager.py)

```python
# core/key/manager.py
import secrets
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json
import os

from lpg.core.config.service import ConfigService

class KeyManager:
    """
    虚拟 Key 管理器
    
    职责:
    1. 生成虚拟 Key
    2. 管理虚拟 Key 与真实 Key 的映射
    3. Key 的生命周期管理
    """
    
    KEY_PREFIX = "sk-virtual-"
    
    def __init__(self, config_service: ConfigService):
        self._config = config_service
        self._keys: Dict[str, Dict] = {}
        self._load_keys()
    
    def _load_keys(self):
        """从配置加载 Key"""
        keys_config = self._config.get('virtual_keys', [])
        for key_config in keys_config:
            self._keys[key_config['id']] = key_config
    
    def _save_keys(self):
        """保存 Key 到配置"""
        self._config.set('virtual_keys', list(self._keys.values()))
    
    def create(self, provider: str, name: str, 
               expires_at: Optional[str] = None,
               permissions: Optional[Dict] = None) -> Dict[str, Any]:
        """
        创建虚拟 Key
        
        Args:
            provider: 提供商名称
            name: Key 标识名称
            expires_at: 过期时间（ISO 格式）
            permissions: 权限配置
            
        Returns:
            创建的 Key 信息
        """
        # 验证提供商存在
        provider_config = self._config.get_provider(provider)
        if not provider_config:
            raise ValueError(f"Provider '{provider}' not found")
        
        # 生成虚拟 Key
        random_part = secrets.token_hex(24)
        virtual_key = f"{self.KEY_PREFIX}{random_part}"
        key_id = hashlib.sha256(virtual_key.encode()).hexdigest()[:16]
        
        # 创建 Key 记录
        key_record = {
            'id': f"vk_{key_id}",
            'virtual_key': virtual_key,
            'provider': provider,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at,
            'permissions': permissions or {},
            'usage_count': 0,
            'last_used': None
        }
        
        self._keys[key_record['id']] = key_record
        self._save_keys()
        
        return key_record
    
    def resolve(self, virtual_key: str) -> Optional[Dict[str, Any]]:
        """
        解析虚拟 Key，返回映射信息
        
        Args:
            virtual_key: 虚拟 Key 字符串
            
        Returns:
            映射信息 {"provider": str, "real_key": str} 或 None
        """
        for key_id, key_record in self._keys.items():
            if key_record['virtual_key'] == virtual_key:
                # 检查过期
                if self._is_expired(key_record):
                    return None
                
                # 获取真实 Key
                provider = key_record['provider']
                real_key = self._config.get_provider_key(provider)
                
                if not real_key:
                    return None
                
                # 更新使用统计
                key_record['usage_count'] += 1
                key_record['last_used'] = datetime.now().isoformat()
                self._save_keys()
                
                return {
                    'provider': provider,
                    'real_key': real_key,
                    'key_id': key_id
                }
        
        return None
    
    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有 Key"""
        return [
            {
                'id': k['id'],
                'name': k['name'],
                'provider': k['provider'],
                'virtual_key': k['virtual_key'],
                'created_at': k['created_at'],
                'expires_at': k.get('expires_at'),
                'usage_count': k.get('usage_count', 0),
                'last_used': k.get('last_used')
            }
            for k in self._keys.values()
        ]
    
    def get_info(self, key_id: str) -> Optional[Dict[str, Any]]:
        """获取 Key 详情"""
        return self._keys.get(key_id)
    
    def revoke(self, key_id: str) -> bool:
        """吊销 Key"""
        if key_id in self._keys:
            del self._keys[key_id]
            self._save_keys()
            return True
        return False
    
    def count(self) -> int:
        """获取有效 Key 数量"""
        return len([
            k for k in self._keys.values() 
            if not self._is_expired(k)
        ])
    
    def _is_expired(self, key_record: Dict) -> bool:
        """检查 Key 是否过期"""
        expires_at = key_record.get('expires_at')
        if not expires_at:
            return False
        return datetime.fromisoformat(expires_at) < datetime.now()
```

#### 3.2.7 规则管理器设计 (rule/manager.py)

```python
# core/rule/manager.py
import yaml
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RuleManager:
    """
    规则管理器
    
    职责:
    1. 加载和管理检测规则
    2. 规则的启用/禁用
    3. 自定义规则导入
    4. 规则测试
    """
    
    def __init__(self, config_service):
        self._config = config_service
        self._rules: Dict[str, Dict] = {}
        self._load_builtin_rules()
        self._load_custom_rules()
    
    def _load_builtin_rules(self):
        """加载内置规则"""
        rules_dir = Path(__file__).parent.parent.parent / 'rules'
        if rules_dir.exists():
            for rule_file in rules_dir.glob('*.yaml'):
                self._load_rule_file(rule_file)
    
    def _load_custom_rules(self):
        """加载自定义规则"""
        custom_dir = self._config.get('rules.custom_rules_dir')
        if custom_dir:
            custom_path = Path(custom_dir).expanduser()
            if custom_path.exists():
                for rule_file in custom_path.glob('*.yaml'):
                    self._load_rule_file(rule_file)
    
    def _load_rule_file(self, file_path: Path):
        """加载规则文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if 'rules' in data:
                for rule in data['rules']:
                    rule_id = rule.get('id')
                    if rule_id:
                        rule['enabled'] = rule.get('enabled', True)
                        rule['source'] = str(file_path)
                        self._rules[rule_id] = rule
                        
            logger.info(f"Loaded {len(data.get('rules', []))} rules from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load rules from {file_path}: {e}")
    
    def list_all(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出规则"""
        rules = list(self._rules.values())
        
        if category:
            rules = [r for r in rules if r.get('category') == category]
        
        return [
            {
                'id': r['id'],
                'name': r.get('name', r['id']),
                'category': r.get('category', 'uncategorized'),
                'type': r.get('type', 'regex'),
                'entity_type': r.get('entity_type'),
                'enabled': r.get('enabled', True),
                'description': r.get('description', '')
            }
            for r in rules
        ]
    
    def get_enabled_rules(self) -> List[Dict[str, Any]]:
        """获取启用的规则"""
        return [r for r in self._rules.values() if r.get('enabled', True)]
    
    def enable(self, rule_id: str) -> bool:
        """启用规则"""
        if rule_id in self._rules:
            self._rules[rule_id]['enabled'] = True
            return True
        return False
    
    def disable(self, rule_id: str) -> bool:
        """禁用规则"""
        if rule_id in self._rules:
            self._rules[rule_id]['enabled'] = False
            return True
        return False
    
    def import_from_file(self, file_path: str) -> int:
        """从文件导入规则"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Rule file not found: {file_path}")
        
        count_before = len(self._rules)
        self._load_rule_file(path)
        return len(self._rules) - count_before
    
    def test_rule(self, rule_config: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        测试规则
        
        Args:
            rule_config: 规则配置
            text: 测试文本
            
        Returns:
            测试结果 {"matches": [...], "count": int}
        """
        rule_type = rule_config.get('type', 'regex')
        matches = []
        
        if rule_type == 'regex':
            pattern = rule_config.get('pattern', '')
            if pattern:
                try:
                    regex = re.compile(pattern)
                    for match in regex.finditer(text):
                        matches.append({
                            'start': match.start(),
                            'end': match.end(),
                            'text': match.group()
                        })
                except re.error as e:
                    return {'error': f"Invalid regex: {e}"}
        
        elif rule_type == 'keyword':
            keywords = rule_config.get('keywords', [])
            for keyword in keywords:
                start = 0
                while True:
                    pos = text.find(keyword, start)
                    if pos == -1:
                        break
                    matches.append({
                        'start': pos,
                        'end': pos + len(keyword),
                        'text': keyword
                    })
                    start = pos + 1
        
        return {
            'matches': matches,
            'count': len(matches)
        }
    
    def count(self) -> int:
        """获取规则数量"""
        return len(self._rules)
```

#### 3.2.8 审计服务设计 (audit/service.py)

```python
# core/audit/service.py
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class AuditService:
    """
    审计服务
    
    职责:
    1. 记录请求处理日志
    2. 日志查询和统计
    3. 日志导出
    """
    
    def __init__(self, config_service):
        self._config = config_service
        self._log_file = self._get_log_file()
        self._ensure_log_dir()
    
    def _get_log_file(self) -> Path:
        """获取日志文件路径"""
        log_path = self._config.get('audit.log_file')
        if log_path:
            return Path(log_path).expanduser()
        
        # 默认路径
        home = Path.home()
        return home / '.llm-privacy-gateway' / 'logs' / 'audit.jsonl'
    
    def _ensure_log_dir(self):
        """确保日志目录存在"""
        self._log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_request(self, url: str, method: str, status: int,
                    duration_ms: float, detections: List[Dict],
                    is_stream: bool = False, error: Optional[str] = None):
        """
        记录请求日志
        
        Args:
            url: 请求 URL
            method: HTTP 方法
            status: 响应状态码
            duration_ms: 处理耗时（毫秒）
            detections: PII 检测结果
            is_stream: 是否流式响应
            error: 错误信息
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'method': method,
            'status': status,
            'duration_ms': round(duration_ms, 2),
            'detections': [
                {
                    'entity_type': d.get('entity_type'),
                    'score': d.get('score')
                }
                for d in detections
            ],
            'pii_count': len(detections),
            'is_stream': is_stream,
            'error': error
        }
        
        try:
            with open(self._log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    def get_logs(self, lines: int = 50, level: Optional[str] = None,
                 since: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取日志
        
        Args:
            lines: 返回行数
            level: 日志级别过滤（info/warn/error）
            since: 时间范围（1h/1d/1w）
        """
        if not self._log_file.exists():
            return []
        
        logs = []
        try:
            with open(self._log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        
                        # 时间过滤
                        if since and not self._match_time_filter(entry['timestamp'], since):
                            continue
                        
                        # 状态过滤（模拟 level）
                        if level:
                            if level == 'error' and entry.get('status', 200) < 400:
                                continue
                            if level == 'warn' and entry.get('status', 200) < 300:
                                continue
                        
                        logs.append(entry)
        except Exception as e:
            logger.error(f"Failed to read audit log: {e}")
        
        # 返回最新 N 条
        return logs[-lines:]
    
    def get_stats(self, since: Optional[str] = None) -> Dict[str, Any]:
        """
        获取统计信息
        
        Args:
            since: 时间范围（1h/1d/1w）
        """
        logs = self.get_logs(lines=10000, since=since)
        
        if not logs:
            return {
                'total_requests': 0,
                'success_requests': 0,
                'failed_requests': 0,
                'pii_detected': 0,
                'avg_duration_ms': 0
            }
        
        total = len(logs)
        success = len([l for l in logs if l.get('status', 200) < 400])
        failed = total - success
        pii_count = sum(l.get('pii_count', 0) for l in logs)
        total_duration = sum(l.get('duration_ms', 0) for l in logs)
        
        # PII 类型分布
        pii_types = {}
        for log in logs:
            for detection in log.get('detections', []):
                entity_type = detection.get('entity_type', 'unknown')
                pii_types[entity_type] = pii_types.get(entity_type, 0) + 1
        
        return {
            'total_requests': total,
            'success_requests': success,
            'failed_requests': failed,
            'pii_detected': pii_count,
            'avg_duration_ms': round(total_duration / total, 2) if total > 0 else 0,
            'pii_type_distribution': pii_types
        }
    
    def export(self, output_path: str, since: Optional[str] = None) -> int:
        """
        导出日志
        
        Args:
            output_path: 输出文件路径
            since: 时间范围
            
        Returns:
            导出的记录数
        """
        logs = self.get_logs(lines=100000, since=since)
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return len(logs)
    
    def _match_time_filter(self, timestamp: str, since: str) -> bool:
        """检查时间是否在范围内"""
        from datetime import timedelta
        
        try:
            log_time = datetime.fromisoformat(timestamp)
            now = datetime.now()
            
            if since == '1h':
                return now - log_time <= timedelta(hours=1)
            elif since == '1d':
                return now - log_time <= timedelta(days=1)
            elif since == '1w':
                return now - log_time <= timedelta(weeks=1)
            elif since == '1m':
                return now - log_time <= timedelta(days=30)
        except:
            pass
        
        return True
```

### 3.3 工具模块 (utils/)

#### 3.3.1 目录结构

```
utils/
├── __init__.py
├── crypto.py        # 加密工具
├── logging.py       # 日志配置
└── validators.py    # 验证工具
```

#### 3.3.2 加密工具设计 (crypto.py)

```python
# utils/crypto.py
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoUtils:
    """加密工具类"""
    
    @staticmethod
    def generate_key() -> str:
        """生成加密密钥"""
        return Fernet.generate_key().decode()
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """从密码派生密钥"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt(data: str, key: str) -> str:
        """加密数据"""
        f = Fernet(key.encode() if isinstance(key, str) else key)
        return f.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted: str, key: str) -> str:
        """解密数据"""
        f = Fernet(key.encode() if isinstance(key, str) else key)
        return f.decrypt(encrypted.encode()).decode()
```

---

## 4. 接口设计

### 4.1 Presidio 服务接口

#### 4.1.1 Analyzer 接口

**请求：**
```http
POST /analyze HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "text": "我的邮箱是 user@example.com，电话是 13812345678",
  "language": "zh",
  "score_threshold": 0.5,
  "entities": ["EMAIL_ADDRESS", "PHONE_NUMBER"]
}
```

**响应：**
```json
[
  {
    "entity_type": "EMAIL_ADDRESS",
    "start": 6,
    "end": 24,
    "score": 0.95
  },
  {
    "entity_type": "PHONE_NUMBER",
    "start": 29,
    "end": 40,
    "score": 0.9
  }
]
```

#### 4.1.2 Anonymizer 接口

**请求：**
```http
POST /anonymize HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "text": "我的邮箱是 user@example.com",
  "analyzer_results": [
    {"entity_type": "EMAIL_ADDRESS", "start": 6, "end": 24, "score": 0.95}
  ],
  "operators": {
    "EMAIL_ADDRESS": {"type": "mask", "masking_char": "*", "chars_to_mask": 4, "from_end": false}
  }
}
```

**响应：**
```json
{
  "text": "我的邮箱是 ****@example.com",
  "items": [
    {
      "operator": "mask",
      "entity_type": "EMAIL_ADDRESS",
      "start": 6,
      "end": 20,
      "original": "user@example.com"
    }
  ]
}
```

### 4.2 CLI 输出格式规范

#### 4.2.1 JSON 输出模式

所有命令支持 `-j/--json` 选项，输出结构化 JSON：

```json
{
  "status": "success",
  "data": { ... },
  "error": null
}
```

#### 4.2.2 表格输出格式

使用 Rich 库格式化表格输出：

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ ID           │ Name         │ Provider     │ Usage Count  │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ vk_abc123    │ vscode       │ openai       │ 42           │
│ vk_def456    │ cursor       │ openai       │ 18           │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 5. 数据模型设计

### 5.1 配置数据模型

```python
# models/config.py
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProxyConfig(BaseModel):
    """代理配置"""
    host: str = "127.0.0.1"
    port: int = 8080
    timeout: int = 60
    max_connections: int = 100

class PresidioConfig(BaseModel):
    """Presidio 配置"""
    enabled: bool = True
    endpoint: str = "http://localhost:5001"
    language: str = "zh"

class LogConfig(BaseModel):
    """日志配置"""
    level: str = "info"
    file: Optional[str] = None
    max_size: str = "100MB"
    max_files: int = 10
    format: str = "json"

class ProviderConfig(BaseModel):
    """LLM 提供商配置"""
    name: str
    type: str  # openai, anthropic, gemini, custom
    base_url: str
    auth_type: str = "bearer"
    api_key_file: Optional[str] = None
    timeout: int = 60

class VirtualKeyConfig(BaseModel):
    """虚拟 Key 配置"""
    id: str
    name: str
    provider: str
    virtual_key: str
    permissions: Dict[str, Any] = Field(default_factory=dict)
    expires_at: Optional[str] = None

class RulesConfig(BaseModel):
    """规则配置"""
    enabled_categories: List[str] = Field(default_factory=lambda: ["pii", "credentials"])
    custom_rules_dir: Optional[str] = None

class MaskingConfig(BaseModel):
    """脱敏配置"""
    default_strategy: str = "replace"
    enable_restoration: bool = True

class AuditConfig(BaseModel):
    """审计配置"""
    enabled: bool = True
    log_file: Optional[str] = None
    retention_days: int = 30

class GatewayConfig(BaseModel):
    """网关主配置"""
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    presidio: PresidioConfig = Field(default_factory=PresidioConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    providers: List[ProviderConfig] = Field(default_factory=list)
    virtual_keys: List[VirtualKeyConfig] = Field(default_factory=list)
    rules: RulesConfig = Field(default_factory=RulesConfig)
    masking: MaskingConfig = Field(default_factory=MaskingConfig)
    audit: AuditConfig = Field(default_factory=AuditConfig)
```

### 5.2 规则数据模型

```yaml
# rules/pii.yaml 示例
version: "1.0"
category: pii
rules:
  - id: email_detector
    name: 邮箱地址检测
    type: regex
    entity_type: EMAIL_ADDRESS
    pattern: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    strategy: mask
    masking_char: "*"
    chars_to_mask: 4
    description: 检测标准邮箱地址格式
    enabled: true
    
  - id: cn_phone_detector
    name: 中国手机号检测
    type: regex
    entity_type: CN_PHONE_NUMBER
    pattern: '1[3-9]\d{9}'
    strategy: replace
    replacement: "<PHONE>"
    description: 检测中国大陆手机号码
    enabled: true
```

### 5.3 审计日志模型

```json
{
  "timestamp": "2026-04-04T10:30:45.123456",
  "url": "https://api.openai.com/v1/chat/completions",
  "method": "POST",
  "status": 200,
  "duration_ms": 156.78,
  "detections": [
    {"entity_type": "EMAIL_ADDRESS", "score": 0.95},
    {"entity_type": "PHONE_NUMBER", "score": 0.9}
  ],
  "pii_count": 2,
  "is_stream": false,
  "error": null
}
```

---

## 6. 配置系统设计

### 6.1 配置文件结构

**全局配置：** `~/.llm-privacy-gateway/config.yaml`

```yaml
# LLM Privacy Gateway 配置文件 v1.0

# 代理服务器配置
proxy:
  host: 127.0.0.1
  port: 8080
  timeout: 60
  max_connections: 100

# Presidio 服务配置
presidio:
  enabled: true
  endpoint: http://localhost:5001
  language: zh

# 日志配置
log:
  level: info
  file: ~/.llm-privacy-gateway/logs/gateway.log
  max_size: 100MB
  max_files: 10
  format: json

# LLM 提供商配置
providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    auth_type: bearer
    api_key_file: ~/.llm-privacy-gateway/keys/openai.key
    timeout: 60

# 虚拟 Key 配置（自动生成）
virtual_keys: []

# 规则配置
rules:
  enabled_categories:
    - pii
    - credentials
  custom_rules_dir: ~/.llm-privacy-gateway/rules/

# 脱敏策略
masking:
  default_strategy: replace
  enable_restoration: true

# 审计配置
audit:
  enabled: true
  log_file: ~/.llm-privacy-gateway/logs/audit.jsonl
  retention_days: 30
```

### 6.2 配置优先级

```
1. 命令行参数（最高优先级）
2. 环境变量（LPG_ 前缀）
3. 本地配置（./.lpg/config.yaml）
4. 全局配置（~/.llm-privacy-gateway/config.yaml）
5. 默认值（最低优先级）
```

### 6.3 环境变量映射

| 环境变量 | 配置项 | 说明 |
|----------|--------|------|
| `LPG_PROXY_HOST` | proxy.host | 代理监听地址 |
| `LPG_PROXY_PORT` | proxy.port | 代理监听端口 |
| `LPG_PRESIDIO_ENDPOINT` | presidio.endpoint | Presidio 服务地址 |
| `LPG_LOG_LEVEL` | log.level | 日志级别 |
| `LPG_CONFIG_PATH` | - | 配置文件路径 |

---

## 7. 扩展性设计

### 7.1 为后续版本预留的扩展点

#### 7.1.1 服务门面扩展

```python
# core/service_facade.py - 预留扩展点

class ServiceFacade:
    """服务门面 - v1.1+ 可扩展"""
    
    def __init__(self, config_path: Optional[str] = None):
        # v1.0 核心服务
        self._config_service = ConfigService(config_path)
        self._presidio_client = PresidioClient(self._config_service)
        self._audit_service = AuditService(self._config_service)
        self._key_manager = KeyManager(self._config_service)
        self._rule_manager = RuleManager(self._config_service)
        
        # v1.1+ 扩展服务（预留）
        # self._subscription_service = None  # 订阅服务
        # self._rule_sync_service = None     # 规则同步服务
        # self._update_service = None        # 更新服务
    
    # v1.1+ 扩展方法（预留接口）
    # def sync_rules(self) -> bool:
    #     """同步云端规则（v1.1+）"""
    #     pass
    # 
    # def check_subscription(self) -> Dict:
    #     """检查订阅状态（v1.1+）"""
    #     pass
```

#### 7.1.2 规则管理器扩展

```python
# core/rule/manager.py - 预留扩展点

class RuleManager:
    """规则管理器 - v1.1+ 可扩展"""
    
    def __init__(self, config_service):
        # v1.0 本地规则
        self._rules: Dict[str, Dict] = {}
        self._load_builtin_rules()
        self._load_custom_rules()
        
        # v1.1+ 云端规则（预留）
        # self._cloud_rules: Dict[str, Dict] = {}
        # self._subscription_tier = 'free'
    
    # v1.1+ 扩展方法（预留接口）
    # def sync_from_cloud(self, subscription_tier: str) -> int:
    #     """从云端同步规则（v1.1+）"""
    #     pass
    # 
    # def get_available_packages(self) -> List[Dict]:
    #     """获取可用规则包（v1.1+）"""
    #     pass
```

#### 7.1.3 CLI 命令扩展

```python
# cli/main.py - 预留扩展点

@click.group()
def cli():
    """LLM Privacy Gateway"""
    pass

# v1.0 命令
cli.add_command(start.start)
cli.add_command(stop.stop)
# ...

# v1.1+ 扩展命令（预留）
# cli.add_command(sync.sync)      # 规则同步命令
# cli.add_command(subscribe.sub)  # 订阅管理命令
# cli.add_command(update.update)  # 更新命令
```

### 7.2 插件化设计预留

```python
# core/plugins/ - v2.0+ 预留目录

class PluginInterface(ABC):
    """插件接口（v2.0+）"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self, context: Dict) -> None:
        pass
    
    @abstractmethod
    def process_request(self, request: Dict) -> Dict:
        pass
```

### 7.3 扩展兼容性清单

| 扩展点 | v1.0 实现 | v1.1+ 扩展 | 兼容性保证 |
|--------|-----------|------------|------------|
| 服务门面 | 核心服务 | 订阅/同步服务 | 接口稳定，增量添加 |
| 规则管理 | 本地规则 | 云端规则同步 | 本地规则优先，云端补充 |
| CLI 命令 | 基础命令 | 订阅/同步命令 | Click group 可扩展 |
| 配置系统 | YAML 配置 | 云端配置同步 | 配置合并策略 |
| 提供商 | 内置类型 | 自定义提供商 | 注册机制 |

---

## 8. 测试策略

### 8.1 测试分层

```
┌─────────────────────────────────────────────────────────────┐
│                      E2E 测试 (5%)                          │
│  - 完整请求流程测试                                          │
│  - CLI 命令集成测试                                          │
├─────────────────────────────────────────────────────────────┤
│                    集成测试 (15%)                            │
│  - 服务间交互测试                                            │
│  - Presidio 集成测试                                         │
│  - 配置加载测试                                              │
├─────────────────────────────────────────────────────────────┤
│                    单元测试 (80%)                            │
│  - 各模块独立功能测试                                        │
│  - 边界条件测试                                              │
│  - 错误处理测试                                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 测试目录结构

```
tests/
├── __init__.py
├── conftest.py              # pytest fixtures
├── unit/
│   ├── __init__.py
│   ├── test_key_manager.py
│   ├── test_rule_manager.py
│   ├── test_config_service.py
│   ├── test_audit_service.py
│   ├── test_crypto_utils.py
│   └── test_presidio_client.py
├── integration/
│   ├── __init__.py
│   ├── test_proxy_handler.py
│   ├── test_service_facade.py
│   └── test_cli_commands.py
└── e2e/
    ├── __init__.py
    └── test_full_workflow.py
```

### 8.3 关键测试用例

#### 8.3.1 单元测试示例

```python
# tests/unit/test_key_manager.py
import pytest
from lpg.core.key.manager import KeyManager

class TestKeyManager:
    
    def test_create_key(self, config_service):
        """测试创建虚拟 Key"""
        manager = KeyManager(config_service)
        result = manager.create(provider="openai", name="test")
        
        assert result['id'].startswith('vk_')
        assert result['virtual_key'].startswith('sk-virtual-')
        assert result['provider'] == 'openai'
        assert result['name'] == 'test'
    
    def test_resolve_key(self, config_service):
        """测试解析虚拟 Key"""
        manager = KeyManager(config_service)
        created = manager.create(provider="openai", name="test")
        
        resolved = manager.resolve(created['virtual_key'])
        assert resolved is not None
        assert resolved['provider'] == 'openai'
        assert resolved['real_key'] is not None
    
    def test_resolve_invalid_key(self, config_service):
        """测试解析无效 Key"""
        manager = KeyManager(config_service)
        resolved = manager.resolve("invalid-key")
        assert resolved is None
    
    def test_revoke_key(self, config_service):
        """测试吊销 Key"""
        manager = KeyManager(config_service)
        created = manager.create(provider="openai", name="test")
        
        assert manager.revoke(created['id']) is True
        assert manager.resolve(created['virtual_key']) is None
```

#### 8.3.2 集成测试示例

```python
# tests/integration/test_proxy_handler.py
import pytest
from aiohttp import web
from lpg.core.proxy.handler import RequestHandler

class TestRequestHandler:
    
    @pytest.fixture
    async def handler(self, config_service, key_manager, rule_manager,
                      presidio_client, audit_service):
        return RequestHandler(
            key_manager=key_manager,
            rule_manager=rule_manager,
            presidio_client=presidio_client,
            audit_service=audit_service,
            config_service=config_service
        )
    
    async def test_handle_request_without_key(self, handler):
        """测试无 Key 请求"""
        request = self._mock_request(headers={})
        response = await handler.handle(request)
        assert response.status == 401
    
    async def test_handle_request_with_valid_key(self, handler, key_manager):
        """测试有效 Key 请求"""
        key_info = key_manager.create(provider="openai", name="test")
        request = self._mock_request(
            headers={'Authorization': f'Bearer {key_info["virtual_key"]}'},
            body={'model': 'gpt-4', 'messages': [{'role': 'user', 'content': 'Hello'}]}
        )
        response = await handler.handle(request)
        assert response.status == 200
```

#### 8.3.3 E2E 测试示例

```python
# tests/e2e/test_full_workflow.py
import pytest
import subprocess
import requests
import time

class TestFullWorkflow:
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """启动和停止服务"""
        # 启动服务
        self.process = subprocess.Popen(
            ['lpg', 'start', '-p', '8081'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)  # 等待启动
        
        yield
        
        # 停止服务
        self.process.terminate()
        self.process.wait()
    
    def test_full_request_flow(self):
        """测试完整请求流程"""
        # 1. 创建虚拟 Key
        result = subprocess.run(
            ['lpg', 'key', 'create', '-p', 'openai', '-n', 'test', '-j'],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        
        # 2. 使用虚拟 Key 发送请求
        response = requests.post(
            'http://127.0.0.1:8081/v1/chat/completions',
            headers={'Authorization': 'Bearer sk-virtual-test'},
            json={
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': 'Hello'}]
            }
        )
        assert response.status_code == 200
    
    def test_pii_detection(self):
        """测试 PII 检测"""
        response = requests.post(
            'http://127.0.0.1:8081/v1/chat/completions',
            headers={'Authorization': 'Bearer sk-virtual-test'},
            json={
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': 'My email is test@example.com'}]
            }
        )
        # 验证请求被正确处理
        assert response.status_code == 200
```

### 8.4 测试运行命令

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行 E2E 测试
pytest tests/e2e/

# 生成覆盖率报告
pytest --cov=lpg --cov-report=html

# 运行特定测试文件
pytest tests/unit/test_key_manager.py

# 运行特定测试用例
pytest tests/unit/test_key_manager.py::TestKeyManager::test_create_key
```

---

## 9. 实现计划

### 9.1 开发阶段划分

```
Phase 1: 基础框架 (3天)
├── 项目结构搭建
├── 依赖配置 (pyproject.toml)
├── CLI 入口框架
├── 配置系统
└── 基础工具类

Phase 2: 核心服务 (5天)
├── Presidio 客户端
├── Key 管理器
├── 规则管理器
├── 审计服务
└── 服务门面

Phase 3: 代理服务 (4天)
├── HTTP 服务器
├── 请求处理器
├── SSE 流式处理
└── 错误处理

Phase 4: CLI 命令 (3天)
├── start/stop/status
├── config 命令
├── key 命令
├── rule 命令
├── provider 命令
└── log 命令

Phase 5: 测试与优化 (5天)
├── 单元测试
├── 集成测试
├── E2E 测试
├── 性能优化
└── 文档完善
```

### 9.2 实现优先级

| 优先级 | 模块 | 依赖 | 预计工时 |
|--------|------|------|----------|
| P0 | 配置系统 | 无 | 1天 |
| P0 | Presidio 客户端 | 配置系统 | 2天 |
| P0 | Key 管理器 | 配置系统 | 1天 |
| P0 | 代理服务器 | 所有核心服务 | 3天 |
| P1 | 规则管理器 | 配置系统 | 2天 |
| P1 | 审计服务 | 配置系统 | 1天 |
| P1 | CLI 命令 | 服务门面 | 3天 |
| P2 | 测试套件 | 所有模块 | 5天 |
| P2 | 文档 | 无 | 2天 |

### 9.3 里程碑

| 里程碑 | 交付物 | 验收标准 |
|--------|--------|----------|
| M1: 基础框架 | CLI 可运行，配置可加载 | `lpg --help` 正常输出 |
| M2: 核心服务 | Presidio 集成，Key 管理 | 单元测试通过 |
| M3: 代理服务 | HTTP 代理可转发请求 | 代理请求成功 |
| M4: 完整功能 | 所有 CLI 命令可用 | E2E 测试通过 |
| M5: 发布就绪 | 文档完整，测试覆盖 > 80% | 可发布 v1.0.0 |

---

## 10. 附录

### A. 项目结构

```
llm-privacy-gateway/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
│
├── src/
│   └── lpg/
│       ├── __init__.py
│       ├── __main__.py          # python -m lpg 入口
│       │
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py          # CLI 入口
│       │   ├── commands/
│       │   │   ├── __init__.py
│       │   │   ├── start.py
│       │   │   ├── stop.py
│       │   │   ├── status.py
│       │   │   ├── config.py
│       │   │   ├── key.py
│       │   │   ├── rule.py
│       │   │   ├── provider.py
│       │   │   └── log.py
│       │   └── utils/
│       │       ├── __init__.py
│       │       ├── output.py
│       │       └── interactive.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── service_facade.py
│       │   ├── proxy/
│       │   │   ├── __init__.py
│       │   │   ├── server.py
│       │   │   ├── handler.py
│       │   │   ├── stream.py
│       │   │   └── models.py
│       │   ├── key/
│       │   │   ├── __init__.py
│       │   │   ├── manager.py
│       │   │   ├── resolver.py
│       │   │   └── store.py
│       │   ├── rule/
│       │   │   ├── __init__.py
│       │   │   ├── manager.py
│       │   │   ├── loader.py
│       │   │   └── models.py
│       │   ├── presidio/
│       │   │   ├── __init__.py
│       │   │   ├── client.py
│       │   │   ├── analyzer.py
│       │   │   └── anonymizer.py
│       │   ├── audit/
│       │   │   ├── __init__.py
│       │   │   ├── service.py
│       │   │   └── models.py
│       │   └── config/
│       │       ├── __init__.py
│       │       ├── service.py
│       │       └── models.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── provider.py
│       │   ├── rule.py
│       │   └── audit.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── crypto.py
│           ├── logging.py
│           └── validators.py
│
├── rules/
│   ├── pii.yaml
│   ├── credentials.yaml
│   └── finance.yaml
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── install.sh
│   └── setup_presidio.sh
│
└── docs/
    ├── design/
    └── api/
```

### B. 依赖清单 (pyproject.toml)

```toml
[project]
name = "llm-privacy-gateway"
version = "1.0.0"
description = "Local privacy protection proxy for LLM APIs"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "LLM Privacy Gateway Team"}
]

dependencies = [
    "click>=8.1.0",
    "aiohttp>=3.9.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0",
    "rich>=13.0.0",
    "cryptography>=41.0.0",
    "loguru>=0.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[project.scripts]
lpg = "lpg.cli.main:cli"

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true
```

### C. 开发规范

1. **代码风格**：遵循 PEP 8，使用 Black 格式化
2. **类型注解**：所有公共接口必须有类型注解
3. **文档字符串**：所有模块、类、函数必须有 docstring
4. **测试覆盖**：核心模块测试覆盖率 > 80%
5. **提交规范**：使用 Conventional Commits 格式

### D. 参考文档

- [Presidio 官方文档](https://microsoft.github.io/presidio/)
- [Click 文档](https://click.palletsprojects.com/)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)

---

**文档结束**

如有疑问或建议，请联系设计团队。
