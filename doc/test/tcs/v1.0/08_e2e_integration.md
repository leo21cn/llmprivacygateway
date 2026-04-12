# LLM Privacy Gateway v1.0 端到端集成黑盒测试用例

## 1. 文档概述

### 1.1 目的
本文档定义 LLM Privacy Gateway v1.0 的端到端集成黑盒测试用例，验证系统各组件协同工作的正确性和完整性。

### 1.2 测试范围
基于设计文档中的整体架构和数据流设计，覆盖以下端到端场景：
- 完整请求流程测试
- CLI到代理服务集成测试
- Key管理到代理服务集成测试
- 规则管理到PII检测集成测试
- 配置管理集成测试
- 审计日志集成测试
- 错误处理集成测试
- 并发场景集成测试
- 性能场景集成测试
- 安全场景集成测试

### 1.3 测试环境
- **操作系统**: macOS/Linux/Windows
- **Python版本**: 3.9+
- **依赖服务**: Presidio Analyzer/Anonymizer, 目标LLM服务
- **网络环境**: 本地网络环境

### 1.4 测试数据
测试数据文件存储在 `test_data/` 目录下，包括：
- `e2e_test_payloads.json` - 端到端测试请求数据
- `e2e_test_configs.yaml` - 端到端测试配置
- `pii_samples.json` - PII样本数据

---

## 2. 完整请求流程测试

### 2.1 TC-E2E-001: 正常请求完整流程（无PII）

**用例ID**: TC-E2E-001  
**用例名称**: 正常请求完整流程（无PII）  
**前置条件**:
1. LPG代理服务已启动并运行在默认端口8080
2. Presidio服务已启动并可访问
3. 目标LLM服务已启动并可访问
4. 已配置有效的API Key

**测试步骤**:
1. 使用CLI启动代理服务：`lpg start`
2. 使用curl向代理服务发送不包含PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [
         {"role": "user", "content": "请介绍一下人工智能的发展历史"}
       ]
     }'
   ```
3. 记录响应内容和状态码
4. 检查审计日志记录

**测试数据**:
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request_without_pii`
- 配置数据: `test_data/e2e_test_configs.yaml` 中的 `default_config`

**预期结果**:
1. 代理服务返回200状态码
2. 响应内容包含LLM返回的正常回答
3. 请求头中包含 `X-Request-ID` 和 `X-Processing-Time`
4. 审计日志记录请求处理过程，状态为"success"
5. 日志中显示PII检测结果为"无PII检测到"

**优先级**: P0  
**自动化**: 是

---

### 2.2 TC-E2E-002: 包含PII的请求完整流程

**用例ID**: TC-E2E-002  
**用例名称**: 包含PII的请求完整流程  
**前置条件**:
1. LPG代理服务已启动并运行在默认端口8080
2. Presidio服务已启动并可访问
3. 目标LLM服务已启动并可访问
4. 已配置有效的API Key
5. PII检测规则已启用

**测试步骤**:
1. 使用CLI启动代理服务：`lpg start`
2. 使用curl向代理服务发送包含PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [
         {"role": "user", "content": "我的邮箱是test@example.com，手机号是13800138000，身份证号是110105199001011234，请帮我处理这些信息"}
       ]
     }'
   ```
3. 记录响应内容和状态码
4. 检查审计日志记录
5. 验证PII脱敏结果

**测试数据**:
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `request_with_pii`
- PII样本: `test_data/pii_samples.json` 中的 `email_samples`, `phone_samples`, `id_card_samples`

**预期结果**:
1. 代理服务返回200状态码
2. 响应内容包含LLM返回的回答
3. 请求头中包含 `X-Request-ID` 和 `X-Processing-Time`
4. 审计日志记录PII检测结果：
   - 检测到EMAIL_ADDRESS实体
   - 检测到PHONE_NUMBER实体
   - 检测到ID_CARD实体
5. 审计日志记录脱敏操作
6. 发送给LLM的请求中PII已被脱敏

**优先级**: P0  
**自动化**: 是

---

### 2.3 TC-E2E-003: 流式请求完整流程

**用例ID**: TC-E2E-003  
**用例名称**: 流式请求完整流程  
**前置条件**:
1. LPG代理服务已启动并运行在默认端口8080
2. Presidio服务已启动并可访问
3. 目标LLM服务支持流式响应
4. 已配置有效的API Key

**测试步骤**:
1. 使用CLI启动代理服务：`lpg start`
2. 使用curl向代理服务发送流式请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [
         {"role": "user", "content": "请详细解释机器学习的基本概念"}
       ],
       "stream": true
     }'
   ```
