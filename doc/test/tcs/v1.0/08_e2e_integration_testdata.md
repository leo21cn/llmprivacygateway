# 端到端集成测试数据

## 1. 完整请求流程测试数据

### 1.1 无PII的请求内容

```json
{
  "request_no_pii": {
    "prompt": "Hello, how are you today?",
    "expected_pii_count": 0,
    "expected_masked_text": "Hello, how are you today?",
    "expected_response_contains": ["Hello", "how are you"]
  }
}
```

### 1.2 包含单个PII的请求内容

```json
{
  "request_single_pii": {
    "prompt": "My email is user@example.com",
    "expected_pii_count": 1,
    "expected_pii_types": ["EMAIL_ADDRESS"],
    "expected_masked_text": "My email is [EMAIL_REDACTED]",
    "expected_response_contains": ["email"]
  }
}
```

### 1.3 包含多个PII的请求内容

```json
{
  "request_multiple_pii": {
    "prompt": "Contact me at user@example.com or 13812345678",
    "expected_pii_count": 2,
    "expected_pii_types": ["EMAIL_ADDRESS", "PHONE_NUMBER"],
    "expected_masked_text": "Contact me at [EMAIL_REDACTED] or [PHONE_REDACTED]",
    "expected_response_contains": ["contact"]
  }
}
```

### 1.4 包含混合PII的请求内容

```json
{
  "request_mixed_pii": {
    "prompt": "I'm 张三, my email is zhangsan@example.com, ID: 110101199001011234",
    "expected_pii_count": 3,
    "expected_pii_types": ["PERSON", "EMAIL_ADDRESS", "CN_ID_CARD"],
    "expected_masked_text": "I'm [PERSON_REDACTED], my email is [EMAIL_REDACTED], ID: [ID_CARD_REDACTED]",
    "expected_response_contains": ["name", "email", "ID"]
  }
}
```

### 1.5 流式请求数据

```json
{
  "stream_request": {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "My email is test@example.com"}],
    "stream": true,
    "expected_stream_events": ["data: ", "data: [DONE]"],
    "expected_chunks_min": 1,
    "expected_chunks_max": 50
  }
}
```

### 1.6 非流式请求数据

```json
{
  "non_stream_request": {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "stream": false,
    "expected_response_format": "json",
    "expected_fields": ["id", "object", "created", "model", "choices"]
  }
}
```

---

## 2. OpenAI API格式测试数据

### 2.1 /v1/chat/completions 请求体

```json
{
  "chat_completion_request": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 150,
    "stream": false
  }
}
```

### 2.2 /v1/completions 请求体

```json
{
  "completion_request": {
    "model": "text-davinci-003",
    "prompt": "The capital of France is",
    "max_tokens": 50,
    "temperature": 0.5,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
  }
}
```

### 2.3 /v1/embeddings 请求体

```json
{
  "embedding_request": {
    "model": "text-embedding-ada-002",
    "input": "The quick brown fox jumps over the lazy dog"
  }
}
```

### 2.4 带system消息的请求

```json
{
  "system_message_request": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant that speaks Chinese. My name is 张三 and my email is zhangsan@example.com"
      },
      {"role": "user", "content": "What is your name?"}
    ],
    "temperature": 0.7
  }
}
```

### 2.5 带多轮对话的请求

```json
{
  "multi_turn_request": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "My name is 李四"},
      {"role": "assistant", "content": "Nice to meet you, 李四!"},
      {"role": "user", "content": "What is my email? It's lisi@example.com"},
      {"role": "assistant", "content": "Your email is lisi@example.com"},
      {"role": "user", "content": "Can you remind me of my phone number? 13912345678"}
    ],
    "temperature": 0.7
  }
}
```

### 2.6 带temperature等参数的请求

```json
{
  "parameterized_request": {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Write a short poem"}],
    "temperature": 0.9,
    "max_tokens": 200,
    "top_p": 0.95,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.3,
    "stop": ["\n\n"],
    "n": 1
  }
}
```

---

## 3. 虚拟Key场景测试数据

### 3.1 有效虚拟Key

