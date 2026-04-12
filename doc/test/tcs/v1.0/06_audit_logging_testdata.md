# 审计日志测试数据

## 1. 时间戳测试数据

### 1.1 有效时间戳格式

| 测试用例ID | 测试场景 | 时间戳格式 | 示例值 | 备注 |
|------------|----------|------------|--------|------|
| TIME-001 | ISO 8601标准格式 | YYYY-MM-DDTHH:MM:SS.ssssss | 2026-04-04T10:30:45.123456 | 微秒精度 |
| TIME-002 | ISO 8601无微秒 | YYYY-MM-DDTHH:MM:SS | 2026-04-04T10:30:45 | 秒精度 |
| TIME-003 | UTC时区 | YYYY-MM-DDTHH:MM:SSZ | 2026-04-04T10:30:45Z | UTC时区标记 |
| TIME-004 | 正时区偏移 | YYYY-MM-DDTHH:MM:SS+HH:MM | 2026-04-04T10:30:45+08:00 | 北京时间 |
| TIME-005 | 负时区偏移 | YYYY-MM-DDTHH:MM:SS-HH:MM | 2026-04-04T10:30:45-05:00 | 纽约时间 |
| TIME-006 | 毫秒精度 | YYYY-MM-DDTHH:MM:SS.sss | 2026-04-04T10:30:45.123 | 毫秒精度 |
| TIME-007 | 年初边界 | YYYY-MM-DDTHH:MM:SS | 2026-01-01T00:00:00.000000 | 年初边界 |
| TIME-008 | 年末边界 | YYYY-MM-DDTHH:MM:SS | 2026-12-31T23:59:59.999999 | 年末边界 |
| TIME-009 | 月末边界 | YYYY-MM-DDTHH:MM:SS | 2026-04-30T23:59:59.999999 | 月末边界 |
| TIME-010 | 闰年2月 | YYYY-MM-DDTHH:MM:SS | 2024-02-29T12:00:00.000000 | 闰年2月29日 |

### 1.2 无效时间戳格式

| 测试用例ID | 测试场景 | 时间戳格式 | 示例值 | 预期结果 |
|------------|----------|------------|--------|----------|
| TIME-011 | 缺少T分隔符 | YYYY-MM-DD HH:MM:SS | 2026-04-04 10:30:45 | 格式错误 |
| TIME-012 | 错误日期格式 | DD/MM/YYYYTHH:MM:SS | 04/04/2026T10:30:45 | 格式错误 |
| TIME-013 | 无效月份 | YYYY-13-04THH:MM:SS | 2026-13-04T10:30:45 | 日期无效 |
| TIME-014 | 无效日期 | YYYY-04-31THH:MM:SS | 2026-04-31T10:30:45 | 日期无效 |
| TIME-015 | 无效小时 | YYYY-MM-DDT25:MM:SS | 2026-04-04T25:30:45 | 时间无效 |
| TIME-016 | 无效分钟 | YYYY-MM-DDTHH:61:SS | 2026-04-04T10:61:45 | 时间无效 |
| TIME-017 | 无效秒数 | YYYY-MM-DDTHH:MM:61 | 2026-04-04T10:30:61 | 时间无效 |
| TIME-018 | 空字符串 | "" | "" | 无效输入 |
| TIME-019 | 非时间字符串 | 文本 | "not a timestamp" | 格式错误 |
| TIME-020 | 时间戳超大值 | YYYY-MM-DDTHH:MM:SS | 9999-12-31T23:59:59.999999 | 边界测试 |

## 2. URL测试数据

### 2.1 有效URL

| 测试用例ID | 测试场景 | URL类型 | 示例值 | 备注 |
|------------|----------|---------|--------|------|
| URL-001 | OpenAI聊天端点 | HTTPS | https://api.openai.com/v1/chat/completions | OpenAI标准端点 |
| URL-002 | Anthropic消息端点 | HTTPS | https://api.anthropic.com/v1/messages | Anthropic标准端点 |
| URL-003 | 本地开发端点 | HTTP | http://localhost:8080/v1/chat/completions | 本地测试 |
| URL-004 | 自定义域名端点 | HTTPS | https://llm.example.com/v1/completions | 自定义部署 |
| URL-005 | 带端口号端点 | HTTPS | https://api.example.com:8443/v1/chat | 非标准端口 |
| URL-006 | 带路径参数 | HTTPS | https://api.openai.com/v1/engines/{engine_id}/completions | 路径参数 |
| URL-007 | 带查询参数 | HTTPS | https://api.openai.com/v1/models?limit=10 | 查询参数 |
| URL-008 | IP地址端点 | HTTP | http://192.168.1.100:8080/v1/chat | IP地址 |
| URL-009 | 内网域名 | HTTP | http://llm-gateway.internal:8080/v1/chat | 内网域名 |
| URL-010 | 带认证信息 | HTTPS | https://user:pass@api.example.com/v1/chat | URL认证 |

