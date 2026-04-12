# 代理服务测试数据

本文档提供代理服务测试的测试数据，旨在覆盖95%以上的代码分支。

## 1. 服务器启动测试数据

### 有效端口

| 端口 | 说明 | 预期结果 |
|------|------|----------|
| 8080 | 常用代理端口 | 启动成功 |
| 80 | HTTP标准端口 | 启动成功（可能需要root权限） |
| 443 | HTTPS标准端口 | 启动成功（可能需要root权限） |
| 3000 | 常用开发端口 | 启动成功 |
| 9000 | 常用服务端口 | 启动成功 |
| 65535 | 最大有效端口 | 启动成功 |

### 无效端口

| 端口 | 说明 | 预期结果 |
|------|------|----------|
| 0 | 保留端口 | 启动失败，抛出`ConfigError` |
| -1 | 负数端口 | 启动失败，抛出`ConfigError` |
| 65536 | 超出范围 | 启动失败，抛出`ConfigError` |
| 99999 | 超出范围 | 启动失败，抛出`ConfigError` |
| "abc" | 非数字 | 启动失败，抛出`ConfigError` |
| "" | 空字符串 | 启动失败，抛出`ConfigError` |

### 有效Host

| Host | 说明 | 预期结果 |
|------|------|----------|
| 127.0.0.1 | 回环地址 | 启动成功 |
| 0.0.0.0 | 监听所有接口 | 启动成功 |
| localhost | 主机名 | 启动成功 |

### 无效Host

| Host | 说明 | 预期结果 |
|------|------|----------|
| 999.999.999.999 | 无效IP | 启动失败，抛出`ConfigError` |
| "abc" | 无效主机名 | 启动失败，抛出`ConfigError` |
| "" | 空字符串 | 启动失败，抛出`ConfigError` |

## 2. 请求测试数据

### OpenAI格式请求体

#### Chat/Completions 请求

**基础请求：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}
```

**带系统消息的请求：**
```json
{
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the weather today?"}
    ],
    "temperature": 0.5
}
```

**带历史对话的请求：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you today?"},
        {"role": "user", "content": "What's the capital of France?"}
    ]
}
```

#### Completions 请求

```json
{
    "model": "text-davinci-003",
    "prompt": "Once upon a time",
    "max_tokens": 50,
    "temperature": 0.8
}
```

#### Embeddings 请求

```json
{
    "model": "text-embedding-ada-002",
    "input": "The quick brown fox jumps over the lazy dog"
}
```

### 流式请求

**stream=true 请求：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true,
    "max_tokens": 200
}
```

**stream=false 请求：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "What is 2+2?"}
    ],
    "stream": false
}
```

### 边界条件请求

**空messages数组：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": []
}
```

**超长messages数组（100条消息）：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Response 1"},
        {"role": "user", "content": "Message 2"},
        {"role": "assistant", "content": "Response 2"},
        // ... 重复98次
        {"role": "user", "content": "Message 100"}
    ]
}
```

**包含PII的请求内容：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "我的邮箱是test@example.com，电话是13800138000"}
    ]
}
```

**不包含PII的请求内容：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "今天天气怎么样？"}
    ]
}
```

**特殊字符内容：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello! @#$%^&*()_+-=[]{}|;':\",./<>?"}
    ]
}
```

**Unicode内容：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "你好！😊 🚀 ⭐"}
    ]
}
```

**多语言内容：**
```json
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello, 你好, こんにちは, 안녕하세요, Bonjour"}
    ]
}
```

## 3. 请求头测试数据

### Authorization头

**有效Bearer token：**
```
Authorization: Bearer sk-1234567890abcdef
```

**有效x-api-key头：**
```
x-api-key: sk-1234567890abcdef
```

**无效Authorization头：**
```
Authorization: InvalidTokenFormat
```

**缺少Authorization头：**
（无Authorization头）

**Content-Type为application/json：**
```
Content-Type: application/json
```

**Content-Type为其他值：**
```
Content-Type: text/plain
```

## 4. 响应测试数据

### 成功响应

