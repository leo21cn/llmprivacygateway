# 配置管理测试数据

## 1. 配置文件路径测试数据

### 1.1 有效路径测试数据

| 测试ID | 路径类型 | 路径值 | 描述 |
|--------|----------|--------|------|
| CFG-PATH-001 | 默认全局路径 | `~/.llm-privacy-gateway/config.yaml` | 用户主目录下的默认配置文件 |
| CFG-PATH-002 | 默认本地路径 | `./.lpg/config.yaml` | 当前目录下的本地配置文件 |
| CFG-PATH-003 | 自定义路径 | `/tmp/test-config.yaml` | 临时测试配置文件 |
| CFG-PATH-004 | 绝对路径 | `/etc/lpg/config.yaml` | 系统级配置文件 |
| CFG-PATH-005 | 相对路径 | `config/dev.yaml` | 相对于当前目录的配置文件 |

### 1.2 无效路径测试数据

| 测试ID | 路径类型 | 路径值 | 预期错误 | 描述 |
|--------|----------|--------|----------|------|
| CFG-PATH-101 | 不存在路径 | `/nonexistent/path/config.yaml` | FileNotFoundError | 路径不存在 |
| CFG-PATH-102 | 无权限路径 | `/root/config.yaml` | PermissionError | 无读取权限 |
| CFG-PATH-103 | 目录路径 | `/tmp/config_dir/` | IsADirectoryError | 路径是目录而非文件 |
| CFG-PATH-104 | 空路径 | `""` | ValueError | 空路径字符串 |
| CFG-PATH-105 | 特殊字符路径 | `/tmp/config\x00.yaml` | ValueError | 包含空字符 |

## 2. 代理配置测试数据

### 2.1 有效host测试数据

| 测试ID | host值 | 描述 |
|--------|--------|------|
| CFG-HOST-001 | `127.0.0.1` | 本地回环地址 |
| CFG-HOST-002 | `0.0.0.0` | 监听所有接口 |
| CFG-HOST-003 | `localhost` | 本地主机名 |
| CFG-HOST-004 | `192.168.1.100` | 私有网络IP |
| CFG-HOST-005 | `proxy.example.com` | 有效域名 |

### 2.2 无效host测试数据

| 测试ID | host值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-HOST-101 | `999.999.999.999` | ValidationError | 无效IP地址 |
| CFG-HOST-102 | `abc` | ValidationError | 非法主机名（非localhost） |
| CFG-HOST-103 | `""` | ValidationError | 空字符串 |
| CFG-HOST-104 | `256.1.1.1` | ValidationError | IP地址超出范围 |
| CFG-HOST-105 | `host with spaces` | ValidationError | 包含空格 |

### 2.3 有效端口测试数据

| 测试ID | 端口值 | 描述 |
|--------|--------|------|
| CFG-PORT-001 | `8080` | 常用代理端口 |
| CFG-PORT-002 | `80` | HTTP默认端口 |
| CFG-PORT-003 | `443` | HTTPS默认端口 |
| CFG-PORT-004 | `3000` | 常用开发端口 |
| CFG-PORT-005 | `65535` | 最大有效端口 |
| CFG-PORT-006 | `1024` | 注册端口起始 |

### 2.4 无效端口测试数据

| 测试ID | 端口值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-PORT-101 | `0` | ValidationError | 端口0（需要root权限） |
| CFG-PORT-102 | `-1` | ValidationError | 负数端口 |
| CFG-PORT-103 | `65536` | ValidationError | 超出最大端口范围 |
| CFG-PORT-104 | `99999` | ValidationError | 超大端口值 |
| CFG-PORT-105 | `abc` | ValidationError | 非数字端口 |
| CFG-PORT-106 | `80.5` | ValidationError | 浮点数端口 |

### 2.5 有效超时测试数据

| 测试ID | 超时值（秒） | 描述 |
|--------|--------------|------|
| CFG-TIMEOUT-001 | `1` | 最小有效超时 |
| CFG-TIMEOUT-002 | `30` | 默认超时 |
| CFG-TIMEOUT-003 | `60` | 常用超时 |
| CFG-TIMEOUT-004 | `120` | 长超时 |
| CFG-TIMEOUT-005 | `300` | 最大有效超时 |

### 2.6 无效超时测试数据

| 测试ID | 超时值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-TIMEOUT-101 | `0` | ValidationError | 零超时 |
| CFG-TIMEOUT-102 | `-1` | ValidationError | 负数超时 |
| CFG-TIMEOUT-103 | `301` | ValidationError | 超出最大超时 |
| CFG-TIMEOUT-104 | `abc` | ValidationError | 非数字超时 |
| CFG-TIMEOUT-105 | `30.5` | ValidationError | 浮点数超时 |