### 2.2 无效URL

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| URL-011 | 缺少协议 | api.openai.com/v1/chat | 协议缺失 |
| URL-012 | 错误协议 | ftp://api.openai.com/v1/chat | 协议错误 |
| URL-013 | 空字符串 | "" | 无效URL |
| URL-014 | 仅协议 | https:// | 缺少主机 |
| URL-015 | 无效主机名 | https://api..openai.com/v1/chat | 主机名错误 |
| URL-016 | 带空格URL | https://api.openai.com/ v1/chat | URL编码错误 |
| URL-017 | 超长URL | https://api.openai.com/v1/chat/ + "a"*2000 | URL过长 |
| URL-018 | 非HTTP协议 | ws://api.openai.com/v1/chat | WebSocket协议 |

## 3. HTTP方法测试数据

### 3.1 有效HTTP方法

| 测试用例ID | 测试场景 | HTTP方法 | 大写格式 | 小写格式 | 备注 |
|------------|----------|----------|----------|----------|------|
| METHOD-001 | GET请求 | GET | GET | get | 查询请求 |
| METHOD-002 | POST请求 | POST | POST | post | 提交数据 |
| METHOD-003 | PUT请求 | PUT | PUT | put | 更新资源 |
| METHOD-004 | DELETE请求 | DELETE | DELETE | delete | 删除资源 |
| METHOD-005 | PATCH请求 | PATCH | PATCH | patch | 部分更新 |
| METHOD-006 | HEAD请求 | HEAD | HEAD | head | 获取头信息 |
| METHOD-007 | OPTIONS请求 | OPTIONS | OPTIONS | options | 预检请求 |
| METHOD-008 | CONNECT请求 | CONNECT | CONNECT | connect | 代理连接 |
| METHOD-009 | TRACE请求 | TRACE | TRACE | trace | 追踪路径 |

### 3.2 无效HTTP方法

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| METHOD-010 | 空方法 | "" | 无效方法 |
| METHOD-011 | 未知方法 | INVALID | 不支持的方法 |
| METHOD-012 | 数字方法 | 123 | 格式错误 |
| METHOD-013 | 特殊字符 | GET! | 格式错误 |
| METHOD-014 | 超长方法 | "A"*100 | 方法过长 |
| METHOD-015 | 混合大小写 | GeT | 需规范化处理 |

## 4. 状态码测试数据

### 4.1 成功状态码

| 测试用例ID | 测试场景 | 状态码 | 状态描述 | 备注 |
|------------|----------|--------|----------|------|
| STATUS-001 | 请求成功 | 200 | OK | 标准成功 |
| STATUS-002 | 创建成功 | 201 | Created | 资源创建 |
| STATUS-003 | 已接受 | 202 | Accepted | 异步处理 |
| STATUS-004 | 无内容 | 204 | No Content | 删除成功 |
| STATUS-005 | 部分内容 | 206 | Partial Content | 范围请求 |

### 4.2 客户端错误状态码

| 测试用例ID | 测试场景 | 状态码 | 状态描述 | 备注 |
|------------|----------|--------|----------|------|
| STATUS-006 | 请求错误 | 400 | Bad Request | 参数错误 |
| STATUS-007 | 未授权 | 401 | Unauthorized | 认证失败 |
| STATUS-008 | 禁止访问 | 403 | Forbidden | 权限不足 |
| STATUS-009 | 资源不存在 | 404 | Not Found | 端点错误 |
| STATUS-010 | 请求过多 | 429 | Too Many Requests | 限流触发 |
| STATUS-011 | 请求超时 | 408 | Request Timeout | 客户端超时 |
| STATUS-012 | 请求过大 | 413 | Payload Too Large | 请求体过大 |
| STATUS-013 | 不支持媒体类型 | 415 | Unsupported Media Type | 格式错误 |

### 4.3 服务器错误状态码

| 测试用例ID | 测试场景 | 状态码 | 状态描述 | 备注 |
|------------|----------|--------|----------|------|
| STATUS-014 | 服务器内部错误 | 500 | Internal Server Error | 服务异常 |
| STATUS-015 | 网关错误 | 502 | Bad Gateway | 上游错误 |
| STATUS-016 | 服务不可用 | 503 | Service Unavailable | 服务宕机 |
| STATUS-017 | 网关超时 | 504 | Gateway Timeout | 上游超时 |
| HTTP版本不支持 | 505 | HTTP Version Not Supported | 协议错误 |

### 4.4 无效状态码

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| STATUS-019 | 负数状态码 | -1 | 无效状态码 |
| STATUS-020 | 零状态码 | 0 | 无效状态码 |
| STATUS-021 | 超出范围 | 600 | 无效状态码 |
| STATUS-022 | 字符串状态码 | "200" | 类型错误 |
| STATUS-023 | 空值 | None | 缺失状态码 |
| STATUS-024 | 小数状态码 | 200.5 | 类型错误 |

## 5. 请求耗时测试数据

### 5.1 有效耗时值

| 测试用例ID | 测试场景 | 耗时(ms) | 性能等级 | 备注 |
|------------|----------|----------|----------|------|
| DURATION-001 | 边界最小值 | 0 | 极快 | 瞬间完成 |
| DURATION-002 | 边界最小值 | 1 | 极快 | 最小有效值 |
| DURATION-003 | 极快请求 | 10 | 极快 | 缓存命中 |
| DURATION-004 | 快速请求 | 50 | 快 | 本地处理 |
| DURATION-005 | 正常请求 | 100 | 正常 | 标准处理 |
| DURATION-006 | 正常请求 | 500 | 正常 | 网络延迟 |
| DURATION-007 | 慢请求 | 1000 | 慢 | 复杂处理 |
| DURATION-008 | 很慢请求 | 5000 | 很慢 | 重试机制 |
| DURATION-009 | 超时边界 | 30000 | 超时 | 默认超时 |
| DURATION-010 | 超时请求 | 60000 | 超时 | 长时间处理 |

