# CLI 命令测试数据

## 1. 全局选项测试数据

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| GLOBAL-001 | 有效配置文件路径 | `--config /etc/lpg/config.yaml` | 成功加载配置 | 标准配置文件路径 |
| GLOBAL-002 | 有效配置文件路径（相对路径） | `--config ./config.yaml` | 成功加载配置 | 相对路径，文件存在 |
| GLOBAL-003 | 有效配置文件路径（家目录） | `--config ~/lpg/config.yaml` | 成功加载配置 | 使用~扩展 |
| GLOBAL-004 | 无效配置文件路径（格式错误） | `--config /invalid/path/config.txt` | 错误：配置文件格式不支持 | 非YAML/JSON扩展名 |
| GLOBAL-005 | 不存在的配置文件路径 | `--config /nonexistent/config.yaml` | 错误：配置文件不存在 | 文件路径无效 |
| GLOBAL-006 | 空配置文件路径 | `--config ""` | 错误：配置文件路径不能为空 | 空字符串 |
| GLOBAL-007 | 仅verbose模式 | `-v` | 输出详细调试信息 | 单个-v |
| GLOBAL-008 | 仅quiet模式 | `-q` | 仅输出错误信息 | 单个-q |
| GLOBAL-009 | 仅JSON输出模式 | `--json` | 输出JSON格式 | 启用JSON模式 |
| GLOBAL-010 | verbose + JSON模式 | `-v --json` | JSON格式的详细输出 | 组合使用 |
| GLOBAL-011 | quiet + JSON模式 | `-q --json` | JSON格式的错误输出 | 组合使用，quiet优先 |
| GLOBAL-012 | verbose + quiet模式 | `-v -q` | quiet模式优先，仅错误 | 冲突处理，quiet优先 |
| GLOBAL-013 | 多级verbose | `-vvv` | 极详细调试输出 | 多个-v |
| GLOBAL-014 | 帮助信息 | `--help` | 显示帮助信息 | 全局帮助 |
| GLOBAL-015 | 版本信息 | `--version` | 显示版本号 | 版本查询 |

## 2. start命令测试数据

### 2.1 端口测试

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| START-001 | 有效端口（8080） | `--port 8080` | 服务启动在8080端口 | 默认端口 |
| START-002 | 有效端口（80） | `--port 80` | 服务启动在80端口 | HTTP标准端口 |
| START-003 | 有效端口（65535） | `--port 65535` | 服务启动在65535端口 | 最大端口号 |
| START-004 | 有效端口（1024） | `--port 1024` | 服务启动在1024端口 | 非特权端口 |
| START-005 | 无效端口（0） | `--port 0` | 错误：端口必须在1-65535之间 | 端口0无效 |
| START-006 | 无效端口（-1） | `--port -1` | 错误：端口必须是正整数 | 负数端口 |
| START-007 | 无效端口（65536） | `--port 65536` | 错误：端口必须在1-65535之间 | 超出范围 |
| START-008 | 无效端口（99999） | `--port 99999` | 错误：端口必须在1-65535之间 | 大幅超出范围 |
| START-009 | 无效端口（非数字） | `--port abc` | 错误：端口必须是数字 | 非数字字符串 |
| START-010 | 无效端口（空字符串） | `--port ""` | 错误：端口不能为空 | 空值 |
| START-011 | 无效端口（小数） | `--port 80.5` | 错误：端口必须是整数 | 浮点数 |
| START-012 | 无效端口（特殊字符） | `--port 8080!` | 错误：端口必须是数字 | 包含特殊字符 |

