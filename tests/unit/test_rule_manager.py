"""Unit tests for RuleManager."""

import pytest
import tempfile
import os
from pathlib import Path
from lpg.core.rule.manager import RuleManager
from lpg.core.config.service import ConfigService


class TestRuleManager:
    """Test cases for RuleManager."""

    def test_load_builtin_rules(self, temp_config_file: str) -> None:
        """Test loading builtin rules."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        # Should load rules from rules/ directory
        assert manager.count() > 0

    def test_list_all_rules(self, temp_config_file: str) -> None:
        """TC-RULE-001: 列出所有规则."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        rules = manager.list_all()
        
        assert len(rules) > 0
        for rule in rules:
            assert "id" in rule
            assert "name" in rule
            assert "category" in rule
            assert "type" in rule
            assert "enabled" in rule

    def test_list_rules_by_category(self, temp_config_file: str) -> None:
        """Test listing rules filtered by category."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        pii_rules = manager.list_all(category="pii")
        
        for rule in pii_rules:
            assert rule["category"] == "pii"

    def test_enable_rule(self, temp_config_file: str) -> None:
        """TC-RULE-002: 启用规则."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        # Get a rule and disable it first
        rules = manager.list_all()
        if rules:
            rule_id = rules[0]["id"]
            manager.disable(rule_id)
            
            # Now enable it
            result = manager.enable(rule_id)
            assert result is True
            
            # Verify it's enabled
            enabled_rules = manager.get_enabled_rules()
            enabled_ids = [r["id"] for r in enabled_rules]
            assert rule_id in enabled_ids

    def test_disable_rule(self, temp_config_file: str) -> None:
        """TC-RULE-003: 禁用规则."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        rules = manager.list_all()
        if rules:
            rule_id = rules[0]["id"]
            result = manager.disable(rule_id)
            assert result is True
            
            # Verify it's disabled
            enabled_rules = manager.get_enabled_rules()
            enabled_ids = [r["id"] for r in enabled_rules]
            assert rule_id not in enabled_ids

    def test_enable_nonexistent_rule(self, temp_config_file: str) -> None:
        """Test enabling a non-existent rule."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        result = manager.enable("nonexistent-rule")
        assert result is False

    def test_disable_nonexistent_rule(self, temp_config_file: str) -> None:
        """Test disabling a non-existent rule."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        result = manager.disable("nonexistent-rule")
        assert result is False

    def test_test_regex_rule(self, temp_config_file: str) -> None:
        """Test testing a regex rule."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        rule_config = {
            "type": "regex",
            "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        }
        
        result = manager.test_rule(rule_config, "Contact me at test@example.com")
        
        assert "matches" in result
        assert result["count"] == 1
        assert result["matches"][0]["text"] == "test@example.com"

    def test_test_keyword_rule(self, temp_config_file: str) -> None:
        """Test testing a keyword rule."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        rule_config = {
            "type": "keyword",
            "keywords": ["password", "secret"]
        }
        
        result = manager.test_rule(rule_config, "My password is secret123")
        
        assert "matches" in result
        assert result["count"] == 2

    def test_test_invalid_regex(self, temp_config_file: str) -> None:
        """Test testing an invalid regex pattern."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        rule_config = {
            "type": "regex",
            "pattern": "[invalid("
        }
        
        result = manager.test_rule(rule_config, "test text")
        
        assert "error" in result
        assert "Invalid regex" in result["error"]

    def test_import_from_file(self, temp_config_file: str) -> None:
        """TC-RULE-004: 从文件导入规则."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        # Create a temporary rule file
        rule_content = """
rules:
  - id: custom-test-rule
    name: Custom Test Rule
    category: test
    type: regex
    pattern: "test[0-9]+"
    entity_type: TEST_ENTITY
    enabled: true
    description: A test rule
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(rule_content)
            rule_file = f.name
        
        try:
            count_before = manager.count()
            imported = manager.import_from_file(rule_file)
            
            assert imported == 1
            assert manager.count() == count_before + 1
            
            # Verify the rule was added
            rules = manager.list_all()
            rule_ids = [r["id"] for r in rules]
            assert "custom-test-rule" in rule_ids
        finally:
            os.unlink(rule_file)

    def test_import_nonexistent_file(self, temp_config_file: str) -> None:
        """Test importing from a non-existent file."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        with pytest.raises(FileNotFoundError):
            manager.import_from_file("/nonexistent/path/rules.yaml")

    def test_get_enabled_rules(self, temp_config_file: str) -> None:
        """Test getting only enabled rules."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        all_rules = manager.list_all()
        enabled_rules = manager.get_enabled_rules()
        
        # Initially all rules should be enabled
        assert len(enabled_rules) == len(all_rules)
        
        # Disable one rule
        if all_rules:
            manager.disable(all_rules[0]["id"])
            
            enabled_rules = manager.get_enabled_rules()
            assert len(enabled_rules) == len(all_rules) - 1

    def test_count_rules(self, temp_config_file: str) -> None:
        """Test counting rules."""
        config = ConfigService(temp_config_file)
        manager = RuleManager(config)
        
        count = manager.count()
        rules = manager.list_all()
        
        assert count == len(rules)
