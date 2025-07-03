import time
from typing import Dict, Tuple
import random

# 存储邮箱和验证码的映射
email_code_store: Dict[str, Tuple[str, float]] = {}

class EmailCodeService:
    @staticmethod
    def generate_code() -> str:
        """生成6位数字验证码"""
        return str(random.randint(100000, 999999))

    @staticmethod
    def store_code(email: str, code: str):
        """存储邮箱和对应的验证码，并记录时间戳"""
        email_code_store[email] = (code, time.time())

    @staticmethod
    def cleanup_expired():
        """清理过期的验证码"""
        current_time = time.time()
        expired_emails = [email for email, (_, timestamp) in email_code_store.items() if current_time - timestamp > 300]
        for email in expired_emails:
            del email_code_store[email]

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """验证验证码是否正确且未过期"""
        stored_code, timestamp = email_code_store.get(email, (None, None))
        if stored_code and stored_code == code and time.time() - timestamp <= 300:
            del email_code_store[email]
            return True
        return False