```json
{
  "valid_virtual_keys": [
    {
      "key": "sk-virtual-abc123def456",
      "provider": "openai",
      "is_valid": true,
      "expected_status": 200
    },
    {
      "key": "sk-virtual-xyz789ghi012",
      "provider": "anthropic",
      "is_valid": true,
      "expected_status": 200
    },
    {
      "key": "sk-virtual-custom001",
      "provider": "custom",
      "is_valid": true,
      "expected_status": 200
    }
  ]
}
```

### 3.2 无效虚拟Key

```json
{
  "invalid_virtual_keys": [
    {
      "key": "invalid-key",
      "reason": "invalid_format",
      "expected_status": 401,
      "expected_error": "Invalid API key"
    },
    {
      "key": "sk-invalid-xxx",
      "reason": "not_found",
      "expected_status": 401,
      "expected_error": "Invalid API key"
    },
    {
      "key": "",
      "reason": "empty_key",
      "expected_status": 401,
      "expected_error": "Missing API key"
    },
    {
      "key": "sk-virtual-nonexistent",
      "reason": "key_not_exist",
      "expected_status": 401,
      "expected_error": "Invalid API key"
    }
  ]
}
```

### 3.3 已吊销虚拟Key

```json
{
  "revoked_virtual_keys": [
    {
      "key": "sk-virtual-revoked001",
      "revoked_at": "2025-01-01T00:00:00Z",
      "reason": "security_breach",
      "expected_status": 401,
      "expected_error": "API key has been revoked"
    },
    {
      "key": "sk-virtual-revoked002",
      "revoked_at": "2025-06-15T10:30:00Z",
      "reason": "user_request",
      "expected_status": 401,
      "expected_error": "API key has been revoked"
    }
  ]
}
```

### 3.4 已过期虚拟Key

```json
{
  "expired_virtual_keys": [
    {
      "key": "sk-virtual-expired001",
      "expired_at": "2025-12-31T23:59:59Z",
      "expected_status": 401,
      "expected_error": "API key has expired"
    },
    {
      "key": "sk-virtual-expired002",
      "expired_at": "2024-06-30T12:00:00Z",
      "expected_status": 401,
      "expected_error": "API key has expired"
    }
  ]
}
```

### 3.5 不同provider的虚拟Key

```json
{
  "provider_virtual_keys": [
    {
      "key": "sk-virtual-openai001",
      "provider": "openai",
      "target_url": "https://api.openai.com",
      "supported_endpoints": ["/v1/chat/completions", "/v1/completions", "/v1/embeddings"]
    },
    {
      "key": "sk-virtual-anthropic001",
      "provider": "anthropic",
      "target_url": "https://api.anthropic.com",
      "supported_endpoints": ["/v1/messages"]
    },
    {
      "key": "sk-virtual-custom001",
      "provider": "custom",
      "target_url": "https://custom-llm.example.com",
      "supported_endpoints": ["/v1/chat/completions"]
    }
  ]
}
```

---

## 4. 真实Key场景测试数据

### 4.1 OpenAI真实Key

```json
{
  "openai_real_keys": [
    {
      "key": "sk-xxxxxxxxxxxxxxxxxxxxxxxx",
      "provider": "openai",
      "format_pattern": "^sk-[a-zA-Z0-9]{48}$",
      "is_valid_format": true,
      "target_endpoint": "https://api.openai.com/v1/chat/completions"
    },
    {
      "key": "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx",
      "provider": "openai",
      "format_pattern": "^sk-proj-[a-zA-Z0-9]{48}$",
      "is_valid_format": true,
      "target_endpoint": "https://api.openai.com/v1/chat/completions"
    }
  ]
}
```

### 4.2 Anthropic真实Key

```json
{
  "anthropic_real_keys": [
    {
      "key": "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx",
      "provider": "anthropic",
      "format_pattern": "^sk-ant-[a-zA-Z0-9-]{95}$",
      "is_valid_format": true,
      "target_endpoint": "https://api.anthropic.com/v1/messages"
    }
  ]
}
```

### 4.3 自定义provider真实Key

