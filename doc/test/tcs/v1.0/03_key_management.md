# LLM Privacy Gateway v1.0 Key 管理黑盒测试用例

**文档版本：** 1.0  
**创建日期：** 2026-04-04  
**测试类型：** 黑盒功能测试  
**覆盖范围：** Key 管理模块（虚拟 Key 创建、解析、列表、详情、吊销、过期处理、使用统计）

---

## 1. 测试概述

本文档覆盖 LLM Privacy Gateway v1.0 版本 Key 管理模块的黑盒测试用例，包括正常流程和异常流程测试。

### 1.1 测试环境

| 项目 | 说明 |
|------|------|
| 操作系统 | macOS / Linux |
| Python 版本 | 3.9+ |
| 测试工具 | CLI 命令 / API 调用 |
| 前置依赖 | 配置文件、至少一个 LLM 提供商配置 |

### 1.2 测试数据

| 文件路径 | 说明 |
|----------|------|
| `test_data/config_sample.yaml` | 标准配置文件（包含提供商配置） |
| `test_data/config_no_provider.yaml` | 无提供商配置的配置文件 |
| `test_data/config_multi_provider.yaml` | 多提供商配置文件 |
| `test_data/key_permissions.json` | Key 权限配置样本 |

---

## 2. 测试用例

### 2.1 虚拟 Key 创建

#### TC-KEY-001: 使用有效 provider 创建虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-001 |
| **用例名称** | 使用有效 provider 创建虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 至少配置了一个有效提供商（如 openai） |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name test-key-001` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 创建成功，返回 Key 信息 2. 返回的 Key ID 格式为 `vk_xxxxxxxxxxxxxxxx` 3. 虚拟 Key 格式为 `sk-virtual-xxxxxxxx` 4. provider 字段为 `openai` 5. name 字段为 `test-key-001` 6. created_at 为当前时间戳 |

---

#### TC-KEY-002: 使用无效 provider 创建虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-002 |
| **用例名称** | 使用不存在的 provider 创建虚拟 Key 失败 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在 |
| **测试步骤** | 1. 执行 `lpg key create --provider nonexistent-provider --name test-key` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 创建失败 2. 显示错误信息：`Provider 'nonexistent-provider' not found` 3. 退出码非零 |

---

#### TC-KEY-003: 创建带名称的虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-003 |
| **用例名称** | 创建带自定义名称的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 至少配置了一个提供商 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name "Production API Key"` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 创建成功 2. name 字段为 `Production API Key` 3. 名称支持空格和特殊字符 |

---

#### TC-KEY-004: 创建带过期时间的虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-004 |
| **用例名称** | 创建带过期时间的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 至少配置了一个提供商 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name temp-key --expires 2026-12-31T23:59:59` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 创建成功 2. expires_at 字段为 `2026-12-31T23:59:59` 3. Key 在过期前可正常使用 |

---

#### TC-KEY-005: 创建带权限的虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-005 |
| **用例名称** | 创建带权限配置的虚拟 Key |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 至少配置了一个提供商 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name limited-key --permissions '{"endpoints": ["/v1/chat/completions"]}'` |
| **测试数据** | `test_data/config_sample.yaml`, `test_data/key_permissions.json` |
| **预期结果** | 1. 创建成功 2. permissions 字段包含指定的权限配置 |

---

#### TC-KEY-006: 创建多个虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-006 |
| **用例名称** | 创建多个虚拟 Key 并验证唯一性 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 配置文件存在 2. 至少配置了一个提供商 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name key-1` 2. 执行 `lpg key create --provider openai --name key-2` 3. 执行 `lpg key create --provider openai --name key-3` 4. 执行 `lpg key list` |
| **测试数据** | `test_data/config_sample.yaml` |
| **预期结果** | 1. 三个 Key 均创建成功 2. 每个 Key 的 ID 和 virtual_key 唯一不重复 3. 列表显示所有 3 个 Key |

---

### 2.2 虚拟 Key 解析

#### TC-KEY-007: 解析有效虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-007 |
| **用例名称** | 解析有效的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 已创建一个有效的虚拟 Key 2. 代理服务器已启动 |
| **测试步骤** | 1. 使用虚拟 Key 发送请求：`curl -H "Authorization: Bearer sk-virtual-xxxxx" http://localhost:8080/v1/chat/completions` |
| **测试数据** | 有效的虚拟 Key |
| **预期结果** | 1. 请求通过认证 2. 虚拟 Key 被正确解析为对应的真实 Key 3. 请求被转发到配置的提供商 |

