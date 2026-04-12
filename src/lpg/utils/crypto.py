"""加密工具."""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoUtils:
    """加密工具类."""

    @staticmethod
    def generate_key() -> str:
        """生成加密密钥."""
        return Fernet.generate_key().decode()

    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """从密码派生密钥."""
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def encrypt(data: str, key: str) -> str:
        """加密数据."""
        f = Fernet(key.encode() if isinstance(key, str) else key)
        return f.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt(encrypted: str, key: str) -> str:
        """解密数据."""
        f = Fernet(key.encode() if isinstance(key, str) else key)
        return f.decrypt(encrypted.encode()).decode()
