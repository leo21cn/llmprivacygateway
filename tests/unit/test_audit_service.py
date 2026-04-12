"""Unit tests for AuditService."""

import pytest
import json
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
from lpg.core.audit.service import AuditService
from lpg.core.config.service import ConfigService


class TestAuditService:
    """Test cases for AuditService."""

    def test_log_request(self, temp_config_file: str) -> None:
        """TC-AUDIT-001: 记录请求日志."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            # Set log file to temp directory
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            service.log_request(
                url="https://api.openai.com/v1/chat/completions",
                method="POST",
                status=200,
                duration_ms=150.5,
                detections=[
                    {"entity_type": "EMAIL", "score": 0.95},
                    {"entity_type": "PHONE", "score": 0.88}
                ],
                is_stream=False
            )
            
            # Verify log file was created
            assert service._log_file.exists()
            
            # Read and verify log content
            with open(service._log_file, "r") as f:
                log_entry = json.loads(f.readline())
            
            assert log_entry["url"] == "https://api.openai.com/v1/chat/completions"
            assert log_entry["method"] == "POST"
            assert log_entry["status"] == 200
            assert log_entry["duration_ms"] == 150.5
            assert log_entry["pii_count"] == 2
            assert log_entry["is_stream"] is False
            assert "timestamp" in log_entry

    def test_log_request_with_error(self, temp_config_file: str) -> None:
        """Test logging a request with error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            service.log_request(
                url="https://api.openai.com/v1/chat/completions",
                method="POST",
                status=500,
                duration_ms=50.0,
                detections=[],
                error="Connection timeout"
            )
            
            with open(service._log_file, "r") as f:
                log_entry = json.loads(f.readline())
            
            assert log_entry["status"] == 500
            assert log_entry["error"] == "Connection timeout"

    def test_get_logs(self, temp_config_file: str) -> None:
        """TC-AUDIT-002: 获取日志."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            # Log multiple requests
            for i in range(5):
                service.log_request(
                    url=f"https://api.example.com/endpoint{i}",
                    method="POST",
                    status=200,
                    duration_ms=100.0,
                    detections=[]
                )
            
            logs = service.get_logs(lines=3)
            
            assert len(logs) == 3
            # Should return the last 3 logs
            assert logs[0]["url"] == "https://api.example.com/endpoint2"
            assert logs[2]["url"] == "https://api.example.com/endpoint4"

    def test_get_logs_empty(self, temp_config_file: str) -> None:
        """Test getting logs when no log file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "nonexistent", "audit.jsonl"))
            
            service = AuditService(config)
            
            logs = service.get_logs()
            
            assert logs == []

    def test_get_stats(self, temp_config_file: str) -> None:
        """TC-AUDIT-003: 获取审计统计."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            # Log requests with different statuses
            service.log_request(
                url="https://api.example.com/1",
                method="POST",
                status=200,
                duration_ms=100.0,
                detections=[{"entity_type": "EMAIL", "score": 0.9}]
            )
            service.log_request(
                url="https://api.example.com/2",
                method="POST",
                status=200,
                duration_ms=200.0,
                detections=[]
            )
            service.log_request(
                url="https://api.example.com/3",
                method="POST",
                status=500,
                duration_ms=50.0,
                detections=[{"entity_type": "PHONE", "score": 0.8}]
            )
            
            stats = service.get_stats()
            
            assert stats["total_requests"] == 3
            assert stats["success_requests"] == 2
            assert stats["failed_requests"] == 1
            assert stats["pii_detected"] == 2
            assert stats["avg_duration_ms"] == 116.67
            assert "EMAIL" in stats["pii_type_distribution"]
            assert "PHONE" in stats["pii_type_distribution"]

    def test_get_stats_empty(self, temp_config_file: str) -> None:
        """Test getting stats when no logs exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            stats = service.get_stats()
            
            assert stats["total_requests"] == 0
            assert stats["success_requests"] == 0
            assert stats["failed_requests"] == 0
            assert stats["pii_detected"] == 0
            assert stats["avg_duration_ms"] == 0

    def test_export_logs(self, temp_config_file: str) -> None:
        """TC-AUDIT-004: 导出日志."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            # Log some requests
            for i in range(3):
                service.log_request(
                    url=f"https://api.example.com/{i}",
                    method="POST",
                    status=200,
                    duration_ms=100.0,
                    detections=[]
                )
            
            output_path = os.path.join(tmpdir, "exported.json")
            count = service.export(output_path)
            
            assert count == 3
            assert os.path.exists(output_path)
            
            with open(output_path, "r") as f:
                exported = json.load(f)
            
            assert len(exported) == 3

    def test_time_filter_1h(self, temp_config_file: str) -> None:
        """Test time filter for 1 hour."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            # Create a log entry with current time
            service.log_request(
                url="https://api.example.com/recent",
                method="POST",
                status=200,
                duration_ms=100.0,
                detections=[]
            )
            
            logs = service.get_logs(since="1h")
            
            # Should include the recent log
            assert len(logs) >= 1

    def test_time_filter_invalid(self, temp_config_file: str) -> None:
        """Test time filter with invalid timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigService(temp_config_file)
            config.set("audit.log_file", os.path.join(tmpdir, "audit.jsonl"))
            
            service = AuditService(config)
            
            # Manually write an entry with invalid timestamp
            with open(service._log_file, "w") as f:
                f.write(json.dumps({"timestamp": "invalid", "url": "test"}) + "\n")
            
            # Should not crash
            logs = service.get_logs(since="1h")
            assert len(logs) == 1  # Invalid timestamp passes through