3. 记录流式响应内容
4. 检查审计日志记录

**测试数据**:
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `stream_request`
- 配置数据: `test_data/e2e_test_configs.yaml` 中的 `stream_config`

**预期结果**:
1. 代理服务返回200状态码
2. 响应内容为SSE格式的数据流
3. 每个数据块包含 `data: ` 前缀
4. 最后一个数据块为 `data: [DONE]`
5. 审计日志记录流式请求处理过程
6. 请求头中包含 `X-Request-ID`

**优先级**: P1  
**自动化**: 否（需要流式响应验证工具）

---

### 2.4 TC-E2E-004: 多轮对话请求流程

**用例ID**: TC-E2E-004  
**用例名称**: 多轮对话请求流程  
**前置条件**:
1. LPG代理服务已启动并运行在默认端口8080
2. Presidio服务已启动并可访问
3. 目标LLM服务支持多轮对话
4. 已配置有效的API Key

**测试步骤**:
1. 使用CLI启动代理服务：`lpg start`
2. 发送第一轮对话请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [
         {"role": "user", "content": "你好，我叫张三，我的邮箱是zhangsan@example.com"}
       ]
     }'
   ```
3. 记录第一轮响应
4. 发送第二轮对话请求（包含上下文）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [
         {"role": "user", "content": "你好，我叫张三，我的邮箱是zhangsan@example.com"},
         {"role": "assistant", "content": "你好张三！很高兴认识你。"},
         {"role": "user", "content": "请记住我的邮箱地址，方便后续联系"}
       ]
     }'
   ```
5. 检查两轮对话的审计日志

**测试数据**:
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `multi_turn_request_1`, `multi_turn_request_2`
- PII样本: `test_data/pii_samples.json` 中的 `email_samples`

**预期结果**:
1. 两轮请求都返回200状态码
2. 第一轮请求中PII被脱敏
3. 第二轮请求中上下文信息被正确传递
4. 审计日志记录两轮对话的处理过程
5. 两轮请求的 `X-Request-ID` 不同

**优先级**: P1  
**自动化**: 是

---

## 3. CLI到代理服务集成测试

### 3.1 TC-E2E-005: CLI启动代理服务并处理请求

**用例ID**: TC-E2E-005  
**用例名称**: CLI启动代理服务并处理请求  
**前置条件**:
1. LPG已正确安装
2. 配置文件已正确设置
3. Presidio服务已启动
4. 目标LLM服务已启动

**测试步骤**:
1. 使用CLI启动代理服务：
   ```bash
   lpg start --host 127.0.0.1 --port 8080
   ```
2. 等待服务启动完成（检查日志输出）
3. 验证服务是否监听指定端口：
   ```bash
   netstat -an | grep 8080
   ```
4. 发送测试请求验证服务正常工作：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
5. 检查CLI输出日志

**测试数据**:
- 配置数据: `test_data/e2e_test_configs.yaml` 中的 `cli_start_config`
- 命令行参数: `--host 127.0.0.1 --port 8080`

**预期结果**:
1. CLI显示服务启动成功信息
2. 服务监听在指定的127.0.0.1:8080
3. 测试请求返回200状态码
4. CLI日志显示请求处理过程
5. 服务进程正常运行

**优先级**: P0  
**自动化**: 是

---

### 3.2 TC-E2E-006: CLI停止代理服务

**用例ID**: TC-E2E-006  
**用例名称**: CLI停止代理服务  
**前置条件**:
1. 代理服务已通过CLI启动并运行中
2. 服务监听在默认端口8080

**测试步骤**:
1. 验证服务正在运行：
   ```bash
   curl http://localhost:8080/health
   ```
