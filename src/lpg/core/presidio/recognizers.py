"""中文 PII 识别器配置.

提供中国特定 PII 实体的正则识别器，包括：
- 中国身份证号 (CN_ID_CARD)
- 中国手机号 (CN_PHONE_NUMBER)
- 中国银行卡号 (CN_BANK_CARD)
"""

from typing import List, Dict, Any


class ChineseRecognizers:
    """中文 PII 识别器.
    
    使用正则表达式匹配中国特定 PII 实体。
    """

    # 中国身份证号正则（15位或18位）
    # 18位：17位数字 + 1位数字或X/x
    # 15位：15位数字
    CN_ID_CARD_PATTERN = r"(?:^|[^\d])(\d{17}[\dXx]|\d{15})(?:[^\d]|$)"
    
    # 中国手机号正则（支持 +86 前缀）
    CN_PHONE_PATTERN = r"(?:\+86[-\s]?)?1[3-9]\d{9}(?:[^\d]|$)"
    
    # 中国银行卡号正则（16-19位）
    CN_BANK_CARD_PATTERN = r"(?:^|[^\d])(\d{16,19})(?:[^\d]|$)"

    @classmethod
    def get_recognizers(cls) -> List[Dict[str, Any]]:
        """获取所有中文识别器配置.
        
        Returns:
            Presidio ad_hoc_recognizers 格式的识别器列表
        """
        return [
            {
                "name": "CN_ID_CARD_Recognizer",
                "supported_language": "en",
                "supported_entity": "CN_ID_CARD",
                "patterns": [
                    {
                        "name": "cn_id_card",
                        "regex": cls.CN_ID_CARD_PATTERN,
                        "score": 0.9
                    }
                ]
            },
            {
                "name": "CN_PHONE_Recognizer",
                "supported_language": "en",
                "supported_entity": "CN_PHONE_NUMBER",
                "patterns": [
                    {
                        "name": "cn_phone",
                        "regex": cls.CN_PHONE_PATTERN,
                        "score": 0.85
                    }
                ]
            },
            {
                "name": "CN_BANK_CARD_Recognizer",
                "supported_language": "en",
                "supported_entity": "CN_BANK_CARD",
                "patterns": [
                    {
                        "name": "cn_bank_card",
                        "regex": cls.CN_BANK_CARD_PATTERN,
                        "score": 0.8
                    }
                ]
            }
        ]

    @classmethod
    def analyze_with_chinese_recognizers(cls, text: str) -> List[Dict[str, Any]]:
        """使用本地中文识别器分析文本.
        
        当 Presidio 服务不可用时，使用本地正则进行识别。
        
        Args:
            text: 待检测文本
            
        Returns:
            检测结果列表
        """
        import re
        results = []
        
        # 检测身份证号
        for match in re.finditer(cls.CN_ID_CARD_PATTERN, text):
            # 提取捕获组中的实际身份证号
            if match.lastindex and match.lastindex >= 1:
                start = match.start(1)
                end = match.end(1)
            else:
                start = match.start()
                end = match.end()
            results.append({
                "entity_type": "CN_ID_CARD",
                "start": start,
                "end": end,
                "score": 0.9,
                "analysis_explanation": None
            })
        
        # 检测手机号
        for match in re.finditer(cls.CN_PHONE_PATTERN, text):
            # 去除末尾的非数字字符
            phone_text = match.group(0)
            # 找到实际的数字部分
            digit_match = re.search(r'(?:\+86[-\s]?)?1[3-9]\d{9}', phone_text)
            if digit_match:
                start = match.start() + digit_match.start()
                end = start + len(digit_match.group(0))
                results.append({
                    "entity_type": "CN_PHONE_NUMBER",
                    "start": start,
                    "end": end,
                    "score": 0.85,
                    "analysis_explanation": None
                })
        
        # 检测银行卡号（需要排除身份证号的误报）
        for match in re.finditer(cls.CN_BANK_CARD_PATTERN, text):
            # 提取捕获组中的实际卡号
            if match.lastindex and match.lastindex >= 1:
                card_number = match.group(1)
                start = match.start(1)
                end = match.end(1)
                # 排除身份证号（15或18位）
                if len(card_number) not in [15, 18]:
                    results.append({
                        "entity_type": "CN_BANK_CARD",
                        "start": start,
                        "end": end,
                        "score": 0.8,
                        "analysis_explanation": None
                    })
        
        return results