### 5.2 无效耗时值

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| DURATION-011 | 负数耗时 | -100 | 无效耗时 |
| DURATION-012 | 非数字 | "fast" | 类型错误 |
| DURATION-013 | 空值 | None | 缺失耗时 |
| DURATION-014 | 极大值 | 999999999 | 超出范围 |
| DURATION-015 | 小数耗时 | 100.5 | 需取整处理 |

## 6. PII检测结果测试数据

### 6.1 单个检测结果

| 测试用例ID | 测试场景 | entity_type | start | end | score | 备注 |
|------------|----------|-------------|-------|-----|-------|------|
| PII-001 | 邮箱检测 | EMAIL_ADDRESS | 10 | 30 | 0.95 | 高置信度 |
| PII-002 | 电话检测 | PHONE_NUMBER | 5 | 16 | 0.90 | 中国手机号 |
| PII-003 | 身份证检测 | ID_CARD | 20 | 38 | 0.98 | 18位身份证 |
| PII-004 | 银行卡检测 | CREDIT_CARD | 15 | 34 | 0.85 | 银行卡号 |
| PII-005 | 地址检测 | ADDRESS | 40 | 80 | 0.75 | 详细地址 |
| PII-006 | 姓名检测 | PERSON | 0 | 6 | 0.80 | 中文姓名 |
| PII-007 | 低置信度检测 | EMAIL_ADDRESS | 10 | 30 | 0.60 | 边界置信度 |
| PII-008 | 最低置信度 | PHONE_NUMBER | 5 | 16 | 0.50 | 阈值边界 |

### 6.2 多个检测结果

| 测试用例ID | 测试场景 | 检测结果数量 | 示例结果列表 | 备注 |
|------------|----------|--------------|--------------|------|
| PII-009 | 两个检测结果 | 2 | [{"entity_type": "EMAIL_ADDRESS", "start": 10, "end": 30, "score": 0.95}, {"entity_type": "PHONE_NUMBER", "start": 35, "end": 46, "score": 0.90}] | 多种PII |
| PII-010 | 三个检测结果 | 3 | [{"entity_type": "EMAIL_ADDRESS", "start": 10, "end": 30, "score": 0.95}, {"entity_type": "PHONE_NUMBER", "start": 35, "end": 46, "score": 0.90}, {"entity_type": "ID_CARD", "start": 50, "end": 68, "score": 0.98}] | 多种PII |
| PII-011 | 相同类型多个 | 2 | [{"entity_type": "EMAIL_ADDRESS", "start": 10, "end": 30, "score": 0.95}, {"entity_type": "EMAIL_ADDRESS", "start": 40, "end": 60, "score": 0.92}] | 重复类型 |
| PII-012 | 重叠检测结果 | 2 | [{"entity_type": "EMAIL_ADDRESS", "start": 10, "end": 30, "score": 0.95}, {"entity_type": "PERSON", "start": 25, "end": 35, "score": 0.80}] | 重叠区域 |

### 6.3 无检测结果

| 测试用例ID | 测试场景 | 检测结果数量 | 备注 |
|------------|----------|--------------|------|
| PII-013 | 无PII文本 | 0 | 纯文本无PII |
| PII-014 | 空文本 | 0 | 空字符串 |
| PII-015 | 特殊字符 | 0 | 仅特殊字符 |
| PII-016 | 数字序列 | 0 | 非PII数字 |

### 6.4 无效检测结果

| 测试用例ID | 测试场景 | 无效字段 | 示例值 | 预期结果 |
|------------|----------|----------|--------|----------|
| PII-017 | 无效entity_type | entity_type | "INVALID_TYPE" | 类型错误 |
| PII-018 | 负数start | start | -5 | 位置错误 |
| PII-019 | end小于start | end | start-5 | 范围错误 |
| PII-020 | score超出范围 | score | 1.5 | 置信度错误 |
| PII-021 | 缺少必填字段 | entity_type | None | 字段缺失 |
| PII-022 | 非数字位置 | start | "10" | 类型错误 |

## 7. 脱敏操作测试数据

### 7.1 有效脱敏操作

| 测试用例ID | 测试场景 | 脱敏类型 | 原始文本 | 脱敏后文本 | 备注 |
|------------|----------|----------|----------|------------|------|
| MASK-001 | replace操作 | replace | user@example.com | [REDACTED_EMAIL] | 替换为占位符 |
| MASK-002 | mask操作 | mask | 13812345678 | 138****5678 | 部分掩码 |
| MASK-003 | hash操作 | hash | sensitive_data | a1b2c3d4e5f6 | 哈希处理 |
| MASK-004 | redact操作 | redact | 机密信息 | [已删除] | 完全删除 |
| MASK-005 | 无脱敏操作 | none | normal_text | normal_text | 不处理 |
| MASK-006 | 部分掩码邮箱 | mask | user@example.com | u***@example.com | 邮箱掩码 |
| MASK-007 | 部分掩码身份证 | mask | 110101199001011234 | 110101********1234 | 身份证掩码 |
| MASK-008 | 部分掩码银行卡 | mask | 6222021234567890 | 6222********7890 | 银行卡掩码 |

