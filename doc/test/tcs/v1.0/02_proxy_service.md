# LLM Privacy Gateway v1.0 - 代理服务黑盒测试用例

## 概述

本文档定义 LLM Privacy Gateway v1.0 代理服务模块的黑盒测试用例，覆盖代理服务器的启动/停止、请求转发、流式响应、错误处理、并发处理、健康检查及统计信息等核心功能。

## 测试用例概览

| 用例ID | 名称 | 优先级 | 自动化 |
|--------|------|--------|--------|
| TC-PROXY-001 | 默认参数启动代理服务器 | P0 | 是 |
| TC-PROXY-002 | 自定义端口启动代理服务器 | P0 | 是 |
| TC-PROXY-003 | 自定义host启动代理服务器 | P1 | 是 |
| TC-PROXY-004 | 后台模式启动代理服务器 | P1 | 是 |
| TC-PROXY-005 | 正常停止代理服务器 | P0 | 是 |
| TC-PROXY-006 | 强制停止代理服务器 | P1 | 是 |
| TC-PROXY-007 | 重复启动检测 | P0 | 是 |
| TC-PROXY-008 | 正常转发POST请求到/v1/chat/completions | P0 | 是 |
| TC-PROXY-009 | 正常转发POST请求到/v1/completions | P0 | 是 |
| TC-PROXY-010 | 正常转发POST请求到/v1/embeddings | P0 | 是 |
| TC-PROXY-011 | 转发GET请求 | P1 | 是 |
| TC-PROXY-012 | 转发带query参数的请求 | P1 | 是 |
| TC-PROXY-013 | 转发大请求体 | P1 | 是 |
| TC-PROXY-014 | 正常处理流式响应 | P0 | 是 |
| TC-PROXY-015 | 流式响应中断处理 | P1 | 是 |
| TC-PROXY-016 | 流式响应超时处理 | P1 | 是 |
| TC-PROXY-017 | 目标服务器连接失败 | P0 | 是 |
| TC-PROXY-018 | 目标服务器超时 | P0 | 是 |
| TC-PROXY-019 | 目标服务器返回4xx错误 | P1 | 是 |
| TC-PROXY-020 | 目标服务器返回5xx错误 | P1 | 是 |
| TC-PROXY-021 | 请求体格式错误 | P1 | 是 |
| TC-PROXY-022 | 响应体格式错误 | P2 | 是 |
| TC-PROXY-023 | 并发请求处理 | P1 | 是 |
| TC-PROXY-024 | 最大连接数限制 | P2 | 是 |
| TC-PROXY-025 | 请求队列管理 | P2 | 否 |
| TC-PROXY-026 | /health端点正常响应 | P0 | 是 |
| TC-PROXY-027 | 服务状态信息正确 | P1 | 是 |
| TC-PROXY-028 | 请求数统计正确 | P1 | 是 |
| TC-PROXY-029 | 成功/失败数统计正确 | P1 | 是 |
| TC-PROXY-030 | 平均延迟计算正确 | P2 | 是 |
| TC-PROXY-031 | PII检测数统计正确 | P1 | 是 |
| TC-PROXY-032 | 运行时间计算正确 | P2 | 是 |

## 详细测试用例

### 1. 代理服务器启动/停止

#### TC-PROXY-001: 默认参数启动代理服务器

**用例ID**: TC-PROXY-001  
**用例名称**: 默认参数启动代理服务器  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. LLM Privacy Gateway 已正确安装
2. 默认配置文件已存在
3. 端口 8080 未被占用
4. 目标 LLM 服务可访问

**测试步骤**:
1. 执行启动命令：`lpg proxy start`
2. 等待服务启动完成（最多 10 秒）
3. 检查服务状态：`lpg status`
4. 尝试访问健康检查端点：`curl http://localhost:8080/health`
5. 停止服务：`lpg proxy stop`

**测试数据**:
- 配置文件: `tests/data/configs/default_config.yaml`
- 请求数据: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 启动命令返回成功信息，包含 PID
2. 服务状态显示为 "running"，端口为 8080
3. 健康检查返回 HTTP 200，响应包含 `{"status": "ok"}`
4. 服务日志无错误信息
5. 进程 PID 与启动时一致

---

#### TC-PROXY-002: 自定义端口启动代理服务器

**用例ID**: TC-PROXY-002  
**用例名称**: 自定义端口启动代理服务器  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. LLM Privacy Gateway 已正确安装
2. 端口 9090 未被占用
3. 目标 LLM 服务可访问

