# LLM Privacy Gateway v1.0 配置管理黑盒测试用例

**文档版本：** 1.0  
**创建日期：** 2026-04-04  
**测试类型：** 黑盒功能测试  
**覆盖范围：** 配置管理模块（配置初始化、加载、读取、设置、验证、环境变量、优先级、持久化、提供商配置）

---

## 1. 测试概述

本文档覆盖 LLM Privacy Gateway v1.0 版本配置管理模块的黑盒测试用例，包括正常流程和异常流程测试。

### 1.1 测试环境

| 项目 | 说明 |
|------|------|
| 操作系统 | macOS / Linux |
| Python 版本 | 3.9+ |
| 测试工具 | CLI 命令 |
| 前置依赖 | 无 |

### 1.2 测试数据

| 文件路径 | 说明 |
|----------|------|
| `test_data/config_sample.yaml` | 标准配置文件样本 |
| `test_data/config_invalid.yaml` | 格式错误的配置文件 |
| `test_data/config_empty.yaml` | 空配置文件 |
| `test_data/config_env_override.yaml` | 环境变量覆盖配置样本 |
| `test_data/providers_sample.yaml` | 提供商配置样本 |

---

## 2. 测试用例

### 2.1 配置初始化

#### TC-CONFIG-001: 交互式初始化配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-001 |
| **用例名称** | 交互式初始化配置 |
| **优先级** | P0 |
| **自动化** | 否 |
| **前置条件** | 1. 无现有配置文件 2. 用户有交互权限 |
| **测试步骤** | 1. 执行 `lpg config init` 2. 按照提示输入配置值：host=127.0.0.1, port=8080, log_level=info 3. 确认保存 |
| **测试数据** | 无 |
| **预期结果** | 1. 交互提示正确显示 2. 接受用户输入 3. 在默认路径 `~/.lpg/config.yaml` 生成配置文件 4. 配置文件内容包含用户输入的值 |

---

#### TC-CONFIG-002: 非交互式初始化配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-002 |
| **用例名称** | 非交互式初始化配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 无现有配置文件 |
| **测试步骤** | 1. 执行 `lpg config init --non-interactive` |
| **测试数据** | 无 |
| **预期结果** | 1. 不显示交互提示 2. 使用默认值生成配置文件 3. 默认配置包含：host=127.0.0.1, port=8080, log_level=info |

---

#### TC-CONFIG-003: 初始化配置到指定路径

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-003 |
| **用例名称** | 初始化配置到指定路径 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 目标目录存在且可写 |
| **测试步骤** | 1. 执行 `lpg config init --output /tmp/test_config.yaml` |
| **测试数据** | 无 |
| **预期结果** | 1. 在指定路径 `/tmp/test_config.yaml` 生成配置文件 2. 配置文件内容正确 3. 默认路径无配置文件生成 |

---

#### TC-CONFIG-004: 覆盖已存在的配置文件

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-004 |
| **用例名称** | 覆盖已存在的配置文件 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件已存在 2. 配置文件包含有效配置 |
| **测试步骤** | 1. 执行 `lpg config init --force` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示警告：配置文件已存在 2. 使用 `--force` 后覆盖原文件 3. 新配置文件为默认值 4. 返回成功消息 |

---

### 2.2 配置加载

#### TC-CONFIG-005: 从默认路径加载配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-005 |
| **用例名称** | 从默认路径加载配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在于默认路径 `~/.lpg/config.yaml` |
| **测试步骤** | 1. 执行 `lpg config list` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 成功加载配置 2. 显示配置内容 3. 无错误信息 |

---

#### TC-CONFIG-006: 从指定路径加载配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-006 |
| **用例名称** | 从指定路径加载配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 指定路径存在有效配置文件 |
| **测试步骤** | 1. 执行 `lpg config list --config /tmp/custom_config.yaml` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 成功加载指定路径的配置 2. 显示配置内容 3. 忽略默认路径配置 |

---

#### TC-CONFIG-007: 加载不存在的配置文件

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-007 |
| **用例名称** | 加载不存在的配置文件 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 指定路径无配置文件 |
| **测试步骤** | 1. 执行 `lpg config list --config /nonexistent/config.yaml` |
| **测试数据** | 无 |
| **预期结果** | 1. 显示错误：配置文件不存在 2. 提示使用 `lpg config init` 初始化配置 3. 退出码非零 |

---

#### TC-CONFIG-008: 加载格式错误的配置文件

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-008 |
| **用例名称** | 加载格式错误的配置文件 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在但格式错误 |
| **测试步骤** | 1. 执行 `lpg config list --config test_data/config_invalid.yaml` |
| **测试数据** | `test_data/config_invalid.yaml` |
| **预期结果** | 1. 显示错误：配置文件格式错误 2. 显示具体错误位置 3. 退出码非零 |

---

