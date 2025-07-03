import os
from tortoise import Tortoise
from dotenv import load_dotenv

# 从.env文件加载环境变量
load_dotenv()

# Tortoise ORM的配置字典
TORTOISE_ORM = {
    # 数据库连接配置，从环境变量中获取数据库连接URL
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            # 指定应用中使用的模型模块
            "models": ["app.models.user","app.models.prompt","aerich.models"],
            # 指定默认的数据库连接
            "default_connection": "default",
        }
    },
}

class Settings:
    EMAILS_FROM_NAME = os.getenv("EMAILS_FROM_NAME", "Your App Name")
    EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_TLS = bool(os.getenv("SMTP_TLS", True))
    SMTP_SSL = bool(os.getenv("SMTP_SSL", False))
    SMTP_user = os.getenv("SMTP_user")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

settings = Settings()