---

#### TC-KEY-008: 解析无效虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-008 |
| **用例名称** | 解析无效的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 代理服务器已启动 |
| **测试步骤** | 1. 使用无效 Key 发送请求：`curl -H "Authorization: Bearer sk-virtual-invalidkey123" http://localhost:8080/v1/chat/completions` |
| **测试数据** | 无效的虚拟 Key 字符串 |
| **预期结果** | 1. 返回 401 状态码 2. 错误信息：`Invalid API key` 3. 请求不被转发 |

---

#### TC-KEY-009: 解析已吊销虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-009 |
| **用例名称** | 解析已吊销的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 已创建一个虚拟 Key 2. 已吊销该 Key 3. 代理服务器已启动 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name temp-key` 记录返回的 virtual_key 2. 执行 `lpg key revoke <key_id>` 吊销 Key 3. 使用吊销的 Key 发送请求 |
| **测试数据** | 已吊销的虚拟 Key |
| **预期结果** | 1. 返回 401 状态码 2. 错误信息：`Invalid API key` 3. 吊销的 Key 无法使用 |

---

#### TC-KEY-010: 解析已过期虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-010 |
| **用例名称** | 解析已过期的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 创建一个已过期的虚拟 Key（设置过去的时间） 2. 代理服务器已启动 |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name expired-key --expires 2020-01-01T00:00:00` 2. 使用该 Key 发送请求 |
| **测试数据** | 过期的虚拟 Key |
| **预期结果** | 1. 返回 401 状态码 2. 错误信息：`Invalid API key` 3. 过期的 Key 无法使用 |

---

#### TC-KEY-011: 验证 Key 映射关系正确

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-011 |
| **用例名称** | 验证虚拟 Key 正确映射到对应提供商的真实 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 配置了多个提供商（openai, anthropic） 2. 为每个提供商创建了虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name openai-key` 2. 执行 `lpg key create --provider anthropic --name anthropic-key` 3. 使用 openai-key 发送请求，验证转发到 OpenAI 4. 使用 anthropic-key 发送请求，验证转发到 Anthropic |
| **测试数据** | `test_data/config_multi_provider.yaml` |
| **预期结果** | 1. openai-key 的请求被转发到 OpenAI API 2. anthropic-key 的请求被转发到 Anthropic API 3. 每个 Key 使用对应提供商的真实 API Key |

---

### 2.3 虚拟 Key 列表

#### TC-KEY-012: 列出所有虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-012 |
| **用例名称** | 列出所有虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 存在一个或多个虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key list` |
| **测试数据** | 无 |
| **预期结果** | 1. 显示所有虚拟 Key 列表 2. 每个 Key 显示：ID、名称、提供商、创建时间、过期时间、使用次数 3. 列表格式清晰易读 |

---

#### TC-KEY-013: 列出空 Key 列表

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-013 |
| **用例名称** | 列出空的 Key 列表 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 没有任何虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key list` |
| **测试数据** | 无 |
| **预期结果** | 1. 显示空列表或提示信息 2. 不报错，正常退出 |

---

#### TC-KEY-014: 列出包含过期 Key 的列表

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-014 |
| **用例名称** | 列出包含过期 Key 的列表 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 存在有效的虚拟 Key 2. 存在已过期的虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name active-key` 2. 执行 `lpg key create --provider openai --name expired-key --expires 2020-01-01` 3. 执行 `lpg key list` |
| **测试数据** | 无 |
| **预期结果** | 1. 列表显示所有 Key（包括过期的） 2. 过期 Key 有明确的状态标识 3. 有效 Key 和过期 Key 可以区分 |

---

### 2.4 虚拟 Key 详情