**200 成功响应（非流式）：**
```json
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "Hello! How can I assist you today?"
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 12,
        "total_tokens": 21
    }
}
```

**200 成功响应（流式）：**
```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-3.5-turbo","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-3.5-turbo","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-3.5-turbo","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1677652288,"model":"gpt-3.5-turbo","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

### 客户端错误

**400 错误请求：**
```json
{
    "error": {
        "message": "Invalid request: missing required field 'model'",
        "type": "invalid_request_error",
        "param": null,
        "code": null
    }
}
```

**401 未授权：**
```json
{
    "error": {
        "message": "Incorrect API key provided",
        "type": "invalid_request_error",
        "param": null,
        "code": "invalid_api_key"
    }
}
```

**403 禁止访问：**
```json
{
    "error": {
        "message": "You don't have permission to access this resource",
        "type": "access_denied",
        "param": null,
        "code": "access_denied"
    }
}
```

**404 未找到：**
```json
{
    "error": {
        "message": "Resource not found",
        "type": "not_found",
        "param": null,
        "code": "not_found"
    }
}
```

### 服务器错误

**500 内部服务器错误：**
```json
{
    "error": {
        "message": "Internal server error",
        "type": "server_error",
        "param": null,
        "code": "internal_error"
    }
}
```

**502 网关错误：**
```json
{
    "error": {
        "message": "Bad gateway",
        "type": "server_error",
        "param": null,
        "code": "bad_gateway"
    }
}
```

**503 服务不可用：**
```json
{
    "error": {
        "message": "Service temporarily unavailable",
        "type": "server_error",
        "param": null,
        "code": "service_unavailable"
    }
}
```

**504 网关超时：**
```json
{
    "error": {
        "message": "Gateway timeout",
        "type": "server_error",
        "param": null,
        "code": "gateway_timeout"
    }
}
```

### 超时响应

**连接超时：**
```
Connection timeout after 30 seconds
```

**读取超时：**
```
Read timeout after 60 seconds
```

### 大响应体

**大响应体（10KB）：**
```json
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "Very long response content..."
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 2500,
        "total_tokens": 2510
    }
}
```

### 包含PII的响应内容

**包含邮箱和电话的响应：**
```json
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "您的邮箱是user@example.com，电话是13800138000"
        },
        "finish_reason": "stop"
    }]
}
```

## 5. 并发测试数据

### 并发请求数量

| 并发数 | 说明 | 预期结果 |
|--------|------|----------|
| 1 | 单个请求 | 正常处理 |
| 10 | 少量并发 | 正常处理 |
| 50 | 中等并发 | 正常处理 |
| 100 | 高并发 | 正常处理，可能有性能下降 |

### 并发请求间隔

| 间隔 | 说明 | 预期结果 |
|------|------|----------|
| 0ms | 无间隔 | 测试最大并发能力 |
| 10ms | 短间隔 | 测试高并发能力 |
| 100ms | 长间隔 | 测试持续负载能力 |

### 不同端点的并发请求

**混合端点并发：**
- 50% chat/completions 请求
- 30% completions 请求
- 20% embeddings 请求

## 6. 超时测试数据

### 请求超时时间

| 超时时间 | 说明 | 预期结果 |
|----------|------|----------|
| 1s | 极短超时 | 大多数请求超时 |
| 30s | 标准超时 | 正常请求完成 |
| 60s | 长超时 | 长时间请求完成 |
| 120s | 极长超时 | 最复杂请求完成 |

### 连接超时时间

| 超时时间 | 说明 | 预期结果 |
|----------|------|----------|
| 1s | 极短连接超时 | 连接可能失败 |
| 5s | 标准连接超时 | 正常连接建立 |
| 10s | 长连接超时 | 确保连接建立 |

### 读取超时时间

| 超时时间 | 说明 | 预期结果 |
|----------|------|----------|
| 1s | 极短读取超时 | 大多数读取超时 |
| 30s | 标准读取超时 | 正常读取完成 |
| 60s | 长读取超时 | 大响应读取完成 |

## 7. 错误场景测试数据

### 目标服务器不可达

**测试配置：**
- 目标URL：`http://192.0.2.1:8080` (TEST-NET-1，不可达)
- 预期结果：连接超时或拒绝连接