```json
{
  "custom_provider_real_keys": [
    {
      "key": "custom-key-1234567890abcdef",
      "provider": "custom-llm",
      "format_pattern": "^[a-zA-Z0-9-]{32,}$",
      "is_valid_format": true,
      "target_endpoint": "https://custom-llm.example.com/v1/chat/completions"
    },
    {
      "key": "Bearer token-xyz789",
      "provider": "custom-llm",
      "format_pattern": "^Bearer\\s[a-zA-Z0-9-]+$",
      "is_valid_format": true,
      "target_endpoint": "https://custom-llm.example.com/v1/chat/completions"
    }
  ]
}
```

---

## 5. PII检测结果测试数据

### 5.1 邮箱检测结果

```json
{
  "email_detection": {
    "input_text": "Contact me at user@example.com for more info",
    "expected_result": {
      "entity_type": "EMAIL_ADDRESS",
      "start": 14,
      "end": 32,
      "score": 0.95
    },
    "masked_text": "Contact me at [EMAIL_REDACTED] for more info"
  }
}
```

### 5.2 手机号检测结果

```json
{
  "phone_detection": {
    "input_text": "Call me at 13812345678",
    "expected_result": {
      "entity_type": "PHONE_NUMBER",
      "start": 11,
      "end": 22,
      "score": 0.9
    },
    "masked_text": "Call me at [PHONE_REDACTED]"
  }
}
```

### 5.3 身份证检测结果

```json
{
  "id_card_detection": {
    "input_text": "My ID is 110101199001011234",
    "expected_result": {
      "entity_type": "CN_ID_CARD",
      "start": 9,
      "end": 27,
      "score": 0.98
    },
    "masked_text": "My ID is [ID_CARD_REDACTED]"
  }
}
```

### 5.4 人名检测结果

```json
{
  "person_name_detection": {
    "input_text": "I'm 张三",
    "expected_result": {
      "entity_type": "PERSON",
      "start": 4,
      "end": 6,
      "score": 0.85
    },
    "masked_text": "I'm [PERSON_REDACTED]"
  }
}
```

### 5.5 多个检测结果

```json
{
  "multiple_detections": {
    "input_text": "I'm 张三, my email is zhangsan@example.com, phone: 13912345678, ID: 110101199001011234",
    "expected_results": [
      {"entity_type": "PERSON", "start": 4, "end": 6, "score": 0.85},
      {"entity_type": "EMAIL_ADDRESS", "start": 20, "end": 40, "score": 0.95},
      {"entity_type": "PHONE_NUMBER", "start": 49, "end": 60, "score": 0.9},
      {"entity_type": "CN_ID_CARD", "start": 66, "end": 84, "score": 0.98}
    ],
    "masked_text": "I'm [PERSON_REDACTED], my email is [EMAIL_REDACTED], phone: [PHONE_REDACTED], ID: [ID_CARD_REDACTED]"
  }
}
```

---

## 6. 脱敏结果测试数据

### 6.1 replace脱敏结果

```json
{
  "replace_masking": {
    "method": "replace",
    "input_text": "Email: user@example.com",
    "pii_entity": {"type": "EMAIL_ADDRESS", "start": 7, "end": 25},
    "replacement": "[EMAIL_REDACTED]",
    "expected_result": "Email: [EMAIL_REDACTED]"
  }
}
```

### 6.2 mask脱敏结果

```json
{
  "mask_masking": {
    "method": "mask",
    "input_text": "Phone: 13812345678",
    "pii_entity": {"type": "PHONE_NUMBER", "start": 7, "end": 18},
    "mask_char": "*",
    "visible_chars": 4,
    "expected_result": "Phone: ********45678"
  }
}
```

### 6.3 hash脱敏结果

```json
{
  "hash_masking": {
    "method": "hash",
    "input_text": "ID: 110101199001011234",
    "pii_entity": {"type": "CN_ID_CARD", "start": 4, "end": 22},
    "hash_algorithm": "sha256",
    "expected_result_pattern": "^ID: [a-f0-9]{16}$"
  }
}
```

### 6.4 redact脱敏结果

