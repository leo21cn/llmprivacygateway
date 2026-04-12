"""Presidio service client."""

import aiohttp
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PresidioClient:
    """Presidio 服务客户端.

    职责:
    1. 调用 presidio-analyzer 进行 PII 检测
    2. 调用 presidio-anonymizer 进行脱敏处理
    3. 管理服务连接和健康检查
    """

    def __init__(self, config_service):
        """初始化 Presidio 客户端.

        Args:
            config_service: 配置服务
        """
        self._config = config_service
        self._base_url = config_service.get("presidio.endpoint", "http://localhost:5001")
        self._language = config_service.get("presidio.language", "zh")
        self._timeout = aiohttp.ClientTimeout(total=30)

    async def analyze(
        self,
        text: str,
        language: Optional[str] = None,
        entities: Optional[List[str]] = None,
        score_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """调用 Presidio Analyzer 检测 PII.

        Args:
            text: 待检测文本
            language: 语言代码
            entities: 指定检测的实体类型
            score_threshold: 置信度阈值

        Returns:
            检测结果列表
        """
        url = f"{self._base_url}/analyze"

        payload = {
            "text": text,
            "language": language or self._language,
            "score_threshold": score_threshold,
        }

        if entities:
            payload["entities"] = entities

        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logger.error(f"Analyzer failed: {resp.status}")
                        return []
        except Exception as e:
            logger.error(f"Analyzer error: {e}")
            return []

    async def anonymize(
        self,
        text: str,
        analyzer_results: List[Dict[str, Any]],
        operators: Optional[Dict[str, Dict]] = None,
    ) -> str:
        """调用 Presidio Anonymizer 进行脱敏.

        Args:
            text: 原始文本
            analyzer_results: 检测结果
            operators: 自定义脱敏操作符

        Returns:
            脱敏后的文本
        """
        url = f"{self._base_url}/anonymize"

        default_operators = self._get_default_operators()
        if operators:
            default_operators.update(operators)

        payload = {
            "text": text,
            "analyzer_results": analyzer_results,
            "operators": default_operators,
        }

        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result.get("text", text)
                    else:
                        logger.error(f"Anonymizer failed: {resp.status}")
                        return text
        except Exception as e:
            logger.error(f"Anonymizer error: {e}")
            return text

    def _get_default_operators(self) -> Dict[str, Dict]:
        """获取默认脱敏策略."""
        return {
            "DEFAULT": {"type": "replace", "new_value": "<REDACTED>"},
            "EMAIL_ADDRESS": {
                "type": "mask",
                "masking_char": "*",
                "chars_to_mask": 4,
                "from_end": False,
            },
            "PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"},
            "CREDIT_CARD": {
                "type": "mask",
                "masking_char": "*",
                "chars_to_mask": 12,
                "from_end": False,
            },
            "PERSON": {"type": "replace", "new_value": "<PERSON>"},
            "LOCATION": {"type": "replace", "new_value": "<LOCATION>"},
            "IP_ADDRESS": {"type": "replace", "new_value": "<IP>"},
            "URL": {
                "type": "mask",
                "masking_char": "*",
                "chars_to_mask": 10,
                "from_end": False,
            },
            "CN_PHONE_NUMBER": {"type": "replace", "new_value": "<PHONE>"},
            "CN_ID_CARD": {"type": "replace", "new_value": "<ID_CARD>"},
            "CN_BANK_CARD": {"type": "replace", "new_value": "<BANK_CARD>"},
        }

    async def health_check(self) -> bool:
        """健康检查."""
        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.get(f"{self._base_url}/health") as resp:
                    return resp.status == 200
        except Exception:
            return False
