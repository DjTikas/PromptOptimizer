from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "modelproviders" (
    "provider_id" SERIAL NOT NULL PRIMARY KEY,
    "provider_name" VARCHAR(50) NOT NULL,
    "base_url" VARCHAR(255) NOT NULL,
    "api_key" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "modelproviders"."provider_name" IS '名称（OpenAIAnthropic等）';
COMMENT ON COLUMN "modelproviders"."base_url" IS 'API基础地址';
COMMENT ON COLUMN "modelproviders"."api_key" IS '加密存储的系统级API密钥';
CREATE TABLE IF NOT EXISTS "users" (
    "user_id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "role" VARCHAR(5) NOT NULL  DEFAULT 'user',
    "avatar_url" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."email" IS '注册邮箱';
COMMENT ON COLUMN "users"."password_hash" IS '加密后的密码（建议使用bcrypt）';
COMMENT ON COLUMN "users"."role" IS '用户角色';
COMMENT ON COLUMN "users"."avatar_url" IS '头像存储路径';
COMMENT ON COLUMN "users"."created_at" IS '注册时间';
CREATE TABLE IF NOT EXISTS "apikeys" (
    "key_id" SERIAL NOT NULL PRIMARY KEY,
    "api_key" VARCHAR(255) NOT NULL UNIQUE,
    "description" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "apikeys"."api_key" IS '加密存储的API密钥';
COMMENT ON COLUMN "apikeys"."description" IS '描述';
COMMENT ON COLUMN "apikeys"."created_at" IS '创建时间';
COMMENT ON COLUMN "apikeys"."is_active" IS '是否启用';
COMMENT ON COLUMN "apikeys"."user_id" IS '关联用户';
CREATE TABLE IF NOT EXISTS "folders" (
    "folder_id" SERIAL NOT NULL PRIMARY KEY,
    "folder_name" VARCHAR(100) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "folders"."folder_name" IS '文件夹名称';
COMMENT ON COLUMN "folders"."user_id" IS '所属用户';
CREATE TABLE IF NOT EXISTS "generations" (
    "generation_id" SERIAL NOT NULL PRIMARY KEY,
    "input_text" TEXT NOT NULL,
    "generation_strategy" VARCHAR(3) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "generations"."input_text" IS '用户输入的原始需求';
COMMENT ON COLUMN "generations"."generation_strategy" IS '生成策略';
COMMENT ON COLUMN "generations"."created_at" IS '生成时间';
COMMENT ON COLUMN "generations"."user_id" IS '用户ID';
CREATE TABLE IF NOT EXISTS "sessions" (
    "session_id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "sessions"."title" IS '会话标题';
COMMENT ON COLUMN "sessions"."created_at" IS '创建时间';
COMMENT ON COLUMN "sessions"."user_id" IS '关联用户';
CREATE TABLE IF NOT EXISTS "prompts" (
    "prompt_id" SERIAL NOT NULL PRIMARY KEY,
    "original_content" TEXT NOT NULL,
    "optimized_content" TEXT,
    "usage_count" INT NOT NULL  DEFAULT 0,
    "is_shared" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "session_id" INT NOT NULL REFERENCES "sessions" ("session_id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "prompts"."original_content" IS '原始提示词内容';
COMMENT ON COLUMN "prompts"."optimized_content" IS '优化后内容';
COMMENT ON COLUMN "prompts"."usage_count" IS '使用次数';
COMMENT ON COLUMN "prompts"."is_shared" IS '是否分享到社区';
COMMENT ON COLUMN "prompts"."created_at" IS '创建时间';
COMMENT ON COLUMN "prompts"."session_id" IS '所属会话';
COMMENT ON COLUMN "prompts"."user_id" IS '创建用户';
CREATE TABLE IF NOT EXISTS "apicalls" (
    "call_id" SERIAL NOT NULL PRIMARY KEY,
    "tokens_used" INT NOT NULL,
    "cost" DECIMAL(10,4) NOT NULL,
    "called_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("prompt_id") ON DELETE CASCADE,
    "provider_id" INT NOT NULL REFERENCES "modelproviders" ("provider_id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "apicalls"."tokens_used" IS '消耗的token数量';
COMMENT ON COLUMN "apicalls"."cost" IS '计算后的成本';
COMMENT ON COLUMN "apicalls"."called_at" IS '调用时间';
COMMENT ON COLUMN "apicalls"."prompt_id" IS '关联提示词';
COMMENT ON COLUMN "apicalls"."provider_id" IS '模型提供商';
COMMENT ON COLUMN "apicalls"."user_id" IS '用户ID';
CREATE TABLE IF NOT EXISTS "communityinteractions" (
    "interaction_id" SERIAL NOT NULL PRIMARY KEY,
    "action_type" VARCHAR(10) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("prompt_id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "communityinteractions"."action_type" IS '互动类型';
COMMENT ON COLUMN "communityinteractions"."created_at" IS '操作时间';
COMMENT ON COLUMN "communityinteractions"."prompt_id" IS '关联提示词';
COMMENT ON COLUMN "communityinteractions"."user_id" IS '操作用户';
CREATE TABLE IF NOT EXISTS "optimizationconfigs" (
    "config_id" SERIAL NOT NULL PRIMARY KEY,
    "optimization_model" VARCHAR(50) NOT NULL,
    "role_enhancement" TEXT,
    "example_enhancement" TEXT,
    "cot_enabled" BOOL NOT NULL,
    "chain_decomposition" BOOL NOT NULL,
    "reflection_enabled" BOOL NOT NULL,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("prompt_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "optimizationconfigs"."optimization_model" IS '使用的优化模型';
COMMENT ON COLUMN "optimizationconfigs"."role_enhancement" IS '角色强化配置';
COMMENT ON COLUMN "optimizationconfigs"."example_enhancement" IS '示例增强配置';
COMMENT ON COLUMN "optimizationconfigs"."cot_enabled" IS '是否启用思维链';
COMMENT ON COLUMN "optimizationconfigs"."chain_decomposition" IS '是否启用链式分解';
COMMENT ON COLUMN "optimizationconfigs"."reflection_enabled" IS '是否启用反思迭代';
COMMENT ON COLUMN "optimizationconfigs"."prompt_id" IS '关联提示词';
CREATE TABLE IF NOT EXISTS "promptfolders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "folder_id" INT NOT NULL REFERENCES "folders" ("folder_id") ON DELETE CASCADE,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("prompt_id") ON DELETE CASCADE,
    CONSTRAINT "uid_promptfolde_prompt__3b3cdb" UNIQUE ("prompt_id", "folder_id")
);
COMMENT ON COLUMN "promptfolders"."folder_id" IS '文件夹ID';
COMMENT ON COLUMN "promptfolders"."prompt_id" IS '提示词ID';
CREATE TABLE IF NOT EXISTS "tags" (
    "tag_id" SERIAL NOT NULL PRIMARY KEY,
    "tag_name" VARCHAR(50) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("user_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tags"."tag_name" IS '标签名称（需唯一约束 per user）';
COMMENT ON COLUMN "tags"."user_id" IS '所属用户';
CREATE TABLE IF NOT EXISTS "prompttags" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "prompt_id" INT NOT NULL REFERENCES "prompts" ("prompt_id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tags" ("tag_id") ON DELETE CASCADE,
    CONSTRAINT "uid_prompttags_prompt__4814ac" UNIQUE ("prompt_id", "tag_id")
);
COMMENT ON COLUMN "prompttags"."prompt_id" IS '提示词ID';
COMMENT ON COLUMN "prompttags"."tag_id" IS '标签ID';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