2. 使用CLI停止代理服务：
   ```bash
   lpg stop
   ```
3. 等待服务停止（检查日志输出）
4. 验证服务已停止：
   ```bash
   curl http://localhost:8080/health
   ```
5. 检查端口是否已释放：
   ```bash
   netstat -an | grep 8080
   ```

**测试数据**:
- 配置数据: `test_data/e2e_test_configs.yaml` 中的 `default_config`

**预期结果**:
1. 停止前健康检查返回200状态码
2. CLI显示服务停止成功信息
3. 停止后健康检查返回连接拒绝或超时
4. 端口8080不再被监听
5. 服务进程已终止

**优先级**: P0  
**自动化**: 是

---

### 3.3 TC-E2E-007: CLI查看代理服务状态

**用例ID**: TC-E2E-007  
**用例名称**: CLI查看代理服务状态  
**前置条件**:
1. LPG已正确安装
2. 可能有服务运行，也可能没有

**测试步骤**:
1. 在没有服务运行时查看状态：
   ```bash
   lpg status
   ```
2. 启动代理服务：
   ```bash
   lpg start
   ```
3. 在有服务运行时查看状态：
   ```bash
   lpg status
   ```
4. 停止代理服务：
   ```bash
   lpg stop
   ```
5. 再次查看状态：
   ```bash
   lpg status
   ```

**测试数据**:
- 配置数据: `test_data/e2e_test_configs.yaml` 中的 `default_config`

**预期结果**:
1. 无服务运行时显示"服务未运行"或类似信息
2. 有服务运行时显示：
   - 服务状态：运行中
   - 监听地址和端口
   - 运行时间
   - 处理请求数量（如果可用）
3. 服务停止后显示"服务未运行"
4. 状态信息准确反映实际服务状态

**优先级**: P1  
**自动化**: 是

---

## 4. Key管理到代理服务集成测试

### 4.1 TC-E2E-008: 创建虚拟Key后使用Key请求

**用例ID**: TC-E2E-008  
**用例名称**: 创建虚拟Key后使用Key请求  
**前置条件**:
1. LPG代理服务已启动并运行
2. Key管理服务正常工作
3. 已配置管理员权限

**测试步骤**:
1. 使用CLI创建虚拟Key：
   ```bash
   lpg key create --name "测试Key" --provider "openai" --expires "2024-12-31"
   ```
2. 记录返回的虚拟Key（格式如 `lpg-vk-xxxxx`）
3. 使用新创建的虚拟Key发送请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer lpg-vk-xxxxx" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
4. 检查审计日志记录

**测试数据**:
- Key配置: `test_data/e2e_test_configs.yaml` 中的 `virtual_key_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 虚拟Key创建成功，返回Key ID和名称
2. 使用虚拟Key的请求返回200状态码
3. 请求被正确转发到目标LLM服务
4. 审计日志记录Key验证成功
5. 审计日志记录请求处理过程

**优先级**: P0  
**自动化**: 是

---

### 4.2 TC-E2E-009: 吊销虚拟Key后请求失败

**用例ID**: TC-E2E-009  
**用例名称**: 吊销虚拟Key后请求失败  
**前置条件**:
1. LPG代理服务已启动并运行
2. 已创建虚拟Key `lpg-vk-test-revoke`
3. 该Key可以正常请求

**测试步骤**:
1. 验证Key可以正常请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer lpg-vk-test-revoke" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
2. 使用CLI吊销虚拟Key：
   ```bash
   lpg key revoke lpg-vk-test-revoke
   ```
3. 使用已吊销的Key发送请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer lpg-vk-test-revoke" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
4. 检查审计日志记录

**测试数据**:
- Key配置: `test_data/e2e_test_configs.yaml` 中的 `revoked_key_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 吊销前请求返回200状态码
2. CLI显示Key吊销成功
3. 吊销后请求返回401状态码
4. 响应内容包含"Key已吊销"或类似错误信息
5. 审计日志记录Key验证失败原因

**优先级**: P0  
**自动化**: 是

---

### 4.3 TC-E2E-010: 过期虚拟Key请求失败