### 2.7 有效最大连接数测试数据

| 测试ID | 最大连接数 | 描述 |
|--------|------------|------|
| CFG-MAXCONN-001 | `1` | 最小有效连接数 |
| CFG-MAXCONN-002 | `50` | 常用连接数 |
| CFG-MAXCONN-003 | `100` | 默认最大连接数 |
| CFG-MAXCONN-004 | `1000` | 高并发连接数 |

### 2.8 无效最大连接数测试数据

| 测试ID | 最大连接数 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-MAXCONN-101 | `0` | ValidationError | 零连接数 |
| CFG-MAXCONN-102 | `-1` | ValidationError | 负数连接数 |
| CFG-MAXCONN-103 | `10001` | ValidationError | 超出最大连接数 |
| CFG-MAXCONN-104 | `abc` | ValidationError | 非数字连接数 |
| CFG-MAXCONN-105 | `50.5` | ValidationError | 浮点数连接数 |

## 3. Presidio配置测试数据

### 3.1 有效endpoint测试数据

| 测试ID | endpoint值 | 描述 |
|--------|------------|------|
| CFG-PRESIDIO-001 | `http://localhost:5001` | 本地HTTP端点 |
| CFG-PRESIDIO-002 | `https://presidio.example.com` | 远程HTTPS端点 |
| CFG-PRESIDIO-003 | `http://192.168.1.100:5001` | 内网IP端点 |
| CFG-PRESIDIO-004 | `https://presidio.internal.company.com` | 内部域名端点 |

### 3.2 无效endpoint测试数据

| 测试ID | endpoint值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-PRESIDIO-101 | `localhost:5001` | ValidationError | 缺少协议前缀 |
| CFG-PRESIDIO-102 | `abc` | ValidationError | 无效URL格式 |
| CFG-PRESIDIO-103 | `""` | ValidationError | 空字符串 |
| CFG-PRESIDIO-104 | `ftp://presidio.com` | ValidationError | 不支持的协议 |
| CFG-PRESIDIO-105 | `http://` | ValidationError | 不完整的URL |

### 3.3 有效language测试数据

| 测试ID | language值 | 描述 |
|--------|------------|------|
| CFG-LANG-001 | `zh` | 中文 |
| CFG-LANG-002 | `en` | 英文 |
| CFG-LANG-003 | `ja` | 日文 |
| CFG-LANG-004 | `ko` | 韩文 |
| CFG-LANG-005 | `de` | 德文 |
| CFG-LANG-006 | `fr` | 法文 |

### 3.4 无效language测试数据

| 测试ID | language值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-LANG-101 | `中文` | ValidationError | 非ISO 639-1代码 |
| CFG-LANG-102 | `abc` | ValidationError | 无效语言代码 |
| CFG-LANG-103 | `""` | ValidationError | 空字符串 |
| CFG-LANG-104 | `ZH` | ValidationError | 大写语言代码 |
| CFG-LANG-105 | `zho` | ValidationError | ISO 639-2代码 |

### 3.5 有效enabled测试数据

| 测试ID | enabled值 | 描述 |
|--------|-----------|------|
| CFG-ENABLED-001 | `true` | 启用Presidio |
| CFG-ENABLED-002 | `false` | 禁用Presidio |

### 3.6 无效enabled测试数据

| 测试ID | enabled值 | 预期错误 | 描述 |
|--------|-----------|----------|------|
| CFG-ENABLED-101 | `"yes"` | ValidationError | 字符串"yes" |
| CFG-ENABLED-102 | `"no"` | ValidationError | 字符串"no" |
| CFG-ENABLED-103 | `1` | ValidationError | 数字1 |
| CFG-ENABLED-104 | `0` | ValidationError | 数字0 |
| CFG-ENABLED-105 | `"True"` | ValidationError | 大写字符串 |

## 4. 日志配置测试数据

### 4.1 有效level测试数据

| 测试ID | level值 | 描述 |
|--------|---------|------|
| CFG-LOG-001 | `debug` | 调试级别 |
| CFG-LOG-002 | `info` | 信息级别 |
| CFG-LOG-003 | `warn` | 警告级别 |
| CFG-LOG-004 | `error` | 错误级别 |
| CFG-LOG-005 | `critical` | 严重错误级别 |

### 4.2 无效level测试数据

