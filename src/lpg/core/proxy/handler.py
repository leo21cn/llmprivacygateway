"""Request handler."""

import json
import logging
from typing import Dict, Any, List, Optional
from aiohttp import web
import time
import aiohttp

from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.presidio.client import PresidioClient
from lpg.core.audit.service import AuditService
from lpg.core.config.service import ConfigService

logger = logging.getLogger(__name__)


class RequestHandler:
    """请求处理器.

    职责:
    1. 验证虚拟 Key
    2. 提取并检测 PII
    3. 执行脱敏处理
    4. 转发请求到 LLM API
    5. 处理响应
    6. 记录审计日志
    """

    def __init__(
        self,
        key_manager: KeyManager,
        rule_manager: RuleManager,
        presidio_client: PresidioClient,
        audit_service: AuditService,
        config_service: ConfigService,
    ):
        """初始化请求处理器."""
        self._key_manager = key_manager
        self._rule_manager = rule_manager
        self._presidio = presidio_client
        self._audit = audit_service
        self._config = config_service

    async def handle(self, request: web.Request) -> web.Response:
        """处理请求主流程."""
        start_time = time.time()

        # Step 1: 验证虚拟 Key
        virtual_key = self._extract_api_key(request)
        if not virtual_key:
            return self._error_response(401, "Missing API key")

        key_mapping = self._key_manager.resolve(virtual_key)
        if not key_mapping:
            return self._error_response(401, "Invalid API key")

        # Step 2: 获取提供商配置
        provider = self._config.get_provider(key_mapping["provider"])
        if not provider:
            return self._error_response(500, "Provider not configured")

        # Step 3: 读取请求体
        body = await request.read()
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            return self._error_response(400, "Invalid JSON body")

        # Step 4: PII 检测与脱敏
        detection_results = []

        if self._should_process(request_data):
            messages = self._extract_messages(request_data)
            for msg in messages:
                content = msg.get("content", "")
                if content:
                    detections = await self._presidio.analyze(content)
                    if detections:
                        detection_results.extend(detections)
                        anonymized_content = await self._presidio.anonymize(
                            content, detections
                        )
                        msg["content"] = anonymized_content

        # Step 5: 转发请求
        target_url = self._build_target_url(provider, request.path)
        headers = self._build_headers(
            provider, key_mapping["real_key"], request.headers
        )

        is_stream = request_data.get("stream", False)

        if is_stream:
            return await self._handle_stream_response(
                target_url, headers, request_data, start_time, detection_results, request
            )
        else:
            return await self._handle_normal_response(
                target_url, headers, request_data, start_time, detection_results
            )

    def _extract_api_key(self, request: web.Request) -> Optional[str]:
        """从请求头提取 API Key."""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        return request.headers.get("x-api-key")

    def _should_process(self, request_data: Dict) -> bool:
        """判断是否需要进行 PII 处理."""
        return "messages" in request_data

    def _extract_messages(self, request_data: Dict) -> List[Dict]:
        """提取消息内容."""
        return request_data.get("messages", [])

    def _build_target_url(self, provider: Dict, path: str) -> str:
        """构建目标 URL."""
        base_url = provider.get("base_url", "").rstrip("/")
        return f"{base_url}{path}"

    def _build_headers(
        self, provider: Dict, real_key: str, original_headers: Dict
    ) -> Dict:
        """构建请求头."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "LLM-Privacy-Gateway/1.0",
        }

        auth_type = provider.get("auth_type", "bearer")
        if auth_type == "bearer":
            headers["Authorization"] = f"Bearer {real_key}"
        elif auth_type == "x-api-key":
            headers["x-api-key"] = real_key
        elif auth_type == "api-key":
            headers["api-key"] = real_key

        return headers

    async def _handle_normal_response(
        self,
        url: str,
        headers: Dict,
        data: Dict,
        start_time: float,
        detections: List,
    ) -> web.Response:
        """处理普通响应."""
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                response_data = await resp.json()

                self._audit.log_request(
                    url=url,
                    method="POST",
                    status=resp.status,
                    duration_ms=(time.time() - start_time) * 1000,
                    detections=detections,
                )

                return web.json_response(response_data, status=resp.status)

    async def _handle_stream_response(
        self,
        url: str,
        headers: Dict,
        data: Dict,
        start_time: float,
        detections: List,
        request: web.Request,
    ) -> web.StreamResponse:
        """处理流式响应（SSE）."""
        response = web.StreamResponse()
        response.headers["Content-Type"] = "text/event-stream"
        response.headers["Cache-Control"] = "no-cache"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                # 设置响应状态码
                response.set_status(resp.status)
                await response.prepare(request)
                async for chunk in resp.content:
                    await response.write(chunk)
                await response.write_eof()

        self._audit.log_request(
            url=url,
            method="POST",
            status=200,
            duration_ms=(time.time() - start_time) * 1000,
            detections=detections,
            is_stream=True,
        )

        return response

    def _error_response(self, status: int, message: str) -> web.Response:
        """错误响应."""
        return web.json_response(
            {"error": {"message": message, "type": "invalid_request_error"}},
            status=status,
        )