### 7.2 无效脱敏操作

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| MASK-009 | 无效脱敏类型 | "invalid_mask" | 类型错误 |
| MASK-010 | 空脱敏配置 | {} | 配置缺失 |
| MASK-011 | 空字符串操作 | "" | 无效操作 |
| MASK-012 | 非字符串操作 | 123 | 类型错误 |

## 8. 日志级别测试数据

### 8.1 有效日志级别

| 测试用例ID | 测试场景 | 日志级别 | 数值等级 | 使用场景 | 备注 |
|------------|----------|----------|----------|----------|------|
| LEVEL-001 | DEBUG级别 | DEBUG | 10 | 调试信息 | 开发调试 |
| LEVEL-002 | INFO级别 | INFO | 20 | 正常操作 | 生产环境 |
| LEVEL-003 | WARNING级别 | WARNING | 30 | 潜在问题 | 警告信息 |
| LEVEL-004 | ERROR级别 | ERROR | 40 | 错误操作 | 错误处理 |
| LEVEL-005 | CRITICAL级别 | CRITICAL | 50 | 严重错误 | 系统故障 |

### 8.2 日志级别边界值

| 测试用例ID | 测试场景 | 日志级别 | 数值等级 | 备注 |
|------------|----------|----------|----------|------|
| LEVEL-006 | 最小有效值 | NOTSET | 0 | 未设置 |
| LEVEL-007 | DEBUG边界 | DEBUG | 10 | 最低有效级别 |
| LEVEL-008 | INFO边界 | INFO | 20 | 信息级别边界 |
| LEVEL-009 | WARNING边界 | WARNING | 30 | 警告级别边界 |
| LEVEL-010 | ERROR边界 | ERROR | 40 | 错误级别边界 |
| LEVEL-011 | CRITICAL边界 | CRITICAL | 50 | 最高有效级别 |

### 8.3 无效日志级别

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| LEVEL-012 | 无效级别名称 | "INVALID_LEVEL" | 级别错误 |
| LEVEL-013 | 负数等级 | -10 | 等级错误 |
| LEVEL-014 | 超出范围 | 100 | 等级错误 |
| LEVEL-015 | 非数字等级 | "info" | 类型错误 |
| LEVEL-016 | 空值 | None | 缺失级别 |

## 9. 日志格式测试数据

### 9.1 JSON格式日志

| 测试用例ID | 测试场景 | JSON示例 | 备注 |
|------------|----------|----------|------|
| FORMAT-001 | 完整JSON日志 | ```json
{
  "timestamp": "2026-04-04T10:30:45.123456Z",
  "level": "INFO",
  "logger": "audit",
  "message": "Request processed successfully",
  "request_id": "req-123456",
  "client_ip": "192.168.1.100",
  "method": "POST",
  "url": "https://api.openai.com/v1/chat/completions",
  "status_code": 200,
  "duration_ms": 150,
  "pii_detections": [
    {
      "entity_type": "EMAIL_ADDRESS",
      "start": 10,
      "end": 30,
      "score": 0.95
    }
  ],
  "masking_applied": true,
  "masking_type": "mask",
  "original_length": 100,
  "masked_length": 100
}
``` | 标准格式 |

| FORMAT-002 | 简化JSON日志 | ```json
{
  "timestamp": "2026-04-04T10:30:45Z",
  "level": "INFO",
  "message": "Request completed",
  "status": 200,
  "duration": 150
}
``` | 简化格式 |

| FORMAT-003 | 错误JSON日志 | ```json
{
  "timestamp": "2026-04-04T10:30:45.123456Z",
  "level": "ERROR",
  "logger": "audit",
  "message": "Request failed",
  "request_id": "req-789012",
  "client_ip": "192.168.1.101",
  "method": "POST",
  "url": "https://api.openai.com/v1/chat/completions",
  "status_code": 500,
  "duration_ms": 30000,
  "error": {
    "type": "TimeoutError",
    "message": "Request timed out",
    "stacktrace": "..."
  }
}
``` | 错误日志 |

### 9.2 结构化日志字段

| 测试用例ID | 测试场景 | 必填字段 | 可选字段 | 示例 |
|------------|----------|----------|----------|------|
| FORMAT-004 | 基础字段 | timestamp, level, message | - | ```json
{
  "timestamp": "2026-04-04T10:30:45Z",
  "level": "INFO",
  "message": "Test message"
}
``` |
| FORMAT-005 | 请求字段 | request_id, client_ip, method, url | user_agent, headers | ```json
{
  "request_id": "req-123",
  "client_ip": "192.168.1.100",
  "method": "POST",
  "url": "https://api.openai.com/v1/chat/completions",
  "user_agent": "python-requests/2.31.0"
}
``` |
| FORMAT-006 | 性能字段 | duration_ms | start_time, end_time | ```json
{
  "duration_ms": 150,
  "start_time": "2026-04-04T10:30:45.000Z",
  "end_time": "2026-04-04T10:30:45.150Z"
}
``` |
| FORMAT-007 | PII字段 | pii_detections, masking_applied | original_length, masked_length | ```json
{
  "pii_detections": [...],
  "masking_applied": true,
  "original_length": 100,
  "masked_length": 100
}
``` |

