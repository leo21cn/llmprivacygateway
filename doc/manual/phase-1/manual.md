# LLM Privacy Gateway - 操作手册（Phase 1）

> **适用版本**：v1.0.0  
> **更新日期**：2026-04-12  
> **阅读对象**：初次接触本项目的新手用户、开发者、运维人员

---

## 目录

1. [产品简介](#1-产品简介)
2. [快速开始](#2-快速开始)
3. [安装与配置](#3-安装与配置)
4. [核心概念](#4-核心概念)
5. [命令行使用](#5-命令行使用)
6. [配置管理](#6-配置管理)
7. [虚拟 Key 管理](#7-虚拟-key-管理)
8. [规则管理](#8-规则管理)
9. [LLM 提供商管理](#9-llm-提供商管理)
10. [日志与审计](#10-日志与审计)
11. [服务运维](#11-服务运维)
12. [常见问题排查](#12-常见问题排查)
13. [进阶使用](#13-进阶使用)
14. [附录](#14-附录)

---

## 1. 产品简介

### 1.1 什么是 LLM Privacy Gateway？

LLM Privacy Gateway（简称 LPG）是一个**本地化的智能隐私保护代理服务器**。它在你的应用程序和 LLM API（如 OpenAI、Anthropic 等）之间充当中间层，自动检测并脱敏敏感信息（如邮箱、手机号、身份证号等），确保隐私数据不会泄露给第三方 LLM 服务。

### 1.2 核心功能

| 功能 | 说明 |
|------|------|
| **透明代理** | 应用无需修改代码，只需将 API 地址指向 LPG 即可 |
| **虚拟 Key 管理** | 用虚拟 Key 替代真实 API Key，安全可控 |
| **PII 检测与脱敏** | 基于微软 Presidio，自动识别并脱敏个人身份信息 |
| **规则管理** | 支持 YAML 定义检测规则，可按需启用/禁用 |
| **审计日志** | 记录每次请求的检测结果，支持查询和导出 |
| **多提供商支持** | 支持配置多个 LLM 提供商（OpenAI、Anthropic 等） |

### 1.3 工作原理

```
你的应用
    │
    │  请求: "我的邮箱是 test@example.com"
    │  Header: Authorization: Bearer sk-virtual-xxxxx
    ▼
┌─────────────────────────────┐
│  LLM Privacy Gateway (LPG)  │
│                             │
│  1. 验证虚拟 Key             │
│  2. 调用 Presidio 检测 PII   │
│  3. 脱敏处理                 │
│     "我的邮箱是 ****@example.com" │
│  4. 转发到真实 LLM API       │
│  5. 记录审计日志             │
└──────────────┬──────────────┘
               │  脱敏后的请求
               ▼
        LLM API (OpenAI 等)
```

### 1.4 技术架构

LPG 采用**四层架构**设计：

```
CLI 层 (src/lpg/cli/)     →  命令行交互
    ↓
Core 层 (src/lpg/core/)   →  核心业务逻辑
    ↓
Models 层 (src/lpg/models/) → 数据模型定义
    ↓
Utils 层 (src/lpg/utils/) →  通用工具函数
```

> **架构特点**：上层可调用下层，下层不依赖上层，确保代码清晰、可测试。

---

## 2. 快速开始

### 2.1 一行命令安装

```bash
# 克隆项目
git clone <repository-url>
cd llm-privacy-gateway

# 安装依赖
pip install -e .
```

### 2.2 三步启动服务

```bash
# 第 1 步：初始化配置（生成默认配置文件）
lpg config init

# 第 2 步：添加 LLM 提供商（以 OpenAI 为例）
lpg provider add -t openai -n openai -u https://api.openai.com

# 第 3 步：启动代理服务器
lpg start --daemon
```

### 2.3 测试服务

```bash
# 检查服务状态
lpg status

# 健康检查
curl http://127.0.0.1:8080/health
```

看到 `{"status": "ok"}` 即表示服务正常运行。

### 2.4 创建并使用虚拟 Key

```bash
# 创建虚拟 Key
lpg key create -p openai -n my-test-key

# 使用虚拟 Key 调用 API（替代真实 API Key）
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-virtual-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "我的邮箱是 test@example.com"}]
  }'
```

返回的响应中，敏感信息已被自动脱敏。

---

## 3. 安装与配置

### 3.1 环境要求

| 项目 | 要求 |
|------|------|
| **Python** | >= 3.10 |
| **操作系统** | macOS / Linux / Windows |
| **Presidio 服务** | 需要独立部署（参考微软 Presidio 文档） |

### 3.2 安装步骤

```bash
# 1. 确保 Python 版本 >= 3.10
python --version

# 2. 克隆项目
git clone <repository-url>
cd llm-privacy-gateway

# 3. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 4. 安装项目
pip install -e .

# 5. 安装开发依赖（可选，用于运行测试）
pip install -e ".[dev]"
```

### 3.3 部署 Presidio 服务

LPG 依赖微软 Presidio 服务进行 PII 检测。你需要单独部署 Presidio Analyzer 和 Anonymizer。

**使用 Docker 快速部署（推荐）：**

```bash
# 启动 Presidio Analyzer + Anonymizer
docker run -d -p 5001:3000 --name presidio mcr.microsoft.com/presidio-analyzer:latest
docker run -d -p 5002:3000 --name presidio-anonymizer mcr.microsoft.com/presidio-anonymizer:latest
```

**验证 Presidio 服务：**

```bash
curl http://localhost:5001/health
```

### 3.4 配置文件位置

| 环境 | 路径 |
|------|------|
| **默认配置路径** | `~/.llm-privacy-gateway/config.yaml` |
| **审计日志路径** | `~/.llm-privacy-gateway/logs/audit.jsonl` |
| **规则文件路径** | `<项目根目录>/rules/` |

> **提示**：首次运行 `lpg config init` 会自动创建配置文件。

---

## 4. 核心概念

### 4.1 虚拟 Key

**什么是虚拟 Key？**

虚拟 Key 是 LPG 生成的一串随机字符串，格式为 `sk-virtual-<48位随机字符>`。它替代真实的 LLM API Key，应用使用虚拟 Key 发起请求，LPG 在代理层将其映射回真实 Key。

**为什么要用虚拟 Key？**

- **安全**：真实 Key 不暴露在应用中
- **可控**：可随时吊销，不影响真实 Key
- **可追踪**：每次使用都记录统计信息
- **可过期**：支持设置过期时间

**虚拟 Key 的生命周期：**

```
创建 → 使用（统计次数/最后使用时间） → 过期/吊销 → 失效
```

### 4.2 PII（个人身份信息）

PII（Personally Identifiable Information）指能识别个人身份的信息，例如：

| 类型 | 示例 | 脱敏效果 |
|------|------|----------|
| 邮箱 | `test@example.com` | `****@example.com` |
| 手机号 | `13812345678` | `<PHONE>` |
| 身份证号 | `110101199001011234` | `<ID_CARD>` |
| 信用卡号 | `4111111111111111` | `************1111` |
| IP 地址 | `192.168.1.100` | `<IP>` |

### 4.3 检测规则

规则定义了"如何检测敏感信息"以及"如何脱敏"。每条规则包含：

| 字段 | 说明 | 示例 |
|------|------|------|
| `id` | 规则唯一标识 | `email_detector` |
| `name` | 规则名称 | 邮箱地址检测 |
| `type` | 检测类型 | `regex`, `keyword` |
| `entity_type` | 实体类型 | `EMAIL_ADDRESS` |
| `pattern` | 匹配模式 | 正则表达式 |
| `strategy` | 脱敏策略 | `mask`, `replace` |
| `enabled` | 是否启用 | `true` / `false` |

### 4.4 LLM 提供商

提供商指你使用的 LLM 服务（如 OpenAI、Anthropic 等）。LPG 支持配置多个提供商，每个提供商有独立的：

- **base_url**：API 地址
- **auth_type**：认证方式（bearer、x-api-key 等）
- **api_key_file**：真实 API Key 的存储文件路径

---

## 5. 命令行使用

### 5.1 全局选项

所有命令支持以下全局选项：

```bash
lpg [OPTIONS] COMMAND [ARGS]...

全局选项：
  --config PATH    指定配置文件路径（默认：~/.llm-privacy-gateway/config.yaml）
  --verbose, -v    启用详细输出
  --quiet, -q      仅输出错误信息
  --json, -j       以 JSON 格式输出结果
  --help           显示帮助信息
```

**示例：**

```bash
# 使用自定义配置文件
lpg --config /path/to/config.yaml status

# JSON 格式输出
lpg --json key list

# 详细模式
lpg -v start
```

### 5.2 命令速查表

| 命令 | 用途 | 常用选项 |
|------|------|----------|
| `lpg start` | 启动代理服务器 | `-p`, `-h`, `-d`, `--log-level` |
| `lpg stop` | 停止代理服务器 | `-f` |
| `lpg status` | 查看服务状态 | `-j` |
| `lpg config init` | 初始化配置 | - |
| `lpg config show` | 显示全部配置 | - |
| `lpg config get <key>` | 获取单个配置项 | - |
| `lpg config set <key> <value>` | 设置配置项 | - |
| `lpg key list` | 列出虚拟 Key | `-j` |
| `lpg key create` | 创建虚拟 Key | `-p`, `-n`, `-e` |
| `lpg key revoke <key_id>` | 吊销虚拟 Key | - |
| `lpg rule list` | 列出检测规则 | `-c`, `-j` |
| `lpg rule enable <rule_id>` | 启用规则 | - |
| `lpg rule disable <rule_id>` | 禁用规则 | - |
| `lpg provider list` | 列出 LLM 提供商 | `-j` |
| `lpg provider add` | 添加 LLM 提供商 | `-t`, `-n`, `-u`, `-k` |
| `lpg log show` | 显示审计日志 | `-n`, `--since`, `-j` |
| `lpg log stats` | 日志统计 | `--since` |

---

## 6. 配置管理

### 6.1 初始化配置

```bash
# 交互式初始化（推荐新手）
lpg config init

# 非交互式初始化（使用默认值）
lpg config init --non-interactive
```

执行后会在 `~/.llm-privacy-gateway/` 目录下生成 `config.yaml` 文件。

### 6.2 查看配置

```bash
# 显示全部配置
lpg config show

# JSON 格式显示
lpg config show --json

# 获取单个配置项
lpg config get proxy.host
lpg config get proxy.port
lpg config get presidio.endpoint
```

**输出示例：**

```
proxy.host = 127.0.0.1
proxy.port = 8080
presidio.endpoint = http://localhost:5001
presidio.language = zh
presidio.timeout = 30
```

### 6.3 修改配置

```bash
# 修改代理端口（配置项使用点号分隔）
lpg config set proxy.port 9000

# 修改 Presidio 端点
lpg config set presidio.endpoint http://presidio.example.com:5001

# 启用审计日志
lpg config set audit.enabled true
lpg config set audit.log_file ~/.llm-privacy-gateway/logs/audit.jsonl
```

### 6.4 配置文件结构

```yaml
# ~/.llm-privacy-gateway/config.yaml

proxy:
  host: "127.0.0.1"
  port: 8080
  timeout: 60
  max_connections: 100

presidio:
  enabled: true
  endpoint: "http://localhost:5001"
  language: "zh"
  timeout: 30

log:
  level: "info"
  file: null
  max_size: "100MB"
  max_files: 10
  format: "json"

providers:
  - name: "openai"
    type: "openai"
    base_url: "https://api.openai.com"
    auth_type: "bearer"
    timeout: 60

virtual_keys: {}  # 由 lpg key create 自动管理

rules:
  enabled_categories:
    - pii
    - credentials
  custom_rules_dir: null

masking:
  default_strategy: "replace"
  enable_restoration: true

audit:
  enabled: true
  log_file: "~/.llm-privacy-gateway/logs/audit.jsonl"
  retention_days: 30
```

---

## 7. 虚拟 Key 管理

### 7.1 创建虚拟 Key

```bash
# 最简用法（必填参数）
lpg key create -p openai -n my-app-key

# 带过期时间
lpg key create -p openai -n temp-key -e 2026-12-31T23:59:59

# JSON 格式输出（方便程序解析）
lpg key create -p openai -n my-app-key --json
```

**输出示例：**

```
✓ Virtual Key created successfully

  Key ID:       vk_a1b2c3d4e5f6g7h8
  Virtual Key:  sk-virtual-4f8a2c9d1e7b3a6f5c8d2e9b4a7c1f3d6e8b5a2c9d4f7e1b
  Provider:     openai
  Name:         my-app-key
  Created At:   2026-04-12T10:30:00
  Expires At:   2026-12-31T23:59:59
```

> **⚠️ 重要**：虚拟 Key 只在创建时显示一次，请立即保存！

### 7.2 查看虚拟 Key 列表

```bash
# 列表形式（默认）
lpg key list

# JSON 格式
lpg key list --json
```

**输出示例：**

```
Virtual Keys (3 total)

Key ID                      Provider   Name           Created             Expires              Usage
──────────────────────────  ─────────  ─────────────  ──────────────────  ───────────────────  ─────
vk_a1b2c3d4e5f6g7h8         openai     my-app-key     2026-04-12 10:30    2026-12-31 23:59     152
vk_b2c3d4e5f6g7h8i9         openai     test-key       2026-04-10 14:20    -                    45
vk_c3d4e5f6g7h8i9j0         anthropic  prod-key       2026-04-01 09:00    2026-06-01 00:00     1023
```

### 7.3 查看 Key 详情

```bash
lpg key info vk_a1b2c3d4e5f6g7h8
```

### 7.4 吊销虚拟 Key

```bash
lpg key revoke vk_a1b2c3d4e5f6g7h8
```

吊销后该 Key 立即失效，应用再次使用该 Key 请求会被拒绝。

**验证吊销：**

```bash
lpg key list
# 被吊销的 Key 不再显示在列表中
```

### 7.5 虚拟 Key 使用场景

**场景 1：多应用隔离**

为每个应用创建独立的虚拟 Key，某个 Key 泄露不影响其他应用。

```bash
lpg key create -p openai -n web-app
lpg key create -p openai -n mobile-app
lpg key create -p openai -n internal-tool
```

**场景 2：临时访问权限**

为外包团队创建有过期时间的 Key。

```bash
lpg key create -p openai -n contractor-access -e 2026-05-01T00:00:00
```

---

## 8. 规则管理

### 8.1 查看规则列表

```bash
# 列出所有规则
lpg rule list

# 按分类查看
lpg rule list -c pii              # 仅查看 PII 检测规则
lpg rule list -c credentials      # 仅查看凭证检测规则

# JSON 格式输出
lpg rule list --json
```

**输出示例：**

```
Detection Rules (10 total)

Rule ID                     Category     Name                Type     Status
──────────────────────────  ───────────  ──────────────────  ───────  ──────
email_detector              pii          邮箱地址检测        regex    ✓
cn_phone_detector           pii          中国手机号检测      regex    ✓
cn_id_card_detector         pii          中国身份证号检测    regex    ✓
credit_card_detector        pii          信用卡号检测        regex    ✓
ip_address_detector         pii          IPv4 地址检测       regex    ✓
api_key_detector            credentials  API Key 检测        regex    ✓
password_detector           credentials  密码检测            keyword  ✓
token_detector              credentials  Token 检测          regex    ✓
secret_detector             credentials  Secret 检测         regex    ✓
custom_rule_001             custom       自定义规则          regex    ✗
```

### 8.2 启用/禁用规则

```bash
# 禁用某条规则（不再检测该类型 PII）
lpg rule disable ip_address_detector

# 重新启用
lpg rule enable ip_address_detector
```

### 8.3 规则文件结构

规则文件位于 `<项目根目录>/rules/` 目录：

**`rules/pii.yaml`** - PII 检测规则：

```yaml
version: "1.0"
category: pii
description: "个人身份信息检测规则"
rules:
  - id: email_detector
    name: 邮箱地址检测
    type: regex
    entity_type: EMAIL_ADDRESS
    pattern: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    strategy: mask
    enabled: true

  - id: cn_phone_detector
    name: 中国手机号检测
    type: regex
    entity_type: CN_PHONE_NUMBER
    pattern: '1[3-9]\d{9}'
    strategy: replace
    replacement: "<PHONE>"
    enabled: true
```

**`rules/credentials.yaml`** - 凭证检测规则：

```yaml
version: "1.0"
category: credentials
description: "凭证检测规则"
rules:
  - id: api_key_detector
    name: API Key 检测
    type: regex
    entity_type: API_KEY
    pattern: 'sk-[a-zA-Z0-9]{32,}'
    strategy: replace
    replacement: "<API_KEY>"
    enabled: true
```

### 8.4 自定义规则

你可以创建自己的规则文件并放置在 `rules/` 目录下：

```yaml
# rules/custom.yaml
version: "1.0"
category: custom
description: "自定义检测规则"
rules:
  - id: internal_project_code
    name: 内部项目代号检测
    type: regex
    entity_type: PROJECT_CODE
    pattern: 'PRJ-[A-Z]{3}-\d{4}'
    strategy: replace
    replacement: "<PROJECT_CODE>"
    enabled: true
```

然后在配置中启用自定义规则目录：

```bash
lpg config set rules.custom_rules_dir /path/to/rules
```

---

## 9. LLM 提供商管理

### 9.1 查看已配置的提供商

```bash
lpg provider list

# JSON 格式
lpg provider list --json
```

**输出示例：**

```
LLM Providers (2 configured)

Name         Type        Base URL                        Auth Type    Timeout
───────────  ──────────  ──────────────────────────────  ───────────  ────────
openai       openai      https://api.openai.com          bearer       60
anthropic    anthropic   https://api.anthropic.com       x-api-key    60
```

### 9.2 添加提供商

```bash
# 添加 OpenAI
lpg provider add -t openai -n openai -u https://api.openai.com

# 添加 Anthropic
lpg provider add -t anthropic -n anthropic -u https://api.anthropic.com

# 指定 API Key 文件（安全做法，避免 Key 明文出现在配置中）
lpg provider add -t openai -n openai -u https://api.openai.com -k ~/.llm-privacy-gateway/keys/openai.key
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `-t, --type` | 是 | 提供商类型（openai、anthropic 等） |
| `-n, --name` | 是 | 提供商名称（唯一标识） |
| `-u, --base-url` | 是 | API 基础 URL |
| `-k, --api-key-file` | 否 | API Key 文件路径 |

### 9.3 API Key 文件格式

API Key 文件仅包含一行文本（真实 Key）：

```bash
# 创建 Key 文件
echo "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > ~/.llm-privacy-gateway/keys/openai.key

# 设置权限（仅当前用户可读）
chmod 600 ~/.llm-privacy-gateway/keys/openai.key
```

### 9.4 多提供商路由

LPG 根据虚拟 Key 创建时指定的提供商，自动路由到对应的 LLM API。

```bash
# 创建指向 OpenAI 的 Key
lpg key create -p openai -n openai-key

# 创建指向 Anthropic 的 Key
lpg key create -p anthropic -n anthropic-key
```

---

## 10. 日志与审计

### 10.1 查看审计日志

```bash
# 显示最近 20 条日志
lpg log show

# 显示最近 50 条
lpg log show -n 50

# JSON 格式输出
lpg log show --json
```

**输出示例：**

```
Audit Logs (20 entries)

Timestamp              Method   URL                      Status   PII   Duration
─────────────────────  ───────  ───────────────────────  ───────  ────  ────────
2026-04-12 10:30:00    POST     /v1/chat/completions     200      1     152ms
2026-04-12 10:29:45    POST     /v1/chat/completions     200      0     98ms
2026-04-12 10:29:30    POST     /v1/completions          200      2     210ms
```

### 10.2 按时间过滤

```bash
# 最近 1 小时
lpg log show --since 1h

# 最近 1 天
lpg log show --since 1d

# 最近 1 周
lpg log show --since 1w

# 最近 1 个月
lpg log show --since 1m
```

### 10.3 日志统计

```bash
# 总体统计
lpg log stats

# 最近 1 小时统计
lpg log stats --since 1h
```

**输出示例：**

```
Audit Log Statistics

  Total Requests:        1,234
  Successful Requests:   1,200 (97.2%)
  Failed Requests:       34 (2.8%)
  PII Detected:          456 (37.0%)
  Average Latency:       145ms
  Stream Requests:       89
```

### 10.4 日志文件格式

审计日志以 JSONL（JSON Lines）格式存储：

```bash
# 直接查看日志文件
cat ~/.llm-privacy-gateway/logs/audit.jsonl
```

每行一条 JSON 记录：

```json
{
  "timestamp": "2026-04-12T10:30:00",
  "url": "/v1/chat/completions",
  "method": "POST",
  "status": 200,
  "duration_ms": 150.5,
  "detections": [
    {"entity_type": "EMAIL_ADDRESS", "start": 6, "end": 24, "score": 0.95}
  ],
  "pii_count": 1,
  "is_stream": false,
  "error": null
}
```

---

## 11. 服务运维

### 11.1 启动服务

```bash
# 后台运行（推荐）
lpg start --daemon

# 前台运行（调试用，Ctrl+C 停止）
lpg start

# 指定端口
lpg start -p 9000

# 指定地址和端口
lpg start -h 0.0.0.0 -p 9000

# 详细日志
lpg start --log-level debug

# 指定日志文件
lpg start --log-file /var/log/lpg.log
```

**启动参数说明：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-p, --port` | 8080 | 监听端口 |
| `-h, --host` | 127.0.0.1 | 监听地址 |
| `-d, --daemon` | false | 后台运行 |
| `--log-level` | info | 日志级别（debug/info/warning/error） |
| `--log-file` | null | 日志文件路径 |

### 11.2 停止服务

```bash
# 正常停止（等待当前请求完成）
lpg stop

# 强制停止（立即终止）
lpg stop --force
```

### 11.3 查看服务状态

```bash
lpg status

# JSON 格式
lpg status --json
```

**输出示例：**

```
Service Status

  Status:          Running
  PID:             12345
  Host:            127.0.0.1
  Port:            8080
  Uptime:          2h 15m 30s
  Total Requests:  1,234
  PII Detected:    456
```

### 11.4 健康检查

```bash
# 使用 CLI
lpg status

# 使用 HTTP 接口
curl http://127.0.0.1:8080/health
```

**响应示例：**

```json
{"status": "ok", "version": "1.0.0"}
```

---

## 12. 常见问题排查

### 12.1 服务无法启动

**症状：** `lpg start` 报错

**可能原因及解决方案：**

| 问题 | 排查方法 | 解决方案 |
|------|----------|----------|
| 端口被占用 | `lsof -i :8080` | 更换端口：`lpg start -p 9000` |
| 配置文件不存在 | `lpg config show` | 运行 `lpg config init` |
| Presidio 服务未启动 | `curl http://localhost:5001/health` | 启动 Presidio Docker |
| 权限不足 | 检查错误信息 | 使用 `sudo` 或修改文件权限 |

### 12.2 虚拟 Key 无法使用

**症状：** 应用使用虚拟 Key 请求被拒

**排查步骤：**

```bash
# 1. 确认 Key 存在且未过期
lpg key list

# 2. 查看 Key 详情
lpg key info <key_id>

# 3. 检查审计日志
lpg log show --since 1h

# 4. 检查请求头格式
# 正确格式：
# Authorization: Bearer sk-virtual-xxxxx
# 或
# x-api-key: sk-virtual-xxxxx
```

### 12.3 PII 未检测到

**症状：** 请求中包含敏感信息，但未被脱敏

**排查步骤：**

```bash
# 1. 确认 Presidio 服务正常
curl http://localhost:5001/health

# 2. 确认规则已启用
lpg rule list

# 3. 测试规则
# 手动调用 Presidio 测试
curl -X POST http://localhost:5001/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "我的邮箱是 test@example.com", "language": "zh"}'

# 4. 检查配置中的 Presidio 端点
lpg config get presidio.endpoint
```

### 12.4 请求延迟高

**症状：** 响应时间明显增加

**排查方法：**

```bash
# 查看平均延迟
lpg log stats

# 查看最近请求延迟
lpg log show -n 50
```

**可能原因：**

| 原因 | 解决方案 |
|------|----------|
| Presidio 服务响应慢 | 增加 Presidio 资源或优化网络 |
| 网络延迟 | 检查 LPG 与 Presidio/LLM API 的网络连接 |
| 日志写入慢 | 检查磁盘 I/O |

### 12.5 日志文件过大

**解决方案：**

```bash
# 查看日志文件大小
ls -lh ~/.llm-privacy-gateway/logs/audit.jsonl

# 手动清理（保留最近 7 天）
# 建议配置自动轮转
lpg config set audit.retention_days 7
```

---

## 13. 进阶使用

### 13.1 自定义脱敏策略

LPG 支持多种脱敏策略：

| 策略 | 说明 | 效果 |
|------|------|------|
| `mask` | 掩码（保留部分字符） | `****@email.com` |
| `replace` | 完全替换 | `<EMAIL_ADDRESS>` |
| `redact` | 删除（替换为空） | `` |
| `hash` | 哈希化 | `a1b2c3d4...` |

在规则文件中指定策略：

```yaml
rules:
  - id: email_detector
    strategy: mask
    mask_chars: 4  # 保留前 4 位
```

### 13.2 流式响应支持

LPG 完全支持 OpenAI 的 SSE 流式响应（`stream: true`）。

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-virtual-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": true
  }'
```

PII 检测与脱敏在流式响应中同样生效。

### 13.3 多环境配置

使用环境变量覆盖配置文件中的值：

```bash
# 临时修改端口
LPG_PROXY_PORT=9000 lpg start

# 临时修改 Presidio 端点
LPG_PRESIDIO_ENDPOINT=http://presidio.prod:5001 lpg start
```

> **环境变量命名规则**：`LPG_<配置路径大写，点号变下划线>`

### 13.4 API Key 加密存储

对于生产环境，建议加密存储 API Key：

```bash
# 使用 Python 加密 Key
python -c "
from lpg.utils.crypto import CryptoUtils
key = 'sk-your-real-api-key'
encrypted = CryptoUtils.encrypt(key, 'your-password')
print(encrypted)
" > ~/.llm-privacy-gateway/keys/openai.encrypted
```

### 13.5 与现有应用集成

**OpenAI SDK（Python）：**

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",  # 指向 LPG
    api_key="sk-virtual-xxxxx"             # 使用虚拟 Key
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "我的邮箱是 test@example.com"}]
)
```

**OpenAI SDK（Node.js）：**

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://127.0.0.1:8080/v1",
  apiKey: "sk-virtual-xxxxx"
});

const response = await client.chat.completions.create({
  model: "gpt-3.5-turbo",
  messages: [{ role: "user", content: "我的邮箱是 test@example.com" }]
});
```

**cURL：**

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-virtual-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

---

## 14. 附录

### 14.1 完整配置示例

```yaml
# ~/.llm-privacy-gateway/config.yaml

proxy:
  host: "127.0.0.1"
  port: 8080
  timeout: 60
  max_connections: 100

presidio:
  enabled: true
  endpoint: "http://localhost:5001"
  language: "zh"
  timeout: 30

log:
  level: "info"
  file: null
  max_size: "100MB"
  max_files: 10
  format: "json"

providers:
  - name: "openai"
    type: "openai"
    base_url: "https://api.openai.com"
    auth_type: "bearer"
    api_key_file: "~/.llm-privacy-gateway/keys/openai.key"
    timeout: 60
  - name: "anthropic"
    type: "anthropic"
    base_url: "https://api.anthropic.com"
    auth_type: "x-api-key"
    api_key_file: "~/.llm-privacy-gateway/keys/anthropic.key"
    timeout: 60

rules:
  enabled_categories:
    - pii
    - credentials
  custom_rules_dir: null

masking:
  default_strategy: "replace"
  enable_restoration: true

audit:
  enabled: true
  log_file: "~/.llm-privacy-gateway/logs/audit.jsonl"
  retention_days: 30
```

### 14.2 默认脱敏策略

| PII 类型 | 脱敏方式 | 效果示例 |
|----------|----------|----------|
| EMAIL_ADDRESS | mask (掩码4字符) | `****@example.com` |
| PHONE_NUMBER | replace | `<PHONE>` |
| CN_PHONE_NUMBER | replace | `<PHONE>` |
| CN_ID_CARD | replace | `<ID_CARD>` |
| CREDIT_CARD | mask (掩码12字符) | `************1111` |
| IP_ADDRESS | replace | `<IP>` |
| API_KEY | replace | `<API_KEY>` |
| PASSWORD | replace | `<PASSWORD>` |
| TOKEN | replace | `<TOKEN>` |
| SECRET | replace | `<SECRET>` |
| PERSON | replace | `<PERSON>` |
| DEFAULT | replace | `<REDACTED>` |

### 14.3 支持的 API 端点

LPG 代理服务器支持以下端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | 聊天补全（支持流式） |
| `/v1/completions` | POST | 文本补全 |
| `/v1/embeddings` | POST | 嵌入向量 |
| `/health` | GET | 健康检查 |
| `/{path:.*}` | POST/GET | 通配路由（转发到其他 LLM API） |

### 14.4 命令速查卡片

```
┌───────────── 服务管理 ─────────────┐
│ lpg start [-p PORT] [-d]           │
│ lpg stop [-f]                      │
│ lpg status                         │
└────────────────────────────────────┘

┌───────────── 配置管理 ─────────────┐
│ lpg config init                    │
│ lpg config show                    │
│ lpg config get <key>               │
│ lpg config set <key> <value>       │
└────────────────────────────────────┘

┌───────────── 虚拟 Key ─────────────┐
│ lpg key list                       │
│ lpg key create -p <provider>       │
│                -n <name>           │
│                [-e <expire>]       │
│ lpg key revoke <key_id>            │
└────────────────────────────────────┘

┌───────────── 规则管理 ─────────────┐
│ lpg rule list [-c <category>]      │
│ lpg rule enable <rule_id>          │
│ lpg rule disable <rule_id>         │
└────────────────────────────────────┘

┌───────────── 提供商管理 ────────────┐
│ lpg provider list                  │
│ lpg provider add -t <type>         │
│                  -n <name>         │
│                  -u <base-url>     │
└────────────────────────────────────┘

┌───────────── 日志审计 ─────────────┐
│ lpg log show [-n LINES]            │
│            [--since 1h/1d/1w/1m]  │
│ lpg log stats [--since 1h]         │
└────────────────────────────────────┘
```

### 14.5 开发相关

**运行测试：**

```bash
# 运行全部测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=lpg --cov-report=html
```

**代码格式化：**

```bash
# 格式化代码
black src/ tests/

# Lint 检查
ruff check src/ tests/

# 类型检查
mypy src/
```

**项目结构：**

```
llm-privacy-gateway/
├── src/lpg/
│   ├── cli/              # CLI 模块
│   ├── core/             # 核心业务逻辑
│   ├── models/           # 数据模型
│   └── utils/            # 工具函数
├── rules/                # 检测规则
├── tests/                # 测试代码
└── doc/                  # 文档
```

### 14.6 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-12 | Phase 1 发布：CLI 工具、HTTP 代理、Presidio 集成、虚拟 Key 管理、规则管理、审计日志 |

### 14.7 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 产品需求 | `doc/req/req-init-20260401.md` | 详细需求规格 |
| 技术设计 | `doc/design/design-update-20260404-v1.0-init.md` | v1.0 技术设计 |
| 编码规范 | `doc/rules/coding-rule.md` | 编码标准 |
| 架构规范 | `doc/rules/architecture-rule.md` | 架构分层规则 |

---

**文档结束**

如有问题或建议，请通过 Issue 或讨论区反馈。