| 测试ID | level值 | 预期错误 | 描述 |
|--------|---------|----------|------|
| CFG-LOG-101 | `DEBUG` | ValidationError | 大写级别 |
| CFG-LOG-102 | `abc` | ValidationError | 无效级别 |
| CFG-LOG-103 | `""` | ValidationError | 空字符串 |
| CFG-LOG-104 | `information` | ValidationError | 完整单词 |
| CFG-LOG-105 | `5` | ValidationError | 数字级别 |

### 4.3 有效file路径测试数据

| 测试ID | file路径 | 描述 |
|--------|----------|------|
| CFG-LOGFILE-001 | `~/.llm-privacy-gateway/logs/gateway.log` | 默认日志路径 |
| CFG-LOGFILE-002 | `/tmp/lpg.log` | 临时日志文件 |
| CFG-LOGFILE-003 | `./logs/app.log` | 相对路径日志 |
| CFG-LOGFILE-004 | `/var/log/lpg/gateway.log` | 系统日志目录 |

### 4.4 无效file路径测试数据

| 测试ID | file路径 | 预期错误 | 描述 |
|--------|----------|----------|------|
| CFG-LOGFILE-101 | `/nonexistent/path/log.log` | FileNotFoundError | 路径不存在 |
| CFG-LOGFILE-102 | `/root/logs/gateway.log` | PermissionError | 无写入权限 |
| CFG-LOGFILE-103 | `""` | ValueError | 空路径 |
| CFG-LOGFILE-104 | `/tmp/log\x00.log` | ValueError | 包含空字符 |

### 4.5 有效max_size测试数据

| 测试ID | max_size值 | 描述 |
|--------|------------|------|
| CFG-LOGSIZE-001 | `1MB` | 最小有效大小 |
| CFG-LOGSIZE-002 | `100MB` | 常用日志大小 |
| CFG-LOGSIZE-003 | `1GB` | 大日志文件 |
| CFG-LOGSIZE-004 | `500KB` | 千字节单位 |
| CFG-LOGSIZE-005 | `10GB` | 超大日志文件 |

### 4.6 无效max_size测试数据

| 测试ID | max_size值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-LOGSIZE-101 | `0MB` | ValidationError | 零大小 |
| CFG-LOGSIZE-102 | `-1MB` | ValidationError | 负数大小 |
| CFG-LOGSIZE-103 | `abc` | ValidationError | 无效格式 |
| CFG-LOGSIZE-104 | `100` | ValidationError | 缺少单位 |
| CFG-LOGSIZE-105 | `100XB` | ValidationError | 无效单位 |

### 4.7 有效max_files测试数据

| 测试ID | max_files值 | 描述 |
|--------|-------------|------|
| CFG-LOGFILES-001 | `1` | 最小文件数 |
| CFG-LOGFILES-002 | `10` | 常用文件数 |
| CFG-LOGFILES-003 | `100` | 大量备份文件 |
| CFG-LOGFILES-004 | `1000` | 最大文件数 |

### 4.8 无效max_files测试数据

| 测试ID | max_files值 | 预期错误 | 描述 |
|--------|-------------|----------|------|
| CFG-LOGFILES-101 | `0` | ValidationError | 零文件数 |
| CFG-LOGFILES-102 | `-1` | ValidationError | 负数文件数 |
| CFG-LOGFILES-103 | `1001` | ValidationError | 超出最大文件数 |
| CFG-LOGFILES-104 | `abc` | ValidationError | 非数字 |
| CFG-LOGFILES-105 | `10.5` | ValidationError | 浮点数 |

### 4.9 有效format测试数据

| 测试ID | format值 | 描述 |
|--------|----------|------|
| CFG-LOGFMT-001 | `json` | JSON格式 |
| CFG-LOGFMT-002 | `text` | 文本格式 |
| CFG-LOGFMT-003 | `structured` | 结构化格式 |

### 4.10 无效format测试数据

| 测试ID | format值 | 预期错误 | 描述 |
|--------|----------|----------|------|
| CFG-LOGFMT-101 | `xml` | ValidationError | 不支持的格式 |
| CFG-LOGFMT-102 | `abc` | ValidationError | 无效格式 |
| CFG-LOGFMT-103 | `""` | ValidationError | 空字符串 |
| CFG-LOGFMT-104 | `JSON` | ValidationError | 大写格式 |

## 5. 提供商配置测试数据

### 5.1 有效name测试数据

| 测试ID | name值 | 描述 |
|--------|--------|------|
| CFG-PROV-001 | `openai` | OpenAI提供商 |
| CFG-PROV-002 | `anthropic` | Anthropic提供商 |
| CFG-PROV-003 | `gemini` | Google Gemini提供商 |
| CFG-PROV-004 | `custom` | 自定义提供商 |
| CFG-PROV-005 | `azure-openai` | Azure OpenAI |