### 2.2 Host地址测试

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| START-013 | 有效host（127.0.0.1） | `--host 127.0.0.1` | 服务绑定到127.0.0.1 | 本地回环地址 |
| START-014 | 有效host（0.0.0.0） | `--host 0.0.0.0` | 服务绑定到所有接口 | 监听所有地址 |
| START-015 | 有效host（localhost） | `--host localhost` | 服务绑定到localhost | 主机名 |
| START-016 | 有效host（IPv6本地） | `--host ::1` | 服务绑定到::1 | IPv6回环地址 |
| START-017 | 有效host（IPv6所有） | `--host ::` | 服务绑定到所有IPv6接口 | IPv6通配符 |
| START-018 | 无效host（999.999.999.999） | `--host 999.999.999.999` | 错误：无效的IP地址 | 超出范围的IP |
| START-019 | 无效host（abc） | `--host abc` | 错误：无效的主机名 | 非法主机名 |
| START-020 | 无效host（空字符串） | `--host ""` | 错误：主机名不能为空 | 空值 |
| START-021 | 无效host（包含空格） | `--host "127. 0.0.1"` | 错误：无效的IP地址 | 包含空格 |

### 2.3 日志级别测试

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| START-022 | 有效log-level（debug） | `--log-level debug` | 设置日志级别为DEBUG | 最详细 |
| START-023 | 有效log-level（info） | `--log-level info` | 设置日志级别为INFO | 默认级别 |
| START-024 | 有效log-level（warn） | `--log-level warn` | 设置日志级别为WARNING | 警告级别 |
| START-025 | 有效log-level（error） | `--log-level error` | 设置日志级别为ERROR | 仅错误 |
| START-026 | 有效log-level（DEBUG） | `--log-level DEBUG` | 设置日志级别为DEBUG | 大写，应该不区分大小写 |
| START-027 | 无效log-level（trace） | `--log-level trace` | 错误：无效的日志级别 | 不支持的级别 |
| START-028 | 无效log-level（空字符串） | `--log-level ""` | 错误：日志级别不能为空 | 空值 |
| START-029 | 无效log-level（数字） | `--log-level 123` | 错误：无效的日志级别 | 数字值 |

### 2.4 日志文件测试

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| START-030 | 有效log-file路径 | `--log-file /var/log/lpg.log` | 日志输出到指定文件 | 可写路径 |
| START-031 | 有效log-file路径（相对路径） | `--log-file ./lpg.log` | 日志输出到相对路径文件 | 当前目录 |
| START-032 | 有效log-file路径（自动创建） | `--log-file /tmp/new_dir/lpg.log` | 自动创建目录并写入日志 | 目录不存在时创建 |
| START-033 | 无效log-file路径（无权限） | `--log-file /root/lpg.log` | 错误：无法写入日志文件 | 权限不足 |
| START-034 | 无效log-file路径（只读目录） | `--log-file /readonly_dir/lpg.log` | 错误：无法写入日志文件 | 目录只读 |
| START-035 | 无效log-file路径（空字符串） | `--log-file ""` | 错误：日志文件路径不能为空 | 空值 |
| START-036 | 无效log-file路径（特殊字符） | `--log-file "/path/with spaces/lpg.log"` | 正常工作 | 路径包含空格，需要引号 |

### 2.5 组合测试

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| START-037 | 所有有效参数 | `--host 0.0.0.0 --port 8080 --log-level debug --log-file /tmp/lpg.log` | 服务成功启动 | 完整参数 |
| START-038 | 无效端口+有效host | `--port 70000 --host 127.0.0.1` | 错误：端口无效 | 验证参数顺序处理 |
| START-039 | 无参数启动 | （无参数） | 使用默认配置启动 | 默认host=127.0.0.1, port=8080 |

## 3. stop命令测试数据

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| STOP-001 | 正常停止 | `stop` | 优雅停止服务 | 发送SIGTERM |
| STOP-002 | 强制停止 | `stop -f` | 强制停止服务 | 发送SIGKILL |
| STOP-003 | 强制停止（长选项） | `stop --force` | 强制停止服务 | 等同于-f |
| STOP-004 | 服务未运行时停止 | `stop` | 提示：服务未运行 | 无进程运行 |
| STOP-005 | 服务未运行时强制停止 | `stop -f` | 提示：服务未运行 | 强制模式也需检查 |
| STOP-006 | 停止超时 | `stop --timeout 5` | 等待5秒后强制停止 | 超时参数 |
| STOP-007 | 停止超时（无效值） | `stop --timeout abc` | 错误：超时必须是数字 | 非数字值 |
| STOP-008 | 停止超时（负数） | `stop --timeout -1` | 错误：超时必须是正数 | 负数超时 |
| STOP-009 | 停止其他用户服务 | `stop` | 错误：无权停止其他用户服务 | 权限检查 |

