/*
 Navicat Premium Dump SQL

 Source Server         : Local PostgreSQL
 Source Server Type    : PostgreSQL
 Source Server Version : 160008 (160008)
 Source Host           : localhost:5432
 Source Catalog        : myProject
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160008 (160008)
 File Encoding         : 65001

 Date: 04/06/2025 15:53:17
*/


-- ----------------------------
-- Sequence structure for aerich_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."aerich_id_seq";
CREATE SEQUENCE "public"."aerich_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for apicalls_call_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."apicalls_call_id_seq";
CREATE SEQUENCE "public"."apicalls_call_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for apikeys_key_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."apikeys_key_id_seq";
CREATE SEQUENCE "public"."apikeys_key_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for communityinteractions_interaction_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."communityinteractions_interaction_id_seq";
CREATE SEQUENCE "public"."communityinteractions_interaction_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for examples_example_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."examples_example_id_seq";
CREATE SEQUENCE "public"."examples_example_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for folders_folder_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."folders_folder_id_seq";
CREATE SEQUENCE "public"."folders_folder_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for generations_generation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."generations_generation_id_seq";
CREATE SEQUENCE "public"."generations_generation_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for modelproviders_provider_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."modelproviders_provider_id_seq";
CREATE SEQUENCE "public"."modelproviders_provider_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for optimizationconfigs_config_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."optimizationconfigs_config_id_seq";
CREATE SEQUENCE "public"."optimizationconfigs_config_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for promptfolders_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."promptfolders_id_seq";
CREATE SEQUENCE "public"."promptfolders_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for prompts_prompt_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."prompts_prompt_id_seq";
CREATE SEQUENCE "public"."prompts_prompt_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for prompttags_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."prompttags_id_seq";
CREATE SEQUENCE "public"."prompttags_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for roles_role_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."roles_role_id_seq";
CREATE SEQUENCE "public"."roles_role_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for sessions_session_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."sessions_session_id_seq";
CREATE SEQUENCE "public"."sessions_session_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tags_tag_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."tags_tag_id_seq";
CREATE SEQUENCE "public"."tags_tag_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_user_id_seq";
CREATE SEQUENCE "public"."users_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for aerich
-- ----------------------------
DROP TABLE IF EXISTS "public"."aerich";
CREATE TABLE "public"."aerich" (
  "id" int4 NOT NULL DEFAULT nextval('aerich_id_seq'::regclass),
  "version" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "app" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "content" jsonb NOT NULL
)
;