**用例ID**: TC-E2E-010  
**用例名称**: 过期虚拟Key请求失败  
**前置条件**:
1. LPG代理服务已启动并运行
2. 已创建虚拟Key `lpg-vk-test-expire`
3. 该Key设置为过去时间过期

**测试步骤**:
1. 使用CLI创建已过期的虚拟Key：
   ```bash
   lpg key create --name "过期Key" --provider "openai" --expires "2023-01-01"
   ```
2. 使用过期Key发送请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer lpg-vk-test-expire" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
3. 检查审计日志记录

**测试数据**:
- Key配置: `test_data/e2e_test_configs.yaml` 中的 `expired_key_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 过期Key创建成功
2. 使用过期Key的请求返回401状态码
3. 响应内容包含"Key已过期"或类似错误信息
4. 审计日志记录Key验证失败原因
5. 请求未被转发到目标LLM服务

**优先级**: P0  
**自动化**: 是

---

## 5. 规则管理到PII检测集成测试

### 5.1 TC-E2E-011: 启用规则后PII检测生效

**用例ID**: TC-E2E-011  
**用例名称**: 启用规则后PII检测生效  
**前置条件**:
1. LPG代理服务已启动并运行
2. PII检测规则已禁用
3. Presidio服务已启动

**测试步骤**:
1. 发送包含PII的请求（规则禁用状态）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
2. 使用CLI启用PII检测规则：
   ```bash
   lpg rule enable pii_detection
   ```
3. 发送包含相同PII的请求（规则启用状态）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
4. 检查两次请求的审计日志

**测试数据**:
- PII样本: `test_data/pii_samples.json` 中的 `email_samples`
- 规则配置: `test_data/e2e_test_configs.yaml` 中的 `pii_rules_config`

**预期结果**:
1. 规则禁用时，请求直接转发，无PII检测
2. 规则启用后，请求经过PII检测
3. 第二次请求中邮箱被脱敏处理
4. 审计日志显示两次请求的处理差异
5. 规则启用操作成功

**优先级**: P0  
**自动化**: 是

---

### 5.2 TC-E2E-012: 禁用规则后PII检测跳过

**用例ID**: TC-E2E-012  
**用例名称**: 禁用规则后PII检测跳过  
**前置条件**:
1. LPG代理服务已启动并运行
2. PII检测规则已启用
3. Presidio服务已启动

**测试步骤**:
1. 发送包含PII的请求（规则启用状态）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
2. 使用CLI禁用PII检测规则：
   ```bash
   lpg rule disable pii_detection
   ```
3. 发送包含相同PII的请求（规则禁用状态）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
4. 检查两次请求的审计日志

**测试数据**:
- PII样本: `test_data/pii_samples.json` 中的 `email_samples`
- 规则配置: `test_data/e2e_test_configs.yaml` 中的 `pii_rules_config`

**预期结果**:
1. 规则启用时，邮箱被脱敏处理
2. 规则禁用操作成功
3. 规则禁用后，邮箱未被脱敏，直接转发
4. 审计日志显示两次请求的处理差异
5. 规则状态变化被正确记录

**优先级**: P0  
**自动化**: 是

---

### 5.3 TC-E2E-013: 导入自定义规则后检测生效

**用例ID**: TC-E2E-013  
**用例名称**: 导入自定义规则后检测生效  
**前置条件**:
1. LPG代理服务已启动并运行
2. 已准备自定义规则文件 `custom_rules.yaml`
3. Presidio服务已启动

**测试步骤**:
1. 发送包含自定义PII的请求（使用默认规则）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的工号是EMP-12345"}]}'
   ```
2. 使用CLI导入自定义规则：
   ```bash
   lpg rule import custom_rules.yaml
   ```
