from fastapi import APIRouter, Depends, HTTPException, status, Body
from models import *
from pydantic import BaseModel
from typing import List, Optional
from tortoise.transactions import in_transaction
from tortoise.exceptions import DoesNotExist
from app.core.security import get_current_active_user
from llm.llm_client import *
from llm.config import APIConfig
from llm.optimization import apply_role_enhancement

optimize_api = APIRouter()

# ---- 基础模型定义 ----
class APIConfig_temp(BaseModel):
    api_key: str = "sk-QGEkpTzYOdG6jkOtTR2UIpR09XINClFMG77POafAefkknppB"
    model: str = "gpt-3.5-turbo"
    api_base: str = "https://api.chatanywhere.tech"
    api_type: str = "openai"

class OptimizationConfig(BaseModel):
    optimization_model: str = "gpt-4"  # 默认优化模型
    role_enhancement: Optional[str] = None  # 角色强化配置
    example_enhancement: Optional[str] = None  # 示例增强配置
    cot_enabled: bool = False  # 是否启用思维链
    chain_decomposition: bool = False  # 是否启用链式分解
    reflection_enabled: bool = False  # 是否启用反思迭代

class OptimizationRequest(BaseModel):
    original_content: str  # 原始提示词内容
    config: OptimizationConfig = OptimizationConfig()  # 优化配置

class TestRequest(BaseModel):
    test_input: str  # 测试输入内容
    use_original: bool = True  # 是否测试原始提示词
    use_optimized: bool = True  # 是否测试优化后提示词

class OptimizationResult(BaseModel):
    optimized_content: str  # 优化后的提示词内容
    config: OptimizationConfig  # 使用的优化配置

class TestResult(BaseModel):
    original_result: Optional[str] = None  # 原始提示词测试结果
    optimized_result: Optional[str] = None  # 优化后提示词测试结果

# ---- 角色和示例管理 ----
class RoleExampleBase(BaseModel):
    name: str
    description: str
    content: str

class RoleExampleCreate(RoleExampleBase):
    is_preset: bool = False  # 是否为系统预置

class RoleExampleResponse(RoleExampleBase):
    id: int
    is_preset: bool

@optimize_api.get("/preset-roles", response_model=List[RoleExampleResponse])
async def get_preset_roles():
    """获取系统预置角色列表"""
    # 查询所有系统预置角色
    roles = await Roles.filter(is_preset=True).all()
    
    # 将 Roles 对象转换为 RoleExampleResponse 模型
    return [
        RoleExampleResponse(
            id=role.role_id,
            name=role.name,
            description=role.description,
            content=role.content,
            is_preset=role.is_preset
        )
        for role in roles
    ]

@optimize_api.get("/user-roles", response_model=List[RoleExampleResponse])
async def get_user_roles(user_id: Users = Depends(get_current_active_user)):
    """获取当前用户的自定义角色"""
    roles = await Roles.filter(user_id=user_id).all()
    
    return [
        RoleExampleResponse(
            id=role.role_id,
            name=role.name,
            description=role.description,
            content=role.content,
            is_preset=role.is_preset
        )
        for role in roles
    ]

@optimize_api.get("/preset-examples", response_model=List[RoleExampleResponse])
async def get_preset_examples():
    """获取系统预置示例列表"""
    # 查询所有系统预置示例
    examples = await Examples.filter(is_preset=True).all()
    
    # 将 Examples 对象转换为 RoleExampleResponse 模型
    example_responses = [
        RoleExampleResponse(
            id=example.example_id,  # 将 example_id 映射为 id
            name=example.name,
            description=example.description,
            content=example.content,
            is_preset=example.is_preset
        )
        for example in examples
    ]
    
    return example_responses