## 4. status命令测试数据

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| STATUS-001 | 服务运行时状态 | `status` | 显示运行状态、PID、端口等 | 正常运行 |
| STATUS-002 | 服务未运行时状态 | `status` | 提示：服务未运行 | 无进程 |
| STATUS-003 | JSON格式输出（运行中） | `status --json` | JSON格式的状态信息 | 包含所有字段 |
| STATUS-004 | JSON格式输出（未运行） | `status --json` | JSON格式，running=false | 未运行状态 |
| STATUS-005 | 简洁模式 | `status -q` | 仅显示运行状态 | 简洁输出 |
| STATUS-006 | 详细模式 | `status -v` | 显示详细运行信息 | 包含系统信息 |
| STATUS-007 | 检查其他实例 | `status --instance myapp` | 检查指定实例状态 | 多实例支持 |

## 5. config命令测试数据

### 5.1 配置项查询

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| CONFIG-001 | 有效配置项（proxy.host） | `config get proxy.host` | 返回当前host值 | 嵌套配置 |
| CONFIG-002 | 有效配置项（proxy.port） | `config get proxy.port` | 返回当前端口值 | 数字类型 |
| CONFIG-003 | 有效配置项（presidio.endpoint） | `config get presidio.endpoint` | 返回Presidio端点URL | 完整URL |
| CONFIG-004 | 有效配置项（presidio.timeout） | `config get presidio.timeout` | 返回超时秒数 | 数字类型 |
| CONFIG-005 | 无效配置项（nonexistent.key） | `config get nonexistent.key` | 错误：配置项不存在 | 无效键 |
| CONFIG-006 | 无效配置项（空字符串） | `config get ""` | 错误：配置项不能为空 | 空键 |
| CONFIG-007 | 获取所有配置 | `config list` | 列出所有配置项 | 完整配置 |
| CONFIG-008 | JSON格式配置 | `config list --json` | JSON格式的配置列表 | 格式化输出 |

### 5.2 配置值设置

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| CONFIG-009 | 设置有效host | `config set proxy.host 0.0.0.0` | 成功更新host | 有效IP |
| CONFIG-010 | 设置有效端口 | `config set proxy.port 9000` | 成功更新端口 | 有效端口 |
| CONFIG-011 | 设置无效端口（超出范围） | `config set proxy.port 70000` | 错误：端口必须在1-65535之间 | 边界检查 |
| CONFIG-012 | 设置无效端口（非数字） | `config set proxy.port abc` | 错误：端口必须是数字 | 类型检查 |
| CONFIG-013 | 设置有效超时 | `config set presidio.timeout 60` | 成功更新超时 | 正整数 |
| CONFIG-014 | 设置无效超时（负数） | `config set presidio.timeout -5` | 错误：超时必须是正数 | 范围检查 |
| CONFIG-015 | 设置字符串值 | `config set presidio.language en` | 成功更新语言 | 字符串类型 |
| CONFIG-016 | 设置布尔值 | `config set logging.enable true` | 成功启用日志 | 布尔类型 |
| CONFIG-017 | 设置无效布尔值 | `config set logging.enable maybe` | 错误：无效的布尔值 | 仅接受true/false |
| CONFIG-018 | 删除配置项 | `config delete proxy.temp` | 成功删除临时配置 | 删除操作 |
| CONFIG-019 | 删除不存在的配置项 | `config delete nonexistent` | 提示：配置项不存在 | 不存在的键 |

## 6. key命令测试数据

