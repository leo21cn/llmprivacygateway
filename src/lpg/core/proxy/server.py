"""HTTP proxy server."""

import asyncio
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
        return self._runner is not None

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
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    async def stop_async(self, force: bool = False):
        """异步停止服务器."""
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
            self._site = None
            logger.info("Proxy server stopped")

    def stop(self, force: bool = False):
        """停止服务器（同步接口）."""
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