### 5.2 无效name测试数据

| 测试ID | name值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-PROV-101 | `""` | ValidationError | 空字符串 |
| CFG-PROV-102 | `provider with spaces` | ValidationError | 包含空格 |
| CFG-PROV-103 | `provider@special` | ValidationError | 特殊字符 |
| CFG-PROV-104 | `a] + "b" * 100` | ValidationError | 超长名称 |

### 5.3 有效type测试数据

| 测试ID | type值 | 描述 |
|--------|--------|------|
| CFG-PROVTYPE-001 | `openai` | OpenAI类型 |
| CFG-PROVTYPE-002 | `anthropic` | Anthropic类型 |
| CFG-PROVTYPE-003 | `gemini` | Gemini类型 |
| CFG-PROVTYPE-004 | `custom` | 自定义类型 |

### 5.4 无效type测试数据

| 测试ID | type值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-PROVTYPE-101 | `abc` | ValidationError | 无效类型 |
| CFG-PROVTYPE-102 | `""` | ValidationError | 空字符串 |
| CFG-PROVTYPE-103 | `openai-v2` | ValidationError | 不存在的变体 |

### 5.5 有效base_url测试数据

| 测试ID | base_url值 | 描述 |
|--------|------------|------|
| CFG-URL-001 | `https://api.openai.com` | OpenAI官方API |
| CFG-URL-002 | `https://api.anthropic.com` | Anthropic官方API |
| CFG-URL-003 | `https://generativelanguage.googleapis.com` | Google API |
| CFG-URL-004 | `http://localhost:8000` | 本地开发服务器 |
| CFG-URL-005 | `https://custom-proxy.example.com/v1` | 带路径的URL |

### 5.6 无效base_url测试数据

| 测试ID | base_url值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-URL-101 | `api.openai.com` | ValidationError | 缺少协议 |
| CFG-URL-102 | `abc` | ValidationError | 无效URL |
| CFG-URL-103 | `""` | ValidationError | 空字符串 |
| CFG-URL-104 | `ftp://files.example.com` | ValidationError | 不支持的协议 |
| CFG-URL-105 | `http://` | ValidationError | 不完整URL |

### 5.7 有效auth_type测试数据

| 测试ID | auth_type值 | 描述 |
|--------|-------------|------|
| CFG-AUTH-001 | `bearer` | Bearer token认证 |
| CFG-AUTH-002 | `x-api-key` | API Key头部认证 |
| CFG-AUTH-003 | `api-key` | API Key认证 |
| CFG-AUTH-004 | `basic` | 基础认证 |

### 5.8 无效auth_type测试数据

| 测试ID | auth_type值 | 预期错误 | 描述 |
|--------|-------------|----------|------|
| CFG-AUTH-101 | `abc` | ValidationError | 无效认证类型 |
| CFG-AUTH-102 | `""` | ValidationError | 空字符串 |
| CFG-AUTH-103 | `oauth2` | ValidationError | 不支持的类型 |

### 5.9 有效api_key_file路径测试数据

| 测试ID | api_key_file值 | 描述 |
|--------|----------------|------|
| CFG-KEYFILE-001 | `~/.llm-privacy-gateway/keys/openai.key` | 默认密钥文件 |
| CFG-KEYFILE-002 | `/tmp/test-api-key.txt` | 临时密钥文件 |
| CFG-KEYFILE-003 | `./secrets/api-key.txt` | 相对路径密钥文件 |

### 5.10 无效api_key_file路径测试数据

| 测试ID | api_key_file值 | 预期错误 | 描述 |
|--------|----------------|----------|------|
| CFG-KEYFILE-101 | `/nonexistent/path/key.txt` | FileNotFoundError | 路径不存在 |
| CFG-KEYFILE-102 | `/root/secret.key` | PermissionError | 无读取权限 |
| CFG-KEYFILE-103 | `""` | ValueError | 空路径 |

## 6. 虚拟Key配置测试数据

### 6.1 有效id测试数据

| 测试ID | id值 | 描述 |
|--------|------|------|
| CFG-VKEY-001 | `sk-virtual-abc123` | OpenAI风格虚拟Key |
| CFG-VKEY-002 | `vk_abc123` | 标准虚拟Key格式 |
| CFG-VKEY-003 | `virtual-key-001` | 自定义格式 |
| CFG-VKEY-004 | `a] + "b" * 32` | 长ID格式 |

### 6.2 无效id测试数据

