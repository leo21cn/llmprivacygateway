"""Virtual Key manager."""

import secrets
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime
from lpg.core.config.service import ConfigService


class KeyManager:
    """虚拟 Key 管理器.

    职责:
    1. 生成虚拟 Key
    2. 管理虚拟 Key 与真实 Key 的映射
    3. Key 的生命周期管理
    """

    KEY_PREFIX = "sk-virtual-"

    def __init__(self, config_service: ConfigService):
        """初始化 Key 管理器.

        Args:
            config_service: 配置服务
        """
        self._config = config_service
        self._keys: Dict[str, Dict] = {}
        self._load_keys()

    def _load_keys(self):
        """从配置加载 Key."""
        keys_config = self._config.get("virtual_keys", [])
        for key_config in keys_config:
            # Handle both dict and VirtualKeyConfig objects
            if hasattr(key_config, "id"):
                # It's a VirtualKeyConfig object
                key_dict = {
                    "id": key_config.id,
                    "virtual_key": key_config.virtual_key,
                    "provider": key_config.provider,
                    "name": key_config.name,
                    "created_at": getattr(key_config, "created_at", None),
                    "expires_at": getattr(key_config, "expires_at", None),
                    "permissions": getattr(key_config, "permissions", {}),
                    "usage_count": getattr(key_config, "usage_count", 0),
                    "last_used": getattr(key_config, "last_used", None),
                }
                self._keys[key_dict["id"]] = key_dict
            elif isinstance(key_config, dict):
                self._keys[key_config["id"]] = key_config

    def _save_keys(self):
        """保存 Key 到配置."""
        # Convert key records to plain dicts for storage
        keys_list = []
        for key_record in self._keys.values():
            # Ensure all values are serializable
            key_dict = {
                "id": key_record["id"],
                "virtual_key": key_record["virtual_key"],
                "provider": key_record["provider"],
                "name": key_record["name"],
                "created_at": key_record["created_at"],
                "expires_at": key_record.get("expires_at"),
                "permissions": key_record.get("permissions", {}),
                "usage_count": key_record.get("usage_count", 0),
                "last_used": key_record.get("last_used"),
            }
            keys_list.append(key_dict)
        self._config.set("virtual_keys", keys_list)

    def create(
        self,
        provider: str,
        name: str,
        expires_at: Optional[str] = None,
        permissions: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """创建虚拟 Key.

        Args:
            provider: 提供商名称
            name: Key 标识名称
            expires_at: 过期时间
            permissions: 权限配置

        Returns:
            创建的 Key 信息
        """
        provider_config = self._config.get_provider(provider)
        if not provider_config:
            raise ValueError(f"Provider '{provider}' not found")

        random_part = secrets.token_hex(24)
        virtual_key = f"{self.KEY_PREFIX}{random_part}"
        key_id = hashlib.sha256(virtual_key.encode()).hexdigest()[:16]

        key_record = {
            "id": f"vk_{key_id}",
            "virtual_key": virtual_key,
            "provider": provider,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "permissions": permissions or {},
            "usage_count": 0,
            "last_used": None,
        }

        self._keys[key_record["id"]] = key_record
        self._save_keys()

        return key_record

    def resolve(self, virtual_key: str) -> Optional[Dict[str, Any]]:
        """解析虚拟 Key.

        Args:
            virtual_key: 虚拟 Key 字符串

        Returns:
            映射信息或 None
        """
        for key_id, key_record in self._keys.items():
            if key_record["virtual_key"] == virtual_key:
                if self._is_expired(key_record):
                    return None

                provider = key_record["provider"]
                real_key = self._config.get_provider_key(provider)

                if not real_key:
                    return None

                key_record["usage_count"] += 1
                key_record["last_used"] = datetime.now().isoformat()
                self._save_keys()

                return {
                    "provider": provider,
                    "real_key": real_key,
                    "key_id": key_id,
                }

        return None

    def list_all(self) -> List[Dict[str, Any]]:
        """列出所有 Key."""
        return [
            {
                "id": k["id"],
                "name": k["name"],
                "provider": k["provider"],
                "virtual_key": k["virtual_key"],
                "created_at": k["created_at"],
                "expires_at": k.get("expires_at"),
                "usage_count": k.get("usage_count", 0),
                "last_used": k.get("last_used"),
            }
            for k in self._keys.values()
        ]

    def get_info(self, key_id: str) -> Optional[Dict[str, Any]]:
        """获取 Key 详情."""
        return self._keys.get(key_id)

    def revoke(self, key_id: str) -> bool:
        """吊销 Key."""
        if key_id in self._keys:
            del self._keys[key_id]
            self._save_keys()
            return True
        return False

    def count(self) -> int:
        """获取有效 Key 数量."""
        return len([k for k in self._keys.values() if not self._is_expired(k)])

    def _is_expired(self, key_record: Dict) -> bool:
        """检查 Key 是否过期."""
        expires_at = key_record.get("expires_at")
        if not expires_at:
            return False
        return datetime.fromisoformat(expires_at) < datetime.now()