3. 发送包含相同自定义PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的工号是EMP-12345"}]}'
   ```
4. 检查两次请求的审计日志

**测试数据**:
- 自定义规则: `test_data/e2e_test_configs.yaml` 中的 `custom_rules`
- 自定义PII样本: `test_data/pii_samples.json` 中的 `custom_pii_samples`

**预期结果**:
1. 导入前，自定义PII未被检测到
2. 自定义规则导入成功
3. 导入后，自定义PII被正确检测和脱敏
4. 审计日志记录规则导入操作
5. 审计日志显示两次请求的处理差异

**优先级**: P1  
**自动化**: 是

---

## 6. 配置管理集成测试

### 6.1 TC-E2E-014: 修改配置后服务行为变化

**用例ID**: TC-E2E-014  
**用例名称**: 修改配置后服务行为变化  
**前置条件**:
1. LPG代理服务已启动并运行
2. 配置文件可修改
3. 服务支持配置热重载或重启

**测试步骤**:
1. 记录当前配置的PII检测阈值（如0.5）
2. 发送测试请求，观察PII检测结果
3. 修改配置文件，将PII检测阈值改为0.9
4. 重新加载配置（`lpg reload` 或重启服务）
5. 发送相同测试请求，观察PII检测结果
6. 检查审计日志记录

**测试数据**:
- 配置文件: `test_data/e2e_test_configs.yaml` 中的 `threshold_config`
- PII样本: `test_data/pii_samples.json` 中的 `threshold_test_samples`

**预期结果**:
1. 配置修改前，低置信度PII被检测到
2. 配置修改后，低置信度PII未被检测到
3. 高置信度PII在两种配置下都被检测到
4. 审计日志记录配置变更操作
5. 服务行为随配置正确变化

**优先级**: P1  
**自动化**: 是

---

### 6.2 TC-E2E-015: 环境变量覆盖配置生效

**用例ID**: TC-E2E-015  
**用例名称**: 环境变量覆盖配置生效  
**前置条件**:
1. LPG代理服务支持环境变量配置
2. 配置文件中有默认值
3. 可以设置环境变量

**测试步骤**:
1. 查看当前配置的PII检测阈值（如0.5）
2. 设置环境变量覆盖配置：
   ```bash
   export LPG_PII_THRESHOLD=0.8
   ```
3. 启动代理服务：
   ```bash
   lpg start
   ```
4. 发送测试请求，观察PII检测结果
5. 检查服务日志，确认使用的配置值
6. 清除环境变量，重启服务
7. 再次发送测试请求，观察结果差异

**测试数据**:
- 环境变量: `LPG_PII_THRESHOLD=0.8`
- 配置文件: `test_data/e2e_test_configs.yaml` 中的 `threshold_config`
- PII样本: `test_data/pii_samples.json` 中的 `threshold_test_samples`

**预期结果**:
1. 环境变量设置后，服务使用0.8作为阈值
2. 中置信度PII（0.5-0.8）未被检测到
3. 高置信度PII（>0.8）被检测到
4. 服务日志显示使用环境变量配置
5. 清除环境变量后，恢复默认配置

**优先级**: P1  
**自动化**: 否（需要环境变量操作）

---

## 7. 审计日志集成测试

### 7.1 TC-E2E-016: 请求处理后审计日志记录

**用例ID**: TC-E2E-016  
**用例名称**: 请求处理后审计日志记录  
**前置条件**:
1. LPG代理服务已启动并运行
2. 审计日志服务正常工作
3. 日志级别设置为INFO或更低

**测试步骤**:
1. 清空或备份当前审计日志
2. 发送正常请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试请求"}]}'
   ```
3. 检查审计日志文件
4. 发送包含PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
5. 再次检查审计日志文件

**测试数据**:
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`, `pii_request`
- 日志配置: `test_data/e2e_test_configs.yaml` 中的 `audit_log_config`

**预期结果**:
1. 正常请求的审计日志包含：
   - 请求ID
   - 时间戳
   - 请求路径
   - 处理状态
   - 处理时间
2. PII请求的审计日志额外包含：
   - PII检测结果
   - 脱敏操作记录
3. 日志格式符合配置要求
4. 日志内容准确反映请求处理过程

**优先级**: P0  
**自动化**: 是

---

### 7.2 TC-E2E-017: 异常请求审计日志记录

**用例ID**: TC-E2E-017  
**用例名称**: 异常请求审计日志记录  
**前置条件**:
1. LPG代理服务已启动并运行
2. 审计日志服务正常工作
3. 日志级别设置为INFO或更低

**测试步骤**:
1. 清空或备份当前审计日志
2. 发送无效Key的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer invalid-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
3. 发送格式错误的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"invalid": "json"}'
   ```