| 测试ID | id值 | 预期错误 | 描述 |
|--------|------|----------|------|
| CFG-VKEY-101 | `""` | ValidationError | 空字符串 |
| CFG-VKEY-102 | `key with spaces` | ValidationError | 包含空格 |
| CFG-VKEY-103 | `key@special!` | ValidationError | 特殊字符 |
| CFG-VKEY-104 | `a] + "b" * 100` | ValidationError | 超长ID |

### 6.3 有效name测试数据

| 测试ID | name值 | 描述 |
|--------|--------|------|
| CFG-VKEYNAME-001 | `vscode` | VS Code应用 |
| CFG-VKEYNAME-002 | `cursor` | Cursor编辑器 |
| CFG-VKEYNAME-003 | `我的应用` | 中文应用名 |
| CFG-VKEYNAME-004 | `Test Application` | 英文应用名 |
| CFG-VKEYNAME-005 | `app-with-dashes` | 带连字符的名称 |

### 6.4 无效name测试数据

| 测试ID | name值 | 预期错误 | 描述 |
|--------|--------|----------|------|
| CFG-VKEYNAME-101 | `""` | ValidationError | 空字符串 |
| CFG-VKEYNAME-102 | `a] + "b" * 256` | ValidationError | 超长名称 |

### 6.5 有效provider测试数据

| 测试ID | provider值 | 描述 |
|--------|------------|------|
| CFG-VKEYPROV-001 | `openai` | OpenAI提供商 |
| CFG-VKEYPROV-002 | `anthropic` | Anthropic提供商 |

### 6.6 无效provider测试数据

| 测试ID | provider值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-VKEYPROV-101 | `abc` | ValidationError | 无效提供商 |
| CFG-VKEYPROV-102 | `""` | ValidationError | 空字符串 |

### 6.7 有效permissions配置测试数据

| 测试ID | permissions值 | 描述 |
|--------|---------------|------|
| CFG-VKEYPERM-001 | `{"models": ["gpt-4", "gpt-3.5-turbo"]}` | 允许特定模型 |
| CFG-VKEYPERM-002 | `{"max_tokens": 4096}` | 限制最大令牌数 |
| CFG-VKEYPERM-003 | `{"rate_limit": 100}` | 速率限制 |
| CFG-VKEYPERM-004 | `{"models": ["*"], "max_tokens": 8192}` | 通配符模型 |

### 6.8 无效permissions配置测试数据

| 测试ID | permissions值 | 预期错误 | 描述 |
|--------|---------------|----------|------|
| CFG-VKEYPERM-101 | `{"invalid_key": "value"}` | ValidationError | 无效权限键 |
| CFG-VKEYPERM-102 | `{"max_tokens": -1}` | ValidationError | 负数令牌限制 |
| CFG-VKEYPERM-103 | `{"models": []}` | ValidationError | 空模型列表 |

### 6.9 有效expires_at测试数据

| 测试ID | expires_at值 | 描述 |
|--------|--------------|------|
| CFG-VKEYEXP-001 | `2024-12-31T23:59:59Z` | ISO 8601格式 |
| CFG-VKEYEXP-002 | `2024-12-31` | 日期格式 |
| CFG-VKEYEXP-003 | `+30d` | 相对时间（30天） |
| CFG-VKEYEXP-004 | `+1h` | 相对时间（1小时） |

### 6.10 无效expires_at测试数据

| 测试ID | expires_at值 | 预期错误 | 描述 |
|--------|--------------|----------|------|
| CFG-VKEYEXP-101 | `invalid-date` | ValidationError | 无效日期格式 |
| CFG-VKEYEXP-102 | `2024-13-01` | ValidationError | 无效月份 |
| CFG-VKEYEXP-103 | `2024-02-30` | ValidationError | 无效日期 |

## 7. 规则配置测试数据

### 7.1 有效enabled_categories测试数据

| 测试ID | enabled_categories值 | 描述 |
|--------|----------------------|------|
| CFG-RULECAT-001 | `["pii"]` | 仅PII类别 |
| CFG-RULECAT-002 | `["pii", "credentials"]` | PII和凭据类别 |
| CFG-RULECAT-003 | `["pii", "credentials", "finance"]` | 所有主要类别 |
| CFG-RULECAT-004 | `["pii", "credentials", "finance", "health"]` | 包含健康数据 |

### 7.2 无效enabled_categories测试数据

| 测试ID | enabled_categories值 | 预期错误 | 描述 |
|--------|----------------------|----------|------|
| CFG-RULECAT-101 | `["abc"]` | ValidationError | 无效类别 |
| CFG-RULECAT-102 | `""` | ValidationError | 空字符串 |
| CFG-RULECAT-103 | `[]` | ValidationError | 空列表 |
| CFG-RULECAT-104 | `"pii"` | ValidationError | 非数组格式 |