**测试步骤**:
1. 执行启动命令：`lpg proxy start --port 9090`
2. 等待服务启动完成
3. 检查服务状态：`lpg status`
4. 尝试访问健康检查端点：`curl http://localhost:9090/health`
5. 停止服务

**测试数据**:
- 配置文件: `tests/data/configs/default_config.yaml`

**预期结果**:
1. 启动命令返回成功信息
2. 服务状态显示端口为 9090
3. 健康检查返回 HTTP 200
4. 旧端口 8080 无服务响应

---

#### TC-PROXY-003: 自定义host启动代理服务器

**用例ID**: TC-PROXY-003  
**用例名称**: 自定义host启动代理服务器  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. LLM Privacy Gateway 已正确安装
2. 网络接口 192.168.1.100 可用
3. 防火墙允许该地址访问

**测试步骤**:
1. 执行启动命令：`lpg proxy start --host 192.168.1.100`
2. 等待服务启动完成
3. 从本机访问：`curl http://192.168.1.100:8080/health`
4. 从其他机器访问（如有条件）
5. 停止服务

**测试数据**:
- 配置文件: `tests/data/configs/default_config.yaml`

**预期结果**:
1. 服务绑定到指定 IP 地址
2. 通过指定 IP 可正常访问服务
3. localhost 无法访问（除非同时监听）

---

#### TC-PROXY-004: 后台模式启动代理服务器

**用例ID**: TC-PROXY-004  
**用例名称**: 后台模式启动代理服务器  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. LLM Privacy Gateway 已正确安装
2. 当前无服务运行

**测试步骤**:
1. 执行后台启动命令：`lpg proxy start --daemon`
2. 检查进程是否存在：`ps aux | grep lpg`
3. 检查服务状态：`lpg status`
4. 访问健康检查端点
5. 停止服务

**测试数据**:
- 配置文件: `tests/data/configs/default_config.yaml`

**预期结果**:
1. 命令立即返回，不阻塞终端
2. 进程在后台运行
3. 服务正常响应请求
4. 日志文件中有运行记录

---

#### TC-PROXY-005: 正常停止代理服务器

**用例ID**: TC-PROXY-005  
**用例名称**: 正常停止代理服务器  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正在运行
2. 无正在进行的请求

**测试步骤**:
1. 记录当前 PID
2. 执行停止命令：`lpg proxy stop`
3. 等待停止完成（最多 5 秒）
4. 检查进程是否终止：`ps aux | grep lpg`
5. 尝试访问服务端点

**测试数据**:
- 无

**预期结果**:
1. 停止命令返回成功信息
2. 进程正常终止
3. 服务不再响应请求
4. 端口被释放

---

#### TC-PROXY-006: 强制停止代理服务器

**用例ID**: TC-PROXY-006  
**用例名称**: 强制停止代理服务器  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正在运行
2. 存在长时间运行的请求

**测试步骤**:
1. 启动一个长时间运行的流式请求
2. 执行强制停止命令：`lpg proxy stop --force`
3. 检查进程是否立即终止
4. 检查日志中的终止记录

**测试数据**:
- 流式请求: `tests/data/requests/stream_request.json`

**预期结果**:
1. 强制停止命令立即生效
2. 进程被强制终止
3. 正在处理的请求被中断
4. 日志记录强制停止事件

---

#### TC-PROXY-007: 重复启动检测

**用例ID**: TC-PROXY-007  
**用例名称**: 重复启动检测  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务已在运行

**测试步骤**:
1. 记录当前服务 PID
2. 尝试再次启动：`lpg proxy start`
3. 检查返回的错误信息
4. 验证原服务仍在运行

**测试数据**:
- 无

**预期结果**:
1. 启动命令失败，返回明确的错误信息
2. 错误信息提示服务已在运行
3. 包含当前运行实例的 PID
4. 原服务继续正常运行

---

### 2. 请求转发

#### TC-PROXY-008: 正常转发POST请求到/v1/chat/completions

**用例ID**: TC-PROXY-008  
**用例名称**: 正常转发POST请求到/v1/chat/completions  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标 LLM 服务可访问
3. API Key 有效