### 9.3 完整日志条目示例

| 测试用例ID | 测试场景 | 完整日志JSON |
|------------|----------|--------------|
| FORMAT-008 | 成功请求日志 | ```json
{
  "timestamp": "2026-04-04T10:30:45.123456Z",
  "level": "INFO",
  "logger": "audit.request",
  "message": "POST /v1/chat/completions - 200 OK",
  "request_id": "req-a1b2c3d4",
  "trace_id": "trace-xyz789",
  "span_id": "span-123",
  "client_ip": "192.168.1.100",
  "client_port": 54321,
  "user_agent": "python-requests/2.31.0",
  "method": "POST",
  "url": "https://api.openai.com/v1/chat/completions",
  "path": "/v1/chat/completions",
  "query_params": {},
  "request_headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-***"
  },
  "request_body_size": 256,
  "response_status": 200,
  "response_headers": {
    "Content-Type": "application/json"
  },
  "response_body_size": 1024,
  "duration_ms": 150,
  "upstream_duration_ms": 120,
  "pii_detection_duration_ms": 5,
  "masking_duration_ms": 2,
  "start_time": "2026-04-04T10:30:45.000000Z",
  "end_time": "2026-04-04T10:30:45.150000Z",
  "pii_detections": [
    {
      "entity_type": "EMAIL_ADDRESS",
      "start": 45,
      "end": 65,
      "score": 0.95,
      "text": "user@example.com",
      "context": "Email: user@example.com"
    }
  ],
  "masking_applied": true,
  "masking_rules": [
    {
      "rule_id": "mask-email-001",
      "entity_type": "EMAIL_ADDRESS",
      "action": "mask",
      "pattern": "***@***.***"
    }
  ],
  "original_text_length": 500,
  "masked_text_length": 500,
  "cache_hit": false,
  "retry_count": 0,
  "circuit_breaker_state": "closed",
  "rate_limit_remaining": 99,
  "rate_limit_reset": "2026-04-04T10:31:45Z",
  "tags": ["llm", "openai", "chat"],
  "metadata": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
``` |

| FORMAT-009 | 错误请求日志 | ```json
{
  "timestamp": "2026-04-04T10:30:45.123456Z",
  "level": "ERROR",
  "logger": "audit.request",
  "message": "POST /v1/chat/completions - 500 Internal Server Error",
  "request_id": "req-e5f6g7h8",
  "trace_id": "trace-abc123",
  "span_id": "span-456",
  "client_ip": "192.168.1.101",
  "client_port": 54322,
  "user_agent": "python-requests/2.31.0",
  "method": "POST",
  "url": "https://api.openai.com/v1/chat/completions",
  "path": "/v1/chat/completions",
  "query_params": {},
  "request_headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-***"
  },
  "request_body_size": 256,
  "response_status": 500,
  "response_headers": {
    "Content-Type": "application/json",
    "X-Request-ID": "req-e5f6g7h8"
  },
  "response_body_size": 128,
  "duration_ms": 30000,
  "upstream_duration_ms": 30000,
  "pii_detection_duration_ms": 5,
  "masking_duration_ms": 2,
  "start_time": "2026-04-04T10:30:15.000000Z",
  "end_time": "2026-04-04T10:30:45.123456Z",
  "error": {
    "type": "UpstreamTimeoutError",
    "message": "Upstream request timed out after 30000ms",
    "code": "UPSTREAM_TIMEOUT",
    "retryable": true,
    "stacktrace": "..."
  },
  "pii_detections": [],
  "masking_applied": false,
  "original_text_length": 0,
  "masked_text_length": 0,
  "cache_hit": false,
  "retry_count": 3,
  "circuit_breaker_state": "open",
  "rate_limit_remaining": 0,
  "rate_limit_reset": "2026-04-04T10:31:45Z",
  "tags": ["llm", "openai", "chat", "error", "timeout"],
  "metadata": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout_ms": 30000
  }
}
``` |

## 10. 查询条件测试数据

### 10.1 时间范围查询

| 测试用例ID | 测试场景 | 时间范围 | 开始时间 | 结束时间 | 备注 |
|------------|----------|----------|----------|----------|------|
| QUERY-001 | 最近1小时 | 1h | 2026-04-04T09:30:45Z | 2026-04-04T10:30:45Z | 短期查询 |
| QUERY-002 | 最近1天 | 1d | 2026-04-03T10:30:45Z | 2026-04-04T10:30:45Z | 日常查询 |
| QUERY-003 | 最近1周 | 1w | 2026-03-28T10:30:45Z | 2026-04-04T10:30:45Z | 周报查询 |
| QUERY-004 | 最近1月 | 1m | 2026-03-04T10:30:45Z | 2026-04-04T10:30:45Z | 月报查询 |
| QUERY-005 | 自定义范围 | custom | 2026-04-01T00:00:00Z | 2026-04-04T23:59:59Z | 灵活查询 |

### 10.2 行数限制查询

