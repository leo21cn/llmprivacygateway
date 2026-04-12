"""Unit tests for KeyManager."""

import pytest
from datetime import datetime, timedelta
from lpg.core.key.manager import KeyManager
from lpg.core.config.service import ConfigService


class TestKeyManager:
    """Test cases for KeyManager."""

    def test_create_virtual_key_success(self, key_manager: KeyManager) -> None:
        """TC-KEY-001: 使用有效 provider 创建虚拟 Key."""
        key_record = key_manager.create(
            provider="openai",
            name="test-key-001"
        )
        
        assert key_record["id"].startswith("vk_")
        assert key_record["virtual_key"].startswith("sk-virtual-")
        assert key_record["provider"] == "openai"
        assert key_record["name"] == "test-key-001"
        assert "created_at" in key_record
        assert key_record["usage_count"] == 0
        assert key_record["last_used"] is None

    def test_create_with_invalid_provider(self, key_manager: KeyManager) -> None:
        """TC-KEY-002: 使用无效 provider 创建虚拟 Key 失败."""
        with pytest.raises(ValueError, match="Provider 'nonexistent-provider' not found"):
            key_manager.create(
                provider="nonexistent-provider",
                name="test-key"
            )

    def test_create_with_custom_name(self, key_manager: KeyManager) -> None:
        """TC-KEY-003: 创建带自定义名称的虚拟 Key."""
        key_record = key_manager.create(
            provider="openai",
            name="Production API Key"
        )
        
        assert key_record["name"] == "Production API Key"

    def test_create_with_expiration(self, key_manager: KeyManager) -> None:
        """TC-KEY-004: 创建带过期时间的虚拟 Key."""
        expires = "2026-12-31T23:59:59"
        key_record = key_manager.create(
            provider="openai",
            name="temp-key",
            expires_at=expires
        )
        
        assert key_record["expires_at"] == expires

    def test_create_multiple_keys_unique(self, key_manager: KeyManager) -> None:
        """TC-KEY-006: 创建多个虚拟 Key 并验证唯一性."""
        keys = []
        for i in range(3):
            key = key_manager.create(
                provider="openai",
                name=f"key-{i+1}"
            )
            keys.append(key)
        
        # Verify all keys are unique
        ids = [k["id"] for k in keys]
        virtual_keys = [k["virtual_key"] for k in keys]
        
        assert len(set(ids)) == 3
        assert len(set(virtual_keys)) == 3

    def test_list_all_keys(self, key_manager: KeyManager) -> None:
        """TC-KEY-012: 列出所有虚拟 Key."""
        # Create some keys
        key_manager.create(provider="openai", name="key-1")
        key_manager.create(provider="openai", name="key-2")
        
        keys = key_manager.list_all()
        
        assert len(keys) == 2
        for key in keys:
            assert "id" in key
            assert "name" in key
            assert "provider" in key
            assert "virtual_key" in key
            assert "created_at" in key

    def test_list_empty_keys(self, key_manager: KeyManager) -> None:
        """TC-KEY-013: 列出空的 Key 列表."""
        keys = key_manager.list_all()
        assert keys == []

    def test_get_key_info(self, key_manager: KeyManager) -> None:
        """TC-KEY-015: 获取有效虚拟 Key 的详细信息."""
        created = key_manager.create(
            provider="openai",
            name="full-key",
            expires_at="2026-12-31T23:59:59"
        )
        
        info = key_manager.get_info(created["id"])
        
        assert info is not None
        assert info["id"] == created["id"]
        assert info["virtual_key"] == created["virtual_key"]
        assert info["provider"] == "openai"
        assert info["name"] == "full-key"
        assert info["expires_at"] == "2026-12-31T23:59:59"
        assert "usage_count" in info
        assert "last_used" in info

    def test_get_nonexistent_key_info(self, key_manager: KeyManager) -> None:
        """TC-KEY-016: 获取不存在的 Key 详情."""
        info = key_manager.get_info("nonexistent-key-id")
        assert info is None

    def test_revoke_key(self, key_manager: KeyManager) -> None:
        """TC-KEY-018: 吊销有效的虚拟 Key."""
        created = key_manager.create(
            provider="openai",
            name="revoke-test"
        )
        
        result = key_manager.revoke(created["id"])
        
        assert result is True
        assert key_manager.get_info(created["id"]) is None

    def test_revoke_nonexistent_key(self, key_manager: KeyManager) -> None:
        """TC-KEY-019: 吊销不存在的虚拟 Key."""
        result = key_manager.revoke("nonexistent-key-id")
        assert result is False

    def test_is_expired_with_past_date(self, key_manager: KeyManager) -> None:
        """TC-KEY-022: 过期的 Key 自动失效."""
        expired_key = key_manager.create(
            provider="openai",
            name="expired-key",
            expires_at="2020-01-01T00:00:00"
        )
        
        assert key_manager._is_expired(expired_key) is True

    def test_is_expired_with_future_date(self, key_manager: KeyManager) -> None:
        """TC-KEY-023: 未过期的 Key 正常工作."""
        valid_key = key_manager.create(
            provider="openai",
            name="valid-key",
            expires_at="2099-12-31T23:59:59"
        )
        
        assert key_manager._is_expired(valid_key) is False

    def test_resolve_valid_key(self, key_manager: KeyManager, config_service: ConfigService) -> None:
        """TC-KEY-007: 解析有效的虚拟 Key."""
        # Create a provider key file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("sk-real-api-key")
            key_file = f.name
        
        try:
            # Create a new config with api_key_file set
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(f"""
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key_file: {key_file}
    auth_type: bearer

virtual_keys: []
""")
                config_path = f.name
            
            # Create new config service and key manager
            from lpg.core.config.service import ConfigService
            new_config = ConfigService(config_path)
            key_manager = KeyManager(new_config)
            
            created = key_manager.create(
                provider="openai",
                name="resolve-test"
            )
            
            resolved = key_manager.resolve(created["virtual_key"])
            
            assert resolved is not None
            assert resolved["provider"] == "openai"
            assert resolved["real_key"] == "sk-real-api-key"
            assert resolved["key_id"] == created["id"]
            
            os.unlink(config_path)
        finally:
            os.unlink(key_file)

    def test_resolve_invalid_key(self, key_manager: KeyManager) -> None:
        """TC-KEY-008: 解析无效的虚拟 Key."""
        resolved = key_manager.resolve("sk-virtual-invalidkey123")
        assert resolved is None

    def test_resolve_expired_key(self, key_manager: KeyManager) -> None:
        """TC-KEY-010: 解析已过期的虚拟 Key."""
        expired_key = key_manager.create(
            provider="openai",
            name="expired-key",
            expires_at="2020-01-01T00:00:00"
        )
        
        resolved = key_manager.resolve(expired_key["virtual_key"])
        assert resolved is None

    def test_usage_count_increment(self, key_manager: KeyManager, config_service: ConfigService) -> None:
        """TC-KEY-025: 验证 Key 使用次数正确统计."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("sk-real-api-key")
            key_file = f.name
        
        try:
            # Create a new config with api_key_file set
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(f"""
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key_file: {key_file}
    auth_type: bearer

