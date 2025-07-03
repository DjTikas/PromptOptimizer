from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "communityinteractions" RENAME COLUMN "interaction_id" TO "id";
        ALTER TABLE "communityinteractions" DROP COLUMN "action_type";
        COMMENT ON COLUMN "communityinteractions"."prompt_id" IS '被点赞提示词';
        COMMENT ON COLUMN "communityinteractions"."user_id" IS '点赞用户';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "communityinteractions" RENAME COLUMN "id" TO "interaction_id";
        ALTER TABLE "communityinteractions" ADD "action_type" VARCHAR(10) NOT NULL;
        COMMENT ON COLUMN "communityinteractions"."prompt_id" IS '关联提示词';
        COMMENT ON COLUMN "communityinteractions"."user_id" IS '操作用户';"""