### 6.1 创建虚拟Key

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| KEY-001 | 有效provider（openai） | `key create --provider openai --name mykey` | 成功创建虚拟Key | 标准提供商 |
| KEY-002 | 有效provider（anthropic） | `key create --provider anthropic --name claude-key` | 成功创建虚拟Key | Anthropic提供商 |
| KEY-003 | 有效provider（custom） | `key create --provider custom --name custom-key` | 成功创建虚拟Key | 自定义提供商 |
| KEY-004 | 无效provider（unknown） | `key create --provider unknown --name test` | 错误：不支持的提供商 | 未知提供商 |
| KEY-005 | 无效provider（空字符串） | `key create --provider "" --name test` | 错误：提供商不能为空 | 空值 |
| KEY-006 | 有效key名称（字母数字） | `key create --provider openai --name mykey123` | 成功创建 | 字母数字组合 |
| KEY-007 | 有效key名称（包含连字符） | `key create --provider openai --name my-key` | 成功创建 | 支持连字符 |
| KEY-008 | 有效key名称（包含下划线） | `key create --provider openai --name my_key` | 成功创建 | 支持下划线 |
| KEY-009 | 无效key名称（特殊字符） | `key create --provider openai --name "my@key!"` | 错误：名称包含无效字符 | 特殊字符 |
| KEY-010 | 无效key名称（超长） | `key create --provider openai --name "a" * 100` | 错误：名称长度超出限制 | 超过最大长度 |
| KEY-011 | 无效key名称（空字符串） | `key create --provider openai --name ""` | 错误：名称不能为空 | 空值 |
| KEY-012 | 有效过期时间（ISO格式） | `key create --provider openai --name test --expires 2025-12-31T23:59:59Z` | 成功创建，设置过期时间 | ISO 8601格式 |
| KEY-013 | 有效过期时间（相对时间） | `key create --provider openai --name test --expires 30d` | 成功创建，30天后过期 | 相对时间 |
| KEY-014 | 无效过期时间（过去时间） | `key create --provider openai --name test --expires 2020-01-01T00:00:00Z` | 错误：过期时间不能是过去 | 时间校验 |
| KEY-015 | 无效过期时间（格式错误） | `key create --provider openai --name test --expires "next week"` | 错误：无效的时间格式 | 格式校验 |
| KEY-016 | 无过期时间 | `key create --provider openai --name test` | 成功创建，永不过期 | 可选参数 |

### 6.2 列出虚拟Key

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| KEY-017 | 列出所有Key | `key list` | 显示所有虚拟Key列表 | 完整列表 |
| KEY-018 | 按提供商筛选 | `key list --provider openai` | 仅显示OpenAI的Key | 筛选功能 |
| JSON格式输出 | `key list --json` | JSON格式的Key列表 | 格式化输出 |
| KEY-019 | 无Key时列出 | `key list` | 提示：没有虚拟Key | 空列表 |

### 6.3 查看虚拟Key详情

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| KEY-020 | 有效key-id | `key show abc123` | 显示Key详细信息 | 存在的ID |
| KEY-021 | 无效key-id（不存在） | `key show nonexistent` | 错误：Key不存在 | 无效ID |
| KEY-022 | 无效key-id（格式错误） | `key show "invalid id!"` | 错误：无效的Key ID格式 | 特殊字符 |
| KEY-023 | 无效key-id（空字符串） | `key show ""` | 错误：Key ID不能为空 | 空值 |

### 6.4 删除虚拟Key

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| KEY-024 | 删除存在的Key | `key delete abc123` | 成功删除Key | 确认删除 |
| KEY-025 | 强制删除 | `key delete abc123 -f` | 直接删除，无需确认 | 强制模式 |
| KEY-026 | 删除不存在的Key | `key delete nonexistent` | 错误：Key不存在 | 无效ID |
| KEY-027 | 删除其他用户的Key | `key delete other-user-key` | 错误：无权删除 | 权限检查 |

## 7. provider命令测试数据