```json
{
  "redact_masking": {
    "method": "redact",
    "input_text": "Name: 张三, Email: user@example.com",
    "pii_entities": [
      {"type": "PERSON", "start": 6, "end": 8},
      {"type": "EMAIL_ADDRESS", "start": 16, "end": 34}
    ],
    "expected_result": "Name: , Email: "
  }
}
```

---

## 7. LLM响应测试数据

### 7.1 正常响应（200）

```json
{
  "normal_response_200": {
    "status_code": 200,
    "response": {
      "id": "chatcmpl-abc123",
      "object": "chat.completion",
      "created": 1677858242,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "The capital of France is Paris."
          },
          "finish_reason": "stop"
        }
      ],
      "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 8,
        "total_tokens": 23
      }
    }
  }
}
```

### 7.2 无PII的响应

```json
{
  "response_no_pii": {
    "status_code": 200,
    "response": {
      "id": "chatcmpl-def456",
      "object": "chat.completion",
      "created": 1677858242,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "The weather is nice today."
          },
          "finish_reason": "stop"
        }
      ]
    },
    "expected_pii_count": 0
  }
}
```

### 7.3 包含PII的响应

```json
{
  "response_with_pii": {
    "status_code": 200,
    "response": {
      "id": "chatcmpl-ghi789",
      "object": "chat.completion",
      "created": 1677858242,
      "model": "gpt-3.5-turbo",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "You can contact support at support@example.com or call 1-800-555-0123."
          },
          "finish_reason": "stop"
        }
      ]
    },
    "expected_pii_count": 2,
    "expected_pii_types": ["EMAIL_ADDRESS", "PHONE_NUMBER"],
    "expected_masked_response": "You can contact support at [EMAIL_REDACTED] or call [PHONE_REDACTED]."
  }
}
```

### 7.4 流式响应

```json
{
  "stream_response": {
    "status_code": 200,
    "content_type": "text/event-stream",
    "chunks": [
      {"data": "data: {\"id\":\"chatcmpl-abc\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"delta\":{\"content\":\"The\"}}]}\n\n"},
      {"data": "data: {\"id\":\"chatcmpl-abc\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"delta\":{\"content\":\" capital\"}}]}\n\n"},
      {"data": "data: {\"id\":\"chatcmpl-abc\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"delta\":{\"content\":\" is\"}}]}\n\n"},
      {"data": "data: {\"id\":\"chatcmpl-abc\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"delta\":{\"content\":\" Paris\"}}]}\n\n"},
      {"data": "data: [DONE]\n\n"}
    ],
    "expected_reconstructed": "The capital is Paris"
  }
}
```

### 7.5 错误响应（400, 401, 500）

```json
{
  "error_responses": {
    "400_bad_request": {
      "status_code": 400,
      "error": {
        "error": {
          "message": "Invalid request format",
          "type": "invalid_request_error",
          "code": "invalid_request"
        }
      }
    },
    "401_unauthorized": {
      "status_code": 401,
      "error": {
        "error": {
          "message": "Invalid API key provided",
          "type": "authentication_error",
          "code": "invalid_api_key"
        }
      }
    },
    "500_internal_error": {
      "status_code": 500,
      "error": {
        "error": {
          "message": "Internal server error",
          "type": "server_error",
          "code": "internal_error"
        }
      }
    }
  }
}
```

---

## 8. 规则配置测试数据

### 8.1 启用所有规则

```json
{
  "all_rules_enabled": {
    "rules": {
      "pii_detection": {
        "enabled": true,
        "entities": ["EMAIL_ADDRESS", "PHONE_NUMBER", "CN_ID_CARD", "PERSON", "CREDIT_CARD", "IP_ADDRESS"]
      },
      "credential_detection": {
        "enabled": true,
        "patterns": ["api_key", "password", "token", "secret"]
      },
      "custom_rules": {
        "enabled": true,
        "rules_list": ["custom_pii_pattern", "custom_credential_pattern"]
      }
    },
    "test_input": "Email: user@example.com, Phone: 13812345678, API Key: sk-1234567890abcdef",
    "expected_detections": 3
  }
}
```

### 8.2 仅启用PII规则

