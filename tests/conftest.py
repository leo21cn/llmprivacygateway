"""Pytest fixtures for LLM Privacy Gateway tests."""

import os
import tempfile
import pytest
from pathlib import Path
from typing import Generator

from lpg.core.config.service import ConfigService
from lpg.core.key.manager import KeyManager


@pytest.fixture
def temp_config_file() -> Generator[str, None, None]:
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("""
proxy:
  host: 127.0.0.1
  port: 8080

providers:
  - name: openai
    type: openai
    base_url: https://api.openai.com
    api_key_file: null
    auth_type: bearer
    timeout: 60
  - name: anthropic
    type: anthropic
    base_url: https://api.anthropic.com
    api_key_file: null
    auth_type: x-api-key
    timeout: 60

virtual_keys: []

presidio:
  endpoint: http://localhost:5001
  language: zh

audit:
  log_dir: ./logs
  retention_days: 30
""")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def config_service(temp_config_file: str) -> ConfigService:
    """Create a ConfigService with temporary config."""
    return ConfigService(temp_config_file)


@pytest.fixture
def key_manager(config_service: ConfigService) -> KeyManager:
    """Create a KeyManager with temporary config."""
    return KeyManager(config_service)


@pytest.fixture
def mock_provider_key_file(tmp_path: Path) -> Generator[str, None, None]:
    """Create a mock provider API key file."""
    key_file = tmp_path / "test_api_key.txt"
    key_file.write_text("sk-test-api-key-12345")
    yield str(key_file)