### 7.3 有效custom_rules_dir路径测试数据

| 测试ID | custom_rules_dir值 | 描述 |
|--------|---------------------|------|
| CFG-RULEDIR-001 | `~/.llm-privacy-gateway/rules` | 默认规则目录 |
| CFG-RULEDIR-002 | `/tmp/custom-rules` | 临时规则目录 |
| CFG-RULEDIR-003 | `./rules/custom` | 相对路径规则目录 |

### 7.4 无效custom_rules_dir路径测试数据

| 测试ID | custom_rules_dir值 | 预期错误 | 描述 |
|--------|---------------------|----------|------|
| CFG-RULEDIR-101 | `/nonexistent/path/rules` | FileNotFoundError | 路径不存在 |
| CFG-RULEDIR-102 | `/root/rules` | PermissionError | 无访问权限 |
| CFG-RULEDIR-103 | `""` | ValueError | 空路径 |

## 8. 脱敏配置测试数据

### 8.1 有效default_strategy测试数据

| 测试ID | default_strategy值 | 描述 |
|--------|---------------------|------|
| CFG-MASK-001 | `replace` | 替换策略 |
| CFG-MASK-002 | `mask` | 掩码策略 |
| CFG-MASK-003 | `hash` | 哈希策略 |
| CFG-MASK-004 | `redact` | 编辑策略 |

### 8.2 无效default_strategy测试数据

| 测试ID | default_strategy值 | 预期错误 | 描述 |
|--------|---------------------|----------|------|
| CFG-MASK-101 | `abc` | ValidationError | 无效策略 |
| CFG-MASK-102 | `""` | ValidationError | 空字符串 |
| CFG-MASK-103 | `REPLACE` | ValidationError | 大写策略 |

### 8.3 有效enable_restoration测试数据

| 测试ID | enable_restoration值 | 描述 |
|--------|----------------------|------|
| CFG-RESTORE-001 | `true` | 启用恢复 |
| CFG-RESTORE-002 | `false` | 禁用恢复 |

### 8.4 无效enable_restoration测试数据

| 测试ID | enable_restoration值 | 预期错误 | 描述 |
|--------|----------------------|----------|------|
| CFG-RESTORE-101 | `"yes"` | ValidationError | 字符串"yes" |
| CFG-RESTORE-102 | `"no"` | ValidationError | 字符串"no" |
| CFG-RESTORE-103 | `1` | ValidationError | 数字1 |
| CFG-RESTORE-104 | `0` | ValidationError | 数字0 |

## 9. 审计配置测试数据

### 9.1 有效enabled测试数据

| 测试ID | enabled值 | 描述 |
|--------|-----------|------|
| CFG-AUDIT-001 | `true` | 启用审计 |
| CFG-AUDIT-002 | `false` | 禁用审计 |

### 9.2 无效enabled测试数据

| 测试ID | enabled值 | 预期错误 | 描述 |
|--------|-----------|----------|------|
| CFG-AUDIT-101 | `"yes"` | ValidationError | 字符串"yes" |
| CFG-AUDIT-102 | `"no"` | ValidationError | 字符串"no" |
| CFG-AUDIT-103 | `1` | ValidationError | 数字1 |
| CFG-AUDIT-104 | `0` | ValidationError | 数字0 |

### 9.3 有效log_file路径测试数据

| 测试ID | log_file值 | 描述 |
|--------|------------|------|
| CFG-AUDITLOG-001 | `~/.llm-privacy-gateway/audit.log` | 默认审计日志 |
| CFG-AUDITLOG-002 | `/tmp/audit.log` | 临时审计日志 |
| CFG-AUDITLOG-003 | `./logs/audit.log` | 相对路径审计日志 |

### 9.4 无效log_file路径测试数据

| 测试ID | log_file值 | 预期错误 | 描述 |
|--------|------------|----------|------|
| CFG-AUDITLOG-101 | `/nonexistent/path/audit.log` | FileNotFoundError | 路径不存在 |
| CFG-AUDITLOG-102 | `/root/audit.log` | PermissionError | 无写入权限 |
| CFG-AUDITLOG-103 | `""` | ValueError | 空路径 |

### 9.5 有效retention_days测试数据

| 测试ID | retention_days值 | 描述 |
|--------|------------------|------|
| CFG-AUDITRET-001 | `1` | 最小保留天数 |
| CFG-AUDITRET-002 | `30` | 常用保留期 |
| CFG-AUDITRET-003 | `365` | 一年保留期 |
| CFG-AUDITRET-004 | `3650` | 最大保留期（10年） |

