from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "api_keys" (
    "key_id" SERIAL NOT NULL PRIMARY KEY,
    "api_key" VARCHAR(255) NOT NULL UNIQUE,
    "api_name" VARCHAR(255),
    "api_address" VARCHAR(255),
    "api_type" VARCHAR(50),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
        DROP TABLE IF EXISTS "apikeys";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "api_keys";"""