4. 发送超大请求（超过限制）：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "非常长的文本..."}]}'
   ```
5. 检查审计日志文件

**测试数据**:
- 异常请求: `test_data/e2e_test_payloads.json` 中的 `invalid_key_request`, `malformed_request`, `oversized_request`
- 日志配置: `test_data/e2e_test_configs.yaml` 中的 `audit_log_config`

**预期结果**:
1. 无效Key请求的审计日志记录：
   - 请求ID
   - 错误类型：Key验证失败
   - 错误详情
2. 格式错误请求的审计日志记录：
   - 请求ID
   - 错误类型：请求格式错误
   - 错误详情
3. 超大请求的审计日志记录：
   - 请求ID
   - 错误类型：请求大小超限
   - 错误详情
4. 所有异常请求都有完整的错误上下文
5. 日志级别为ERROR或WARNING

**优先级**: P0  
**自动化**: 是

---

## 8. 错误处理集成测试

### 8.1 TC-E2E-018: Presidio服务不可用时降级处理

**用例ID**: TC-E2E-018  
**用例名称**: Presidio服务不可用时降级处理  
**前置条件**:
1. LPG代理服务已启动并运行
2. Presidio服务已停止或不可达
3. 已配置降级策略（跳过PII检测或拒绝请求）

**测试步骤**:
1. 停止Presidio服务
2. 发送包含PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com"}]}'
   ```
3. 检查响应状态码和内容
4. 检查审计日志记录
5. 重新启动Presidio服务
6. 发送相同请求，验证恢复正常

**测试数据**:
- 降级配置: `test_data/e2e_test_configs.yaml` 中的 `fallback_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `pii_request`

**预期结果**:
1. 根据配置，可能的行为：
   - **跳过检测**: 请求被转发，PII未被脱敏，返回200状态码
   - **拒绝请求**: 返回503状态码，提示服务不可用
2. 审计日志记录Presidio连接失败
3. 审计日志记录降级处理方式
4. 响应头中包含降级处理标识
5. Presidio恢复后，PII检测功能恢复正常

**优先级**: P0  
**自动化**: 是

---

### 8.2 TC-E2E-019: 目标LLM服务不可用时错误处理

**用例ID**: TC-E2E-019  
**用例名称**: 目标LLM服务不可用时错误处理  
**前置条件**:
1. LPG代理服务已启动并运行
2. 目标LLM服务已停止或不可达
3. Presidio服务正常

**测试步骤**:
1. 停止目标LLM服务
2. 发送请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
3. 检查响应状态码和内容
4. 检查审计日志记录
5. 重新启动目标LLM服务
6. 发送相同请求，验证恢复正常

**测试数据**:
- 重试配置: `test_data/e2e_test_configs.yaml` 中的 `retry_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 返回502或503状态码
2. 响应内容包含"目标服务不可用"或类似错误信息
3. 审计日志记录LLM服务连接失败
4. 审计日志记录重试操作（如果配置了重试）
5. LLM服务恢复后，请求处理恢复正常

**优先级**: P0  
**自动化**: 是

---

### 8.3 TC-E2E-020: 网络异常时错误处理

**用例ID**: TC-E2E-020  
**用例名称**: 网络异常时错误处理  
**前置条件**:
1. LPG代理服务已启动并运行
2. 网络环境可以模拟异常（如超时、断网）
3. 已配置超时时间

**测试步骤**:
1. 模拟网络超时（如限制带宽或延迟）
2. 发送请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "测试"}]}'
   ```
3. 检查响应状态码和内容
4. 检查审计日志记录
5. 恢复正常网络
6. 发送相同请求，验证恢复正常

**测试数据**:
- 超时配置: `test_data/e2e_test_configs.yaml` 中的 `timeout_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 超时情况下返回504状态码
2. 响应内容包含"请求超时"或类似错误信息
3. 审计日志记录网络超时错误
4. 审计日志记录超时时间
5. 网络恢复后，请求处理恢复正常