### 9.6 无效retention_days测试数据

| 测试ID | retention_days值 | 预期错误 | 描述 |
|--------|------------------|----------|------|
| CFG-AUDITRET-101 | `0` | ValidationError | 零天 |
| CFG-AUDITRET-102 | `-1` | ValidationError | 负数天数 |
| CFG-AUDITRET-103 | `3651` | ValidationError | 超出最大保留期 |
| CFG-AUDITRET-104 | `abc` | ValidationError | 非数字 |
| CFG-AUDITRET-105 | `30.5` | ValidationError | 浮点数 |

## 10. 环境变量测试数据

### 10.1 有效环境变量测试数据

| 测试ID | 环境变量 | 值 | 描述 |
|--------|----------|----|------|
| CFG-ENV-001 | `LPG_PROXY_HOST` | `127.0.0.1` | 代理主机 |
| CFG-ENV-002 | `LPG_PROXY_HOST` | `0.0.0.0` | 监听所有接口 |
| CFG-ENV-003 | `LPG_PROXY_PORT` | `8080` | 代理端口 |
| CFG-ENV-004 | `LPG_PROXY_PORT` | `9000` | 自定义端口 |
| CFG-ENV-005 | `LPG_PRESIDIO_ENDPOINT` | `http://localhost:5001` | Presidio端点 |
| CFG-ENV-006 | `LPG_LOG_LEVEL` | `debug` | 调试日志级别 |
| CFG-ENV-007 | `LPG_LOG_LEVEL` | `info` | 信息日志级别 |
| CFG-ENV-008 | `LPG_CONFIG_PATH` | `/path/to/config.yaml` | 配置文件路径 |
| CFG-ENV-009 | `LPG_PRESIDIO_ENABLED` | `true` | 启用Presidio |
| CFG-ENV-010 | `LPG_AUDIT_ENABLED` | `false` | 禁用审计 |

### 10.2 无效环境变量测试数据

| 测试ID | 环境变量 | 值 | 预期错误 | 描述 |
|--------|----------|----|----------|------|
| CFG-ENV-101 | `LPG_PROXY_HOST` | `999.999.999.999` | ValidationError | 无效IP地址 |
| CFG-ENV-102 | `LPG_PROXY_PORT` | `0` | ValidationError | 无效端口 |
| CFG-ENV-103 | `LPG_PROXY_PORT` | `65536` | ValidationError | 超出端口范围 |
| CFG-ENV-104 | `LPG_LOG_LEVEL` | `DEBUG` | ValidationError | 大写日志级别 |
| CFG-ENV-105 | `LPG_LOG_LEVEL` | `abc` | ValidationError | 无效日志级别 |
| CFG-ENV-106 | `LPG_PRESIDIO_ENABLED` | `yes` | ValidationError | 字符串"yes" |
| CFG-ENV-107 | `LPG_AUDIT_ENABLED` | `1` | ValidationError | 数字1 |

## 11. 配置合并测试数据

### 11.1 默认配置

```yaml
# 默认配置 (default_config)
proxy:
  host: "127.0.0.1"
  port: 8080
  timeout: 60
  max_connections: 100

presidio:
  endpoint: "http://localhost:5001"
  language: "zh"
  enabled: true
  timeout: 30

logging:
  level: "info"
  file: "~/.llm-privacy-gateway/logs/gateway.log"
  max_size: "100MB"
  max_files: 10
  format: "json"

providers: []

virtual_keys: []

rules:
  enabled_categories: ["pii", "credentials", "finance"]
  custom_rules_dir: null

masking:
  default_strategy: "replace"
  enable_restoration: true

audit:
  enabled: false
  log_file: "~/.llm-privacy-gateway/audit.log"
  retention_days: 30
```

### 11.2 全局配置

```yaml
# 全局配置 (~/.llm-privacy-gateway/config.yaml)
proxy:
  host: "0.0.0.0"
  port: 9000
  timeout: 120

presidio:
  endpoint: "https://presidio.example.com"
  language: "en"

logging:
  level: "debug"
  max_size: "1GB"

providers:
  - name: "openai"
    type: "openai"
    base_url: "https://api.openai.com"
    auth_type: "bearer"
```

### 11.3 本地配置

```yaml
# 本地配置 (./.lpg/config.yaml)
proxy:
  port: 3000
  timeout: 30

presidio:
  enabled: false

logging:
  level: "warn"
  file: "./logs/gateway.log"

virtual_keys:
  - id: "vk_local_001"
    name: "Local Test"
    provider: "openai"
```

