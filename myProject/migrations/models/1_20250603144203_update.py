from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "examples" (
    "example_id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "is_preset" BOOL NOT NULL DEFAULT False,
    "user_id" INT REFERENCES "users" ("user_id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "roles" (
    "role_id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "is_preset" BOOL NOT NULL DEFAULT False,
    "user_id" INT REFERENCES "users" ("user_id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "roles";
        DROP TABLE IF EXISTS "examples";"""