**优先级**: P1  
**自动化**: 否（需要网络环境控制）

---

## 9. 并发场景集成测试

### 9.1 TC-E2E-021: 并发请求处理

**用例ID**: TC-E2E-021  
**用例名称**: 并发请求处理  
**前置条件**:
1. LPG代理服务已启动并运行
2. 服务支持并发处理
3. 有足够的系统资源

**测试步骤**:
1. 使用并发测试工具（如Apache Bench或wrk）发送并发请求：
   ```bash
   ab -n 100 -c 10 -H "Authorization: Bearer sk-test-key" \
      -H "Content-Type: application/json" \
      -p request.json \
      http://localhost:8080/v1/chat/completions
   ```
2. 或使用Python脚本发送并发请求
3. 监控系统资源使用情况
4. 检查所有请求的响应状态码
5. 检查审计日志记录

**测试数据**:
- 并发配置: `test_data/e2e_test_configs.yaml` 中的 `concurrency_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 所有请求都返回200状态码（或可接受的错误率）
2. 平均响应时间在可接受范围内
3. 系统资源使用正常（CPU、内存）
4. 审计日志记录所有请求
5. 没有请求丢失或重复处理

**优先级**: P1  
**自动化**: 是

---

### 9.2 TC-E2E-022: 并发Key操作

**用例ID**: TC-E2E-022  
**用例名称**: 并发Key操作  
**前置条件**:
1. LPG代理服务已启动并运行
2. Key管理服务支持并发操作
3. 有足够的系统资源

**测试步骤**:
1. 使用脚本并发创建多个虚拟Key
2. 使用脚本并发验证这些Key
3. 使用脚本并发吊销部分Key
4. 使用脚本并发使用已吊销的Key发送请求
5. 检查所有操作的结果
6. 检查审计日志记录

**测试数据**:
- Key配置: `test_data/e2e_test_configs.yaml` 中的 `concurrent_key_config`
- 操作脚本: `test_data/e2e_test_payloads.json` 中的 `key_operations`

**预期结果**:
1. 所有Key创建操作成功
2. 所有Key验证操作正确
3. 所有Key吊销操作成功
4. 使用已吊销Key的请求返回401状态码
5. 没有Key状态不一致的情况
6. 审计日志记录所有操作

**优先级**: P1  
**自动化**: 是

---

## 10. 性能场景集成测试

### 10.1 TC-E2E-023: 大量请求处理性能

**用例ID**: TC-E2E-023  
**用例名称**: 大量请求处理性能  
**前置条件**:
1. LPG代理服务已启动并运行
2. 有足够的系统资源
3. 目标LLM服务可以处理大量请求

**测试步骤**:
1. 使用性能测试工具发送大量请求（如1000个请求）
2. 监控系统资源使用情况
3. 记录响应时间分布
4. 检查错误率
5. 检查审计日志记录

**测试数据**:
- 性能配置: `test_data/e2e_test_configs.yaml` 中的 `performance_config`
- 请求数据: `test_data/e2e_test_payloads.json` 中的 `normal_request`

**预期结果**:
1. 总体成功率 > 99%
2. 平均响应时间 < 2秒
3. 95%分位响应时间 < 5秒
4. 系统资源使用稳定
5. 没有内存泄漏
6. 审计日志记录所有请求

**优先级**: P2  
**自动化**: 是

---

### 10.2 TC-E2E-024: 大文本PII检测性能

**用例ID**: TC-E2E-024  
**用例名称**: 大文本PII检测性能  
**前置条件**:
1. LPG代理服务已启动并运行
2. Presidio服务可以处理大文本
3. 有足够的系统资源

**测试步骤**:
1. 准备大文本请求（如10KB、100KB、1MB）
2. 发送大文本请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "大文本内容..."}]}'
   ```
3. 监控系统资源使用情况
4. 记录响应时间
5. 检查PII检测结果

**测试数据**:
- 大文本样本: `test_data/pii_samples.json` 中的 `large_text_samples`
- 性能配置: `test_data/e2e_test_configs.yaml` 中的 `large_text_config`

