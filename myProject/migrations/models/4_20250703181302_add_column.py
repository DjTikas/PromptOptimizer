from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "communityinteractions" RENAME TO "community_interactions";
        COMMENT ON COLUMN "community_interactions"."prompt_id" IS NULL;
        COMMENT ON COLUMN "community_interactions"."user_id" IS NULL;
        COMMENT ON COLUMN "community_interactions"."created_at" IS NULL;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_community_i_prompt__8f9e40" ON "community_interactions" ("prompt_id", "user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_community_i_prompt__8f9e40";
        ALTER TABLE "community_interactions" RENAME TO "communityinteractions";
        COMMENT ON COLUMN "community_interactions"."prompt_id" IS '被点赞提示词';
        COMMENT ON COLUMN "community_interactions"."user_id" IS '点赞用户';
        COMMENT ON COLUMN "community_interactions"."created_at" IS '操作时间';"""
