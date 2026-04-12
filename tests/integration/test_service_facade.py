"""Integration tests for ServiceFacade."""

import pytest
import tempfile
import os
from lpg.core.service_facade import ServiceFacade


class TestServiceFacade:
    """Integration test cases for ServiceFacade."""

    def test_facade_initialization(self, temp_config_file: str) -> None:
        """Test ServiceFacade initialization."""
        facade = ServiceFacade(temp_config_file)
        
        # Verify all services are initialized
        assert facade._config_service is not None
        assert facade._key_manager is not None
        assert facade._rule_manager is not None
        assert facade._audit_service is not None
        assert facade._presidio_client is not None

    def test_create_and_list_keys(self, temp_config_file: str) -> None:
        """Test creating and listing keys through facade."""
        facade = ServiceFacade(temp_config_file)
        
        # Create a key
        key = facade.create_virtual_key(
            provider="openai",
            name="integration-test-key"
        )
        
        assert key["provider"] == "openai"
        assert key["name"] == "integration-test-key"
        
        # List keys
        keys = facade.list_virtual_keys()
        assert len(keys) >= 1
        
        key_ids = [k["id"] for k in keys]
        assert key["id"] in key_ids

    def test_revoke_key(self, temp_config_file: str) -> None:
        """Test revoking a key through facade."""
        facade = ServiceFacade(temp_config_file)
        
        # Create a key
        key = facade.create_virtual_key(
            provider="openai",
            name="revoke-test-key"
        )
        
        # Revoke it
        result = facade.revoke_virtual_key(key["id"])
        assert result is True
        
        # Verify it's gone
        info = facade.get_key_info(key["id"])
        assert info is None

    def test_list_rules(self, temp_config_file: str) -> None:
        """Test listing rules through facade."""
        facade = ServiceFacade(temp_config_file)
        
        rules = facade.list_rules()
        
        assert len(rules) > 0
        for rule in rules:
            assert "id" in rule
            assert "name" in rule
            assert "enabled" in rule

    def test_enable_disable_rule(self, temp_config_file: str) -> None:
        """Test enabling and disabling rules."""
        facade = ServiceFacade(temp_config_file)
        
        # Get a rule
        rules = facade.list_rules()
        if rules:
            rule_id = rules[0]["id"]
            
            # Disable it
            result = facade.disable_rule(rule_id)
            assert result is True
            
            # Enable it
            result = facade.enable_rule(rule_id)
            assert result is True

    def test_list_providers(self, temp_config_file: str) -> None:
        """Test listing providers through facade."""
        facade = ServiceFacade(temp_config_file)
        
        providers = facade.list_providers()
        
        assert len(providers) == 2
        names = [p["name"] for p in providers]
        assert "openai" in names
        assert "anthropic" in names

    def test_add_provider(self, temp_config_file: str) -> None:
        """Test adding a provider through facade."""
        facade = ServiceFacade(temp_config_file)
        
        new_provider = facade.add_provider(
            provider_type="custom",
            name="test-provider",
            base_url="https://api.test.com",
            auth_type="bearer"
        )
        
        assert new_provider["name"] == "test-provider"
        
        # Verify it was added
        providers = facade.list_providers()
        assert len(providers) == 3

    def test_get_set_config(self, temp_config_file: str) -> None:
        """Test getting and setting config through facade."""
        facade = ServiceFacade(temp_config_file)
        
        # Get config
        port = facade.get_config("proxy.port")
        assert port == 8080
        
        # Set config
        facade.set_config("proxy.port", 9090)
        
        # Verify change
        new_port = facade.get_config("proxy.port")
        assert new_port == 9090

    def test_get_status(self, temp_config_file: str) -> None:
        """Test getting service status."""
        facade = ServiceFacade(temp_config_file)
        
        status = facade.get_status()
        
        assert "running" in status
        assert "host" in status
        assert "port" in status
        assert "rules_count" in status
        assert "keys_count" in status

    def test_logs_and_stats(self, temp_config_file: str) -> None:
        """Test logs and stats functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            facade = ServiceFacade(temp_config_file)
            facade.set_config("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            # Get stats (should be empty initially)
            stats = facade.get_log_stats()
            assert stats["total_requests"] == 0
            
            # Get logs (should be empty)
            logs = facade.get_logs()
            assert logs == []

    def test_test_rule(self, temp_config_file: str) -> None:
        """Test rule testing functionality."""
        facade = ServiceFacade(temp_config_file)
        
        rule_config = {
            "type": "regex",
            "pattern": r"\d{3}-\d{4}-\d{4}"
        }
        
        result = facade.test_rule(rule_config, "Call me at 138-1234-5678")
        
        assert result["count"] == 1
        assert result["matches"][0]["text"] == "138-1234-5678"

    def test_key_expiration(self, temp_config_file: str) -> None:
        """Test creating key with expiration."""
        facade = ServiceFacade(temp_config_file)
        
        key = facade.create_virtual_key(
            provider="openai",
            name="expiring-key",
            expires_at="2099-12-31T23:59:59"
        )
        
        assert key["expires_at"] == "2099-12-31T23:59:59"
        
        info = facade.get_key_info(key["id"])
        assert info["expires_at"] == "2099-12-31T23:59:59"