**测试步骤**:
1. 构造标准 chat completions 请求
2. 发送 POST 请求到代理服务：`curl -X POST http://localhost:8080/v1/chat/completions`
3. 验证请求头和请求体
4. 检查响应状态码和响应体
5. 验证请求被正确转发到目标服务

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`
- 期望响应: `tests/data/responses/chat_completion_response.json`

**预期结果**:
1. 返回 HTTP 200 状态码
2. 响应体格式符合 OpenAI API 规范
3. 包含有效的 `id`, `choices`, `usage` 字段
4. 代理日志记录转发过程
5. 统计信息中请求数增加

---

#### TC-PROXY-009: 正常转发POST请求到/v1/completions

**用例ID**: TC-PROXY-009  
**用例名称**: 正常转发POST请求到/v1/completions  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标 LLM 服务支持 completions 端点

**测试步骤**:
1. 构造标准 completions 请求
2. 发送 POST 请求到代理服务：`curl -X POST http://localhost:8080/v1/completions`
3. 验证请求转发
4. 检查响应格式

**测试数据**:
- 请求体: `tests/data/requests/valid_completion_request.json`
- 期望响应: `tests/data/responses/completion_response.json`

**预期结果**:
1. 返回 HTTP 200 状态码
2. 响应体格式符合规范
3. 包含 `choices` 数组
4. 代理正确转发请求

---

#### TC-PROXY-010: 正常转发POST请求到/v1/embeddings

**用例ID**: TC-PROXY-010  
**用例名称**: 正常转发POST请求到/v1/embeddings  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标 LLM 服务支持 embeddings 端点

**测试步骤**:
1. 构造 embeddings 请求
2. 发送 POST 请求到代理服务：`curl -X POST http://localhost:8080/v1/embeddings`
3. 验证请求转发
4. 检查响应格式

**测试数据**:
- 请求体: `tests/data/requests/valid_embedding_request.json`
- 期望响应: `tests/data/responses/embedding_response.json`

**预期结果**:
1. 返回 HTTP 200 状态码
2. 响应体包含 `data` 数组
3. 每个嵌入向量维度正确
4. 代理正确转发请求

---

#### TC-PROXY-011: 转发GET请求

**用例ID**: TC-PROXY-011  
**用例名称**: 转发GET请求  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务支持 GET 请求

**测试步骤**:
1. 发送 GET 请求到代理服务
2. 检查请求是否被正确转发
3. 验证响应

**测试数据**:
- 请求URL: `http://localhost:8080/v1/models`

**预期结果**:
1. GET 请求被正确转发
2. 返回目标服务的响应
3. 查询参数被保留

---

#### TC-PROXY-012: 转发带query参数的请求

**用例ID**: TC-PROXY-012  
**用例名称**: 转发带query参数的请求  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行

**测试步骤**:
1. 构造带查询参数的请求
2. 发送请求到代理服务
3. 验证查询参数被正确转发

**测试数据**:
- 请求URL: `http://localhost:8080/v1/models?limit=10&offset=0`

**预期结果**:
1. 查询参数完整保留
2. 请求被正确转发
3. 响应符合预期

---

#### TC-PROXY-013: 转发大请求体

**用例ID**: TC-PROXY-013  
**用例名称**: 转发大请求体  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务支持大请求体

**测试步骤**:
1. 构造大请求体（>1MB）
2. 发送 POST 请求到代理服务
3. 验证请求被正确转发
4. 检查响应

**测试数据**:
- 大请求体: `tests/data/requests/large_request.json` (约 2MB)

**预期结果**:
1. 大请求体被正确处理
2. 请求被完整转发
3. 返回正确响应
4. 无内存溢出错误

---

### 3. 流式响应（SSE）

#### TC-PROXY-014: 正常处理流式响应

**用例ID**: TC-PROXY-014  
**用例名称**: 正常处理流式响应  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务支持流式响应

**测试步骤**:
1. 构造流式请求（`"stream": true`）
2. 发送请求到代理服务
3. 验证响应为 SSE 格式
4. 检查多个 chunk 是否正确传递
5. 验证流结束标记

**测试数据**:
- 流式请求: `tests/data/requests/stream_request.json`
- 期望SSE格式: `tests/data/responses/stream_response_pattern.txt`

**预期结果**:
1. 响应 Content-Type 为 `text/event-stream`
2. 收到多个 SSE 事件
3. 每个事件格式正确：`data: {...}\n\n`
4. 最后一个事件为 `data: [DONE]\n\n`
5. 无数据丢失或重复

---

#### TC-PROXY-015: 流式响应中断处理

**用例ID**: TC-PROXY-015  
**用例名称**: 流式响应中断处理  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 流式响应正在进行

**测试步骤**:
1. 启动流式请求
2. 在响应过程中断开客户端连接
3. 检查代理服务日志
4. 验证资源被正确释放