#### TC-KEY-015: 获取有效 Key 详情

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-015 |
| **用例名称** | 获取有效虚拟 Key 的详细信息 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 存在一个有效的虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key show <key_id>` |
| **测试数据** | 有效的 Key ID |
| **预期结果** | 1. 显示 Key 完整信息 2. 包含：ID、virtual_key、provider、name、created_at、expires_at、permissions、usage_count、last_used |

---

#### TC-KEY-016: 获取无效 Key 详情

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-016 |
| **用例名称** | 获取不存在的 Key 详情 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 无 |
| **测试步骤** | 1. 执行 `lpg key show nonexistent-key-id` |
| **测试数据** | 不存在的 Key ID |
| **预期结果** | 1. 显示错误信息：Key 不存在 2. 返回空或 None |

---

#### TC-KEY-017: 验证 Key 详情信息完整

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-017 |
| **用例名称** | 验证 Key 详情包含所有必要字段 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 创建一个包含所有可选字段的 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name full-key --expires 2026-12-31 --permissions '{"endpoints": ["/v1/*"]}'` 2. 获取返回的 key_id 3. 执行 `lpg key show <key_id>` |
| **测试数据** | 无 |
| **预期结果** | 详情包含以下字段：`id`, `virtual_key`, `provider`, `name`, `created_at`, `expires_at`, `permissions`, `usage_count`, `last_used` |

---

### 2.5 虚拟 Key 吊销

#### TC-KEY-018: 吊销有效虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-018 |
| **用例名称** | 吊销有效的虚拟 Key |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 存在一个有效的虚拟 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name revoke-test` 记录 key_id 2. 执行 `lpg key revoke <key_id>` |
| **测试数据** | 无 |
| **预期结果** | 1. 吊销成功，显示确认信息 2. Key 状态变为已吊销 3. 从 Key 列表中移除或标记为已吊销 |

---

#### TC-KEY-019: 吊销无效虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-019 |
| **用例名称** | 吊销不存在的虚拟 Key |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 无 |
| **测试步骤** | 1. 执行 `lpg key revoke nonexistent-key-id` |
| **测试数据** | 不存在的 Key ID |
| **预期结果** | 1. 吊销失败 2. 显示错误信息：Key 不存在 3. 返回 False 或错误码 |

---

#### TC-KEY-020: 吊销已吊销的虚拟 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-020 |
| **用例名称** | 重复吊销已吊销的虚拟 Key |
| **优先级** | P2 |
| **自动化** | 是 |
| **前置条件** | 存在一个已吊销的 Key |
| **测试步骤** | 1. 创建并吊销一个 Key 2. 再次执行 `lpg key revoke <key_id>` |
| **测试数据** | 已吊销的 Key ID |
| **预期结果** | 1. 提示 Key 不存在或已吊销 2. 不产生错误 |

---

#### TC-KEY-021: 验证吊销后 Key 不可用

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-021 |
| **用例名称** | 验证吊销后的 Key 无法用于请求 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 已创建并吊销一个 Key |
| **测试步骤** | 1. 创建 Key 并记录 virtual_key 2. 吊销该 Key 3. 使用吊销的 Key 发送 API 请求 |
| **测试数据** | 吊销的虚拟 Key |
| **预期结果** | 1. 请求返回 401 状态码 2. 错误信息：`Invalid API key` |

---

### 2.6 Key 过期处理

#### TC-KEY-022: 过期 Key 自动失效

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-022 |
| **用例名称** | 过期的 Key 自动失效 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 创建一个已过期的 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name expired-key --expires 2020-01-01T00:00:00` 2. 使用该 Key 发送请求 |
| **测试数据** | 过期时间设置为过去的 Key |
| **预期结果** | 1. 请求返回 401 状态码 2. 过期的 Key 被拒绝使用 |

---

#### TC-KEY-023: 未过期 Key 正常工作

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-023 |
| **用例名称** | 未过期的 Key 正常工作 |
| **优先级** | P0 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 创建一个未过期的 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name valid-key --expires 2099-12-31` 2. 使用该 Key 发送请求 |
| **测试数据** | 远未来过期时间的 Key |
| **预期结果** | 1. 请求通过认证 2. Key 正常使用，请求被转发 |

---

#### TC-KEY-024: 过期时间边界测试

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-024 |
| **用例名称** | 过期时间边界值测试 |
| **优先级** | P1 |
| **自动化** | 否 |
| **前置条件** | 代理服务器已运行 |
| **测试步骤** | 1. 创建一个刚好未过期的 Key（过期时间为 1 分钟后） 2. 立即使用该 Key 发送请求 3. 等待 1 分钟后再次使用该 Key 发送请求 |
| **测试数据** | 动态计算的过期时间 |
| **预期结果** | 1. 过期前：请求正常通过 2. 过期后：请求返回 401 |

---

### 2.7 Key 使用统计

#### TC-KEY-025: 验证使用次数统计

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-025 |
| **用例名称** | 验证 Key 使用次数正确统计 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 创建一个新 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name stats-key` 2. 执行 `lpg key show <key_id>` 确认 usage_count 为 0 3. 使用该 Key 发送 3 次请求 4. 执行 `lpg key show <key_id>` |
| **测试数据** | 新创建的 Key |
| **预期结果** | 1. 初始 usage_count 为 0 2. 每次请求后 usage_count 递增 3. 最终 usage_count 为 3 |