### 7.1 添加提供商

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| PROVIDER-001 | 有效provider类型（openai） | `provider add openai --api-key sk-xxx` | 成功添加OpenAI提供商 | 标准类型 |
| PROVIDER-002 | 有效provider类型（anthropic） | `provider add anthropic --api-key sk-ant-xxx` | 成功添加Anthropic提供商 | Anthropic类型 |
| PROVIDER-003 | 有效provider类型（gemini） | `provider add gemini --api-key AIzaSyxxx` | 成功添加Gemini提供商 | Google类型 |
| PROVIDER-004 | 有效provider类型（custom） | `provider add custom --base-url http://api.example.com --api-key xxx` | 成功添加自定义提供商 | 需要base-url |
| PROVIDER-005 | 无效provider类型（unknown） | `provider add unknown --api-key xxx` | 错误：不支持的提供商类型 | 未知类型 |
| PROVIDER-006 | 有效base-url（HTTP） | `provider add custom --base-url http://localhost:8000 --api-key xxx` | 成功添加 | HTTP URL |
| PROVIDER-007 | 有效base-url（HTTPS） | `provider add custom --base-url https://api.example.com --api-key xxx` | 成功添加 | HTTPS URL |
| PROVIDER-008 | 无效base-url（格式错误） | `provider add custom --base-url "not a url" --api-key xxx` | 错误：无效的URL格式 | 非法URL |
| PROVIDER-009 | 无效base-url（空字符串） | `provider add custom --base-url "" --api-key xxx` | 错误：URL不能为空 | 空值 |
| PROVIDER-010 | 有效api-key格式 | `provider add openai --api-key sk-1234567890abcdef` | 成功添加 | 标准格式 |
| PROVIDER-011 | 无效api-key格式（空字符串） | `provider add openai --api-key ""` | 错误：API Key不能为空 | 空值 |
| PROVIDER-012 | 无效api-key格式（特殊字符） | `provider add openai --api-key "sk-!@#$%"` | 成功添加（密钥可能包含特殊字符） | 取决于验证规则 |
| PROVIDER-013 | 自定义提供商缺少base-url | `provider add custom --api-key xxx` | 错误：自定义提供商需要base-url | 必需参数 |

### 7.2 列出提供商

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| PROVIDER-014 | 列出所有提供商 | `provider list` | 显示所有已配置的提供商 | 完整列表 |
| PROVIDER-015 | JSON格式输出 | `provider list --json` | JSON格式的提供商列表 | 格式化输出 |
| PROVIDER-016 | 无提供商时列出 | `provider list` | 提示：没有配置提供商 | 空列表 |

### 7.3 删除提供商

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| PROVIDER-017 | 删除存在的提供商 | `provider remove openai` | 成功删除提供商 | 确认删除 |
| PROVIDER-018 | 删除不存在的提供商 | `provider remove nonexistent` | 错误：提供商不存在 | 无效类型 |
| PROVIDER-019 | 强制删除提供商 | `provider remove openai -f` | 直接删除，无需确认 | 强制模式 |

## 8. rule命令测试数据

### 8.1 添加规则

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| RULE-001 | 有效YAML规则文件 | `rule add rules/pii.yaml` | 成功添加PII规则 | 格式正确 |
| RULE-002 | 有效JSON规则文件 | `rule add rules/pii.json` | 成功添加PII规则 | JSON格式支持 |
| RULE-003 | 无效规则文件（格式错误） | `rule add invalid.yaml` | 错误：规则文件格式错误 | YAML语法错误 |
| RULE-004 | 无效规则文件（结构错误） | `rule add bad_structure.yaml` | 错误：规则结构不完整 | 缺少必需字段 |
| RULE-005 | 不存在的规则文件 | `rule add nonexistent.yaml` | 错误：规则文件不存在 | 文件不存在 |
| RULE-006 | 有效分类（pii） | `rule add rules/pii.yaml --category pii` | 成功添加到pii分类 | 指定分类 |
| RULE-007 | 有效分类（credentials） | `rule add rules/credentials.yaml --category credentials` | 成功添加到credentials分类 | 凭证分类 |
| RULE-008 | 有效分类（finance） | `rule add rules/finance.yaml --category finance` | 成功添加到finance分类 | 金融分类 |
| RULE-009 | 无效分类（unknown） | `rule add rules/pii.yaml --category unknown` | 错误：无效的规则分类 | 不支持的分类 |
| RULE-010 | 自动检测分类 | `rule add rules/pii.yaml` | 自动识别为pii分类 | 无分类参数 |