```json
{
  "pii_only_enabled": {
    "rules": {
      "pii_detection": {
        "enabled": true,
        "entities": ["EMAIL_ADDRESS", "PHONE_NUMBER", "CN_ID_CARD", "PERSON"]
      },
      "credential_detection": {
        "enabled": false
      },
      "custom_rules": {
        "enabled": false
      }
    },
    "test_input": "Email: user@example.com, API Key: sk-1234567890abcdef",
    "expected_detections": 1,
    "expected_detection_type": "EMAIL_ADDRESS"
  }
}
```

### 8.3 仅启用凭证规则

```json
{
  "credentials_only_enabled": {
    "rules": {
      "pii_detection": {
        "enabled": false
      },
      "credential_detection": {
        "enabled": true,
        "patterns": ["api_key", "password", "token", "secret"]
      },
      "custom_rules": {
        "enabled": false
      }
    },
    "test_input": "Email: user@example.com, API Key: sk-1234567890abcdef",
    "expected_detections": 1,
    "expected_detection_type": "API_KEY"
  }
}
```

### 8.4 禁用所有规则

```json
{
  "all_rules_disabled": {
    "rules": {
      "pii_detection": {
        "enabled": false
      },
      "credential_detection": {
        "enabled": false
      },
      "custom_rules": {
        "enabled": false
      }
    },
    "test_input": "Email: user@example.com, Phone: 13812345678, API Key: sk-1234567890abcdef",
    "expected_detections": 0,
    "expected_output_same_as_input": true
  }
}
```

### 8.5 自定义规则

```json
{
  "custom_rules": {
    "rules": {
      "pii_detection": {
        "enabled": true,
        "entities": ["EMAIL_ADDRESS"]
      },
      "credential_detection": {
        "enabled": false
      },
      "custom_rules": {
        "enabled": true,
        "rules_list": [
          {
            "name": "company_id",
            "pattern": "COMP-[0-9]{8}",
            "entity_type": "COMPANY_ID"
          },
          {
            "name": "internal_code",
            "pattern": "INT-[A-Z]{3}-[0-9]{4}",
            "entity_type": "INTERNAL_CODE"
          }
        ]
      }
    },
    "test_input": "Employee: COMP-12345678, Code: INT-ABC-1234, Email: user@example.com",
    "expected_detections": 3,
    "expected_types": ["COMPANY_ID", "INTERNAL_CODE", "EMAIL_ADDRESS"]
  }
}
```

---

## 9. 配置场景测试数据

### 9.1 默认配置

```json
{
  "default_config": {
    "proxy": {
      "host": "127.0.0.1",
      "port": 8080,
      "workers": 4
    },
    "presidio": {
      "endpoint": "http://localhost:5001",
      "language": "zh",
      "timeout": 30
    },
    "logging": {
      "level": "INFO",
      "format": "json"
    },
    "rules": {
      "enabled": true
    }
  }
}
```

### 9.2 自定义端口配置

```json
{
  "custom_port_config": {
    "proxy": {
      "host": "127.0.0.1",
      "port": 9090,
      "workers": 2
    },
    "presidio": {
      "endpoint": "http://localhost:5001",
      "language": "zh",
      "timeout": 30
    }
  },
  "test_cases": [
    {"port": 8080, "expected_status": "running"},
    {"port": 9090, "expected_status": "running"},
    {"port": 80, "expected_status": "running", "requires_root": true},
    {"port": 65535, "expected_status": "running"}
  ]
}
```

### 9.3 自定义host配置

```json
{
  "custom_host_config": {
    "test_cases": [
      {
        "host": "127.0.0.1",
        "description": "Localhost only",
        "expected_accessible_from": ["localhost"],
        "expected_not_accessible_from": ["external"]
      },
      {
        "host": "0.0.0.0",
        "description": "All interfaces",
        "expected_accessible_from": ["localhost", "external"],
        "expected_not_accessible_from": []
      },
      {
        "host": "192.168.1.100",
        "description": "Specific interface",
        "expected_accessible_from": ["192.168.1.x"],
        "expected_not_accessible_from": ["localhost", "external"]
      }
    ]
  }
}
```

### 9.4 自定义日志级别配置