**预期结果**:
1. 所有大小的文本都能被正确处理
2. 大文本处理时间在可接受范围内
3. PII检测结果正确
4. 系统资源使用正常
5. 没有内存溢出或超时

**优先级**: P2  
**自动化**: 是

---

## 11. 安全场景集成测试

### 11.1 TC-E2E-025: API Key安全存储

**用例ID**: TC-E2E-025  
**用例名称**: API Key安全存储  
**前置条件**:
1. LPG代理服务已启动并运行
2. 已创建虚拟Key
3. 可以访问存储介质

**测试步骤**:
1. 创建虚拟Key：
   ```bash
   lpg key create --name "安全测试Key" --provider "openai"
   ```
2. 检查Key存储位置（如数据库或文件）
3. 验证Key是否加密存储
4. 尝试直接读取存储的Key值
5. 使用CLI获取Key信息：
   ```bash
   lpg key list
   ```
6. 验证CLI显示的Key信息是否脱敏

**测试数据**:
- Key配置: `test_data/e2e_test_configs.yaml` 中的 `key_storage_config`
- 安全配置: `test_data/e2e_test_configs.yaml` 中的 `security_config`

**预期结果**:
1. Key在存储介质中加密存储
2. 直接读取存储的Key值是加密后的密文
3. CLI显示的Key信息脱敏（如显示后四位）
4. 只有授权操作可以获取完整Key
5. 审计日志记录Key访问操作

**优先级**: P0  
**自动化**: 否（需要存储介质访问）

---

### 11.2 TC-E2E-026: 敏感数据内存清理

**用例ID**: TC-E2E-026  
**用例名称**: 敏感数据内存清理  
**前置条件**:
1. LPG代理服务已启动并运行
2. 可以监控内存使用
3. 有内存分析工具

**测试步骤**:
1. 发送包含PII的请求：
   ```bash
   curl -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer sk-test-key" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "我的邮箱是test@example.com，手机号是13800138000"}]}'
   ```
2. 使用内存分析工具检查内存中的PII数据
3. 等待一段时间（如GC运行）
4. 再次检查内存中的PII数据
5. 发送多个请求，检查内存使用趋势

**测试数据**:
- 安全配置: `test_data/e2e_test_configs.yaml` 中的 `memory_config`
- PII样本: `test_data/pii_samples.json` 中的 `email_samples`, `phone_samples`

**预期结果**:
1. 请求处理完成后，PII数据从内存中清除
2. 内存中不保留明文PII数据
3. 内存使用稳定，没有持续增长
4. 敏感数据在使用后及时清理
5. 审计日志记录内存清理操作（如果配置）

**优先级**: P1  
**自动化**: 否（需要内存分析工具）

---

## 12. 测试执行指南

### 12.1 测试环境准备
1. 安装LPG及其依赖
2. 启动Presidio服务
3. 启动目标LLM服务
4. 配置测试环境
5. 准备测试数据

### 12.2 测试执行顺序
1. 先执行基础功能测试（TC-E2E-001到TC-E2E-004）
2. 再执行集成测试（TC-E2E-005到TC-E2E-017）
3. 最后执行特殊场景测试（TC-E2E-018到TC-E2E-026）

### 12.3 测试结果记录
1. 记录每个测试用例的执行结果
2. 收集相关日志和证据
3. 分析失败原因
4. 提交缺陷报告

### 12.4 测试数据清理
1. 测试完成后清理测试数据
2. 停止所有服务
3. 恢复原始配置

---

## 13. 附录

### 13.1 测试数据文件列表
- `test_data/e2e_test_payloads.json` - 端到端测试请求数据
- `test_data/e2e_test_configs.yaml` - 端到端测试配置
- `test_data/pii_samples.json` - PII样本数据

### 13.2 测试工具列表
- `curl` - HTTP请求工具
- `ab` - Apache Bench性能测试工具
- `netstat` - 网络端口检查工具
- `jq` - JSON处理工具

### 13.3 相关文档
- 设计文档：`doc/design/v1.0/`
- 单元测试用例：`doc/test/tcs/v1.0/01_cli_commands.md` 到 `07_configuration.md`
- 测试数据文档：`doc/test/tcs/v1.0/*_testdata.md`
