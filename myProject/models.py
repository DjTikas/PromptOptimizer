from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_id = fields.IntField(pk=True)  # 主键
    email = fields.CharField(max_length=255, unique=True, description="注册邮箱")
    password_hash = fields.CharField(max_length=255, description="加密后的密码（建议使用bcrypt）")
    role = fields.CharField(max_length=5, description="用户角色", default="user")
    avatar_url = fields.CharField(max_length=255, description="头像存储路径", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="注册时间")

class ApiKeys(Model):
    key_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="api_keys", description="关联用户")
    api_key = fields.CharField(max_length=255, unique=True, description="加密存储的API密钥")
    description = fields.CharField(max_length=255, description="描述", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    is_active = fields.BooleanField(default=True, description="是否启用")

class Sessions(Model):
    session_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="sessions", description="关联用户")
    title = fields.CharField(max_length=100, description="会话标题")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

class Prompts(Model):
    prompt_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="prompts", description="创建用户")
    session = fields.ForeignKeyField("models.Sessions", related_name="prompts", description="所属会话")
    original_content = fields.TextField(description="原始提示词内容")
    optimized_content = fields.TextField(description="优化后内容", null=True)
    usage_count = fields.IntField(default=0, description="使用次数")
    is_shared = fields.BooleanField(default=False, description="是否分享到社区")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

class Tags(Model):
    tag_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="tags", description="所属用户")
    tag_name = fields.CharField(max_length=50, description="标签名称（需唯一约束 per user）")

class PromptTags(Model):
    prompt = fields.ForeignKeyField("models.Prompts", related_name="tags", description="提示词ID")
    tag = fields.ForeignKeyField("models.Tags", related_name="prompts", description="标签ID")

    class Meta:
        unique_together = (("prompt", "tag"),)

class Folders(Model):
    folder_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="folders", description="所属用户")
    folder_name = fields.CharField(max_length=100, description="文件夹名称")

class PromptFolders(Model):
    prompt = fields.ForeignKeyField("models.Prompts", related_name="folders", description="提示词ID")
    folder = fields.ForeignKeyField("models.Folders", related_name="prompts", description="文件夹ID")

    class Meta:
        unique_together = (("prompt", "folder"),)

class OptimizationConfigs(Model):
    config_id = fields.IntField(pk=True)  # 主键
    prompt = fields.ForeignKeyField("models.Prompts", related_name="optimization_configs", description="关联提示词")
    optimization_model = fields.CharField(max_length=50, description="使用的优化模型")
    role_enhancement = fields.TextField(description="角色强化配置", null=True)
    example_enhancement = fields.TextField(description="示例增强配置", null=True)
    cot_enabled = fields.BooleanField(description="是否启用思维链")
    chain_decomposition = fields.BooleanField(description="是否启用链式分解")
    reflection_enabled = fields.BooleanField(description="是否启用反思迭代")

class CommunityInteractions(Model):
    interaction_id = fields.IntField(pk=True)  # 主键
    prompt = fields.ForeignKeyField("models.Prompts", related_name="community_interactions", description="关联提示词")
    user = fields.ForeignKeyField("models.Users", related_name="community_interactions", description="操作用户")
    action_type = fields.CharField(max_length=10, description="互动类型", choices=["like", "collect", "use"])
    created_at = fields.DatetimeField(auto_now_add=True, description="操作时间")

class Generations(Model):
    generation_id = fields.IntField(pk=True)  # 主键
    user = fields.ForeignKeyField("models.Users", related_name="generations", description="用户ID")
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
    user = fields.ForeignKeyField("models.Users", related_name="api_calls", description="用户ID")
    provider = fields.ForeignKeyField("models.ModelProviders", related_name="api_calls", description="模型提供商")
    prompt = fields.ForeignKeyField("models.Prompts", related_name="api_calls", description="关联提示词")
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