```json
{
  "custom_log_level_config": {
    "test_cases": [
      {
        "level": "DEBUG",
        "expected_log_entries": ["request_details", "response_details", "pii_detection_details", "timing_info"],
        "expected_min_logs_per_request": 5
      },
      {
        "level": "INFO",
        "expected_log_entries": ["request_summary", "response_summary", "pii_summary"],
        "expected_min_logs_per_request": 2
      },
      {
        "level": "WARNING",
        "expected_log_entries": ["pii_detected", "errors"],
        "expected_min_logs_per_request": 0
      },
      {
        "level": "ERROR",
        "expected_log_entries": ["critical_errors"],
        "expected_min_logs_per_request": 0
      }
    ]
  }
}
```

### 9.5 环境变量覆盖配置

```json
{
  "env_override_config": {
    "environment_variables": {
      "LPG_PROXY_HOST": "0.0.0.0",
      "LPG_PROXY_PORT": "9090",
      "LPG_PRESIDIO_ENDPOINT": "http://presidio:5001",
      "LPG_LOG_LEVEL": "DEBUG",
      "LPG_WORKERS": "8"
    },
    "expected_overrides": {
      "proxy.host": "0.0.0.0",
      "proxy.port": 9090,
      "presidio.endpoint": "http://presidio:5001",
      "logging.level": "DEBUG",
      "proxy.workers": 8
    }
  }
}
```

---

## 10. 并发场景测试数据

### 10.1 并发请求数量

```json
{
  "concurrent_requests": {
    "test_cases": [
      {
        "concurrency": 1,
        "description": "Single request",
        "expected_success_rate": 1.0,
        "expected_avg_latency_ms": 500
      },
      {
        "concurrency": 5,
        "description": "Low concurrency",
        "expected_success_rate": 0.99,
        "expected_avg_latency_ms": 600
      },
      {
        "concurrency": 10,
        "description": "Medium concurrency",
        "expected_success_rate": 0.95,
        "expected_avg_latency_ms": 800
      },
      {
        "concurrency": 20,
        "description": "High concurrency",
        "expected_success_rate": 0.90,
        "expected_avg_latency_ms": 1200
      }
    ]
  }
}
```

### 10.2 并发请求间隔

```json
{
  "concurrent_request_intervals": {
    "test_cases": [
      {
        "interval_ms": 0,
        "description": "No interval (burst)",
        "expected_behavior": "All requests processed, may have rate limiting"
      },
      {
        "interval_ms": 10,
        "description": "Short interval",
        "expected_behavior": "Smooth processing, minimal queuing"
      },
      {
        "interval_ms": 100,
        "description": "Medium interval",
        "expected_behavior": "Sequential-like processing, no queuing"
      }
    ]
  }
}
```

### 10.3 不同端点的并发请求

```json
{
  "multi_endpoint_concurrent": {
    "endpoints": [
      {"path": "/v1/chat/completions", "method": "POST", "weight": 0.7},
      {"path": "/v1/completions", "method": "POST", "weight": 0.2},
      {"path": "/v1/embeddings", "method": "POST", "weight": 0.1}
    ],
    "total_requests": 100,
    "concurrency": 10,
    "expected_distribution": {
      "/v1/chat/completions": 70,
      "/v1/completions": 20,
      "/v1/embeddings": 10
    },
    "expected_success_rate": 0.95
  }
}
```

---

## 11. 性能场景测试数据

### 11.1 短文本请求（<100字符）

```json
{
  "short_text_requests": {
    "test_cases": [
      {
        "text": "Hello",
        "length": 5,
        "expected_latency_ms": 200,
        "expected_pii_count": 0
      },
      {
        "text": "What is the capital of France?",
        "length": 29,
        "expected_latency_ms": 250,
        "expected_pii_count": 0
      },
      {
        "text": "Email: user@example.com",
        "length": 24,
        "expected_latency_ms": 300,
        "expected_pii_count": 1
      }
    ],
    "max_expected_latency_ms": 500
  }
}
```

### 11.2 中等文本请求（100-1000字符）