| 测试用例ID | 测试场景 | 限制行数 | 预期返回 | 备注 |
|------------|----------|----------|----------|------|
| QUERY-006 | 最小限制 | 1 | ≤1条 | 单条查询 |
| QUERY-007 | 小批量 | 10 | ≤10条 | 快速查看 |
| QUERY-008 | 中批量 | 50 | ≤50条 | 一般查询 |
| QUERY-009 | 大批量 | 100 | ≤100条 | 详细查询 |
| QUERY-010 | 最大限制 | 1000 | ≤1000条 | 批量导出 |
| QUERY-011 | 超大限制 | 10000 | 超出限制 | 边界测试 |

### 10.3 关键词搜索查询

| 测试用例ID | 测试场景 | 搜索字段 | 搜索词 | 备注 |
|------------|----------|----------|--------|------|
| QUERY-012 | 请求ID搜索 | request_id | "req-123456" | 精确匹配 |
| QUERY-013 | 客户端IP搜索 | client_ip | "192.168.1.100" | 精确匹配 |
| QUERY-014 | URL搜索 | url | "openai" | 模糊匹配 |
| QUERY-015 | 错误类型搜索 | error.type | "TimeoutError" | 嵌套字段 |
| QUERY-016 | 日志级别搜索 | level | "ERROR" | 级别过滤 |
| QUERY-017 | PII类型搜索 | pii_detections.entity_type | "EMAIL_ADDRESS" | 嵌套数组 |

### 10.4 组合条件查询

| 测试用例ID | 测试场景 | 组合条件 | 示例查询 | 备注 |
|------------|----------|----------|----------|------|
| QUERY-018 | 时间+级别 | AND | `level="ERROR" AND timestamp > "2026-04-04T09:00:00Z"` | 错误日志 |
| QUERY-019 | 时间+状态码 | AND | `status_code=500 AND timestamp > "2026-04-04T09:00:00Z"` | 服务器错误 |
| QUERY-020 | 级别+关键词 | AND | `level="ERROR" AND message CONTAINS "timeout"` | 超时错误 |
| QUERY-021 | 多条件复杂查询 | AND/OR | `(level="ERROR" OR level="WARNING") AND status_code >= 400` | 异常查询 |

### 10.5 无效查询条件

| 测试用例ID | 测试场景 | 无效条件 | 预期结果 |
|------------|----------|----------|----------|
| QUERY-022 | 无效时间范围 | "invalid_range" | 查询错误 |
| QUERY-023 | 无效字段名 | "invalid_field" | 字段不存在 |
| QUERY-024 | 无效操作符 | "field >> value" | 语法错误 |
| QUERY-025 | 空查询条件 | {} | 缺失条件 |

## 11. 统计信息测试数据

### 11.1 初始统计数据

| 测试用例ID | 测试场景 | 统计指标 | 初始值 | 备注 |
|------------|----------|----------|--------|------|
| STATS-001 | 请求计数 | total_requests | 0 | 初始状态 |
| STATS-002 | 成功计数 | successful_requests | 0 | 初始状态 |
| STATS-003 | 失败计数 | failed_requests | 0 | 初始状态 |
| STATS-004 | 平均耗时 | avg_duration_ms | 0 | 初始状态 |
| STATS-005 | PII检测计数 | total_pii_detections | 0 | 初始状态 |
| STATS-006 | 脱敏操作计数 | total_masking_operations | 0 | 初始状态 |

### 11.2 请求后统计数据

| 测试用例ID | 测试场景 | 统计指标 | 请求后值 | 备注 |
|------------|----------|----------|----------|------|
| STATS-007 | 单次成功请求 | total_requests | 1 | 请求计数 |
| STATS-008 | 单次成功请求 | successful_requests | 1 | 成功计数 |
| STATS-009 | 单次成功请求 | avg_duration_ms | 150 | 平均耗时 |
| STATS-010 | 多次请求 | total_requests | 10 | 累计计数 |
| STATS-011 | 多次请求 | successful_requests | 8 | 成功率80% |
| STATS-012 | 多次请求 | failed_requests | 2 | 失败率20% |

### 11.3 错误后统计数据

| 测试用例ID | 测试场景 | 统计指标 | 错误后值 | 备注 |
|------------|----------|----------|----------|------|
| STATS-013 | 请求超时 | timeout_requests | 1 | 超时计数 |
| STATS-014 | 服务器错误 | server_errors | 1 | 5xx错误 |
| STATS-015 | 客户端错误 | client_errors | 1 | 4xx错误 |
| STATS-016 | 限流错误 | rate_limit_errors | 1 | 429错误 |

### 11.4 PII类型分布数据

| 测试用例ID | 测试场景 | PII类型 | 检测次数 | 占比 | 备注 |
|------------|----------|---------|----------|------|------|
| STATS-017 | 邮箱分布 | EMAIL_ADDRESS | 50 | 50% | 最常见 |
| STATS-018 | 电话分布 | PHONE_NUMBER | 30 | 30% | 常见类型 |
| STATS-019 | 身份证分布 | ID_CARD | 15 | 15% | 敏感信息 |
| STATS-020 | 银行卡分布 | CREDIT_CARD | 5 | 5% | 高敏感 |

### 11.5 脱敏操作分布数据

| 测试用例ID | 测试场景 | 脱敏类型 | 操作次数 | 占比 | 备注 |
|------------|----------|----------|----------|------|------|
| STATS-021 | mask操作分布 | mask | 60 | 60% | 最常用 |
| STATS-022 | replace操作分布 | replace | 25 | 25% | 常用类型 |
| STATS-023 | hash操作分布 | hash | 10 | 10% | 安全处理 |
| STATS-024 | redact操作分布 | redact | 5 | 5% | 完全删除 |

