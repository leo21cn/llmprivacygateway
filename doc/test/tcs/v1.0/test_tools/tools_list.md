# 测试工具列表

**版本：** 1.0  
**日期：** 2026-04-04  
**适用范围：** v1.0 MVP 黑盒/白盒测试

---

## 目录

1. [测试框架](#1-测试框架)
2. [单元测试工具](#2-单元测试工具)
3. [集成测试工具](#3-集成测试工具)
4. [性能测试工具](#4-性能测试工具)
5. [代码质量工具](#5-代码质量工具)
6. [Mock与Fixture工具](#6-mock与fixture工具)
7. [HTTP测试工具](#7-http测试工具)
8. [CLI测试工具](#8-cli测试工具)
9. [日志与调试工具](#9-日志与调试工具)
10. [测试数据工具](#10-测试数据工具)

---

## 1. 测试框架

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| pytest | ≥7.4.0 | 主测试框架 | `pip install pytest` |
| pytest-asyncio | ≥0.21.0 | 异步测试支持 | `pip install pytest-asyncio` |
| pytest-xdist | ≥3.3.0 | 并行测试执行 | `pip install pytest-xdist` |

---

## 2. 单元测试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| pytest-cov | ≥4.1.0 | 测试覆盖率 | `pip install pytest-cov` |
| pytest-mock | ≥3.11.0 | Mock支持 | `pip install pytest-mock` |
| pytest-timeout | ≥2.1.0 | 测试超时控制 | `pip install pytest-timeout` |
| pytest-randomly | ≥3.12.0 | 随机化测试顺序 | `pip install pytest-randomly` |

---

## 3. 集成测试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| pytest-integration | ≥0.2.0 | 集成测试标记 | `pip install pytest-integration` |
| testcontainers | ≥3.7.0 | 容器化测试环境 | `pip install testcontainers` |
| docker-compose | ≥1.29.0 | 多容器编排 | `pip install docker-compose` |

---

## 4. 性能测试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| pytest-benchmark | ≥4.0.0 | 性能基准测试 | `pip install pytest-benchmark` |
| locust | ≥2.15.0 | 负载测试 | `pip install locust` |
| memory-profiler | ≥0.60.0 | 内存分析 | `pip install memory-profiler` |
| py-spy | ≥0.3.14 | CPU性能分析 | `pip install py-spy` |

---

## 5. 代码质量工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| black | ≥23.0.0 | 代码格式化 | `pip install black` |
| ruff | ≥0.1.0 | 代码Lint检查 | `pip install ruff` |
| mypy | ≥1.5.0 | 类型检查 | `pip install mypy` |
| bandit | ≥1.7.0 | 安全检查 | `pip install bandit` |
| pylint | ≥2.17.0 | 代码质量检查 | `pip install pylint` |

---

## 6. Mock与Fixture工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| unittest.mock | 内置 | 基础Mock | 无需安装 |
| pytest-fixture | 内置 | Fixture支持 | 无需安装 |
| factory-boy | ≥3.3.0 | 测试工厂 | `pip install factory-boy` |
| faker | ≥19.0.0 | 假数据生成 | `pip install faker` |
| responses | ≥0.23.0 | HTTP Mock | `pip install responses` |
| aioresponses | ≥0.7.0 | 异步HTTP Mock | `pip install aioresponses` |

---

## 7. HTTP测试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| httpx | ≥0.24.0 | HTTP客户端测试 | `pip install httpx` |
| requests | ≥2.31.0 | HTTP请求 | `pip install requests` |
| aiohttp | ≥3.9.0 | 异步HTTP客户端 | `pip install aiohttp` |
| pytest-httpserver | ≥1.0.0 | HTTP服务器Mock | `pip install pytest-httpserver` |

---

## 8. CLI测试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| click.testing | 内置 | Click CLI测试 | 无需安装 |
| typer.testing | ≥0.9.0 | Typer CLI测试 | `pip install typer` |
| pytest-console-scripts | ≥1.4.0 | 控制台脚本测试 | `pip install pytest-console-scripts` |
| pexpect | ≥4.8.0 | 交互式CLI测试 | `pip install pexpect` |

---

## 9. 日志与调试工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| loguru | ≥0.7.0 | 日志记录 | `pip install loguru` |
| pytest-sugar | ≥0.9.7 | 美化测试输出 | `pip install pytest-sugar` |
| pytest-clarity | ≥1.0.0 | 断言美化 | `pip install pytest-clarity` |
| icecream | ≥2.1.0 | 调试打印 | `pip install icecream` |
| pdb | 内置 | 调试器 | 无需安装 |

---

## 10. 测试数据工具

| 工具名称 | 版本要求 | 用途 | 安装命令 |
|----------|----------|------|----------|
| pyyaml | ≥6.0 | YAML配置解析 | `pip install pyyaml` |
| jsonschema | ≥4.17.0 | JSON Schema验证 | `pip install jsonschema` |
| hypothesis | ≥6.82.0 | 属性测试 | `pip install hypothesis` |
| pytest-datadir | ≥1.4.0 | 测试数据目录 | `pip install pytest-datadir` |
| pytest-regressions | ≥2.4.0 | 回归测试 | `pip install pytest-regressions` |

---

## 安装命令汇总

### 基础测试套件

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-timeout
```

### 完整测试套件

```bash
pip install -r requirements-test.txt
```

### requirements-test.txt

```txt
# 测试框架
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-xdist>=3.3.0

# 单元测试
pytest-cov>=4.1.0
pytest-mock>=3.11.0
pytest-timeout>=2.1.0

# 集成测试
pytest-integration>=0.2.0

# 性能测试
pytest-benchmark>=4.0.0

# 代码质量
black>=23.0.0
ruff>=0.1.0
mypy>=1.5.0

# Mock与Fixture
factory-boy>=3.3.0
faker>=19.0.0
responses>=0.23.0
aioresponses>=0.7.0

# HTTP测试
httpx>=0.24.0
requests>=2.31.0
pytest-httpserver>=1.0.0

# CLI测试
pexpect>=4.8.0

# 日志与调试
loguru>=0.7.0
pytest-sugar>=0.9.7
pytest-clarity>=1.0.0

# 测试数据
pyyaml>=6.0
jsonschema>=4.17.0
hypothesis>=6.82.0
pytest-datadir>=1.4.0
pytest-regressions>=2.4.0
```

---

## 测试环境配置

### pytest.ini

```ini
[pytest]
testpaths = tests
asyncio_mode = auto
timeout = 60
addopts = -v --tb=short
markers =
    unit: 单元测试
    integration: 集成测试
    e2e: 端到端测试
    slow: 慢速测试
```

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
timeout = 60
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src/lpg"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## 相关文档

- [测试用例索引](../README.md)
- [编码规范](../../../rules/coding-rule.md)
- [技术设计文档](../../../design/design-update-20260404-v1.0-init.md)
