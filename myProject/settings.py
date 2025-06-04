TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "5432",
                "user": "postgres",
                "password": "123456",
                "database": "myProject",
                "minsize": 1,
                "maxsize": 5,
            },
        },
    },
    "apps": {
        "models": { # 应用名称改为models
            "models": ["models", "aerich.models"], # models.py的路径
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai"
}