@optimize_api.post("/custom-roles", response_model=RoleExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_role(
    role: RoleExampleCreate,
    user_id: Users = Depends(get_current_active_user)
):
    """创建自定义角色"""
    role_obj = await Roles.create(
        user_id=user_id,
        **role.model_dump()
    )
    return role_obj

@optimize_api.post("/custom-examples", response_model=RoleExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_example(
    example: RoleExampleCreate,
    user_id: Users = Depends(get_current_active_user)
):
    """创建自定义示例"""
    example_obj = await Examples.create(
        user_id=user_id,
        **example.model_dump()
    )
    return example_obj

# ---- 核心优化接口 ----
@optimize_api.post("/optimize", response_model=OptimizationResult)
async def optimize_prompt(
    request: OptimizationRequest,
    api_config: APIConfig_temp = Body(default=APIConfig_temp()),
    user_id: Users = Depends(get_current_active_user)
):
    """
    优化提示词
    - 接收原始提示词和优化配置
    - 返回优化后的提示词内容
    """

    # 这里会调用实际的优化逻辑（伪代码）
    optimized_content = await apply_optimization(
        request.original_content,
        request.config,
        api_config,
        user_id  # 传递用户ID
    )
    
    return OptimizationResult(
        optimized_content=optimized_content,
        config=request.config
    )

@optimize_api.post("/test", response_model=TestResult)
async def test_prompt(
    original_content: str,
    optimized_content: str,
    test_request: TestRequest,
    user_id: Users = Depends(get_current_active_user)
):
    """
    测试提示词效果
    - 接收原始提示词和优化后提示词
    - 接收测试输入内容
    - 返回原始和优化后的生成结果
    """
    results = TestResult()
    
    # 测试原始提示词
    if test_request.use_original:
        results.original_result = generate_with_prompt(
            prompt=original_content,
            input=test_request.test_input
        )
    
    # 测试优化后提示词
    if test_request.use_optimized:
        results.optimized_result = generate_with_prompt(
            prompt=optimized_content,
            input=test_request.test_input
        )
    
    return results

# ---- 优化配置管理 ----
@optimize_api.post("/prompts/{prompt_id}/config", response_model=OptimizationConfig)
async def save_optimization_config(
    prompt_id: int,
    config: OptimizationConfig,
    user_id: Users = Depends(get_current_active_user)
):
    """保存优化配置到提示词"""
    # 验证提示词存在且属于当前用户
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, user_id=user_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权操作"
        )
    
    # 创建或更新优化配置
    opt_config, created = await OptimizationConfigs.update_or_create(
        prompt_id=prompt_id,
        defaults=config.model_dump()
    )
    
    return opt_config

@optimize_api.get("/prompts/{prompt_id}/config", response_model=OptimizationConfig)
async def get_optimization_config(
    prompt_id: int,
    user_id: Users = Depends(get_current_active_user)
):
    """获取提示词的优化配置"""
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, user_id=user_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权操作"
        )
    
    config = await OptimizationConfigs.get_or_none(prompt_id=prompt_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到优化配置"
        )
    
    return config

# ---- 伪实现函数 ----
async def apply_optimization(
    original_content: str, 
    config: OptimizationConfig, 
    api_config_in: APIConfig_temp,
    user_id: int  # 添加用户ID参数
) -> str:
    """应用优化设置生成优化后提示词"""
    optimized = original_content
    
    # 1. 角色强化
    if config.role_enhancement:
        optimized = await apply_role_enhancement(
            optimized, 
            config.role_enhancement,
            user_id
        )
    
    # 2. 示例增强
    if config.example_enhancement:
        # example = get_example_content(config.example_enhancement)
        # optimized = f"{optimized}\n\nExamples:\n{example}"
        pass
    
    # 3. 思维链(CoT)
    if config.cot_enabled:
        optimized += "\n\n请一步步思考，详细解释你的推理过程。"
    
    # 4. 链式分解（简化实现）
    if config.chain_decomposition:
        # optimized = decompose_prompt(optimized)
        pass
    
    # 5. 反思式迭代（简化实现）
    if config.reflection_enabled:
        optimized += "\n\nAfter generating, review your response for accuracy, completeness, and logical consistency. Make necessary corrections."
    
    # 6. 通用优化 (调用LLM进行最终优化)
    api_config = APIConfig(
        model=api_config_in.model,
        api_base=api_config_in.api_base,
        api_type=api_config_in.api_type,
        api_key=api_config_in.api_key
    )
    
    # 调用LLM进行通用优化
    optimized = await optimize_prompt_in_llm(
        original_prompt=optimized,
        config=api_config
    )

    return optimized


def generate_with_prompt(prompt: str, input: str) -> str:
    """伪代码：使用提示词生成内容"""
    # 实际项目中会调用AI模型API
    return f"Generated response for input: {input} using prompt: {prompt[:50]}..."

