from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "users"."created_at" IS '注册时间(UTC)';
        ALTER TABLE "users" ALTER COLUMN "role" TYPE VARCHAR(5) USING "role"::VARCHAR(5);
        COMMENT ON COLUMN "users"."password_hash" IS '加密后的密码';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "users"."created_at" IS '注册时间';
        ALTER TABLE "users" ALTER COLUMN "role" TYPE VARCHAR(5) USING "role"::VARCHAR(5);
        COMMENT ON COLUMN "users"."password_hash" IS '加密后的密码（建议使用bcrypt）';"""
