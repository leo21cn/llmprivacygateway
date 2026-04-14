# LLM Privacy Gateway

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

LLM Privacy Gateway 是一个本地隐私保护代理，用于在访问大型语言模型（LLM）API 时自动检测和脱敏敏感信息（PII），确保企业数据安全合规。

---

## 📋 需求

### 核心功能

- **PII 检测与脱敏**：自动识别并脱敏文本中的个人身份信息（邮箱、手机号、身份证号、信用卡等）
- **虚拟 Key 管理**：为不同用户/应用分配独立的虚拟 API Key，实现细粒度访问控制
- **多提供商支持**：支持 OpenAI、Anthropic、阿里云百炼等多种 LLM 提供商
- **审计日志**：完整记录所有请求和响应，支持合规审计
- **规则管理**：灵活配置检测规则和脱敏策略

### 典型应用场景

1. 企业内部使用 LLM 时防止敏感数据泄露
2. 开发团队共享 LLM API 访问权限
3. 满足数据合规要求（GDPR、个人信息保护法等）

📖 **详细需求文档**：[doc/req/req-init-20260401.md](doc/req/req-init-20260401.md)

---

## 🏗️ 架构

### 系统架构图

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   用户/应用      │────▶│  LLM Privacy     │────▶│   LLM 提供商     │
│                 │     │    Gateway       │     │ (OpenAI/百炼等)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Presidio PII    │
                        │  检测与脱敏引擎   │
                        └──────────────────┘
```

### 四层架构设计

```
┌─────────────────────────────────────┐
│           CLI 层 (lpg/cli/)         │  ← 命令行交互界面
├─────────────────────────────────────┤
│          Core 层 (lpg/core/)        │  ← 核心业务逻辑
│  ├─ ConfigService    配置管理       │
│  ├─ KeyManager       虚拟Key管理    │
│  ├─ RuleManager      规则管理       │
│  ├─ PresidioClient   PII检测客户端  │
│  ├─ AuditService     审计日志       │
│  └─ ProxyServer      HTTP代理服务   │
├─────────────────────────────────────┤
│         Models 层 (lpg/models/)      │  ← 数据模型定义
├─────────────────────────────────────┤
│         Utils 层 (lpg/utils/)        │  ← 通用工具函数
└─────────────────────────────────────┘
```

### 技术栈

- **Python 3.10+**：核心开发语言
- **Click**：CLI 框架
- **aiohttp**：异步 HTTP 代理服务器
- **Pydantic**：数据模型验证
- **Presidio**：微软 PII 检测引擎
- **Rich**：终端美化输出

📖 **详细设计文档**：[doc/design/design-update-20260404-v1.0-init.md](doc/design/design-update-20260404-v1.0-init.md)

📖 **架构规范**：[doc/rules/architecture-rule.md](doc/rules/architecture-rule.md)

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone <repository-url>
cd llm-privacy-gateway

# 安装依赖
pip install -e .

# 安装开发依赖（可选）
pip install -e ".[dev]"
```

### 前置依赖

启动前需要确保 **Presidio 服务**已运行：

```bash
# 使用 Docker 启动 Presidio
docker run -d -p 5001:5001 mcr.microsoft.com/presidio-analyzer:latest
docker run -d -p 5002:5002 mcr.microsoft.com/presidio-anonymizer:latest
```

### 配置与启动

```bash
# 1. 初始化配置
lpg config init

# 2. 添加 LLM 提供商（以阿里云百炼为例）
lpg provider add \
  --type openai \
  --name bailian \
  --base-url https://dashscope.aliyuncs.com/compatible-mode

# 3. 创建 API Key 文件
echo "your-api-key" > ~/.bailian_api_key

# 4. 创建虚拟 Key
lpg key create --provider bailian --name my-key

# 5. 启动代理服务
lpg start

# 6. 查看状态
lpg status
```

### 使用代理

将 LLM API 调用指向本地代理：

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-virtual-xxxxx" \
  -d '{
    "model": "qwen-turbo",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

或使用 Python：

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-virtual-xxxxx",
    base_url="http://localhost:8080/v1"
)

response = client.chat.completions.create(
    model="qwen-turbo",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

---

## 📚 操作指南

### CLI 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `lpg config init` | 初始化配置 | `lpg config init` |
| `lpg config show` | 显示配置 | `lpg config show` |
| `lpg provider list` | 列出提供商 | `lpg provider list` |
| `lpg provider add` | 添加提供商 | `lpg provider add --type openai --name openai --base-url ...` |
| `lpg key list` | 列出虚拟 Key | `lpg key list` |
| `lpg key create` | 创建虚拟 Key | `lpg key create --provider openai --name my-key` |
| `lpg key revoke` | 吊销虚拟 Key | `lpg key revoke <key-id>` |
| `lpg rule list` | 列出检测规则 | `lpg rule list` |
| `lpg rule enable` | 启用规则 | `lpg rule enable <rule-id>` |
| `lpg rule disable` | 禁用规则 | `lpg rule disable <rule-id>` |
| `lpg start` | 启动代理 | `lpg start [--port 8080]` |
| `lpg stop` | 停止代理 | `lpg stop` |
| `lpg status` | 查看状态 | `lpg status` |
| `lpg log show` | 查看日志 | `lpg log show --lines 20` |
| `lpg log stats` | 查看统计 | `lpg log stats` |

📖 **详细测试用例**：[doc/test/tcs/v1.0/README.md](doc/test/tcs/v1.0/README.md)

---

## 🧪 测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=lpg --cov-report=html
```

---

## 📁 项目结构

```
llm-privacy-gateway/
├── doc/                    # 文档目录
│   ├── design/            # 设计文档
│   ├── req/               # 需求文档
│   ├── rules/             # 编码规范
│   └── test/              # 测试用例
├── rules/                 # 内置检测规则
│   ├── pii.yaml          # PII 检测规则
│   └── credentials.yaml  # 凭证检测规则
├── src/lpg/              # 源代码
│   ├── cli/              # CLI 命令
│   ├── core/             # 核心服务
│   ├── models/           # 数据模型
│   └── utils/            # 工具函数
├── tests/                # 测试代码
│   ├── unit/             # 单元测试
│   ├── integration/      # 集成测试
│   └── conftest.py       # 测试配置
├── pyproject.toml        # 项目配置
└── README.md            # 本文件
```

---

## 🤝 贡献指南

请阅读 [doc/rules/coding-rule.md](doc/rules/coding-rule.md) 了解编码规范。

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

## 🔗 相关链接

- [需求文档](doc/req/req-init-20260401.md)
- [设计文档](doc/design/design-update-20260404-v1.0-init.md)
- [编码规范](doc/rules/coding-rule.md)
- [架构规范](doc/rules/architecture-rule.md)
- [测试用例](doc/test/tcs/v1.0/README.md)