virtual_keys: []
""")
                config_path = f.name
            
            from lpg.core.config.service import ConfigService
            new_config = ConfigService(config_path)
            key_manager = KeyManager(new_config)
            
            created = key_manager.create(
                provider="openai",
                name="stats-key"
            )
            
            # Initial count should be 0
            assert created["usage_count"] == 0
            
            # Resolve multiple times
            for _ in range(3):
                key_manager.resolve(created["virtual_key"])
            
            # Check updated count - need to reload from config
            key_manager2 = KeyManager(new_config)
            info = key_manager2.get_info(created["id"])
            assert info["usage_count"] == 3
            
            os.unlink(config_path)
        finally:
            os.unlink(key_file)

    def test_last_used_updated(self, key_manager: KeyManager, config_service: ConfigService) -> None:
        """TC-KEY-026: 验证 Key 最后使用时间正确记录."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("sk-real-api-key")
            key_file = f.name
        
        try:
            # Create a new config with api_key_file set
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(f"""
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key_file: {key_file}
    auth_type: bearer

virtual_keys: []
""")
                config_path = f.name
            
            from lpg.core.config.service import ConfigService
            new_config = ConfigService(config_path)
            key_manager = KeyManager(new_config)
            
            created = key_manager.create(
                provider="openai",
                name="time-key"
            )
            
            # Initial last_used should be None
            assert created["last_used"] is None
            
            # Resolve the key
            key_manager.resolve(created["virtual_key"])
            
            # Check last_used is updated - need to reload from config
            key_manager2 = KeyManager(new_config)
            info = key_manager2.get_info(created["id"])
            assert info["last_used"] is not None
            # Verify it's a valid ISO format timestamp
            datetime.fromisoformat(info["last_used"])
            
            os.unlink(config_path)
        finally:
            os.unlink(key_file)

    def test_key_prefix_constant(self, key_manager: KeyManager) -> None:
        """Verify KEY_PREFIX constant."""
        assert key_manager.KEY_PREFIX == "sk-virtual-"

    def test_count_keys(self, key_manager: KeyManager) -> None:
        """Test counting valid keys."""
        # Create keys
        key_manager.create(provider="openai", name="key-1")
        key_manager.create(
            provider="openai",
            name="key-2",
            expires_at="2099-12-31T23:59:59"
        )
        key_manager.create(
            provider="openai",
            name="key-3",
            expires_at="2020-01-01T00:00:00"  # expired
        )
        
        assert key_manager.count() == 2  # Only non-expired keys
