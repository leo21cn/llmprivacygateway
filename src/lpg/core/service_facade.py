"""Service facade - unified service entry point."""

from typing import Optional, Dict, Any, List
from lpg.core.config.service import ConfigService
from lpg.core.proxy.server import ProxyServer
from lpg.core.key.manager import KeyManager
from lpg.core.rule.manager import RuleManager
from lpg.core.audit.service import AuditService
from lpg.core.presidio.client import PresidioClient


class ServiceFacade:
    """服务门面 - 统一服务入口.

    设计原则:
    1. CLI 命令通过门面访问核心服务
    2. 门面隐藏服务间依赖关系
    3. 便于后续版本添加新服务
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化服务门面.

        Args:
            config_path: 配置文件路径
        """
        self._config_service = ConfigService(config_path)
        self._presidio_client = PresidioClient(self._config_service)
        self._audit_service = AuditService(self._config_service)
        self._key_manager = KeyManager(self._config_service)
        self._rule_manager = RuleManager(self._config_service)
        self._proxy_server: Optional[ProxyServer] = None

    # ========== 代理服务 ==========

    def start_service(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        daemon: bool = False,
        log_level: str = "info",
        log_file: Optional[str] = None,
    ) -> None:
        """启动代理服务."""
        self._proxy_server = ProxyServer(
            config_service=self._config_service,
            key_manager=self._key_manager,
            rule_manager=self._rule_manager,
            presidio_client=self._presidio_client,
            audit_service=self._audit_service,
        )
        self._proxy_server.start(
            host=host, port=port, daemon=daemon, log_level=log_level, log_file=log_file
        )

    def stop_service(self, force: bool = False) -> None:
        """停止代理服务."""
        if self._proxy_server:
            self._proxy_server.stop(force=force)

    def is_running(self) -> bool:
        """检查服务是否运行."""
        return (
            self._proxy_server is not None and self._proxy_server.is_running()
        )

    def get_status(self) -> Dict[str, Any]:
        """获取服务状态."""
        return {
            "running": self.is_running(),
            "host": self._config_service.get("proxy.host", "127.0.0.1"),
            "port": self._config_service.get("proxy.port", 8080),
            "pid": self._proxy_server.pid if self._proxy_server else None,
            "uptime": self._proxy_server.uptime if self._proxy_server else 0,
            "rules_count": self._rule_manager.count(),
            "keys_count": self._key_manager.count(),
            "stats": self._proxy_server.stats if self._proxy_server else {},
        }

    # ========== Key 管理 ==========

    def create_virtual_key(
        self, provider: str, name: str, expires_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """创建虚拟 Key."""
        return self._key_manager.create(
            provider=provider, name=name, expires_at=expires_at
        )

    def list_virtual_keys(self) -> List[Dict[str, Any]]:
        """列出所有虚拟 Key."""
        return self._key_manager.list_all()

    def revoke_virtual_key(self, key_id: str) -> bool:
        """吊销虚拟 Key."""
        return self._key_manager.revoke(key_id)

    def get_key_info(self, key_id: str) -> Optional[Dict[str, Any]]:
        """获取 Key 详情."""
        return self._key_manager.get_info(key_id)

    # ========== 规则管理 ==========

    def list_rules(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出规则."""
        return self._rule_manager.list_all(category=category)

    def enable_rule(self, rule_id: str) -> bool:
        """启用规则."""
        return self._rule_manager.enable(rule_id)

    def disable_rule(self, rule_id: str) -> bool:
        """禁用规则."""
        return self._rule_manager.disable(rule_id)

    def import_rules(self, file_path: str) -> int:
        """导入规则文件."""
        return self._rule_manager.import_from_file(file_path)

    def test_rule(self, rule_config: Dict[str, Any], text: str) -> Dict[str, Any]:
        """测试规则."""
        return self._rule_manager.test_rule(rule_config, text)

    # ========== 配置管理 ==========

    def get_config(self, key: Optional[str] = None) -> Any:
        """获取配置."""
        return self._config_service.get(key)

    def set_config(self, key: str, value: Any) -> None:
        """设置配置."""
        self._config_service.set(key, value)

    def init_config(self, interactive: bool = True) -> None:
        """初始化配置."""
        self._config_service.init(interactive=interactive)

    # ========== 提供商管理 ==========

    def list_providers(self) -> List[Dict[str, Any]]:
        """列出提供商."""
        return self._config_service.get_providers()

    def add_provider(
        self, provider_type: str, name: str, **kwargs
    ) -> Dict[str, Any]:
        """添加提供商."""
        return self._config_service.add_provider(provider_type, name, **kwargs)

    def test_provider(self, name: str) -> bool:
        """测试提供商连接."""
        provider = self._config_service.get_provider(name)
        if not provider:
            return False
        return True  # Simplified for now

    # ========== 日志管理 ==========

    def get_logs(
        self, lines: int = 50, level: Optional[str] = None, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取日志."""
        return self._audit_service.get_logs(lines=lines, level=level, since=since)

    def get_log_stats(self, since: Optional[str] = None) -> Dict[str, Any]:
        """获取日志统计."""
        return self._audit_service.get_stats(since=since)

    def export_logs(self, output_path: str, since: Optional[str] = None) -> int:
        """导出日志."""
        return self._audit_service.export(output_path, since=since)