-- ----------------------------
-- Records of aerich
-- ----------------------------
INSERT INTO "public"."aerich" VALUES (1, '0_20250522124628_init.py', 'models', '{"models.Tags": {"app": "models", "name": "models.Tags", "table": "tags", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "tag_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "tag_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "tag_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tag_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "标签名称（需唯一约束 per user）", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "标签ID", "python_type": "models.PromptTags", "db_constraint": true}], "backward_o2o_fields": []}, "models.Users": {"app": "models", "name": "models.Users", "table": "users", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "user_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "user_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "email", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "注册邮箱", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "password_hash", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password_hash", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密后的密码（建议使用bcrypt）", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "role", "unique": false, "default": "user", "indexed": false, "nullable": false, "db_column": "role", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 5}, "description": "用户角色", "python_type": "str", "db_field_types": {"": "VARCHAR(5)"}}, {"name": "avatar_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "avatar_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "头像存储路径", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "注册时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "用户ID", "python_type": "models.ApiCalls", "db_constraint": true}, {"name": "api_keys", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联用户", "python_type": "models.ApiKeys", "db_constraint": true}, {"name": "community_interactions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "操作用户", "python_type": "models.CommunityInteractions", "db_constraint": true}, {"name": "folders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属用户", "python_type": "models.Folders", "db_constraint": true}, {"name": "generations", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "用户ID", "python_type": "models.Generations", "db_constraint": true}, {"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "创建用户", "python_type": "models.Prompts", "db_constraint": true}, {"name": "sessions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联用户", "python_type": "models.Sessions", "db_constraint": true}, {"name": "tags", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属用户", "python_type": "models.Tags", "db_constraint": true}], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ApiKeys": {"app": "models", "name": "models.ApiKeys", "table": "apikeys", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "key_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "key_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "api_key", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "api_key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密存储的API密钥", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "描述", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "is_active", "unique": false, "default": true, "indexed": false, "nullable": false, "db_column": "is_active", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Folders": {"app": "models", "name": "models.Folders", "table": "folders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "folder_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "folder_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "folder_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "folder_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": "文件夹名称", "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "文件夹ID", "python_type": "models.PromptFolders", "db_constraint": true}], "backward_o2o_fields": []}, "models.Prompts": {"app": "models", "name": "models.Prompts", "table": "prompts", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "prompt_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "创建用户", "python_type": "models.Users", "db_constraint": true}, {"name": "session", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "session_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属会话", "python_type": "models.Sessions", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "original_content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "original_content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "原始提示词内容", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "optimized_content", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "optimized_content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "优化后内容", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "usage_count", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "usage_count", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "使用次数", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "is_shared", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_shared", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否分享到社区", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "session_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "session_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属会话", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "创建用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.ApiCalls", "db_constraint": true}, {"name": "community_interactions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.CommunityInteractions", "db_constraint": true}, {"name": "optimization_configs", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.OptimizationConfigs", "db_constraint": true}, {"name": "folders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "提示词ID", "python_type": "models.PromptFolders", "db_constraint": true}, {"name": "tags", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "提示词ID", "python_type": "models.PromptTags", "db_constraint": true}], "backward_o2o_fields": []}, "models.ApiCalls": {"app": "models", "name": "models.ApiCalls", "table": "apicalls", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "call_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "call_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "用户ID", "python_type": "models.Users", "db_constraint": true}, {"name": "provider", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "provider_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "模型提供商", "python_type": "models.ModelProviders", "db_constraint": true}, {"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "tokens_used", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tokens_used", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "消耗的token数量", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "cost", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "cost", "docstring": null, "generated": false, "field_type": "DecimalField", "constraints": {}, "description": "计算后的成本", "python_type": "decimal.Decimal", "db_field_types": {"": "DECIMAL(10,4)", "sqlite": "VARCHAR(40)"}}, {"name": "called_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "called_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "调用时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "provider_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "provider_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "模型提供商", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "用户ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Sessions": {"app": "models", "name": "models.Sessions", "table": "sessions", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "session_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "session_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "title", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "title", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": "会话标题", "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属会话", "python_type": "models.Prompts", "db_constraint": true}], "backward_o2o_fields": []}, "models.PromptTags": {"app": "models", "name": "models.PromptTags", "table": "prompttags", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "提示词ID", "python_type": "models.Prompts", "db_constraint": true}, {"name": "tag", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "tag_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "标签ID", "python_type": "models.Tags", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "提示词ID", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "tag_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tag_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "标签ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [["prompt", "tag"]], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Generations": {"app": "models", "name": "models.Generations", "table": "generations", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "generation_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "generation_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "用户ID", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "input_text", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "input_text", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "用户输入的原始需求", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "generation_strategy", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "generation_strategy", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 3}, "description": "生成策略", "python_type": "str", "db_field_types": {"": "VARCHAR(3)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "生成时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "用户ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.PromptFolders": {"app": "models", "name": "models.PromptFolders", "table": "promptfolders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "提示词ID", "python_type": "models.Prompts", "db_constraint": true}, {"name": "folder", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "folder_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "文件夹ID", "python_type": "models.Folders", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "folder_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "folder_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "文件夹ID", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "提示词ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [["prompt", "folder"]], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ModelProviders": {"app": "models", "name": "models.ModelProviders", "table": "modelproviders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "provider_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "provider_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "provider_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "provider_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "名称（OpenAIAnthropic等）", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "base_url", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "base_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "API基础地址", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "api_key", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "api_key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密存储的系统级API密钥", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "模型提供商", "python_type": "models.ApiCalls", "db_constraint": true}], "backward_o2o_fields": []}, "models.OptimizationConfigs": {"app": "models", "name": "models.OptimizationConfigs", "table": "optimizationconfigs", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "config_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "config_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "optimization_model", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "optimization_model", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "使用的优化模型", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "role_enhancement", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "role_enhancement", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "角色强化配置", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "example_enhancement", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "example_enhancement", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "示例增强配置", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "cot_enabled", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "cot_enabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用思维链", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "chain_decomposition", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "chain_decomposition", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用链式分解", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "reflection_enabled", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "reflection_enabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用反思迭代", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.CommunityInteractions": {"app": "models", "name": "models.CommunityInteractions", "table": "communityinteractions", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "interaction_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "interaction_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}, {"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "操作用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "action_type", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "action_type", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 10}, "description": "互动类型", "python_type": "str", "db_field_types": {"": "VARCHAR(10)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "操作时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "操作用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}}');
INSERT INTO "public"."aerich" VALUES (2, '1_20250603144203_update.py', 'models', '{"models.Tags": {"app": "models", "name": "models.Tags", "table": "tags", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "tag_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "tag_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "tag_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tag_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "标签名称（需唯一约束 per user）", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "标签ID", "python_type": "models.PromptTags", "db_constraint": true}], "backward_o2o_fields": []}, "models.Roles": {"app": "models", "name": "models.Roles", "table": "roles", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "role_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "role_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "is_preset", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_preset", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Users": {"app": "models", "name": "models.Users", "table": "users", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "user_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "user_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "email", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "注册邮箱", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "password_hash", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password_hash", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密后的密码（建议使用bcrypt）", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "role", "unique": false, "default": "user", "indexed": false, "nullable": false, "db_column": "role", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 5}, "description": "用户角色", "python_type": "str", "db_field_types": {"": "VARCHAR(5)"}}, {"name": "avatar_url", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "avatar_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "头像存储路径", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "注册时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "用户ID", "python_type": "models.ApiCalls", "db_constraint": true}, {"name": "api_keys", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联用户", "python_type": "models.ApiKeys", "db_constraint": true}, {"name": "community_interactions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "操作用户", "python_type": "models.CommunityInteractions", "db_constraint": true}, {"name": "examples", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Examples", "db_constraint": true}, {"name": "folders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属用户", "python_type": "models.Folders", "db_constraint": true}, {"name": "generations", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "用户ID", "python_type": "models.Generations", "db_constraint": true}, {"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "创建用户", "python_type": "models.Prompts", "db_constraint": true}, {"name": "roles", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Roles", "db_constraint": true}, {"name": "sessions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联用户", "python_type": "models.Sessions", "db_constraint": true}, {"name": "tags", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属用户", "python_type": "models.Tags", "db_constraint": true}], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ApiKeys": {"app": "models", "name": "models.ApiKeys", "table": "apikeys", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "key_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "key_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "api_key", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "api_key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密存储的API密钥", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "描述", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "is_active", "unique": false, "default": true, "indexed": false, "nullable": false, "db_column": "is_active", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Folders": {"app": "models", "name": "models.Folders", "table": "folders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "folder_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "folder_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "folder_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "folder_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": "文件夹名称", "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "文件夹ID", "python_type": "models.PromptFolders", "db_constraint": true}], "backward_o2o_fields": []}, "models.Prompts": {"app": "models", "name": "models.Prompts", "table": "prompts", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "prompt_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "创建用户", "python_type": "models.Users", "db_constraint": true}, {"name": "session", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "session_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "所属会话", "python_type": "models.Sessions", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "original_content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "original_content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "原始提示词内容", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "optimized_content", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "optimized_content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "优化后内容", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "usage_count", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "usage_count", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "使用次数", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "is_shared", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_shared", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否分享到社区", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "session_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "session_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "所属会话", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "创建用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.ApiCalls", "db_constraint": true}, {"name": "community_interactions", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.CommunityInteractions", "db_constraint": true}, {"name": "optimization_configs", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "关联提示词", "python_type": "models.OptimizationConfigs", "db_constraint": true}, {"name": "folders", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "提示词ID", "python_type": "models.PromptFolders", "db_constraint": true}, {"name": "tags", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "提示词ID", "python_type": "models.PromptTags", "db_constraint": true}], "backward_o2o_fields": []}, "models.ApiCalls": {"app": "models", "name": "models.ApiCalls", "table": "apicalls", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "call_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "call_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "用户ID", "python_type": "models.Users", "db_constraint": true}, {"name": "provider", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "provider_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "模型提供商", "python_type": "models.ModelProviders", "db_constraint": true}, {"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "tokens_used", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tokens_used", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "消耗的token数量", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "cost", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "cost", "docstring": null, "generated": false, "field_type": "DecimalField", "constraints": {}, "description": "计算后的成本", "python_type": "decimal.Decimal", "db_field_types": {"": "DECIMAL(10,4)", "sqlite": "VARCHAR(40)"}}, {"name": "called_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "called_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "调用时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "provider_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "provider_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "模型提供商", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "用户ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Examples": {"app": "models", "name": "models.Examples", "table": "examples", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "example_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "example_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "is_preset", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_preset", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Sessions": {"app": "models", "name": "models.Sessions", "table": "sessions", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "session_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "session_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "title", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "title", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": "会话标题", "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "创建时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "prompts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "所属会话", "python_type": "models.Prompts", "db_constraint": true}], "backward_o2o_fields": []}, "models.PromptTags": {"app": "models", "name": "models.PromptTags", "table": "prompttags", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "提示词ID", "python_type": "models.Prompts", "db_constraint": true}, {"name": "tag", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "tag_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "标签ID", "python_type": "models.Tags", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "提示词ID", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "tag_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "tag_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "标签ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [["prompt", "tag"]], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Generations": {"app": "models", "name": "models.Generations", "table": "generations", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "generation_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "generation_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "用户ID", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "input_text", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "input_text", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "用户输入的原始需求", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "generation_strategy", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "generation_strategy", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 3}, "description": "生成策略", "python_type": "str", "db_field_types": {"": "VARCHAR(3)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "生成时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "用户ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.PromptFolders": {"app": "models", "name": "models.PromptFolders", "table": "promptfolders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "提示词ID", "python_type": "models.Prompts", "db_constraint": true}, {"name": "folder", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "folder_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "文件夹ID", "python_type": "models.Folders", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "folder_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "folder_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "文件夹ID", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "提示词ID", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [["prompt", "folder"]], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ModelProviders": {"app": "models", "name": "models.ModelProviders", "table": "modelproviders", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "provider_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "provider_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "provider_name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "provider_name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "名称（OpenAIAnthropic等）", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "base_url", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "base_url", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "API基础地址", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "api_key", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "api_key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": "加密存储的系统级API密钥", "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "api_calls", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": "模型提供商", "python_type": "models.ApiCalls", "db_constraint": true}], "backward_o2o_fields": []}, "models.OptimizationConfigs": {"app": "models", "name": "models.OptimizationConfigs", "table": "optimizationconfigs", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "config_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "config_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "optimization_model", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "optimization_model", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 50}, "description": "使用的优化模型", "python_type": "str", "db_field_types": {"": "VARCHAR(50)"}}, {"name": "role_enhancement", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "role_enhancement", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "角色强化配置", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "example_enhancement", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "example_enhancement", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": "示例增强配置", "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "cot_enabled", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "cot_enabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用思维链", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "chain_decomposition", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "chain_decomposition", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用链式分解", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "reflection_enabled", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "reflection_enabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": "是否启用反思迭代", "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.CommunityInteractions": {"app": "models", "name": "models.CommunityInteractions", "table": "communityinteractions", "indexes": [], "managed": null, "abstract": false, "pk_field": {"name": "interaction_id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "interaction_id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [{"name": "prompt", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "prompt_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "关联提示词", "python_type": "models.Prompts", "db_constraint": true}, {"name": "user", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "user_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": "操作用户", "python_type": "models.Users", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "action_type", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "action_type", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 10}, "description": "互动类型", "python_type": "str", "db_field_types": {"": "VARCHAR(10)"}}, {"name": "created_at", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "created_at", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": "操作时间", "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "prompt_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "prompt_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "关联提示词", "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "user_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "user_id", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": "操作用户", "python_type": "int", "db_field_types": {"": "INT"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}}');