#### TC-CONFIG-009: 加载空配置文件

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-009 |
| **用例名称** | 加载空配置文件 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在但内容为空 |
| **测试步骤** | 1. 执行 `lpg config list --config test_data/config_empty.yaml` |
| **测试数据** | `test_data/config_empty.yaml` |
| **预期结果** | 1. 使用默认配置 2. 显示默认配置内容 3. 无错误信息 |

---

### 2.3 配置读取

#### TC-CONFIG-010: 读取单个配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-010 |
| **用例名称** | 读取单个配置项 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在且包含有效配置 |
| **测试步骤** | 1. 执行 `lpg config get proxy.port` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 返回配置值：8080 2. 输出格式正确 3. 无错误信息 |

---

#### TC-CONFIG-011: 读取嵌套配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-011 |
| **用例名称** | 读取嵌套配置项 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在且包含嵌套配置 |
| **测试步骤** | 1. 执行 `lpg config get providers.openai.api_key` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 返回嵌套配置值 2. 输出格式正确 3. 无错误信息 |

---

#### TC-CONFIG-012: 读取不存在的配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-012 |
| **用例名称** | 读取不存在的配置项 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config get nonexistent.key` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示错误：配置项不存在 2. 退出码非零 |

---

#### TC-CONFIG-013: 读取带默认值的配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-013 |
| **用例名称** | 读取带默认值的配置项 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config get nonexistent.key --default "default_value"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 返回默认值："default_value" 2. 无错误信息 |

---

#### TC-CONFIG-014: 显示所有配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-014 |
| **用例名称** | 显示所有配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config list` 2. 执行 `lpg config list --format json` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示所有配置项 2. 格式正确（默认YAML，JSON格式） 3. 包含所有默认配置值 |

---

### 2.4 配置设置

#### TC-CONFIG-015: 设置单个配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-015 |
| **用例名称** | 设置单个配置项 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.port 9090` 2. 执行 `lpg config get proxy.port` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 设置成功 2. 读取返回新值：9090 3. 配置文件已更新 |

---

#### TC-CONFIG-016: 设置嵌套配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-016 |
| **用例名称** | 设置嵌套配置项 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set providers.openai.api_key "sk-new-key"` 2. 执行 `lpg config get providers.openai.api_key` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 设置成功 2. 读取返回新值："sk-new-key" 3. 配置文件已更新 |

---

#### TC-CONFIG-017: 设置无效配置项

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-017 |
| **用例名称** | 设置无效配置项 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set invalid.key "value"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示错误：无效的配置项 2. 提示支持的配置项列表 3. 退出码非零 |

---

#### TC-CONFIG-018: 设置无效配置值

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-018 |
| **用例名称** | 设置无效配置值 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.port "abc"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示错误：端口必须是数字 2. 配置未修改 3. 退出码非零 |

---

#### TC-CONFIG-019: 验证配置值范围

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-019 |
| **用例名称** | 验证配置值范围 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.port 70000` 2. 执行 `lpg config set proxy.timeout 0` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 端口设置失败：端口必须在1-65535之间 2. 超时设置失败：超时必须大于0 3. 配置未修改 |

---

### 2.5 配置验证

#### TC-CONFIG-020: 验证端口范围（1-65535）

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-020 |
| **用例名称** | 验证端口范围（1-65535） |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.port 1` 2. 执行 `lpg config set proxy.port 65535` 3. 执行 `lpg config set proxy.port 0` 4. 执行 `lpg config set proxy.port 65536` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 端口1设置成功 2. 端口65535设置成功 3. 端口0设置失败 4. 端口65536设置失败 |

---

#### TC-CONFIG-021: 验证host地址格式

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-021 |
| **用例名称** | 验证host地址格式 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.host "127.0.0.1"` 2. 执行 `lpg config set proxy.host "0.0.0.0"` 3. 执行 `lpg config set proxy.host "localhost"` 4. 执行 `lpg config set proxy.host "999.999.999.999"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 127.0.0.1设置成功 2. 0.0.0.0设置成功 3. localhost设置成功 4. 999.999.999.999设置失败 |

---

#### TC-CONFIG-022: 验证日志级别（debug/info/warn/error）

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-022 |
| **用例名称** | 验证日志级别（debug/info/warn/error） |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set log.level "debug"` 2. 执行 `lpg config set log.level "info"` 3. 执行 `lpg config set log.level "warn"` 4. 执行 `lpg config set log.level "error"` 5. 执行 `lpg config set log.level "invalid"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. debug设置成功 2. info设置成功 3. warn设置成功 4. error设置成功 5. invalid设置失败 |

---

