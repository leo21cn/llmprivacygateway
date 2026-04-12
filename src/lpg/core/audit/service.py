"""Audit service."""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class AuditService:
    """审计服务.

    职责:
    1. 记录请求处理日志
    2. 日志查询和统计
    3. 日志导出
    """

    def __init__(self, config_service):
        """初始化审计服务.

        Args:
            config_service: 配置服务
        """
        self._config = config_service
        self._log_file = self._get_log_file()
        self._ensure_log_dir()

    def _get_log_file(self) -> Path:
        """获取日志文件路径."""
        log_path = self._config.get("audit.log_file")
        if log_path:
            return Path(log_path).expanduser()

        home = Path.home()
        return home / ".llm-privacy-gateway" / "logs" / "audit.jsonl"

    def _ensure_log_dir(self):
        """确保日志目录存在."""
        self._log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_request(
        self,
        url: str,
        method: str,
        status: int,
        duration_ms: float,
        detections: List[Dict],
        is_stream: bool = False,
        error: Optional[str] = None,
    ):
        """记录请求日志."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "method": method,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "detections": [
                {"entity_type": d.get("entity_type"), "score": d.get("score")}
                for d in detections
            ],
            "pii_count": len(detections),
            "is_stream": is_stream,
            "error": error,
        }

        try:
            with open(self._log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

    def get_logs(
        self, lines: int = 50, level: Optional[str] = None, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取日志."""
        if not self._log_file.exists():
            return []

        logs = []
        try:
            with open(self._log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)

                        if since and not self._match_time_filter(entry["timestamp"], since):
                            continue

                        if level:
                            if level == "error" and entry.get("status", 200) < 400:
                                continue
                            if level == "warn" and entry.get("status", 200) < 300:
                                continue

                        logs.append(entry)
        except Exception as e:
            logger.error(f"Failed to read audit log: {e}")

        return logs[-lines:]

    def get_stats(self, since: Optional[str] = None) -> Dict[str, Any]:
        """获取统计信息."""
        logs = self.get_logs(lines=10000, since=since)

        if not logs:
            return {
                "total_requests": 0,
                "success_requests": 0,
                "failed_requests": 0,
                "pii_detected": 0,
                "avg_duration_ms": 0,
            }

        total = len(logs)
        success = len([l for l in logs if l.get("status", 200) < 400])
        failed = total - success
        pii_count = sum(l.get("pii_count", 0) for l in logs)
        total_duration = sum(l.get("duration_ms", 0) for l in logs)

        pii_types = {}
        for log in logs:
            for detection in log.get("detections", []):
                entity_type = detection.get("entity_type", "unknown")
                pii_types[entity_type] = pii_types.get(entity_type, 0) + 1

        return {
            "total_requests": total,
            "success_requests": success,
            "failed_requests": failed,
            "pii_detected": pii_count,
            "avg_duration_ms": round(total_duration / total, 2) if total > 0 else 0,
            "pii_type_distribution": pii_types,
        }

    def export(self, output_path: str, since: Optional[str] = None) -> int:
        """导出日志."""
        logs = self.get_logs(lines=100000, since=since)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        return len(logs)

    def _match_time_filter(self, timestamp: str, since: str) -> bool:
        """检查时间是否在范围内."""
        try:
            log_time = datetime.fromisoformat(timestamp)
            now = datetime.now()

            if since == "1h":
                return now - log_time <= timedelta(hours=1)
            elif since == "1d":
                return now - log_time <= timedelta(days=1)
            elif since == "1w":
                return now - log_time <= timedelta(weeks=1)
            elif since == "1m":
                return now - log_time <= timedelta(days=30)
        except Exception:
            pass

        return True