```json
{
  "medium_text_requests": {
    "test_cases": [
      {
        "text": "This is a medium length text that contains some information. My email is user@example.com and my phone is 13812345678. Please contact me for more details about the project.",
        "length": 180,
        "expected_latency_ms": 400,
        "expected_pii_count": 2
      },
      {
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "length": 210,
        "expected_latency_ms": 450,
        "expected_pii_count": 0
      }
    ],
    "max_expected_latency_ms": 1000
  }
}
```

### 11.3 长文本请求（1000-10000字符）

```json
{
  "long_text_requests": {
    "test_cases": [
      {
        "text": "<1000字符的长文本，包含多个PII>",
        "length": 1500,
        "expected_latency_ms": 800,
        "expected_pii_count": 5
      },
      {
        "text": "<5000字符的超长文本，包含多个PII>",
        "length": 5000,
        "expected_latency_ms": 1500,
        "expected_pii_count": 15
      }
    ],
    "max_expected_latency_ms": 5000
  }
}
```

### 11.4 超长文本请求（>10000字符）

```json
{
  "very_long_text_requests": {
    "test_cases": [
      {
        "text": "<10000字符的超长文本>",
        "length": 10000,
        "expected_latency_ms": 3000,
        "expected_pii_count": 30
      },
      {
        "text": "<50000字符的极大文本>",
        "length": 50000,
        "expected_latency_ms": 10000,
        "expected_pii_count": 100
      }
    ],
    "max_expected_latency_ms": 30000,
    "notes": "May need to increase timeout for very large texts"
  }
}
```

---

## 12. 错误场景测试数据

### 12.1 Presidio服务不可用

```json
{
  "presidio_unavailable": {
    "scenario": "Presidio service is down or unreachable",
    "presidio_endpoint": "http://localhost:9999",
    "expected_behavior": "Return error or degrade gracefully",
    "expected_status_code": 503,
    "expected_error": "PII detection service unavailable",
    "fallback_behavior": "Pass through request without masking"
  }
}
```

### 12.2 目标LLM服务不可用

```json
{
  "llm_unavailable": {
    "scenario": "Target LLM service is down or unreachable",
    "target_endpoint": "https://api.openai.com/v1/chat/completions",
    "mock_response": {
      "status_code": 502,
      "error": "Bad Gateway"
    },
    "expected_behavior": "Return error from LLM service",
    "expected_status_code": 502
  }
}
```

### 12.3 网络超时

```json
{
  "network_timeout": {
    "scenario": "Network timeout during request",
    "timeout_ms": 5000,
    "expected_behavior": "Return timeout error",
    "expected_status_code": 504,
    "expected_error": "Gateway timeout",
    "test_cases": [
      {"timeout_ms": 1000, "description": "Short timeout"},
      {"timeout_ms": 30000, "description": "Long timeout"},
      {"timeout_ms": 0, "description": "No timeout"}
    ]
  }
}
```

### 12.4 DNS解析失败

```json
{
  "dns_resolution_failure": {
    "scenario": "DNS resolution failure for target endpoint",
    "target_endpoint": "https://nonexistent-llm-provider.invalid",
    "expected_behavior": "Return DNS resolution error",
    "expected_status_code": 502,
    "expected_error": "DNS resolution failed"
  }
}
```

### 12.5 无效请求格式

```json
{
  "invalid_request_format": {
    "test_cases": [
      {
        "scenario": "Invalid JSON in request body",
        "request_body": "{invalid json}",
        "expected_status_code": 400,
        "expected_error": "Invalid JSON"
      },
      {
        "scenario": "Missing required field 'messages'",
        "request_body": {"model": "gpt-3.5-turbo"},
        "expected_status_code": 400,
        "expected_error": "Missing required field"
      },
      {
        "scenario": "Invalid model name",
        "request_body": {"model": "nonexistent-model", "messages": []},
        "expected_status_code": 400,
        "expected_error": "Invalid model"
      },
      {
        "scenario": "Invalid temperature value",
        "request_body": {"model": "gpt-3.5-turbo", "messages": [], "temperature": 2.5},
        "expected_status_code": 400,
        "expected_error": "Invalid temperature"
      }
    ]
  }
}
```

---

## 13. 审计日志验证数据

### 13.1 期望的审计日志条目