**测试数据**:
- 流式请求: `tests/data/requests/stream_request.json`

**预期结果**:
1. 代理检测到客户端断开
2. 日志记录中断事件
3. 与目标服务的连接被关闭
4. 无资源泄漏
5. 统计信息正确记录

---

#### TC-PROXY-016: 流式响应超时处理

**用例ID**: TC-PROXY-016  
**用例名称**: 流式响应超时处理  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务配置了流式超时时间
2. 目标服务响应缓慢

**测试步骤**:
1. 配置较短的流式超时时间
2. 发送流式请求到慢响应服务
3. 等待超时发生
4. 检查错误处理

**测试数据**:
- 流式请求: `tests/data/requests/stream_request.json`
- 超时配置: `tests/data/configs/short_timeout_config.yaml`

**预期结果**:
1. 超时后代理中断流式响应
2. 返回适当的错误信息
3. 日志记录超时事件
4. 资源被正确释放

---

### 4. 错误处理

#### TC-PROXY-017: 目标服务器连接失败

**用例ID**: TC-PROXY-017  
**用例名称**: 目标服务器连接失败  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务器不可达

**测试步骤**:
1. 配置不可达的目标服务器地址
2. 发送请求到代理服务
3. 检查错误响应
4. 验证错误处理逻辑

**测试数据**:
- 配置文件: `tests/data/configs/unreachable_target_config.yaml`
- 请求体: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 返回 HTTP 502 Bad Gateway
2. 响应体包含清晰的错误信息
3. 日志记录连接失败详情
4. 统计信息中失败数增加
5. 服务继续运行，不影响其他请求

---

#### TC-PROXY-018: 目标服务器超时

**用例ID**: TC-PROXY-018  
**用例名称**: 目标服务器超时  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务配置了超时时间
2. 目标服务器响应缓慢

**测试步骤**:
1. 配置较短的超时时间
2. 发送请求到慢响应服务
3. 等待超时发生
4. 检查错误响应

**测试数据**:
- 配置文件: `tests/data/configs/short_timeout_config.yaml`
- 请求体: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 返回 HTTP 504 Gateway Timeout
2. 响应体包含超时错误信息
3. 日志记录超时详情
4. 统计信息中失败数增加

---

#### TC-PROXY-019: 目标服务器返回4xx错误

**用例ID**: TC-PROXY-019  
**用例名称**: 目标服务器返回4xx错误  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务器将返回 4xx 错误

**测试步骤**:
1. 构造会导致 4xx 错误的请求（如无效 API Key）
2. 发送请求到代理服务
3. 检查错误是否被正确传递

**测试数据**:
- 请求体: `tests/data/requests/invalid_api_key_request.json`
- 期望错误: `tests/data/responses/401_error_response.json`

**预期结果**:
1. 代理返回目标服务器的 4xx 状态码
2. 错误响应体被正确传递
3. 代理不修改错误内容
4. 日志记录转发的错误

---

#### TC-PROXY-020: 目标服务器返回5xx错误

**用例ID**: TC-PROXY-020  
**用例名称**: 目标服务器返回5xx错误  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务器将返回 5xx 错误

**测试步骤**:
1. 发送请求到将返回 5xx 的服务
2. 检查错误响应
3. 验证重试逻辑（如配置）

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`
- 期望错误: `tests/data/responses/500_error_response.json`

**预期结果**:
1. 代理返回 5xx 状态码
2. 错误响应体被传递
3. 如配置重试，执行重试逻辑
4. 日志记录错误详情

---

#### TC-PROXY-021: 请求体格式错误

**用例ID**: TC-PROXY-021  
**用例名称**: 请求体格式错误  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行

**测试步骤**:
1. 发送格式错误的 JSON 请求体
2. 检查代理的验证逻辑
3. 验证错误响应

**测试数据**:
- 错误请求体: `tests/data/requests/invalid_json_request.txt`

**预期结果**:
1. 代理返回 HTTP 400 Bad Request
2. 错误信息说明 JSON 解析失败
3. 请求未被转发到目标服务
4. 日志记录验证错误

---

#### TC-PROXY-022: 响应体格式错误

**用例ID**: TC-PROXY-022  
**用例名称**: 响应体格式错误  
**优先级**: P2  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 目标服务返回格式错误的响应

**测试步骤**:
1. 配置返回错误格式响应的服务
2. 发送请求到代理
3. 检查代理的处理方式

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`
- 错误响应: `tests/data/responses/invalid_json_response.txt`

