"""Configuration data models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ProxyConfig(BaseModel):
    """代理配置."""

    host: str = "127.0.0.1"
    port: int = 8080
    timeout: int = 60
    max_connections: int = 100


class PresidioConfig(BaseModel):
    """Presidio 配置."""

    enabled: bool = True
    endpoint: str = "http://localhost:5001"
    language: str = "zh"


class LogConfig(BaseModel):
    """日志配置."""

    level: str = "info"
    file: Optional[str] = None
    max_size: str = "100MB"
    max_files: int = 10
    format: str = "json"


class ProviderConfig(BaseModel):
    """LLM 提供商配置."""

    name: str
    type: str  # openai, anthropic, gemini, custom
    base_url: str
    auth_type: str = "bearer"
    api_key_file: Optional[str] = None
    timeout: int = 60


class VirtualKeyConfig(BaseModel):
    """虚拟 Key 配置."""

    id: str
    name: str
    provider: str
    virtual_key: str
    permissions: Dict[str, Any] = Field(default_factory=dict)
    expires_at: Optional[str] = None


class RulesConfig(BaseModel):
    """规则配置."""

    enabled_categories: List[str] = Field(default_factory=lambda: ["pii", "credentials"])
    custom_rules_dir: Optional[str] = None


class MaskingConfig(BaseModel):
    """脱敏配置."""

    default_strategy: str = "replace"
    enable_restoration: bool = True


class AuditConfig(BaseModel):
    """审计配置."""

    enabled: bool = True
    log_file: Optional[str] = None
    retention_days: int = 30


class GatewayConfig(BaseModel):
    """网关主配置."""

    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    presidio: PresidioConfig = Field(default_factory=PresidioConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    providers: List[ProviderConfig] = Field(default_factory=list)
    virtual_keys: List[VirtualKeyConfig] = Field(default_factory=list)
    rules: RulesConfig = Field(default_factory=RulesConfig)
    masking: MaskingConfig = Field(default_factory=MaskingConfig)
    audit: AuditConfig = Field(default_factory=AuditConfig)