```json
{
  "expected_audit_log_entries": {
    "request_log": {
      "timestamp": "2026-04-04T10:00:00Z",
      "request_id": "req-abc123def456",
      "virtual_key": "sk-virtual-abc123",
      "provider": "openai",
      "endpoint": "/v1/chat/completions",
      "method": "POST",
      "client_ip": "192.168.1.100",
      "user_agent": "OpenAI/1.0"
    },
    "pii_detection_log": {
      "request_id": "req-abc123def456",
      "input_pii_count": 2,
      "input_pii_types": ["EMAIL_ADDRESS", "PHONE_NUMBER"],
      "output_pii_count": 1,
      "output_pii_types": ["EMAIL_ADDRESS"],
      "masking_actions": ["replace", "replace"]
    },
    "response_log": {
      "request_id": "req-abc123def456",
      "status_code": 200,
      "latency_ms": 850,
      "tokens_used": 150,
      "response_size_bytes": 512
    }
  }
}
```

### 13.2 期望的统计信息

```json
{
  "expected_statistics": {
    "total_requests": 100,
    "successful_requests": 95,
    "failed_requests": 5,
    "success_rate": 0.95,
    "average_latency_ms": 650,
    "p50_latency_ms": 500,
    "p95_latency_ms": 1200,
    "p99_latency_ms": 2500,
    "total_tokens_used": 15000,
    "total_pii_detected": 250,
    "total_pii_masked": 245,
    "by_provider": {
      "openai": {"requests": 70, "success": 68, "avg_latency_ms": 600},
      "anthropic": {"requests": 20, "success": 19, "avg_latency_ms": 750},
      "custom": {"requests": 10, "success": 8, "avg_latency_ms": 800}
    },
    "by_endpoint": {
      "/v1/chat/completions": {"requests": 80, "success": 77},
      "/v1/completions": {"requests": 15, "success": 14},
      "/v1/embeddings": {"requests": 5, "success": 4}
    }
  }
}
```

### 13.3 期望的日志格式

```json
{
  "expected_log_format": {
    "json_format": {
      "timestamp": "ISO 8601 format",
      "level": "INFO|WARNING|ERROR",
      "logger": "lpg.audit",
      "message": "Request processed",
      "request_id": "string",
      "virtual_key_hash": "string (hashed for security)",
      "provider": "string",
      "endpoint": "string",
      "status_code": "integer",
      "latency_ms": "number",
      "pii_detected": "integer",
      "pii_masked": "integer",
      "client_ip": "string",
      "user_agent": "string",
      "extra": {}
    },
    "example_entry": {
      "timestamp": "2026-04-04T10:00:00.123Z",
      "level": "INFO",
      "logger": "lpg.audit",
      "message": "Request processed successfully",
      "request_id": "req-abc123def456",
      "virtual_key_hash": "a1b2c3d4e5f6",
      "provider": "openai",
      "endpoint": "/v1/chat/completions",
      "status_code": 200,
      "latency_ms": 850,
      "pii_detected": 2,
      "pii_masked": 2,
      "client_ip": "192.168.1.100",
      "user_agent": "OpenAI/1.0"
    }
  }
}
```

---

## 附录：测试数据生成脚本

```python
# 用于生成测试数据的辅助脚本

def generate_test_request(pii_count: int = 0, stream: bool = False) -> dict:
    """生成测试请求"""
    base_content = "Hello, how are you today?"
    if pii_count == 1:
        base_content = "My email is user@example.com"
    elif pii_count == 2:
        base_content = "Contact me at user@example.com or 13812345678"
    elif pii_count >= 3:
        base_content = "I'm 张三, my email is zhangsan@example.com, ID: 110101199001011234"
    
    return {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": base_content}],
        "stream": stream
    }

def generate_virtual_key(provider: str = "openai", valid: bool = True) -> str:
    """生成虚拟Key"""
    if not valid:
        return "invalid-key"
    return f"sk-virtual-{provider}-{hash(provider) % 100000:05d}"

def generate_pii_detection_result(text: str, entity_type: str) -> dict:
    """生成PII检测结果"""
    return {
        "entity_type": entity_type,
        "start": 0,
        "end": len(text),
        "score": 0.95
    }
```
