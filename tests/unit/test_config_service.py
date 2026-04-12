"""Unit tests for ConfigService."""

import os
import pytest
import tempfile
from pathlib import Path
from lpg.core.config.service import ConfigService
from lpg.models.config import GatewayConfig, ProviderConfig


class TestConfigService:
    """Test cases for ConfigService."""

    def test_init_with_default_path(self) -> None:
        """Test initialization with default config path."""
        service = ConfigService()
        assert service._config_path.endswith("config.yaml")
        assert ".llm-privacy-gateway" in service._config_path

    def test_init_with_custom_path(self) -> None:
        """Test initialization with custom config path."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            custom_path = f.name
        
        try:
            service = ConfigService(custom_path)
            assert service._config_path == custom_path
        finally:
            os.unlink(custom_path)

    def test_get_full_config(self, temp_config_file: str) -> None:
        """Test getting full config object."""
        service = ConfigService(temp_config_file)
        config = service.get()
        
        assert isinstance(config, GatewayConfig)
        assert config.proxy.host == "127.0.0.1"
        assert config.proxy.port == 8080

    def test_get_nested_value(self, temp_config_file: str) -> None:
        """Test getting nested config value."""
        service = ConfigService(temp_config_file)
        
        host = service.get("proxy.host")
        port = service.get("proxy.port")
        
        assert host == "127.0.0.1"
        assert port == 8080

    def test_get_default_value(self, temp_config_file: str) -> None:
        """Test getting default value for non-existent key."""
        service = ConfigService(temp_config_file)
        
        value = service.get("nonexistent.key", default="default_value")
        assert value == "default_value"

    def test_set_value(self, temp_config_file: str) -> None:
        """Test setting config value."""
        service = ConfigService(temp_config_file)
        
        service.set("proxy.port", 9090)
        
        assert service.get("proxy.port") == 9090

    def test_set_nested_value(self, temp_config_file: str) -> None:
        """Test setting nested config value."""
        service = ConfigService(temp_config_file)
        
        # Test setting nested value on existing config object
        service.set("proxy.host", "192.168.1.1")
        service.set("proxy.port", 9090)
        
        assert service.get("proxy.host") == "192.168.1.1"
        assert service.get("proxy.port") == 9090

    def test_get_provider(self, temp_config_file: str) -> None:
        """Test getting provider config."""
        service = ConfigService(temp_config_file)
        
        provider = service.get_provider("openai")
        
        assert provider is not None
        assert provider["name"] == "openai"
        assert provider["type"] == "openai"
        assert provider["base_url"] == "https://api.openai.com"

    def test_get_nonexistent_provider(self, temp_config_file: str) -> None:
        """Test getting non-existent provider."""
        service = ConfigService(temp_config_file)
        
        provider = service.get_provider("nonexistent")
        assert provider is None

    def test_get_providers(self, temp_config_file: str) -> None:
        """Test getting all providers."""
        service = ConfigService(temp_config_file)
        
        providers = service.get_providers()
        
        assert len(providers) == 2
        names = [p["name"] for p in providers]
        assert "openai" in names
        assert "anthropic" in names

    def test_add_provider(self, temp_config_file: str) -> None:
        """Test adding a new provider."""
        service = ConfigService(temp_config_file)
        
        new_provider = service.add_provider(
            provider_type="custom",
            name="custom-provider",
            base_url="https://api.custom.com",
            auth_type="bearer"
        )
        
        assert new_provider["name"] == "custom-provider"
        assert new_provider["type"] == "custom"
        assert new_provider["base_url"] == "https://api.custom.com"
        
        # Verify it was added
        providers = service.get_providers()
        assert len(providers) == 3

    def test_get_provider_key_from_file(self, temp_config_file: str) -> None:
        """Test getting provider API key from file."""
        # Create a temporary key file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("sk-test-key-12345")
            key_file = f.name
        
        try:
            # Create a new config file with api_key_file set
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
            
            service = ConfigService(config_path)
            key = service.get_provider_key("openai")
            assert key == "sk-test-key-12345"
            
            os.unlink(config_path)
        finally:
            os.unlink(key_file)

    def test_get_provider_key_no_file(self, temp_config_file: str) -> None:
        """Test getting provider key when no file is configured."""
        service = ConfigService(temp_config_file)
        
        key = service.get_provider_key("openai")
        assert key is None

    def test_save_and_reload(self, temp_config_file: str) -> None:
        """Test saving and reloading config."""
        service = ConfigService(temp_config_file)
        
        # Modify config
        service.set("proxy.port", 9999)
        
        # Create new service instance with same file
        service2 = ConfigService(temp_config_file)
        
        # Verify changes persisted
        assert service2.get("proxy.port") == 9999

    def test_init_creates_config(self) -> None:
        """Test that init creates config file if not exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.yaml")
            service = ConfigService(config_path)
            service.init()
            
            assert os.path.exists(config_path)