**预期结果**:
1. 代理尝试解析响应
2. 如解析失败，返回适当的错误
3. 日志记录响应解析错误
4. 统计信息正确更新

---

### 5. 并发处理

#### TC-PROXY-023: 并发请求处理

**用例ID**: TC-PROXY-023  
**用例名称**: 并发请求处理  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 支持并发请求处理

**测试步骤**:
1. 同时发送 10 个并发请求
2. 记录每个请求的响应时间
3. 验证所有请求都被正确处理
4. 检查资源使用情况

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`
- 并发脚本: `tests/scripts/concurrent_requests.py`

**预期结果**:
1. 所有请求都被正确处理
2. 无请求丢失
3. 响应时间在合理范围内
4. 无资源竞争错误
5. 统计信息正确更新

---

#### TC-PROXY-024: 最大连接数限制

**用例ID**: TC-PROXY-024  
**用例名称**: 最大连接数限制  
**优先级**: P2  
**自动化**: 是  

**前置条件**:
1. 代理服务配置了最大连接数限制
2. 当前连接数未达上限

**测试步骤**:
1. 配置较小的最大连接数（如 5）
2. 发送超过限制的并发请求
3. 观察超出限制的请求处理
4. 检查错误响应

**测试数据**:
- 配置文件: `tests/data/configs/max_connections_config.yaml`
- 请求体: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 超出限制的请求被拒绝或排队
2. 返回 HTTP 503 Service Unavailable 或排队提示
3. 日志记录连接数超限
4. 已建立的连接正常处理

---

#### TC-PROXY-025: 请求队列管理

**用例ID**: TC-PROXY-025  
**用例名称**: 请求队列管理  
**优先级**: P2  
**自动化**: 否  

**前置条件**:
1. 代理服务配置了请求队列
2. 队列容量有限

**测试步骤**:
1. 配置请求队列容量
2. 发送大量并发请求
3. 观察队列行为
4. 检查队列满时的处理

**测试数据**:
- 配置文件: `tests/data/configs/queue_config.yaml`
- 请求体: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 请求按 FIFO 顺序处理
2. 队列满时新请求被拒绝
3. 返回适当的错误信息
4. 日志记录队列状态

---

### 6. 健康检查

#### TC-PROXY-026: /health端点正常响应

**用例ID**: TC-PROXY-026  
**用例名称**: /health端点正常响应  
**优先级**: P0  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行

**测试步骤**:
1. 发送 GET 请求到 `/health`
2. 检查响应状态码
3. 验证响应体格式
4. 检查响应时间

**测试数据**:
- 无

**预期结果**:
1. 返回 HTTP 200 状态码
2. 响应体包含 `{"status": "ok"}`
3. 响应时间 < 100ms
4. 无额外的认证要求

---

#### TC-PROXY-027: 服务状态信息正确

**用例ID**: TC-PROXY-027  
**用例名称**: 服务状态信息正确  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 服务已处理一些请求

**测试步骤**:
1. 发送请求到 `/health` 或 `/status` 端点
2. 检查返回的状态信息
3. 验证各项指标

**测试数据**:
- 期望字段: `tests/data/responses/status_response_schema.json`

**预期结果**:
1. 包含服务版本信息
2. 包含运行时间
3. 包含请求统计
4. 包含资源使用情况
5. 信息准确无误

---

### 7. 统计信息

#### TC-PROXY-028: 请求数统计正确

**用例ID**: TC-PROXY-028  
**用例名称**: 请求数统计正确  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 统计计数器已重置

**测试步骤**:
1. 记录初始请求数
2. 发送 N 个请求（如 5 个）
3. 查询统计信息
4. 验证请求数增加 N

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`
- 期望统计: `tests/data/responses/stats_response.json`

**预期结果**:
1. 统计信息中请求数增加正确
2. 包含各类请求的分类统计
3. 数值准确无误

---

#### TC-PROXY-029: 成功/失败数统计正确

**用例ID**: TC-PROXY-029  
**用例名称**: 成功/失败数统计正确  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 统计计数器已重置

**测试步骤**:
1. 发送成功请求和失败请求
2. 查询统计信息
3. 验证成功/失败计数

**测试数据**:
- 成功请求: `tests/data/requests/valid_chat_request.json`
- 失败请求: `tests/data/requests/invalid_request.json`

**预期结果**:
1. 成功请求数正确增加
2. 失败请求数正确增加
3. 分类统计准确
4. 总数等于成功数 + 失败数

---

#### TC-PROXY-030: 平均延迟计算正确