---

#### TC-KEY-026: 验证最后使用时间记录

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-026 |
| **用例名称** | 验证 Key 最后使用时间正确记录 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 创建一个新 Key |
| **测试步骤** | 1. 执行 `lpg key create --provider openai --name time-key` 2. 执行 `lpg key show <key_id>` 确认 last_used 为 null 3. 使用该 Key 发送请求 4. 执行 `lpg key show <key_id>` |
| **测试数据** | 新创建的 Key |
| **预期结果** | 1. 初始 last_used 为 null/None 2. 请求后 last_used 更新为当前时间戳 3. 时间戳格式正确（ISO 8601） |

---

### 2.8 并发 Key 操作

#### TC-KEY-027: 并发创建 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-027 |
| **用例名称** | 并发创建多个 Key |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 配置文件存在，至少一个提供商配置 |
| **测试步骤** | 1. 同时执行多个 `lpg key create` 命令（模拟并发） 2. 执行 `lpg key list` 查看结果 |
| **测试数据** | 脚本并发创建 10 个 Key |
| **预期结果** | 1. 所有 Key 均创建成功 2. 每个 Key 的 ID 和 virtual_key 唯一 3. 无数据冲突或丢失 |

---

#### TC-KEY-028: 并发解析 Key

| 项目 | 内容 |
|------|------|
| **用例ID** | TC-KEY-028 |
| **用例名称** | 并发使用同一个 Key 发送请求 |
| **优先级** | P1 |
| **自动化** | 是 |
| **前置条件** | 1. 代理服务器已运行 2. 创建一个 Key |
| **测试步骤** | 1. 创建一个 Key 2. 使用并发工具同时发送 10 个请求 3. 检查 Key 的 usage_count |
| **测试数据** | 并发请求脚本 |
| **预期结果** | 1. 所有请求均成功处理 2. usage_count 正确累加（应为 10） 3. 无竞态条件导致计数错误 |

---

## 3. 测试用例统计

| 类别 | 数量 |
|------|------|
| 虚拟 Key 创建 | 6 |
| 虚拟 Key 解析 | 5 |
| 虚拟 Key 列表 | 3 |
| 虚拟 Key 详情 | 3 |
| 虚拟 Key 吊销 | 4 |
| Key 过期处理 | 3 |
| Key 使用统计 | 2 |
| 并发 Key 操作 | 2 |
| **总计** | **28** |

---

## 4. 优先级分布

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P0 | 14 | 核心功能，必须通过 |
| P1 | 12 | 重要功能，应该通过 |
| P2 | 2 | 辅助功能，可选通过 |

---

## 5. 自动化测试建议

建议将以下测试用例优先实现自动化：
1. 所有 P0 优先级的测试用例
2. 带有明确输入输出的测试用例
3. Key 创建、解析、吊销的基础流程
4. 过期处理逻辑

自动化测试建议使用 Python 的 `subprocess` 模块执行 CLI 命令，并使用 `pytest` 框架组织测试。

---

## 6. 测试数据准备

### 6.1 标准配置文件 (config_sample.yaml)

```yaml
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key: sk-test-openai-key-xxxxx
    auth_type: bearer

virtual_keys: []

presidio:
  endpoint: http://localhost:5001
  language: zh
```

### 6.2 多提供商配置文件 (config_multi_provider.yaml)

```yaml
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key: sk-test-openai-key-xxxxx
    auth_type: bearer
  - name: anthropic
    type: anthropic
    base_url: https://api.anthropic.com
    api_key: sk-ant-test-key-xxxxx
    auth_type: x-api-key

virtual_keys: []
```

### 6.3 Key 权限配置 (key_permissions.json)

```json
{
  "endpoints": ["/v1/chat/completions", "/v1/completions"],
  "max_requests_per_day": 1000,
  "allowed_models": ["gpt-3.5-turbo", "gpt-4"]
}
```