### 11.4 环境变量配置

```bash
# 环境变量
export LPG_PROXY_HOST="192.168.1.100"
export LPG_PROXY_PORT="8080"
export LPG_PRESIDIO_ENDPOINT="http://presidio.local:5001"
export LPG_LOG_LEVEL="info"
```

### 11.5 命令行参数配置

```bash
# 命令行参数
--proxy-port 9090
--log-level error
--config /custom/config.yaml
```

### 11.6 合并后配置（预期结果）

```yaml
# 合并优先级：命令行参数 > 环境变量 > 本地配置 > 全局配置 > 默认配置
proxy:
  host: "192.168.1.100"        # 来自环境变量
  port: 9090                   # 来自命令行参数（最高优先级）
  timeout: 30                  # 来自本地配置
  max_connections: 100         # 来自默认配置

presidio:
  endpoint: "http://presidio.local:5001"  # 来自环境变量
  language: "en"                           # 来自全局配置
  enabled: false                           # 来自本地配置
  timeout: 30                              # 来自默认配置

logging:
  level: "error"                           # 来自命令行参数（最高优先级）
  file: "./logs/gateway.log"               # 来自本地配置
  max_size: "1GB"                          # 来自全局配置
  max_files: 10                            # 来自默认配置
  format: "json"                           # 来自默认配置

providers:
  - name: "openai"
    type: "openai"
    base_url: "https://api.openai.com"
    auth_type: "bearer"

virtual_keys:
  - id: "vk_local_001"
    name: "Local Test"
    provider: "openai"

rules:
  enabled_categories: ["pii", "credentials", "finance"]
  custom_rules_dir: null

masking:
  default_strategy: "replace"
  enable_restoration: true

audit:
  enabled: false
  log_file: "~/.llm-privacy-gateway/audit.log"
  retention_days: 30
```

## 12. 边界条件测试数据

### 12.1 空配置测试

| 测试ID | 测试场景 | 预期行为 |
|--------|----------|----------|
| CFG-EDGE-001 | 完全空的配置文件 | 使用默认配置 |
| CFG-EDGE-002 | 空的YAML文档 | 使用默认配置 |
| CFG-EDGE-003 | 只有注释的配置文件 | 使用默认配置 |

### 12.2 格式错误测试

| 测试ID | 测试场景 | 预期错误 |
|--------|----------|----------|
| CFG-EDGE-101 | 无效的YAML语法 | yaml.YAMLError |
| CFG-EDGE-102 | 包含tab缩进 | yaml.YAMLError |
| CFG-EDGE-103 | 重复的键 | yaml.YAMLError |

### 12.3 类型错误测试

| 测试ID | 测试场景 | 配置值 | 预期错误 |
|--------|----------|--------|----------|
| CFG-EDGE-201 | 端口为字符串 | `"port": "8080"` | ValidationError |
| CFG-EDGE-202 | 布尔值为字符串 | `"enabled": "true"` | ValidationError |
| CFG-EDGE-203 | 数组为字符串 | `"categories": "pii"` | ValidationError |

### 12.4 特殊字符测试

| 测试ID | 测试场景 | 配置值 | 预期行为 |
|--------|----------|--------|----------|
| CFG-EDGE-301 | 路径包含空格 | `"/path with spaces/config.yaml"` | 正常解析 |
| CFG-EDGE-302 | 路径包含中文 | `"/路径/配置.yaml"` | 正常解析 |
| CFG-EDGE-303 | 路径包含特殊符号 | `"/path/@#$%/config.yaml"` | 正常解析 |

## 13. 测试数据使用说明

### 13.1 测试数据组织

所有测试数据按照以下结构组织：
- **有效数据**：用于验证正常功能路径
- **无效数据**：用于验证错误处理和边界条件
- **边界数据**：用于验证边界值和极端情况

### 13.2 测试覆盖率要求

- **分支覆盖率**：≥95%
- **条件覆盖率**：≥90%
- **路径覆盖率**：≥85%

### 13.3 测试执行建议

1. **单元测试**：使用有效数据验证基本功能
2. **边界测试**：使用边界数据验证边界条件
3. **错误测试**：使用无效数据验证错误处理
4. **集成测试**：使用合并测试数据验证配置合并逻辑
5. **环境测试**：使用环境变量数据验证环境配置覆盖

### 13.4 测试数据维护

- 测试数据应与配置模型定义保持同步
- 新增配置项时需同步更新测试数据
- 定期审查测试数据的完整性和有效性