#### TC-CONFIG-023: 验证超时时间范围

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-023 |
| **用例名称** | 验证超时时间范围 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.timeout 1` 2. 执行 `lpg config set proxy.timeout 300` 3. 执行 `lpg config set proxy.timeout 0` 4. 执行 `lpg config set proxy.timeout 301` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 超时1秒设置成功 2. 超时300秒设置成功 3. 超时0秒设置失败 4. 超时301秒设置失败 |

---

#### TC-CONFIG-024: 验证URL格式

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-024 |
| **用例名称** | 验证URL格式 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set providers.openai.base_url "https://api.openai.com"` 2. 执行 `lpg config set providers.openai.base_url "http://localhost:8080"` 3. 执行 `lpg config set providers.openai.base_url "invalid-url"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. HTTPS URL设置成功 2. HTTP URL设置成功 3. 无效URL设置失败 |

---

### 2.6 环境变量

#### TC-CONFIG-025: 环境变量覆盖配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-025 |
| **用例名称** | 环境变量覆盖配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 设置环境变量 `LPG_PROXY_PORT=9999` |
| **测试步骤** | 1. 执行 `lpg config get proxy.port` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 返回环境变量值：9999 2. 配置文件中的值被覆盖 |

---

#### TC-CONFIG-026: 环境变量优先级

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-026 |
| **用例名称** | 环境变量优先级 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 设置多个环境变量 |
| **测试步骤** | 1. 设置环境变量 `LPG_PROXY_HOST=0.0.0.0` 2. 设置环境变量 `LPG_PROXY_PORT=7777` 3. 执行 `lpg config list` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 环境变量值覆盖配置文件值 2. 显示的配置包含环境变量值 |

---

#### TC-CONFIG-027: 无效环境变量值

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-027 |
| **用例名称** | 无效环境变量值 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 设置无效环境变量 `LPG_PROXY_PORT=abc` |
| **测试步骤** | 1. 执行 `lpg config get proxy.port` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 显示警告：环境变量值无效 2. 使用配置文件中的值 3. 不退出程序 |

---

### 2.7 配置优先级

#### TC-CONFIG-028: 命令行参数优先级最高

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-028 |
| **用例名称** | 命令行参数优先级最高 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 设置环境变量 `LPG_PROXY_PORT=8888` |
| **测试步骤** | 1. 执行 `lpg start --port 7777` 2. 执行 `lpg status` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 服务使用端口7777启动 2. 命令行参数覆盖环境变量和配置文件 |

---

#### TC-CONFIG-029: 环境变量优先级次之

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-029 |
| **用例名称** | 环境变量优先级次之 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在（端口8080） 2. 设置环境变量 `LPG_PROXY_PORT=8888` |
| **测试步骤** | 1. 执行 `lpg start` 2. 执行 `lpg status` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 服务使用端口8888启动 2. 环境变量覆盖配置文件值 |

---

#### TC-CONFIG-030: 配置文件优先级最低

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-030 |
| **用例名称** | 配置文件优先级最低 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在（端口8080） |
| **测试步骤** | 1. 执行 `lpg start` 2. 执行 `lpg status` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 服务使用端口8080启动 2. 使用配置文件中的值 |

---

### 2.8 配置持久化

#### TC-CONFIG-031: 配置修改后自动保存

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-031 |
| **用例名称** | 配置修改后自动保存 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg config set proxy.port 9090` 2. 检查配置文件内容 3. 执行 `lpg config get proxy.port` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 配置文件已更新 2. 文件内容包含新值 3. 读取返回新值 |

---

#### TC-CONFIG-032: 配置文件权限检查

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-032 |
| **用例名称** | 配置文件权限检查 |
| **优先级** | P2 |
| **自动化** | 否 |
| **前置条件** | 配置文件存在且权限为600 |
| **测试步骤** | 1. 检查配置文件权限 2. 尝试修改配置 3. 检查修改后权限 |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 配置文件权限为600 2. 修改成功 3. 修改后权限仍为600 |

---

### 2.9 提供商配置

#### TC-CONFIG-033: 添加提供商配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-033 |
| **用例名称** | 添加提供商配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg provider add openai --api-key sk-test123 --base-url https://api.openai.com` 2. 执行 `lpg provider list` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 添加成功 2. 提供商列表包含openai 3. 配置文件已更新 |

---

#### TC-CONFIG-034: 移除提供商配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-034 |
| **用例名称** | 移除提供商配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件包含提供商配置 |
| **测试步骤** | 1. 执行 `lpg provider remove openai` 2. 执行 `lpg provider list` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 移除成功 2. 提供商列表为空 3. 配置文件已更新 |

---

#### TC-CONFIG-035: 修改提供商配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-035 |
| **用例名称** | 修改提供商配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件包含提供商配置 |
| **测试步骤** | 1. 执行 `lpg provider update openai --api-key sk-newkey456` 2. 执行 `lpg provider show openai` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 修改成功 2. 显示新的API Key 3. 配置文件已更新 |

---

#### TC-CONFIG-036: 列出提供商配置

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-CONFIG-036 |
| **用例名称** | 列出提供商配置 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件包含提供商配置 |
| **测试步骤** | 1. 执行 `lpg provider list` 2. 执行 `lpg provider list --format json` |
| **测试数据** | `test_data/providers_sample.yaml` |
| **预期结果** | 1. 显示所有提供商 2. 包含提供商名称、类型、状态 3. JSON格式正确 |

---
