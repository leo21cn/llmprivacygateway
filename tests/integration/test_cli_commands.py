"""Integration tests for CLI commands."""

import pytest
import subprocess
import sys
import tempfile
import os
from click.testing import CliRunner
from lpg.cli.main import cli


class TestCLICommands:
    """Integration test cases for CLI commands."""

    def test_cli_help(self) -> None:
        """TC-CLI-001: 显示帮助信息."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        
        assert result.exit_code == 0
        assert "LLM Privacy Gateway" in result.output
        assert "start" in result.output
        assert "stop" in result.output
        assert "status" in result.output
        assert "config" in result.output
        assert "key" in result.output
        assert "rule" in result.output

    def test_cli_version(self) -> None:
        """TC-CLI-002: 显示版本信息."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        
        assert result.exit_code == 0
        assert "1.0.0" in result.output

    def test_config_init(self) -> None:
        """TC-CLI-003: 初始化配置."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "config.yaml")
            runner = CliRunner()
            
            result = runner.invoke(cli, ["--config", config_path, "config", "init"])
            
            assert result.exit_code == 0
            assert os.path.exists(config_path)

    def test_config_show(self, temp_config_file: str) -> None:
        """TC-CLI-004: 显示配置."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "config", "show"])
        
        assert result.exit_code == 0
        assert "proxy" in result.output or "Proxy" in result.output

    def test_key_create(self, temp_config_file: str) -> None:
        """TC-CLI-005: 创建虚拟 Key."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--config", temp_config_file, "key", "create", "--provider", "openai", "--name", "cli-test-key"]
        )
        
        assert result.exit_code == 0
        assert "sk-virtual-" in result.output

    def test_key_create_invalid_provider(self, temp_config_file: str) -> None:
        """TC-CLI-006: 使用无效 provider 创建 Key 失败."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["--config", temp_config_file, "key", "create", "--provider", "invalid", "--name", "test"]
        )
        
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "Error" in result.output

    def test_key_list(self, temp_config_file: str) -> None:
        """TC-CLI-007: 列出 Key."""
        runner = CliRunner()
        
        # First create a key
        runner.invoke(
            cli,
            ["--config", temp_config_file, "key", "create", "--provider", "openai", "--name", "list-test-key"]
        )
        
        # Then list keys
        result = runner.invoke(cli, ["--config", temp_config_file, "key", "list"])
        
        assert result.exit_code == 0
        assert "list-test-key" in result.output

    def test_key_revoke(self, temp_config_file: str) -> None:
        """TC-CLI-008: 吊销 Key."""
        runner = CliRunner()
        
        # Create a key
        create_result = runner.invoke(
            cli,
            ["--config", temp_config_file, "key", "create", "--provider", "openai", "--name", "revoke-test-key"]
        )
        
        # Extract key ID from output (simplified)
        # In real test, we'd parse the JSON output
        
        # For now, just test that revoke command exists
        result = runner.invoke(cli, ["--config", temp_config_file, "key", "revoke", "--help"])
        assert result.exit_code == 0

    def test_rule_list(self, temp_config_file: str) -> None:
        """TC-CLI-009: 列出规则."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "rule", "list"])
        
        assert result.exit_code == 0
        # Should show some rules from builtin rules

    def test_provider_list(self, temp_config_file: str) -> None:
        """TC-CLI-010: 列出提供商."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "provider", "list"])
        
        assert result.exit_code == 0
        assert "openai" in result.output.lower()

    def test_status_command(self, temp_config_file: str) -> None:
        """TC-CLI-011: 状态命令."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "status"])
        
        assert result.exit_code == 0
        # Should show status information

    def test_verbose_flag(self, temp_config_file: str) -> None:
        """TC-CLI-012: 详细输出模式."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--verbose", "--config", temp_config_file, "status"])
        
        assert result.exit_code == 0

    def test_quiet_flag(self, temp_config_file: str) -> None:
        """TC-CLI-013: 静默模式."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--quiet", "--config", temp_config_file, "status"])
        
        assert result.exit_code == 0
        # Output should be minimal or empty

    def test_json_output_flag(self, temp_config_file: str) -> None:
        """TC-CLI-014: JSON 格式输出."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--json", "--config", temp_config_file, "provider", "list"])
        
        assert result.exit_code == 0
        # Output should be valid JSON

    def test_log_show_command(self, temp_config_file: str) -> None:
        """TC-CLI-015: 查看日志命令."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "log", "show", "--help"])
        
        assert result.exit_code == 0
        assert "lines" in result.output.lower()

    def test_log_stats_command(self, temp_config_file: str) -> None:
        """TC-CLI-016: 日志统计命令."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--config", temp_config_file, "log", "stats"])
        
        assert result.exit_code == 0
