from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum
from datetime import datetime
from pytz import utc

# 1. 角色枚举
class UserRole(str, Enum):
    user  = "user"
    admin = "admin"

# 2. Users 模型
class Users(Model):
    user_id      = fields.IntField(pk=True)
    email        = fields.CharField(max_length=255, unique=True, description="注册邮箱")
    password_hash= fields.CharField(max_length=255, description="加密后的密码")
    role         = fields.CharEnumField(enum_type=UserRole, default=UserRole.user, description="用户角色")
    avatar_url   = fields.CharField(max_length=255, null=True, description="头像存储路径")
    created_at   = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(utc), description="注册时间(UTC)")

    class Meta:
        table = "users"

    def __str__(self):
        return self.email

# 3. Pydantic 模型
User_Pydantic = pydantic_model_creator(
    Users, name="User", exclude=("password_hash",)
)
UserIn_Pydantic = pydantic_model_creator(
    Users,
    name="UserIn",
    exclude_readonly=True,
    exclude=("created_at", "user_id"),
)

class APIKeys(Model):
    key_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.Users", 
        related_name="api_keys",
        on_delete=fields.CASCADE
    )
    api_key = fields.CharField(max_length=255, unique=False)
    api_name = fields.CharField(max_length=255, null=True)  # 原description字段
    api_address = fields.CharField(max_length=255, null=True)  # 新增API地址字段
    api_type = fields.CharField(max_length=50, null=True)    # 新增API类型字段
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "api_keys"

class Sessions(Model):
    session_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="sessions", description="关联用户", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=100, description="会话标题")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

class Prompts(Model):
    prompt_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="prompts", description="创建用户", on_delete=fields.CASCADE)
    session = fields.ForeignKeyField("models.Sessions", related_name="prompts", description="所属会话", on_delete=fields.CASCADE)
    original_content = fields.TextField(description="原始提示词内容")
    optimized_content = fields.TextField(description="优化后内容", null=True)
    usage_count = fields.IntField(default=0, description="使用次数")
    is_shared = fields.BooleanField(default=False, description="是否分享到社区")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    like_count = fields.IntField(default=0, description="点赞数量")  # 新增点赞数字段


# 创建包含点赞数的Pydantic模型
PromptsWithLikes_Pydantic = pydantic_model_creator(
    Prompts, 
    name="PromptsWithLikes",
    exclude=("user.password_hash",)  # 排除敏感字段
)



class Tags(Model):
    tag_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="tags", description="所属用户", on_delete=fields.CASCADE)
    tag_name = fields.CharField(max_length=50, description="标签名称（需唯一约束 per user）")

class PromptTags(Model):
    prompt = fields.ForeignKeyField("models.Prompts", related_name="tags", description="提示词ID", on_delete=fields.CASCADE)
    tag = fields.ForeignKeyField("models.Tags", related_name="prompts", description="标签ID", on_delete=fields.CASCADE)

    class Meta:
        unique_together = (("prompt", "tag"),)

class Folders(Model):
    folder_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="folders", description="所属用户", on_delete=fields.CASCADE)
    folder_name = fields.CharField(max_length=100, description="文件夹名称")

class PromptFolders(Model):
    prompt = fields.ForeignKeyField("models.Prompts", related_name="folders", description="提示词ID", on_delete=fields.CASCADE)
    folder = fields.ForeignKeyField("models.Folders", related_name="prompts", description="文件夹ID", on_delete=fields.CASCADE)

    class Meta:
        unique_together = (("prompt", "folder"),)

class OptimizationConfigs(Model):
    config_id = fields.IntField(pk=True)  # 主键
    prompt = fields.ForeignKeyField("models.Prompts", related_name="optimization_configs", description="关联提示词", on_delete=fields.CASCADE)
    optimization_model = fields.CharField(max_length=50, description="使用的优化模型")
    role_enhancement = fields.TextField(description="角色强化配置", null=True)
    example_enhancement = fields.TextField(description="示例增强配置", null=True)
    cot_enabled = fields.BooleanField(description="是否启用思维链")
    chain_decomposition = fields.BooleanField(description="是否启用链式分解")
    reflection_enabled = fields.BooleanField(description="是否启用反思迭代")

class CommunityInteractions(Model):
    id = fields.IntField(pk=True)  # 新增自增主键
    prompt = fields.ForeignKeyField(
        "models.Prompts", 
        related_name="likes",
        on_delete=fields.CASCADE
    )
    user = fields.ForeignKeyField(
        "models.Users", 
        related_name="liked_prompts",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "community_interactions"
        # 添加唯一约束
        unique_together = [("prompt", "user")]

    def __str__(self):
        return f"Interaction {self.id}"

class Generations(Model):
    generation_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="generations", description="用户ID", on_delete=fields.CASCADE)
    input_text = fields.TextField(description="用户输入的原始需求")
    generation_strategy = fields.CharField(max_length=3, description="生成策略", choices=["RAG", "LLM"])
    created_at = fields.DatetimeField(auto_now_add=True, description="生成时间")

class ModelProviders(Model):
    provider_id = fields.IntField(pk=True)  # 主键
    provider_name = fields.CharField(max_length=50, description="名称（OpenAIAnthropic等）")
    base_url = fields.CharField(max_length=255, description="API基础地址")
    api_key = fields.CharField(max_length=255, description="加密存储的系统级API密钥")

class ApiCalls(Model):
    call_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="api_calls", description="用户ID", on_delete=fields.CASCADE)
    provider = fields.ForeignKeyField("models.ModelProviders", related_name="api_calls", description="模型提供商", on_delete=fields.CASCADE)
    prompt = fields.ForeignKeyField("models.Prompts", related_name="api_calls", description="关联提示词", on_delete=fields.CASCADE)
    tokens_used = fields.IntField(description="消耗的token数量")
    cost = fields.DecimalField(max_digits=10, decimal_places=4, description="计算后的成本")
    called_at = fields.DatetimeField(auto_now_add=True, description="调用时间")

class Roles(Model):
    role_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="roles", null=True)  # null表示系统预置
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    content = fields.TextField()  # 角色内容模板
    is_preset = fields.BooleanField(default=False)  # 是否为系统预置

class Examples(Model):
    example_id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="examples", null=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    content = fields.TextField()  # 示例内容
    is_preset = fields.BooleanField(default=False)



# 创建 Pydantic 模型
Session_Pydantic = pydantic_model_creator(Sessions, name="Session")
Prompts_Pydantic = pydantic_model_creator(Prompts, name="Prompts")
CommunityInteractions_Pydantic = pydantic_model_creator(
    CommunityInteractions, 
    name="CommunityInteractions"
)
Tags_Pydantic = pydantic_model_creator(Tags, name="Tags")

APIKeys_Pydantic = pydantic_model_creator(APIKeys, name="APIKeys")
APIKeysIn_Pydantic = pydantic_model_creator(
    APIKeys, 
    name="APIKeysIn", 
    exclude_readonly=True,
    exclude=("created_at",)  # 排除自动生成的字段
)