### 8.2 列出规则

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| RULE-011 | 列出所有规则 | `rule list` | 显示所有已添加的规则 | 完整列表 |
| RULE-012 | 按分类筛选 | `rule list --category pii` | 仅显示PII规则 | 分类筛选 |
| RULE-013 | JSON格式输出 | `rule list --json` | JSON格式的规则列表 | 格式化输出 |
| RULE-014 | 无规则时列出 | `rule list` | 提示：没有规则 | 空列表 |

### 8.3 查看规则详情

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| RULE-015 | 有效规则ID | `rule show pii-email` | 显示规则详细信息 | 存在的ID |
| RULE-016 | 无效规则ID（不存在） | `rule show nonexistent` | 错误：规则不存在 | 无效ID |
| RULE-017 | 无效规则ID（格式错误） | `rule show "invalid id!"` | 错误：无效的规则ID格式 | 特殊字符 |
| RULE-018 | 无效规则ID（空字符串） | `rule show ""` | 错误：规则ID不能为空 | 空值 |

### 8.4 删除规则

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| RULE-019 | 删除存在的规则 | `rule delete pii-email` | 成功删除规则 | 确认删除 |
| RULE-020 | 强制删除规则 | `rule delete pii-email -f` | 直接删除，无需确认 | 强制模式 |
| RULE-021 | 删除不存在的规则 | `rule delete nonexistent` | 错误：规则不存在 | 无效ID |

## 9. log命令测试数据

### 9.1 查看日志

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| LOG-001 | 有效行数（10） | `log show --lines 10` | 显示最后10行日志 | 小数量 |
| LOG-002 | 有效行数（100） | `log show --lines 100` | 显示最后100行日志 | 中等数量 |
| LOG-003 | 有效行数（1000） | `log show --lines 1000` | 显示最后1000行日志 | 大数量 |
| LOG-004 | 无效行数（0） | `log show --lines 0` | 错误：行数必须是正整数 | 零行 |
| LOG-005 | 无效行数（-1） | `log show --lines -1` | 错误：行数必须是正整数 | 负数 |
| LOG-006 | 无效行数（非数字） | `log show --lines abc` | 错误：行数必须是数字 | 非数字字符串 |
| LOG-007 | 无效行数（空字符串） | `log show --lines ""` | 错误：行数不能为空 | 空值 |
| LOG-008 | 无效行数（小数） | `log show --lines 10.5` | 错误：行数必须是整数 | 浮点数 |
| LOG-009 | 默认行数 | `log show` | 显示默认行数（如50行） | 无参数时 |

### 9.2 时间范围筛选

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| LOG-010 | 有效时间范围（1h） | `log show --since 1h` | 显示最近1小时的日志 | 小时单位 |
| LOG-011 | 有效时间范围（1d） | `log show --since 1d` | 显示最近1天的日志 | 天单位 |
| LOG-012 | 有效时间范围（1w） | `log show --since 1w` | 显示最近1周的日志 | 周单位 |
| LOG-013 | 有效时间范围（30m） | `log show --since 30m` | 显示最近30分钟的日志 | 分钟单位 |
| LOG-014 | 有效时间范围（ISO时间） | `log show --since 2024-01-01T00:00:00Z` | 显示指定时间后的日志 | 绝对时间 |
| LOG-015 | 无效时间范围（格式错误） | `log show --since "last week"` | 错误：无效的时间格式 | 非标准格式 |
| LOG-016 | 无效时间范围（空字符串） | `log show --since ""` | 错误：时间范围不能为空 | 空值 |
| LOG-017 | 无效时间范围（未来时间） | `log show --since 2099-01-01T00:00:00Z` | 提示：没有日志 | 时间在未来 |