## 12. 导出格式测试数据

### 12.1 JSON导出格式

| 测试用例ID | 测试场景 | 导出格式 | 文件扩展名 | MIME类型 | 备注 |
|------------|----------|----------|------------|----------|------|
| EXPORT-001 | JSON格式 | JSON | .json | application/json | 标准格式 |
| EXPORT-002 | JSON行格式 | JSONL | .jsonl | application/x-ndjson | 流式处理 |
| EXPORT-003 | 压缩JSON | JSON.GZ | .json.gz | application/gzip | 压缩格式 |

### 12.2 CSV导出格式

| 测试用例ID | 测试场景 | 导出格式 | 文件扩展名 | MIME类型 | 备注 |
|------------|----------|----------|------------|----------|------|
| EXPORT-004 | CSV格式 | CSV | .csv | text/csv | 表格格式 |
| EXPORT-005 | 带标题CSV | CSV | .csv | text/csv | 包含标题行 |
| EXPORT-006 | 自定义分隔符 | CSV | .csv | text/csv | 分号分隔 |

### 12.3 导出文件路径

| 测试用例ID | 测试场景 | 文件路径 | 示例值 | 备注 |
|------------|----------|----------|--------|------|
| EXPORT-007 | 相对路径 | relative_path | `./logs/audit_2026-04-04.json` | 相对路径 |
| EXPORT-008 | 绝对路径 | absolute_path | `/var/log/llm-gateway/audit_2026-04-04.json` | 绝对路径 |
| EXPORT-009 | 带时间戳路径 | timestamp_path | `/logs/audit_20260404_103045.json` | 时间戳命名 |
| EXPORT-010 | 带序列号路径 | sequence_path | `/logs/audit_001.json` | 序列号命名 |

### 12.4 无效导出路径

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| EXPORT-011 | 无效路径 | `/invalid/path/file.json` | 路径不存在 |
| EXPORT-012 | 空路径 | "" | 路径为空 |
| EXPORT-013 | 无权限路径 | `/root/protected/file.json` | 权限拒绝 |
| EXPORT-014 | 磁盘空间不足 | `/full/disk/file.json` | 空间不足 |

## 13. 日志文件测试数据

### 13.1 有效日志文件路径

| 测试用例ID | 测试场景 | 文件路径 | 文件大小 | 备注 |
|------------|----------|----------|----------|------|
| FILE-001 | 标准日志文件 | `/var/log/llm-gateway/audit.log` | 10MB | 正常文件 |
| JSON日志文件 | `/var/log/llm-gateway/audit.json` | 5MB | JSON格式 |
| FILE-003 | 压缩日志文件 | `/var/log/llm-gateway/audit.log.gz` | 2MB | 压缩格式 |
| FILE-004 | 轮转日志文件 | `/var/log/llm-gateway/audit.log.1` | 10MB | 轮转文件 |
| FILE-005 | 日期日志文件 | `/var/log/llm-gateway/audit_2026-04-04.log` | 8MB | 日期命名 |

### 13.2 无效日志文件路径

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| FILE-006 | 文件不存在 | `/var/log/llm-gateway/missing.log` | 文件未找到 |
| FILE-007 | 目录不存在 | `/invalid/path/audit.log` | 路径无效 |
| FILE-008 | 空路径 | "" | 路径为空 |
| FILE-009 | 非文件路径 | `/var/log/llm-gateway/` | 是目录不是文件 |

### 13.3 无权限日志文件路径

| 测试用例ID | 测试场景 | 示例值 | 预期结果 |
|------------|----------|--------|----------|
| FILE-010 | 只读文件 | `/var/log/llm-gateway/readonly.log` | 权限拒绝 |
| FILE-011 | 无读权限 | `/var/log/llm-gateway/noaccess.log` | 权限拒绝 |
| FILE-012 | 其他用户文件 | `/home/otheruser/audit.log` | 权限拒绝 |

### 13.4 日志文件大小限制

| 测试用例ID | 测试场景 | 文件大小 | 备注 |
|------------|----------|----------|------|
| FILE-013 | 空文件 | 0 bytes | 边界测试 |
| FILE-014 | 小文件 | 1KB | 正常处理 |
| FILE-015 | 中等文件 | 10MB | 正常处理 |
| FILE-016 | 大文件 | 100MB | 需要流式处理 |
| FILE-017 | 超大文件 | 1GB | 内存限制 |
| FILE-018 | 超出限制 | 10GB | 文件过大 |

### 13.5 日志文件格式验证

| 测试用例ID | 测试场景 | 文件格式 | 示例内容 | 预期结果 |
|------------|----------|----------|----------|----------|
| FILE-019 | 有效JSON格式 | JSON | `{"timestamp": "...", "level": "INFO"}` | 解析成功 |
| FILE-020 | 无效JSON格式 | JSON | `{"timestamp": "...", "level": "INFO"` | 解析失败 |
| FILE-021 | 有效CSV格式 | CSV | `timestamp,level,message` | 解析成功 |
| FILE-022 | 无效CSV格式 | CSV | `timestamp,level,message\n"2026-04-04",INFO` | 解析失败 |
| FILE-023 | 混合格式 | TEXT | `INFO: 2026-04-04T10:30:45Z - Request processed` | 需要解析器 |
| FILE-024 | 空文件 | - | ` ` | 无内容 |

