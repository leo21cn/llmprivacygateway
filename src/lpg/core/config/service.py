"""Configuration service."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from lpg.models.config import GatewayConfig, ProviderConfig


class ConfigService:
    """配置服务.

    职责:
    1. 加载和管理配置
    2. 支持多层级配置优先级
    3. 配置持久化
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化配置服务.

        Args:
            config_path: 配置文件路径，None则使用默认路径
        """
        self._config_path = config_path or self._get_default_config_path()
        self._config = self._load_config()

    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径."""
        home = Path.home()
        config_dir = home / ".llm-privacy-gateway"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.yaml")

    def _load_config(self) -> GatewayConfig:
        """加载配置."""
        if Path(self._config_path).exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                return GatewayConfig(**data)
            except Exception:
                pass
        return GatewayConfig()

    def save(self) -> None:
        """保存配置到文件."""
        Path(self._config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self._config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config.model_dump(), f, allow_unicode=True, sort_keys=False)

    def get(self, key: Optional[str] = None, default: Any = None) -> Any:
        """获取配置项.

        Args:
            key: 配置键，支持点号分隔（如 'proxy.port'）
            default: 默认值

        Returns:
            配置值
        """
        if key is None:
            return self._config

        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            elif hasattr(value, k):
                value = getattr(value, k, default)
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """设置配置项.

        Args:
            key: 配置键，支持点号分隔（如 'proxy.port'）
            value: 配置值
        """
        keys = key.split(".")
        target = self._config

        for k in keys[:-1]:
            if isinstance(target, dict):
                if k not in target:
                    target[k] = {}
                target = target[k]
            elif hasattr(target, k):
                attr_value = getattr(target, k)
                # If attribute is None or not a dict/model, create a dict for it
                if attr_value is None:
                    setattr(target, k, {})
                    target = getattr(target, k)
                elif hasattr(attr_value, '__dict__') or isinstance(attr_value, dict):
                    target = attr_value
                else:
                    # Create nested structure as dict
                    setattr(target, k, {})
                    target = getattr(target, k)
            else:
                # Create new attribute as dict
                setattr(target, k, {})
                target = getattr(target, k)

        last_key = keys[-1]
        if isinstance(target, dict):
            target[last_key] = value
        elif hasattr(target, last_key):
            setattr(target, last_key, value)
        else:
            # Create new attribute
            setattr(target, last_key, value)

        self.save()

    def get_provider(self, name: str) -> Optional[Dict[str, Any]]:
        """获取提供商配置."""
        for provider in self._config.providers:
            if provider.name == name:
                return provider.model_dump()
        return None

    def get_provider_key(self, name: str) -> Optional[str]:
        """获取提供商 API Key."""
        provider = self.get_provider(name)
        if not provider:
            return None
        
        # Check for api_key directly (for testing)
        if provider.get("api_key"):
            return provider["api_key"]
        
        # Check for api_key_file
        if provider.get("api_key_file"):
            key_file = Path(provider["api_key_file"]).expanduser()
            if key_file.exists():
                return key_file.read_text().strip()
        return None

    def get_providers(self) -> List[Dict[str, Any]]:
        """获取所有提供商."""
        return [p.model_dump() for p in self._config.providers]

    def add_provider(self, provider_type: str, name: str, **kwargs) -> Dict[str, Any]:
        """添加提供商."""
        provider = ProviderConfig(
            name=name,
            type=provider_type,
            base_url=kwargs.get("base_url", ""),
            auth_type=kwargs.get("auth_type", "bearer"),
            api_key_file=kwargs.get("api_key_file"),
            timeout=kwargs.get("timeout", 60),
        )
        self._config.providers.append(provider)
        self.save()
        return provider.model_dump()

    def init(self, interactive: bool = True) -> None:
        """初始化配置."""
        if not Path(self._config_path).exists():
            self.save()
