"""Rule manager."""

import yaml
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class RuleManager:
    """规则管理器.

    职责:
    1. 加载和管理检测规则
    2. 规则的启用/禁用
    3. 自定义规则导入
    4. 规则测试
    """

    def __init__(self, config_service):
        """初始化规则管理器.

        Args:
            config_service: 配置服务
        """
        self._config = config_service
        self._rules: Dict[str, Dict] = {}
        self._load_builtin_rules()
        self._load_custom_rules()

    def _load_builtin_rules(self):
        """加载内置规则."""
        # Try multiple possible locations for rules directory
        possible_paths = [
            # Development/installed package path
            Path(__file__).parent.parent.parent / "rules",
            # Project root path (when running from source)
            Path(__file__).parent.parent.parent.parent.parent / "rules",
            # Current working directory
            Path.cwd() / "rules",
        ]
        
        for rules_dir in possible_paths:
            if rules_dir.exists():
                for rule_file in rules_dir.glob("*.yaml"):
                    self._load_rule_file(rule_file)
                break  # Stop after finding the first valid rules directory

    def _load_custom_rules(self):
        """加载自定义规则."""
        custom_dir = self._config.get("rules.custom_rules_dir")
        if custom_dir:
            custom_path = Path(custom_dir).expanduser()
            if custom_path.exists():
                for rule_file in custom_path.glob("*.yaml"):
                    self._load_rule_file(rule_file)

    def _load_rule_file(self, file_path: Path):
        """加载规则文件."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if "rules" in data:
                for rule in data["rules"]:
                    rule_id = rule.get("id")
                    if rule_id:
                        rule["enabled"] = rule.get("enabled", True)
                        rule["source"] = str(file_path)
                        self._rules[rule_id] = rule

            logger.info(f"Loaded {len(data.get('rules', []))} rules from {file_path}")
        except Exception as e:
            logger.error(f"Failed to load rules from {file_path}: {e}")

    def list_all(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出规则."""
        rules = list(self._rules.values())

        if category:
            rules = [r for r in rules if r.get("category") == category]

        return [
            {
                "id": r["id"],
                "name": r.get("name", r["id"]),
                "category": r.get("category", "uncategorized"),
                "type": r.get("type", "regex"),
                "entity_type": r.get("entity_type"),
                "enabled": r.get("enabled", True),
                "description": r.get("description", ""),
            }
            for r in rules
        ]

    def get_enabled_rules(self) -> List[Dict[str, Any]]:
        """获取启用的规则."""
        return [r for r in self._rules.values() if r.get("enabled", True)]

    def enable(self, rule_id: str) -> bool:
        """启用规则."""
        if rule_id in self._rules:
            self._rules[rule_id]["enabled"] = True
            return True
        return False

    def disable(self, rule_id: str) -> bool:
        """禁用规则."""
        if rule_id in self._rules:
            self._rules[rule_id]["enabled"] = False
            return True
        return False

    def import_from_file(self, file_path: str) -> int:
        """从文件导入规则."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Rule file not found: {file_path}")

        count_before = len(self._rules)
        self._load_rule_file(path)
        return len(self._rules) - count_before

    def test_rule(self, rule_config: Dict[str, Any], text: str) -> Dict[str, Any]:
        """测试规则."""
        rule_type = rule_config.get("type", "regex")
        matches = []

        if rule_type == "regex":
            pattern = rule_config.get("pattern", "")
            if pattern:
                try:
                    regex = re.compile(pattern)
                    for match in regex.finditer(text):
                        matches.append(
                            {
                                "start": match.start(),
                                "end": match.end(),
                                "text": match.group(),
                            }
                        )
                except re.error as e:
                    return {"error": f"Invalid regex: {e}"}

        elif rule_type == "keyword":
            keywords = rule_config.get("keywords", [])
            for keyword in keywords:
                start = 0
                while True:
                    pos = text.find(keyword, start)
                    if pos == -1:
                        break
                    matches.append(
                        {
                            "start": pos,
                            "end": pos + len(keyword),
                            "text": keyword,
                        }
                    )
                    start = pos + 1

        return {"matches": matches, "count": len(matches)}

    def count(self) -> int:
        """获取规则数量."""
        return len(self._rules)