### 9.3 日志级别筛选

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| LOG-018 | 有效日志级别（debug） | `log show --level debug` | 显示debug及以上级别 | 最详细 |
| LOG-019 | 有效日志级别（info） | `log show --level info` | 显示info及以上级别 | 默认级别 |
| LOG-020 | 有效日志级别（warn） | `log show --level warn` | 显示warn及以上级别 | 警告级别 |
| LOG-021 | 有效日志级别（error） | `log show --level error` | 仅显示error级别 | 仅错误 |
| LOG-022 | 无效日志级别（trace） | `log show --level trace` | 错误：无效的日志级别 | 不支持的级别 |
| LOG-023 | 无效日志级别（空字符串） | `log show --level ""` | 错误：日志级别不能为空 | 空值 |

### 9.4 关键词搜索

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| LOG-024 | 搜索关键词 | `log show --grep "error"` | 搜索包含"error"的日志 | 关键词匹配 |
| LOG-025 | 搜索正则表达式 | `log show --grep "error.*timeout"` | 搜索匹配正则的日志 | 正则支持 |
| LOG-026 | 搜索无效正则 | `log show --grep "[invalid"` | 错误：无效的正则表达式 | 正则语法错误 |
| LOG-027 | 搜索空关键词 | `log show --grep ""` | 显示所有日志 | 空关键词 |
| LOG-028 | 大小写敏感搜索 | `log show --grep "Error" --case-sensitive` | 仅匹配大小写相同 | 区分大小写 |
| LOG-029 | 大小写不敏感搜索 | `log show --grep "error" --ignore-case` | 匹配所有大小写变体 | 不区分大小写 |

### 9.5 组合筛选

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| LOG-030 | 行数+时间范围 | `log show --lines 50 --since 1h` | 显示最近1小时的50行日志 | 组合筛选 |
| LOG-031 | 级别+关键词 | `log show --level error --grep "timeout"` | 搜索error级别的timeout日志 | 多条件 |
| LOG-032 | 所有筛选条件 | `log show --lines 100 --since 1d --level warn --grep "connection"` | 综合筛选 | 完整组合 |

## 10. 边界和异常测试数据

| 测试用例ID | 测试场景 | 参数 | 预期结果 | 备注 |
|------------|----------|------|----------|------|
| EDGE-001 | 超长命令行 | 所有参数都设置为最大长度值 | 正确处理或给出明确错误 | 边界长度 |
| EDGE-002 | 特殊字符参数 | 包含Unicode、emoji的参数 | 正确处理或给出明确错误 | 字符编码 |
| EDGE-003 | 并发命令执行 | 同时运行多个CLI命令 | 正确处理并发，无冲突 | 并发安全 |
| EDGE-004 | 权限不足场景 | 操作需要root权限的资源 | 给出明确的权限错误提示 | 权限处理 |
| EDGE-005 | 磁盘空间不足 | 写入操作时磁盘已满 | 给出明确的磁盘空间错误 | 资源处理 |
| EDGE-006 | 网络连接失败 | 需要网络连接的操作 | 给出明确的网络错误提示 | 网络处理 |
| EDGE-007 | 配置文件损坏 | 使用损坏的YAML配置文件 | 给出明确的配置解析错误 | 文件处理 |
| EDGE-008 | 信号中断处理 | Ctrl+C中断长时间操作 | 正确清理资源并退出 | 信号处理 |

## 测试数据文件说明

### 文件格式
- 本文件为Markdown格式，包含所有CLI命令的测试数据
- 每个测试用例包含：测试用例ID、测试场景、参数、预期结果、备注

### 使用说明
1. 测试用例ID格式：`{模块}-{序号}`，如`START-001`
2. 参数列包含完整的命令行参数
3. 预期结果描述期望的行为
4. 备注提供额外的测试说明

### 覆盖率目标
- 语句覆盖率：>95%
- 分支覆盖率：>95%
- 条件覆盖率：>90%
- 路径覆盖率：>85%

### 测试环境要求
- 操作系统：Linux/macOS/Windows
- Python版本：3.8+
- 依赖：pytest, pytest-cov
- 测试配置：独立测试环境，避免影响生产配置

### 测试数据维护
- 随代码更新同步更新测试数据
- 新增功能必须添加对应的测试用例
- 定期审查测试覆盖率，确保达到目标