**用例ID**: TC-PROXY-030  
**用例名称**: 平均延迟计算正确  
**优先级**: P2  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 统计计数器已重置

**测试步骤**:
1. 发送多个请求并记录响应时间
2. 计算实际平均延迟
3. 查询统计信息中的平均延迟
4. 验证计算准确性

**测试数据**:
- 请求体: `tests/data/requests/valid_chat_request.json`

**预期结果**:
1. 平均延迟计算准确
2. 误差在合理范围内（<5%）
3. 包含最大/最小延迟
4. 延迟单位明确

---

#### TC-PROXY-031: PII检测数统计正确

**用例ID**: TC-PROXY-031  
**用例名称**: PII检测数统计正确  
**优先级**: P1  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. PII 检测功能已启用
3. 统计计数器已重置

**测试步骤**:
1. 发送包含 PII 的请求
2. 发送不包含 PII 的请求
3. 查询统计信息
4. 验证 PII 检测计数

**测试数据**:
- 包含PII请求: `tests/data/requests/pii_request.json`
- 不含PII请求: `tests/data/requests/no_pii_request.json`

**预期结果**:
1. PII 检测数正确增加
2. 包含各类 PII 的分类统计
3. 数值与实际检测结果一致

---

#### TC-PROXY-032: 运行时间计算正确

**用例ID**: TC-PROXY-032  
**用例名称**: 运行时间计算正确  
**优先级**: P2  
**自动化**: 是  

**前置条件**:
1. 代理服务正常运行
2. 记录服务启动时间

**测试步骤**:
1. 记录当前时间和服务启动时间
2. 查询统计信息中的运行时间
3. 验证计算准确性

**测试数据**:
- 无

**预期结果**:
1. 运行时间计算准确
2. 格式清晰（如 "2h30m15s"）
3. 误差在合理范围内（<1 秒）
4. 自动更新

---

## 测试数据文件说明

### 请求数据
- `tests/data/requests/valid_chat_request.json` - 标准 chat completions 请求
- `tests/data/requests/valid_completion_request.json` - 标准 completions 请求
- `tests/data/requests/valid_embedding_request.json` - 标准 embeddings 请求
- `tests/data/requests/stream_request.json` - 流式响应请求
- `tests/data/requests/large_request.json` - 大请求体（>1MB）
- `tests/data/requests/pii_request.json` - 包含 PII 的请求
- `tests/data/requests/no_pii_request.json` - 不包含 PII 的请求
- `tests/data/requests/invalid_request.json` - 格式错误的请求
- `tests/data/requests/invalid_api_key_request.json` - 无效 API Key 请求
- `tests/data/requests/invalid_json_request.txt` - 无效 JSON 格式

### 响应数据
- `tests/data/responses/chat_completion_response.json` - 期望的 chat completion 响应
- `tests/data/responses/completion_response.json` - 期望的 completion 响应
- `tests/data/responses/embedding_response.json` - 期望的 embedding 响应
- `tests/data/responses/stream_response_pattern.txt` - SSE 响应格式模式
- `tests/data/responses/401_error_response.json` - 401 错误响应示例
- `tests/data/responses/500_error_response.json` - 500 错误响应示例
- `tests/data/responses/invalid_json_response.txt` - 无效 JSON 响应
- `tests/data/responses/status_response_schema.json` - 状态响应结构定义
- `tests/data/responses/stats_response.json` - 统计信息响应结构

### 配置文件
- `tests/data/configs/default_config.yaml` - 默认配置
- `tests/data/configs/short_timeout_config.yaml` - 短超时配置
- `tests/data/configs/unreachable_target_config.yaml` - 不可达目标配置
- `tests/data/configs/max_connections_config.yaml` - 最大连接数配置
- `tests/data/configs/queue_config.yaml` - 请求队列配置

### 测试脚本
- `tests/scripts/concurrent_requests.py` - 并发请求测试脚本

---

## 执行说明

### 手动执行
1. 启动代理服务
2. 按照测试步骤执行
3. 验证预期结果
4. 记录实际结果

### 自动化执行
```bash
# 运行所有代理服务测试
pytest tests/integration/test_proxy_service.py -v

# 运行特定测试类
pytest tests/integration/test_proxy_service.py::TestProxyStartStop -v

# 运行特定测试用例
pytest tests/integration/test_proxy_service.py -k "TC-PROXY-001" -v
```

---

## 修订记录

| 版本 | 日期 | 修订人 | 修订内容 |
|------|------|--------|----------|
| 1.0 | 2026-04-04 | - | 初始版本 |