-- ----------------------------
-- Table structure for apicalls
-- ----------------------------
DROP TABLE IF EXISTS "public"."apicalls";
CREATE TABLE "public"."apicalls" (
  "call_id" int4 NOT NULL DEFAULT nextval('apicalls_call_id_seq'::regclass),
  "tokens_used" int4 NOT NULL,
  "cost" numeric(10,4) NOT NULL,
  "called_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "prompt_id" int4 NOT NULL,
  "provider_id" int4 NOT NULL,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."apicalls"."tokens_used" IS '消耗的token数量';
COMMENT ON COLUMN "public"."apicalls"."cost" IS '计算后的成本';
COMMENT ON COLUMN "public"."apicalls"."called_at" IS '调用时间';
COMMENT ON COLUMN "public"."apicalls"."prompt_id" IS '关联提示词';
COMMENT ON COLUMN "public"."apicalls"."provider_id" IS '模型提供商';
COMMENT ON COLUMN "public"."apicalls"."user_id" IS '用户ID';

-- ----------------------------
-- Records of apicalls
-- ----------------------------
INSERT INTO "public"."apicalls" VALUES (1, 850, 0.0085, '2025-05-18 16:07:25.835871+08', 1, 1, 1);
INSERT INTO "public"."apicalls" VALUES (2, 420, 0.0042, '2025-05-23 16:07:25.835871+08', 2, 1, 1);
INSERT INTO "public"."apicalls" VALUES (3, 1250, 0.0125, '2025-05-05 16:07:25.835871+08', 3, 1, 2);
INSERT INTO "public"."apicalls" VALUES (4, 680, 0.0034, '2025-05-28 16:07:25.835871+08', 4, 3, 3);
INSERT INTO "public"."apicalls" VALUES (5, 930, 0.0093, '2025-05-30 16:07:25.835871+08', 5, 1, 4);
INSERT INTO "public"."apicalls" VALUES (6, 760, 0.0076, '2025-06-02 16:07:25.835871+08', 6, 4, 1);
INSERT INTO "public"."apicalls" VALUES (7, 1120, 0.0112, '2025-05-31 16:07:25.835871+08', 6, 2, 2);

-- ----------------------------
-- Table structure for apikeys
-- ----------------------------
DROP TABLE IF EXISTS "public"."apikeys";
CREATE TABLE "public"."apikeys" (
  "key_id" int4 NOT NULL DEFAULT nextval('apikeys_key_id_seq'::regclass),
  "api_key" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "is_active" bool NOT NULL DEFAULT true,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."apikeys"."api_key" IS '加密存储的API密钥';
COMMENT ON COLUMN "public"."apikeys"."description" IS '描述';
COMMENT ON COLUMN "public"."apikeys"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."apikeys"."is_active" IS '是否启用';
COMMENT ON COLUMN "public"."apikeys"."user_id" IS '关联用户';

-- ----------------------------
-- Records of apikeys
-- ----------------------------
INSERT INTO "public"."apikeys" VALUES (1, 'sk-5c7d9e2f1a3b4d6e8f0g1h2i3j4k5l6m', '主要生产密钥', '2025-05-09 16:07:25.828697+08', 't', 1);
INSERT INTO "public"."apikeys" VALUES (2, 'sk-9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4', '管理员仪表盘密钥', '2025-04-24 16:07:25.828697+08', 't', 2);
INSERT INTO "public"."apikeys" VALUES (3, 'sk-3p2q1r0s9t8u7v6w5x4y3z2a1b0c9d8', '内容创作API', '2025-05-22 16:07:25.828697+08', 't', 3);
INSERT INTO "public"."apikeys" VALUES (4, 'sk-7f6e5d4c3b2a1z0y9x8w7v6u5t4s3r2q', '测试环境', '2025-05-29 16:07:25.828697+08', 'f', 1);

-- ----------------------------
-- Table structure for communityinteractions
-- ----------------------------
DROP TABLE IF EXISTS "public"."communityinteractions";
CREATE TABLE "public"."communityinteractions" (
  "interaction_id" int4 NOT NULL DEFAULT nextval('communityinteractions_interaction_id_seq'::regclass),
  "action_type" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "prompt_id" int4 NOT NULL,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."communityinteractions"."action_type" IS '互动类型';
COMMENT ON COLUMN "public"."communityinteractions"."created_at" IS '操作时间';
COMMENT ON COLUMN "public"."communityinteractions"."prompt_id" IS '关联提示词';
COMMENT ON COLUMN "public"."communityinteractions"."user_id" IS '操作用户';

-- ----------------------------
-- Records of communityinteractions
-- ----------------------------
INSERT INTO "public"."communityinteractions" VALUES (1, '点赞', '2025-05-19 16:07:25.83439+08', 1, 2);
INSERT INTO "public"."communityinteractions" VALUES (2, '收藏', '2025-05-22 16:07:25.83439+08', 1, 3);
INSERT INTO "public"."communityinteractions" VALUES (3, '点赞', '2025-05-24 16:07:25.83439+08', 3, 1);
INSERT INTO "public"."communityinteractions" VALUES (4, '使用', '2025-05-26 16:07:25.83439+08', 3, 4);
INSERT INTO "public"."communityinteractions" VALUES (5, '收藏', '2025-05-29 16:07:25.83439+08', 4, 1);
INSERT INTO "public"."communityinteractions" VALUES (6, '点赞', '2025-05-31 16:07:25.83439+08', 4, 2);
INSERT INTO "public"."communityinteractions" VALUES (7, '点赞', '2025-06-01 16:07:25.83439+08', 6, 3);
INSERT INTO "public"."communityinteractions" VALUES (8, '使用', '2025-06-02 16:07:25.83439+08', 6, 4);

-- ----------------------------
-- Table structure for examples
-- ----------------------------
DROP TABLE IF EXISTS "public"."examples";
CREATE TABLE "public"."examples" (
  "example_id" int4 NOT NULL DEFAULT nextval('examples_example_id_seq'::regclass),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "content" text COLLATE "pg_catalog"."default" NOT NULL,
  "is_preset" bool NOT NULL DEFAULT false,
  "user_id" int4
)
;

-- ----------------------------
-- Records of examples
-- ----------------------------
INSERT INTO "public"."examples" VALUES (1, '产品描述', '电子产品营销示例', '产品：降噪耳机\n特性：40小时电池续航，语音助手\n描述：沉浸在纯净音质中，我们的高端耳机采用行业领先的降噪技术。', 't', 1);
INSERT INTO "public"."examples" VALUES (2, '退款回应', '客户服务模板', '亲爱的[客户姓名]，\n\n我们对您的体验感到抱歉。虽然我们的政策要求[政策详情]，但我们愿意提供[替代解决方案]。', 't', NULL);
INSERT INTO "public"."examples" VALUES (3, '广告文案变体', '社交媒体广告示例', '1. 厌倦了拥挤的健身房？随时随地健身。\n2. 20分钟锻炼，带来真正效果\n3. 加入500k+用户，一起改变健身方式', 'f', 1);
INSERT INTO "public"."examples" VALUES (4, '科幻故事开头', '引人入胜的故事开头', '新东京的霓虹灯光在雨中闪烁，基拉看着全息影像闪烁——那条将改变一切的信息："系统在欺骗你。"', 'f', 3);
INSERT INTO "public"."examples" VALUES (5, '销售洞察', '分析报告结构', '关键发现：\n- 第三季度收入增长35%\n- 表现最佳地区：东南亚（+48%）\n建议：\n1. 在高增长地区增加库存\n2. 为表现不佳的产品开发针对性促销活动', 'f', 4);

-- ----------------------------
-- Table structure for folders
-- ----------------------------
DROP TABLE IF EXISTS "public"."folders";
CREATE TABLE "public"."folders" (
  "folder_id" int4 NOT NULL DEFAULT nextval('folders_folder_id_seq'::regclass),
  "folder_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."folders"."folder_name" IS '文件夹名称';
COMMENT ON COLUMN "public"."folders"."user_id" IS '所属用户';

-- ----------------------------
-- Records of folders
-- ----------------------------
INSERT INTO "public"."folders" VALUES (1, '营销项目', 1);
INSERT INTO "public"."folders" VALUES (2, '支持模板', 1);
INSERT INTO "public"."folders" VALUES (3, 'API开发', 2);
INSERT INTO "public"."folders" VALUES (4, '写作作品集', 3);
INSERT INTO "public"."folders" VALUES (5, '商业报告', 4);
INSERT INTO "public"."folders" VALUES (6, '收藏夹', 1);

-- ----------------------------
-- Table structure for generations
-- ----------------------------
DROP TABLE IF EXISTS "public"."generations";
CREATE TABLE "public"."generations" (
  "generation_id" int4 NOT NULL DEFAULT nextval('generations_generation_id_seq'::regclass),
  "input_text" text COLLATE "pg_catalog"."default" NOT NULL,
  "generation_strategy" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."generations"."input_text" IS '用户输入的原始需求';
COMMENT ON COLUMN "public"."generations"."generation_strategy" IS '生成策略';
COMMENT ON COLUMN "public"."generations"."created_at" IS '生成时间';
COMMENT ON COLUMN "public"."generations"."user_id" IS '用户ID';

-- ----------------------------
-- Records of generations
-- ----------------------------
INSERT INTO "public"."generations" VALUES (1, '30小时电池续航的无线耳机', 'LLM', '2025-05-17 16:07:25.83502+08', 1);
INSERT INTO "public"."generations" VALUES (2, '客户对延迟发货不满', 'RAG', '2025-05-23 16:07:25.83502+08', 1);
INSERT INTO "public"."generations" VALUES (3, '用户认证端点', 'LLM', '2025-05-06 16:07:25.83502+08', 2);
INSERT INTO "public"."generations" VALUES (4, 'AI反叛故事开头', 'LLM', '2025-05-27 16:07:25.83502+08', 3);
INSERT INTO "public"."generations" VALUES (5, '第三季度销售数据：地区和产品', 'RAG', '2025-05-30 16:07:25.83502+08', 4);
INSERT INTO "public"."generations" VALUES (6, '30天健身挑战促销', 'LLM', '2025-06-01 16:07:25.83502+08', 1);

-- ----------------------------
-- Table structure for modelproviders
-- ----------------------------
DROP TABLE IF EXISTS "public"."modelproviders";
CREATE TABLE "public"."modelproviders" (
  "provider_id" int4 NOT NULL DEFAULT nextval('modelproviders_provider_id_seq'::regclass),
  "provider_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "base_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "api_key" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."modelproviders"."provider_name" IS '名称（OpenAIAnthropic等）';
COMMENT ON COLUMN "public"."modelproviders"."base_url" IS 'API基础地址';
COMMENT ON COLUMN "public"."modelproviders"."api_key" IS '加密存储的系统级API密钥';

-- ----------------------------
-- Records of modelproviders
-- ----------------------------
INSERT INTO "public"."modelproviders" VALUES (1, 'OpenAI', 'https://api.openai.com/v1', 'encrypted_sk-abc123xyz456');
INSERT INTO "public"."modelproviders" VALUES (2, 'Anthropic', 'https://api.anthropic.com/v1', 'encrypted_sk-ant-claude-789');
INSERT INTO "public"."modelproviders" VALUES (3, 'Google', 'https://generativelanguage.googleapis.com/v1', 'encrypted_gl-ai-key-101');
INSERT INTO "public"."modelproviders" VALUES (4, 'Mistral', 'https://api.mistral.ai/v1', 'encrypted_mistral-key-202');
INSERT INTO "public"."modelproviders" VALUES (5, 'HuggingFace', 'https://api-inference.huggingface.co', 'encrypted_hf-key-303');

-- ----------------------------
-- Table structure for optimizationconfigs
-- ----------------------------
DROP TABLE IF EXISTS "public"."optimizationconfigs";
CREATE TABLE "public"."optimizationconfigs" (
  "config_id" int4 NOT NULL DEFAULT nextval('optimizationconfigs_config_id_seq'::regclass),
  "optimization_model" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "role_enhancement" text COLLATE "pg_catalog"."default",
  "example_enhancement" text COLLATE "pg_catalog"."default",
  "cot_enabled" bool NOT NULL,
  "chain_decomposition" bool NOT NULL,
  "reflection_enabled" bool NOT NULL,
  "prompt_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."optimizationconfigs"."optimization_model" IS '使用的优化模型';
COMMENT ON COLUMN "public"."optimizationconfigs"."role_enhancement" IS '角色强化配置';
COMMENT ON COLUMN "public"."optimizationconfigs"."example_enhancement" IS '示例增强配置';
COMMENT ON COLUMN "public"."optimizationconfigs"."cot_enabled" IS '是否启用思维链';
COMMENT ON COLUMN "public"."optimizationconfigs"."chain_decomposition" IS '是否启用链式分解';
COMMENT ON COLUMN "public"."optimizationconfigs"."reflection_enabled" IS '是否启用反思迭代';
COMMENT ON COLUMN "public"."optimizationconfigs"."prompt_id" IS '关联提示词';

-- ----------------------------
-- Records of optimizationconfigs
-- ----------------------------
INSERT INTO "public"."optimizationconfigs" VALUES (1, 'gpt-4', '资深营销文案撰稿人', '电子产品示例产品描述', 't', 't', 'f', 1);
INSERT INTO "public"."optimizationconfigs" VALUES (2, 'claude-2', '客户支持专员', '退款回应模板', 'f', 'f', 't', 2);
INSERT INTO "public"."optimizationconfigs" VALUES (3, 'gpt-4-turbo', '技术文档撰写人', 'OpenAPI规范示例', 't', 't', 't', 3);
INSERT INTO "public"."optimizationconfigs" VALUES (4, 'gemini-pro', '屡获殊荣的科幻作家', '经典科幻小说开场白', 'f', 't', 'f', 4);
INSERT INTO "public"."optimizationconfigs" VALUES (5, 'mistral-large', '社交媒体策略师', '健身产品高转化广告文案', 't', 'f', 't', 6);

-- ----------------------------
-- Table structure for promptfolders
-- ----------------------------
DROP TABLE IF EXISTS "public"."promptfolders";
CREATE TABLE "public"."promptfolders" (
  "id" int4 NOT NULL DEFAULT nextval('promptfolders_id_seq'::regclass),
  "folder_id" int4 NOT NULL,
  "prompt_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."promptfolders"."folder_id" IS '文件夹ID';
COMMENT ON COLUMN "public"."promptfolders"."prompt_id" IS '提示词ID';

-- ----------------------------
-- Records of promptfolders
-- ----------------------------
INSERT INTO "public"."promptfolders" VALUES (59, 1, 1);
INSERT INTO "public"."promptfolders" VALUES (60, 6, 1);
INSERT INTO "public"."promptfolders" VALUES (61, 2, 2);
INSERT INTO "public"."promptfolders" VALUES (62, 3, 3);
INSERT INTO "public"."promptfolders" VALUES (63, 4, 4);
INSERT INTO "public"."promptfolders" VALUES (64, 5, 5);
INSERT INTO "public"."promptfolders" VALUES (65, 1, 6);
INSERT INTO "public"."promptfolders" VALUES (66, 6, 6);

-- ----------------------------
-- Table structure for prompts
-- ----------------------------
DROP TABLE IF EXISTS "public"."prompts";
CREATE TABLE "public"."prompts" (
  "prompt_id" int4 NOT NULL DEFAULT nextval('prompts_prompt_id_seq'::regclass),
  "original_content" text COLLATE "pg_catalog"."default" NOT NULL,
  "optimized_content" text COLLATE "pg_catalog"."default",
  "usage_count" int4 NOT NULL DEFAULT 0,
  "is_shared" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "session_id" int4 NOT NULL,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."prompts"."original_content" IS '原始提示词内容';
COMMENT ON COLUMN "public"."prompts"."optimized_content" IS '优化后内容';
COMMENT ON COLUMN "public"."prompts"."usage_count" IS '使用次数';
COMMENT ON COLUMN "public"."prompts"."is_shared" IS '是否分享到社区';
COMMENT ON COLUMN "public"."prompts"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."prompts"."session_id" IS '所属会话';
COMMENT ON COLUMN "public"."prompts"."user_id" IS '创建用户';

-- ----------------------------
-- Records of prompts
-- ----------------------------
INSERT INTO "public"."prompts" VALUES (1, '撰写产品描述', '您是一位资深的营销文案撰稿人。为我们的新款无线耳机撰写引人入胜的产品描述，重点关注电池续航和音质。使用有说服力的语言并突出关键特性。', 12, 't', '2025-05-16 16:07:25.830374+08', 1, 1);
INSERT INTO "public"."prompts" VALUES (2, '客户退款回应', '作为客户支持专员，为客户起草一份因产品不满意而请求退款的专业电子邮件回复。表达同理心，同时解释政策。', 8, 'f', '2025-05-22 16:07:25.830374+08', 2, 1);
INSERT INTO "public"."prompts" VALUES (3, '生成API文档', '担任技术作家。为我们的RESTful API端点创建全面的文档。包括参数、示例请求和响应格式。使用清晰简洁的语言。', 15, 't', '2025-05-04 16:07:25.830374+08', 3, 2);
INSERT INTO "public"."prompts" VALUES (4, '科幻故事开头', '您是一位屡获殊荣的科幻作家。为一部设定在2150年、由AI统治社会的故事撰写一个引人入胜的开头段落。介绍一个对系统产生怀疑的内心冲突的主人公。', 5, 't', '2025-05-26 16:07:25.830374+08', 4, 3);
INSERT INTO "public"."prompts" VALUES (5, '销售数据分析', '作为数据分析师，解读月度销售数据并识别关键趋势。在简洁的报告格式中提供见解和可操作的建议。', 7, 'f', '2025-05-29 16:07:25.830374+08', 5, 4);
INSERT INTO "public"."prompts" VALUES (6, '社交媒体广告文案', '为我们健身应用的推出撰写3个Facebook广告变体。目标受众：28-45岁的忙碌专业人士。关注节省时间的好处和可衡量的结果。', 9, 't', '2025-05-31 16:07:25.830374+08', 1, 1);

-- ----------------------------
-- Table structure for prompttags
-- ----------------------------
DROP TABLE IF EXISTS "public"."prompttags";
CREATE TABLE "public"."prompttags" (
  "id" int4 NOT NULL DEFAULT nextval('prompttags_id_seq'::regclass),
  "prompt_id" int4 NOT NULL,
  "tag_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."prompttags"."prompt_id" IS '提示词ID';
COMMENT ON COLUMN "public"."prompttags"."tag_id" IS '标签ID';

-- ----------------------------
-- Records of prompttags
-- ----------------------------
INSERT INTO "public"."prompttags" VALUES (77, 1, 1);
INSERT INTO "public"."prompttags" VALUES (78, 1, 8);
INSERT INTO "public"."prompttags" VALUES (79, 1, 6);
INSERT INTO "public"."prompttags" VALUES (80, 2, 2);
INSERT INTO "public"."prompttags" VALUES (81, 3, 3);
INSERT INTO "public"."prompttags" VALUES (82, 3, 7);
INSERT INTO "public"."prompttags" VALUES (83, 4, 4);
INSERT INTO "public"."prompttags" VALUES (84, 4, 6);
INSERT INTO "public"."prompttags" VALUES (85, 5, 5);
INSERT INTO "public"."prompttags" VALUES (86, 6, 1);
INSERT INTO "public"."prompttags" VALUES (87, 6, 6);

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."roles";
CREATE TABLE "public"."roles" (
  "role_id" int4 NOT NULL DEFAULT nextval('roles_role_id_seq'::regclass),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "content" text COLLATE "pg_catalog"."default" NOT NULL,
  "is_preset" bool NOT NULL DEFAULT false,
  "user_id" int4
)
;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO "public"."roles" VALUES (1, '营销专家', '专业营销内容创作', '您是一位拥有10年以上经验的营销专家，擅长为科技产品创作引人入胜的内容。', 't', NULL);
INSERT INTO "public"."roles" VALUES (2, '技术作家', 'API和文档专家', '您是一位技术作家，擅长为开发人员创作清晰、简洁的文档。', 't', NULL);
INSERT INTO "public"."roles" VALUES (3, '电商专家', '在线销售内容定制角色', '您专注于为电商平台创作有说服力的产品描述。', 'f', 1);
INSERT INTO "public"."roles" VALUES (4, '科幻小说作者', '科幻创意写作', '您创作引人入胜的科幻故事，具有深入的世界构建和复杂的角色。', 'f', 3);
INSERT INTO "public"."roles" VALUES (5, '数据分析师', '商业智能报告', '您将原始数据转化为可操作的商业见解，并提供清晰的可视化。', 'f', 4);

-- ----------------------------
-- Table structure for sessions
-- ----------------------------
DROP TABLE IF EXISTS "public"."sessions";
CREATE TABLE "public"."sessions" (
  "session_id" int4 NOT NULL DEFAULT nextval('sessions_session_id_seq'::regclass),
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."sessions"."title" IS '会话标题';
COMMENT ON COLUMN "public"."sessions"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."sessions"."user_id" IS '关联用户';

-- ----------------------------
-- Records of sessions
-- ----------------------------
INSERT INTO "public"."sessions" VALUES (1, '营销活动优化', '2025-05-14 16:07:25.829648+08', 1);
INSERT INTO "public"."sessions" VALUES (2, '客户支持脚本', '2025-05-19 16:07:25.829648+08', 1);
INSERT INTO "public"."sessions" VALUES (3, 'API文档生成器', '2025-04-29 16:07:25.829648+08', 2);
INSERT INTO "public"."sessions" VALUES (4, '创意写作提示', '2025-05-24 16:07:25.829648+08', 3);
INSERT INTO "public"."sessions" VALUES (5, '商业分析报告', '2025-05-27 16:07:25.829648+08', 4);

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS "public"."tags";
CREATE TABLE "public"."tags" (
  "tag_id" int4 NOT NULL DEFAULT nextval('tags_tag_id_seq'::regclass),
  "tag_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "user_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."tags"."tag_name" IS '标签名称（需唯一约束 per user）';
COMMENT ON COLUMN "public"."tags"."user_id" IS '所属用户';

-- ----------------------------
-- Records of tags
-- ----------------------------
INSERT INTO "public"."tags" VALUES (1, '营销', 1);
INSERT INTO "public"."tags" VALUES (2, '客户支持', 1);
INSERT INTO "public"."tags" VALUES (3, '技术', 2);
INSERT INTO "public"."tags" VALUES (4, '创意', 3);
INSERT INTO "public"."tags" VALUES (5, '分析', 4);
INSERT INTO "public"."tags" VALUES (6, '热门', 2);
INSERT INTO "public"."tags" VALUES (7, '精选', 3);
INSERT INTO "public"."tags" VALUES (8, '电商', 1);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "user_id" int4 NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
  "email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "password_hash" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "role" varchar(5) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'user'::character varying,
  "avatar_url" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."users"."email" IS '注册邮箱';
COMMENT ON COLUMN "public"."users"."password_hash" IS '加密后的密码（建议使用bcrypt）';
COMMENT ON COLUMN "public"."users"."role" IS '用户角色';
COMMENT ON COLUMN "public"."users"."avatar_url" IS '头像存储路径';
COMMENT ON COLUMN "public"."users"."created_at" IS '注册时间';

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES (1, 'emma.tech@example.com', '$2b$12$3kYbZ4GfMx9JcW8VdXq5/.h2XzR7T6YpBq', '用户', 'https://avatarhub.com/emma_profile.jpg', '2025-05-04 16:07:25.827945+08');
INSERT INTO "public"."users" VALUES (2, 'alex.dev@startup.io', '$2b$12$7fGtH8Dv2KpL3sQwE9rF0.c1YzA4B6C7D', '管理员', 'https://avatarhub.com/alex_avatar.png', '2025-04-19 16:07:25.827945+08');
INSERT INTO "public"."users" VALUES (3, 'sarah.writer@creative.com', '$2b$12$9hJkLmNpOqR2sT4uV6wX8.y0Z1A3B4C5D', '用户', NULL, '2025-05-19 16:07:25.827945+08');
INSERT INTO "public"."users" VALUES (4, 'mark.analyst@business.org', '$2b$12$1aB2cD3eF4gH5iJ6kL7m8.n9O0P1Q2R3S', '用户', 'https://avatarhub.com/mark_profile.jpg', '2025-05-24 16:07:25.827945+08');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."aerich_id_seq"
OWNED BY "public"."aerich"."id";
SELECT setval('"public"."aerich_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."apicalls_call_id_seq"
OWNED BY "public"."apicalls"."call_id";
SELECT setval('"public"."apicalls_call_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."apikeys_key_id_seq"
OWNED BY "public"."apikeys"."key_id";
SELECT setval('"public"."apikeys_key_id_seq"', 9, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."communityinteractions_interaction_id_seq"
OWNED BY "public"."communityinteractions"."interaction_id";
SELECT setval('"public"."communityinteractions_interaction_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."examples_example_id_seq"
OWNED BY "public"."examples"."example_id";
SELECT setval('"public"."examples_example_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."folders_folder_id_seq"
OWNED BY "public"."folders"."folder_id";
SELECT setval('"public"."folders_folder_id_seq"', 8, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."generations_generation_id_seq"
OWNED BY "public"."generations"."generation_id";
SELECT setval('"public"."generations_generation_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."modelproviders_provider_id_seq"
OWNED BY "public"."modelproviders"."provider_id";
SELECT setval('"public"."modelproviders_provider_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."optimizationconfigs_config_id_seq"
OWNED BY "public"."optimizationconfigs"."config_id";
SELECT setval('"public"."optimizationconfigs_config_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."promptfolders_id_seq"
OWNED BY "public"."promptfolders"."id";
SELECT setval('"public"."promptfolders_id_seq"', 66, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."prompts_prompt_id_seq"
OWNED BY "public"."prompts"."prompt_id";
SELECT setval('"public"."prompts_prompt_id_seq"', 10, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."prompttags_id_seq"
OWNED BY "public"."prompttags"."id";
SELECT setval('"public"."prompttags_id_seq"', 87, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."roles_role_id_seq"
OWNED BY "public"."roles"."role_id";
SELECT setval('"public"."roles_role_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."sessions_session_id_seq"
OWNED BY "public"."sessions"."session_id";
SELECT setval('"public"."sessions_session_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."tags_tag_id_seq"
OWNED BY "public"."tags"."tag_id";
SELECT setval('"public"."tags_tag_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_user_id_seq"
OWNED BY "public"."users"."user_id";
SELECT setval('"public"."users_user_id_seq"', 4, true);

-- ----------------------------
-- Primary Key structure for table aerich
-- ----------------------------
ALTER TABLE "public"."aerich" ADD CONSTRAINT "aerich_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table apicalls
-- ----------------------------
ALTER TABLE "public"."apicalls" ADD CONSTRAINT "apicalls_pkey" PRIMARY KEY ("call_id");

-- ----------------------------
-- Uniques structure for table apikeys
-- ----------------------------
ALTER TABLE "public"."apikeys" ADD CONSTRAINT "apikeys_api_key_key" UNIQUE ("api_key");

-- ----------------------------
-- Primary Key structure for table apikeys
-- ----------------------------
ALTER TABLE "public"."apikeys" ADD CONSTRAINT "apikeys_pkey" PRIMARY KEY ("key_id");

-- ----------------------------
-- Primary Key structure for table communityinteractions
-- ----------------------------
ALTER TABLE "public"."communityinteractions" ADD CONSTRAINT "communityinteractions_pkey" PRIMARY KEY ("interaction_id");

-- ----------------------------
-- Primary Key structure for table examples
-- ----------------------------
ALTER TABLE "public"."examples" ADD CONSTRAINT "examples_pkey" PRIMARY KEY ("example_id");

-- ----------------------------
-- Primary Key structure for table folders
-- ----------------------------
ALTER TABLE "public"."folders" ADD CONSTRAINT "folders_pkey" PRIMARY KEY ("folder_id");

-- ----------------------------
-- Primary Key structure for table generations
-- ----------------------------
ALTER TABLE "public"."generations" ADD CONSTRAINT "generations_pkey" PRIMARY KEY ("generation_id");

-- ----------------------------
-- Primary Key structure for table modelproviders
-- ----------------------------
ALTER TABLE "public"."modelproviders" ADD CONSTRAINT "modelproviders_pkey" PRIMARY KEY ("provider_id");

-- ----------------------------
-- Primary Key structure for table optimizationconfigs
-- ----------------------------
ALTER TABLE "public"."optimizationconfigs" ADD CONSTRAINT "optimizationconfigs_pkey" PRIMARY KEY ("config_id");

-- ----------------------------
-- Uniques structure for table promptfolders
-- ----------------------------
ALTER TABLE "public"."promptfolders" ADD CONSTRAINT "uid_promptfolde_prompt__3b3cdb" UNIQUE ("prompt_id", "folder_id");

-- ----------------------------
-- Primary Key structure for table promptfolders
-- ----------------------------
ALTER TABLE "public"."promptfolders" ADD CONSTRAINT "promptfolders_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table prompts
-- ----------------------------
ALTER TABLE "public"."prompts" ADD CONSTRAINT "prompts_pkey" PRIMARY KEY ("prompt_id");

-- ----------------------------
-- Uniques structure for table prompttags
-- ----------------------------
ALTER TABLE "public"."prompttags" ADD CONSTRAINT "uid_prompttags_prompt__4814ac" UNIQUE ("prompt_id", "tag_id");

-- ----------------------------
-- Primary Key structure for table prompttags
-- ----------------------------
ALTER TABLE "public"."prompttags" ADD CONSTRAINT "prompttags_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_pkey" PRIMARY KEY ("role_id");

-- ----------------------------
-- Primary Key structure for table sessions
-- ----------------------------
ALTER TABLE "public"."sessions" ADD CONSTRAINT "sessions_pkey" PRIMARY KEY ("session_id");

-- ----------------------------
-- Primary Key structure for table tags
-- ----------------------------
ALTER TABLE "public"."tags" ADD CONSTRAINT "tags_pkey" PRIMARY KEY ("tag_id");

-- ----------------------------
-- Uniques structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_email_key" UNIQUE ("email");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("user_id");

-- ----------------------------
-- Foreign Keys structure for table apicalls
-- ----------------------------
ALTER TABLE "public"."apicalls" ADD CONSTRAINT "apicalls_prompt_id_fkey" FOREIGN KEY ("prompt_id") REFERENCES "public"."prompts" ("prompt_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."apicalls" ADD CONSTRAINT "apicalls_provider_id_fkey" FOREIGN KEY ("provider_id") REFERENCES "public"."modelproviders" ("provider_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."apicalls" ADD CONSTRAINT "apicalls_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table apikeys
-- ----------------------------
ALTER TABLE "public"."apikeys" ADD CONSTRAINT "apikeys_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table communityinteractions
-- ----------------------------
ALTER TABLE "public"."communityinteractions" ADD CONSTRAINT "communityinteractions_prompt_id_fkey" FOREIGN KEY ("prompt_id") REFERENCES "public"."prompts" ("prompt_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."communityinteractions" ADD CONSTRAINT "communityinteractions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table examples
-- ----------------------------
ALTER TABLE "public"."examples" ADD CONSTRAINT "examples_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table folders
-- ----------------------------
ALTER TABLE "public"."folders" ADD CONSTRAINT "folders_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table generations
-- ----------------------------
ALTER TABLE "public"."generations" ADD CONSTRAINT "generations_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table optimizationconfigs
-- ----------------------------
ALTER TABLE "public"."optimizationconfigs" ADD CONSTRAINT "optimizationconfigs_prompt_id_fkey" FOREIGN KEY ("prompt_id") REFERENCES "public"."prompts" ("prompt_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table promptfolders
-- ----------------------------
ALTER TABLE "public"."promptfolders" ADD CONSTRAINT "promptfolders_folder_id_fkey" FOREIGN KEY ("folder_id") REFERENCES "public"."folders" ("folder_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."promptfolders" ADD CONSTRAINT "promptfolders_prompt_id_fkey" FOREIGN KEY ("prompt_id") REFERENCES "public"."prompts" ("prompt_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table prompts
-- ----------------------------
ALTER TABLE "public"."prompts" ADD CONSTRAINT "prompts_session_id_fkey" FOREIGN KEY ("session_id") REFERENCES "public"."sessions" ("session_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."prompts" ADD CONSTRAINT "prompts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table prompttags
-- ----------------------------
ALTER TABLE "public"."prompttags" ADD CONSTRAINT "prompttags_prompt_id_fkey" FOREIGN KEY ("prompt_id") REFERENCES "public"."prompts" ("prompt_id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."prompttags" ADD CONSTRAINT "prompttags_tag_id_fkey" FOREIGN KEY ("tag_id") REFERENCES "public"."tags" ("tag_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table sessions
-- ----------------------------
ALTER TABLE "public"."sessions" ADD CONSTRAINT "sessions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table tags
-- ----------------------------
ALTER TABLE "public"."tags" ADD CONSTRAINT "tags_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("user_id") ON DELETE CASCADE ON UPDATE NO ACTION;