### 目标服务器拒绝连接

**测试配置：**
- 目标URL：`http://127.0.0.1:9999` (未监听的端口)
- 预期结果：连接被拒绝

### 目标服务器返回错误响应

**测试配置：**
- 目标URL：`http://httpstat.us/500` (返回500错误)
- 预期结果：返回500错误响应

### 网络中断

**测试方法：**
- 在请求过程中断开网络
- 预期结果：网络错误异常

### DNS解析失败

**测试配置：**
- 目标URL：`http://nonexistent.domain.example` (无效域名)
- 预期结果：DNS解析失败

## 8. 统计信息测试数据

### 初始统计数据

```json
{
    "start_time": 1677652288,
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_bytes_sent": 0,
    "total_bytes_received": 0,
    "average_response_time": 0,
    "uptime_seconds": 0
}
```

### 请求后统计数据

**单个成功请求后：**
```json
{
    "start_time": 1677652288,
    "total_requests": 1,
    "successful_requests": 1,
    "failed_requests": 0,
    "total_bytes_sent": 256,
    "total_bytes_received": 512,
    "average_response_time": 0.5,
    "uptime_seconds": 10
}
```

**多个请求后：**
```json
{
    "start_time": 1677652288,
    "total_requests": 100,
    "successful_requests": 95,
    "failed_requests": 5,
    "total_bytes_sent": 25600,
    "total_bytes_received": 51200,
    "average_response_time": 0.75,
    "uptime_seconds": 3600
}
```

### 错误后统计数据

**包含错误的统计：**
```json
{
    "start_time": 1677652288,
    "total_requests": 50,
    "successful_requests": 40,
    "failed_requests": 10,
    "total_bytes_sent": 12800,
    "total_bytes_received": 20480,
    "average_response_time": 1.2,
    "uptime_seconds": 1800,
    "error_breakdown": {
        "timeout": 5,
        "connection_refused": 3,
        "internal_error": 2
    }
}
```

### 运行时间计算

**运行1小时后：**
```json
{
    "start_time": 1677652288,
    "current_time": 1677655888,
    "uptime_seconds": 3600,
    "uptime_formatted": "1h 0m 0s"
}
```

**运行1天后：**
```json
{
    "start_time": 1677652288,
    "current_time": 1677738688,
    "uptime_seconds": 86400,
    "uptime_formatted": "1d 0h 0m 0s"
}
```

## 9. 测试数据使用说明

### 测试执行顺序

1. **服务器启动测试**：验证各种配置下的服务器启动
2. **基础功能测试**：使用正常请求验证基本功能
3. **边界条件测试**：测试各种边界和异常情况
4. **并发测试**：验证并发处理能力
5. **超时测试**：验证超时处理机制
6. **错误场景测试**：验证错误处理能力
7. **统计验证**：检查统计数据准确性

### 覆盖率要求

- **代码行覆盖率**：≥ 95%
- **分支覆盖率**：≥ 95%
- **函数覆盖率**：100%

### 测试环境要求

- **Python版本**：3.8+
- **依赖包**：aiohttp, pytest, pytest-asyncio
- **网络环境**：可访问外网（用于真实API测试）

## 10. 附加测试数据

### 性能基准数据

**基准响应时间（P95）：**
- 简单请求：< 100ms
- 复杂请求：< 500ms
- 流式请求首字节：< 200ms

**基准吞吐量：**
- 单实例：100 req/s
- 集群模式：1000 req/s

### 内存使用基准

**基础内存占用：**
- 空闲状态：< 50MB
- 100并发连接：< 200MB
- 1000并发连接：< 500MB

### 日志级别测试数据

| 日志级别 | 预期输出 | 用途 |
|----------|----------|------|
| DEBUG | 详细调试信息 | 开发调试 |
| INFO | 正常操作信息 | 生产环境 |
| WARNING | 警告信息 | 潜在问题 |
| ERROR | 错误信息 | 错误处理 |
| CRITICAL | 严重错误 | 系统故障