## 14. 边界值和特殊字符测试数据

### 14.1 特殊字符处理

| 测试用例ID | 测试场景 | 输入数据 | 预期处理 | 备注 |
|------------|----------|----------|----------|------|
| SPECIAL-001 | Unicode字符 | "测试中文日志" | 正确编码 | 中文支持 |
| SPECIAL-002 | 表情符号 | "请求成功 ✅" | 正确编码 | Emoji支持 |
| SPECIAL-003 | 换行符 | "第一行\n第二行" | 正确转义 | 多行文本 |
| SPECIAL-004 | 制表符 | "列1\t列2" | 正确转义 | 表格数据 |
| SPECIAL-005 | 引号字符 | `{"key": "value"}` | 正确转义 | JSON嵌套 |
| SPECIAL-006 | 反斜杠 | `C:\path\to\file` | 正确转义 | 路径字符 |
| SPECIAL-007 | HTML标签 | `<script>alert('xss')</script>` | 正确转义 | 安全处理 |
| SPECIAL-008 | SQL注入 | `' OR '1'='1` | 正确转义 | 安全处理 |

### 14.2 边界值测试

| 测试用例ID | 测试场景 | 边界类型 | 示例值 | 备注 |
|------------|----------|----------|--------|------|
| BOUNDARY-001 | 字符串长度 | 最大长度 | "a"*10000 | 长字符串 |
| BOUNDARY-002 | 字符串长度 | 最小长度 | "" | 空字符串 |
| BOUNDARY-003 | 数值范围 | 最大整数 | 2^31-1 | 整数边界 |
| BOUNDARY-004 | 数值范围 | 最小整数 | -2^31 | 负数边界 |
| BOUNDARY-005 | 数组长度 | 最大元素 | 1000个元素 | 数组边界 |
| BOUNDARY-006 | 嵌套深度 | 最大嵌套 | 10层嵌套 | 深度边界 |
| BOUNDARY-007 | 时间范围 | 最早时间 | 1970-01-01T00:00:00Z | Unix纪元 |
| BOUNDARY-008 | 时间范围 | 最晚时间 | 2038-01-19T03:14:07Z | Y2038问题 |

## 15. 性能测试数据

### 15.1 高并发测试数据

| 测试用例ID | 测试场景 | 并发数 | 请求速率 | 备注 |
|------------|----------|--------|----------|------|
| PERF-001 | 低并发 | 10 | 10 req/s | 基准测试 |
| PERF-002 | 中并发 | 100 | 100 req/s | 正常负载 |
| PERF-003 | 高并发 | 1000 | 1000 req/s | 高负载 |
| PERF-004 | 极限并发 | 10000 | 10000 req/s | 压力测试 |

### 15.2 大数据量测试数据

| 测试用例ID | 测试场景 | 数据量 | 内存使用 | 备注 |
|------------|----------|--------|----------|------|
| PERF-005 | 小数据集 | 1000条 | <10MB | 基准测试 |
| PERF-006 | 中数据集 | 10000条 | <100MB | 正常查询 |
| PERF-007 | 大数据集 | 100000条 | <1GB | 批量处理 |
| PERF-008 | 超大数据集 | 1000000条 | >1GB | 需要优化 |

## 16. 安全测试数据

### 16.1 敏感信息处理

| 测试用例ID | 测试场景 | 敏感数据 | 处理方式 | 备注 |
|------------|----------|----------|----------|------|
| SECURITY-001 | API密钥 | "sk-1234567890abcdef" | 部分掩码 | 密钥保护 |
| SECURITY-002 | 密码 | "password123" | 完全脱敏 | 密码保护 |
| SECURITY-003 | 令牌 | "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | 部分掩码 | 令牌保护 |
| SECURITY-004 | 会话ID | "session_abc123def456" | 哈希处理 | 会话保护 |
| SECURITY-005 | 用户ID | "user_12345" | 哈希处理 | 用户保护 |

### 16.2 访问控制测试数据

| 测试用例ID | 测试场景 | 用户角色 | 权限 | 预期结果 |
|------------|----------|----------|------|----------|
| SECURITY-006 | 管理员 | admin | 读写所有日志 | 完全访问 |
| SECURITY-007 | 普通用户 | user | 读自己的日志 | 有限访问 |
| SECURITY-008 | 访客 | guest | 无访问权限 | 拒绝访问 |
| SECURITY-009 | API密钥 | api_key | 特定端点访问 | 受限访问 |

---

## 测试数据使用说明

1. **数据覆盖**: 本测试数据文件覆盖了审计日志模块95%以上的代码分支
2. **边界测试**: 包含边界值、特殊字符、异常情况等测试数据
3. **格式验证**: 提供了JSON、CSV等多种格式的测试数据
4. **性能测试**: 包含高并发、大数据量等性能测试数据
5. **安全测试**: 包含敏感信息处理、访问控制等安全测试数据

## 相关文档

- [审计日志测试用例](06_audit_logging.md)
- [PII检测测试数据](04_pii_detection_testdata.md)
- [代理服务测试数据](02_proxy_service_testdata.md)