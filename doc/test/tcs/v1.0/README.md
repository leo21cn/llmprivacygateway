# LLM Privacy Gateway v1.0 测试用例文档

**版本：** 1.0  
**日期：** 2026-04-04  
**测试类型：** 黑盒测试  
**适用范围：** v1.0 MVP CLI 版本

---

## 文档目录

### 测试用例文件

| 文件 | 测试场景 | 测试用例数 | 优先级 | 状态 |
|------|----------|------------|--------|------|
| [01_cli_commands.md](01_cli_commands.md) | CLI 命令行测试 | 41 | P0 | ✅ 完成 |
| [02_proxy_service.md](02_proxy_service.md) | 代理服务测试 | 32 | P0 | ✅ 完成 |
| [03_key_management.md](03_key_management.md) | Key 管理测试 | 28 | P0 | ✅ 完成 |
| [04_pii_detection.md](04_pii_detection.md) | PII 检测脱敏测试 | 42 | P0 | ✅ 完成 |
| [05_rule_management.md](05_rule_management.md) | 规则管理测试 | 35 | P1 | ✅ 完成 |
| [06_audit_logging.md](06_audit_logging.md) | 审计日志测试 | 30 | P1 | ✅ 完成 |
| [07_configuration.md](07_configuration.md) | 配置管理测试 | 36 | P1 | ✅ 完成 |
| [08_e2e_integration.md](08_e2e_integration.md) | 端到端集成测试 | 26 | P1 | ✅ 完成 |

**测试用例总计：** 270 个

### 测试数据文件

| 文件 | 对应测试用例 | 数据条目数 | 覆盖率 |
|------|--------------|------------|--------|
| [01_cli_commands_testdata.md](01_cli_commands_testdata.md) | CLI 命令测试 | ~196 | ≥95% |
| [02_proxy_service_testdata.md](02_proxy_service_testdata.md) | 代理服务测试 | ~150 | ≥95% |
| [03_key_management_testdata.md](03_key_management_testdata.md) | Key 管理测试 | ~120 | ≥95% |
| [04_pii_detection_testdata.md](04_pii_detection_testdata.md) | PII 检测脱敏测试 | ~200 | ≥95% |
| [05_rule_management_testdata.md](05_rule_management_testdata.md) | 规则管理测试 | ~100 | ≥95% |
| [06_audit_logging_testdata.md](06_audit_logging_testdata.md) | 审计日志测试 | ~150 | ≥95% |
| [07_configuration_testdata.md](07_configuration_testdata.md) | 配置管理测试 | ~130 | ≥95% |
| [08_e2e_integration_testdata.md](08_e2e_integration_testdata.md) | 端到端集成测试 | ~180 | ≥95% |

**测试数据总计：** ~1226 条

---

## 测试覆盖统计

### 按优先级分布

| 优先级 | 测试用例数 | 占比 | 执行要求 |
|--------|------------|------|----------|
| P0 | 143 | 53% | 必须通过 |
| P1 | 127 | 47% | 建议通过 |

### 按模块分布

| 模块 | 测试用例数 | 测试数据条目数 | 覆盖率 |
|------|------------|----------------|--------|
| CLI 命令 | 41 | 196 | ≥95% |
| 代理服务 | 32 | 150 | ≥95% |
| Key 管理 | 28 | 120 | ≥95% |
| PII 检测 | 42 | 200 | ≥95% |
| 规则管理 | 35 | 100 | ≥95% |
| 审计日志 | 30 | 150 | ≥95% |
| 配置管理 | 36 | 130 | ≥95% |
| 端到端集成 | 26 | 180 | ≥95% |

---

## 测试环境要求

### 系统环境

- 操作系统：macOS 12.0+ / Linux / Windows
- Python：3.10+
- 网络：需要访问 LLM API 端点（测试环境可用 mock）

### 依赖服务

- Presidio Analyzer：localhost:5001
- Presidio Anonymizer：localhost:5001

### 测试数据

测试用例中使用的标准测试数据：

```yaml
test_data:
  emails:
    - "user@example.com"
    - "test.user+tag@domain.co.uk"
  phones:
    - "13812345678"  # 中国手机号
    - "+86 138 1234 5678"
  id_cards:
    - "110101199001011234"  # 中国身份证
  credit_cards:
    - "4111111111111111"  # Visa 测试卡
  api_keys:
    - "sk-test-1234567890abcdef"
  names:
    - "张三"
    - "John Smith"
```

---

## 测试用例格式规范

每个测试用例包含以下字段：

| 字段 | 说明 | 必填 |
|------|------|------|
| 用例ID | TC-{模块}-{序号}，如 TC-CLI-001 | 是 |
| 用例名称 | 简短描述测试目的 | 是 |
| 前置条件 | 执行前需要满足的条件 | 否 |
| 测试步骤 | 详细的操作步骤 | 是 |
| 测试数据 | 使用的输入数据 | 否 |
| 预期结果 | 期望的输出或行为 | 是 |
| 优先级 | P0/P1/P2 | 是 |
| 自动化 | 是否可自动化（是/否） | 是 |
| 备注 | 补充说明 | 否 |

---

## 优先级定义

| 优先级 | 说明 | 执行要求 |
|--------|------|----------|
| **P0** | 核心功能，阻塞发布 | 必须通过 |
| **P1** | 重要功能，影响体验 | 建议通过 |
| **P2** | 边界场景，锦上添花 | 可选通过 |

---

## 测试执行指南

### 手动执行

```bash
# 1. 安装应用
pip install -e .

# 2. 启动 Presidio 服务
lpg setup-presidio

# 3. 按测试用例步骤执行
lpg start
# ... 执行测试步骤 ...
lpg stop
```

### 自动化执行

```bash
# 运行所有测试
pytest tests/

# 运行特定模块测试
pytest tests/unit/test_key_manager.py

# 运行并生成覆盖率报告
pytest --cov=lpg --cov-report=html
```

---

## 测试覆盖矩阵

| 功能模块 | 单元测试 | 集成测试 | E2E测试 | 总覆盖 |
|----------|----------|----------|---------|--------|
| CLI 命令 | - | ✓ | ✓ | ✓ |
| 代理服务 | ✓ | ✓ | ✓ | ✓ |
| Key 管理 | ✓ | ✓ | ✓ | ✓ |
| PII 检测 | ✓ | ✓ | ✓ | ✓ |
| 规则管理 | ✓ | ✓ | - | ✓ |
| 审计日志 | ✓ | ✓ | - | ✓ |
| 配置管理 | ✓ | ✓ | - | ✓ |

---

## 相关文档

- [产品需求文档](../../../req/req-init-20260401.md)
- [技术设计文档](../../../design/design-update-20260404-v1.0-init.md)
- [编码规范](../../../rules/coding-rule.md)
