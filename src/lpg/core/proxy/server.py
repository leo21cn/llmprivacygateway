"""HTTP proxy server."""

import asyncio
import os
from pathlib import Path
from typing import Optional, Dict, Any
from aiohttp import web
import logging

from lpg.core.config.service import ConfigService
from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.presidio.client import PresidioClient
from lpg.core.audit.service import AuditService
from lpg.core.proxy.handler import RequestHandler

logger = logging.getLogger(__name__)

# PID 文件路径
PID_FILE_PATH = Path.home() / ".lpg" / "proxy.pid"


class ProxyServer:
    """HTTP 代理服务器.

    职责:
    1. 监听本地端口，接收 API 请求
    2. 委托 RequestHandler 处理请求
    3. 管理服务器生命周期
    """

    def __init__(
        self,
        config_service: ConfigService,
        key_manager: KeyManager,
        rule_manager: RuleManager,
        presidio_client: PresidioClient,
        audit_service: AuditService,
    ):
        """初始化代理服务器."""
        self._config = config_service
        self._handler = RequestHandler(
            key_manager=key_manager,
            rule_manager=rule_manager,
            presidio_client=presidio_client,
            audit_service=audit_service,
            config_service=config_service,
        )
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self._pid: Optional[int] = None
        self._start_time: Optional[float] = None
        self._stats = {
            "total_requests": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "pii_detected": 0,
            "total_latency_ms": 0,
        }

    @property
    def pid(self) -> Optional[int]:
        """获取进程 ID."""
        # 优先从 PID 文件读取（支持跨进程检测）
        pid_from_file = self._read_pid_file()
        if pid_from_file:
            return pid_from_file
        return self._pid

    @property
    def uptime(self) -> float:
        """获取运行时间."""
        if self._start_time:
            import time

            return time.time() - self._start_time
        return 0

    @property
    def stats(self) -> Dict[str, Any]:
        """获取统计信息."""
        return self._stats.copy()

    def is_running(self) -> bool:
        """检查服务器是否运行."""
        # 首先检查当前进程的 runner
        if self._runner is not None:
            return True
        # 跨进程检测：检查 PID 文件和进程是否存在
        return self._check_process_running()

    async def start_async(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        log_level: str = "info",
        log_file: Optional[str] = None,
    ):
        """异步启动服务器."""
        import os
        import time

        self._app = web.Application()
        self._setup_routes()

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()

        self._site = web.TCPSite(self._runner, host, port)
        await self._site.start()

        self._pid = os.getpid()
        self._start_time = time.time()

        # 写入 PID 文件
        self._write_pid_file(self._pid, host, port)

        logger.info(f"Proxy server started at http://{host}:{port}")

    def start(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        daemon: bool = False,
        log_level: str = "info",
        log_file: Optional[str] = None,
    ):
        """启动服务器（同步接口）."""
        if daemon:
            self._start_daemon(host, port, log_level, log_file)
        else:
            asyncio.run(self._run_forever(host, port, log_level, log_file))

    async def _run_forever(
        self, host: str, port: int, log_level: str, log_file: Optional[str]
    ):
        """持续运行."""
        await self.start_async(host, port, log_level, log_file)
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            await self.stop_async()

    def _start_daemon(
        self, host: str, port: int, log_level: str, log_file: Optional[str]
    ):
        """后台守护进程模式."""
        import subprocess
        import sys
        import time

        cmd = [
            sys.executable,
            "-m",
            "lpg",
            "start",
            "-h",
            host,
            "-p",
            str(port),
        ]
        process = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        self._pid = process.pid
        # 等待子进程启动并写入 PID 文件
        time.sleep(0.5)
        # 从 PID 文件读取实际的服务进程 PID
        actual_pid = self._read_pid_file()
        if actual_pid:
            self._pid = actual_pid

    def _write_pid_file(self, pid: int, host: str, port: int):
        """写入 PID 文件."""
        try:
            PID_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(PID_FILE_PATH, "w") as f:
                f.write(f"{pid}\n{host}\n{port}\n")
        except Exception as e:
            logger.warning(f"Failed to write PID file: {e}")

    def _read_pid_file(self) -> Optional[int]:
        """从 PID 文件读取 PID."""
        try:
            if PID_FILE_PATH.exists():
                with open(PID_FILE_PATH, "r") as f:
                    lines = f.read().strip().split("\n")
                    if lines:
                        return int(lines[0])
        except Exception:
            pass
        return None

    def _read_pid_file_info(self) -> Dict[str, Any]:
        """从 PID 文件读取完整信息."""
        try:
            if PID_FILE_PATH.exists():
                with open(PID_FILE_PATH, "r") as f:
                    lines = f.read().strip().split("\n")
                    if len(lines) >= 3:
                        return {
                            "pid": int(lines[0]),
                            "host": lines[1],
                            "port": int(lines[2]),
                        }
        except Exception:
            pass
        return {}

    @staticmethod
    def _check_process_running(_self=None) -> bool:
        """检查 PID 文件中的进程是否仍在运行."""
        pid = ProxyServer._read_pid_file_static()
        if not pid:
            return False
        try:
            # 发送信号 0 检查进程是否存在
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            # 进程不存在，清理 PID 文件
            ProxyServer._remove_pid_file_static()
            return False

    @staticmethod
    def _read_pid_file_static() -> Optional[int]:
        """静态方法：从 PID 文件读取 PID."""
        try:
            if PID_FILE_PATH.exists():
                with open(PID_FILE_PATH, "r") as f:
                    lines = f.read().strip().split("\n")
                    if lines:
                        return int(lines[0])
        except Exception:
            pass
        return None

    @staticmethod
    def _remove_pid_file_static():
        """静态方法：删除 PID 文件."""
        try:
            if PID_FILE_PATH.exists():
                PID_FILE_PATH.unlink()
        except Exception:
            pass

    @staticmethod
    def _stop_by_pid_file():
        """通过 PID 文件停止进程."""
        try:
            if PID_FILE_PATH.exists():
                with open(PID_FILE_PATH, "r") as f:
                    lines = f.read().strip().split("\n")
                    if lines:
                        pid = int(lines[0])
                        import signal
                        try:
                            os.kill(pid, signal.SIGTERM)
                        except (OSError, ProcessLookupError):
                            pass
                # 删除 PID 文件
                ProxyServer._remove_pid_file_static()
        except Exception:
            pass

    def _remove_pid_file(self):
        """删除 PID 文件."""
        try:
            if PID_FILE_PATH.exists():
                PID_FILE_PATH.unlink()
        except Exception:
            pass

    async def stop_async(self, force: bool = False):
        """异步停止服务器."""
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
            self._site = None
            logger.info("Proxy server stopped")
        # 清理 PID 文件
        self._remove_pid_file()

    def stop(self, force: bool = False):
        """停止服务器（同步接口）."""
        # 尝试从 PID 文件获取进程信息
        pid_info = self._read_pid_file_info()
        if pid_info and pid_info.get("pid"):
            import signal
            try:
                os.kill(pid_info["pid"], signal.SIGTERM)
            except (OSError, ProcessLookupError):
                pass
        self._remove_pid_file()
        # 如果当前进程有 runner，也停止它
        if self._runner:
            asyncio.run(self.stop_async(force))

    def _setup_routes(self):
        """设置路由."""
        self._app.router.add_post("/v1/chat/completions", self._handle_request)
        self._app.router.add_post("/v1/completions", self._handle_request)
        self._app.router.add_post("/v1/embeddings", self._handle_request)
        self._app.router.add_post("/{path:.*}", self._handle_request)
        self._app.router.add_get("/{path:.*}", self._handle_request)
        self._app.router.add_get("/health", self._handle_health)

    async def _handle_request(self, request: web.Request) -> web.Response:
        """处理 API 请求."""
        import time

        start_time = time.time()
        self._stats["total_requests"] += 1

        try:
            response = await self._handler.handle(request)
            self._stats["success_requests"] += 1
            return response
        except Exception as e:
            self._stats["failed_requests"] += 1
            logger.error(f"Request failed: {e}")
            return web.json_response(
                {"error": {"message": str(e), "type": "internal_error"}},
                status=500,
            )
        finally:
            elapsed = (time.time() - start_time) * 1000
            self._stats["total_latency_ms"] += elapsed

    async def _handle_health(self, request: web.Request) -> web.Response:
        """健康检查端点."""
        return web.json_response(
            {
                "status": "ok",
                "version": "1.0.0",
                "uptime": self.uptime,
            }
        )
