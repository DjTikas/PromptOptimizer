from fastapi import APIRouter, Depends, HTTPException, status, Body
from models import *
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from tortoise.transactions import in_transaction
from tortoise.exceptions import DoesNotExist
from auth import get_current_user  # 假设有认证模块
from llm.llm_client import *
from llm.config import APIConfig
from llm.optimization import apply_role_enhancement
import time

optimize_new_api = APIRouter()


# ---- 基础模型定义 ----
class Cur_user(BaseModel):
    user_id: int
    email: str
    role: str
    avatar_url: str

class ModelConfig(BaseModel):
    api_key: str = "sk-QGEkpTzYOdG6jkOtTR2UIpR09XINClFMG77POafAefkknppB"
    model: str = "gpt-3.5-turbo"
    api_base: str = "https://api.chatanywhere.tech"
    api_type: str = "openai"

class RoleConfig(BaseModel):
    enabled: bool = False
    role_name: Optional[str] = None
    description: Optional[str] = None

class ExampleConfig(BaseModel):
    input: str
    output: str

class CotConfig(BaseModel):
    enabled: bool = False
    level: Literal["basic", "intermediate", "advanced", "creative", "scientific"] = "intermediate"
    custom_steps: Optional[List[str]] = None

class AdvancedConfig(BaseModel):
    temperature: float = Field(0.7, ge=0, le=1)
    max_tokens: int = Field(500, gt=0)
    top_p: float = Field(0.9, ge=0, le=1)

class OptimizeConfig(BaseModel):
    name: str
    model: Optional[ModelConfig] = None
    role: Optional[RoleConfig] = None
    examples: Optional[List[ExampleConfig]] = None
    exam_enabled: bool = False
    cot: Optional[CotConfig] = None
    advanced: Optional[AdvancedConfig] = None

class OptimizeRequest(BaseModel):
    original_prompt: str
    config: OptimizeConfig

# 响应模型，不知道拿来干嘛
class DebugInfo(BaseModel):
    full_instruction: str
    raw_response: str
    cost_estimation: float

class OptimizationStep(BaseModel):
    step_name: str
    input: str
    output: str

class OptimizationMetadata(BaseModel):
    model_used: str
    time_elapsed: float
    config_snapshot: dict
    steps: Optional[List[OptimizationStep]] = None

class OptimizeResponse(BaseModel):
    optimized_prompt: str
    optimization_id: str
    metadata: OptimizationMetadata
    debug_info: Optional[DebugInfo] = None



@optimize_new_api.post("/optimize", response_model=OptimizeResponse)
async def optimize_prompt(
    request: OptimizeRequest,
    user: Cur_user = Depends(get_current_user)
):
    """
    执行提示词优化
    """
    start_time = time.time()
    
    # 1. 构建优化指令
    instruction = build_optimization_instruction(request)
    
    api_config = APIConfig(
        model=request.config.model.model,
        api_base=request.config.model.api_base,
        api_type=request.config.model.api_type,
        api_key=request.config.model.api_key
    )

    # 调用LLM进行通用优化
    optimized_prompt = await optimize_prompt_in_llm(
        original_prompt=instruction,
        config=api_config
    )
    
    
    # 7. 构建响应
    response = OptimizeResponse(
        optimized_prompt=optimized_prompt,
        # optimization_id=history_id,
        optimization_id="dj test",
        metadata=OptimizationMetadata(
            model_used="dj:gpt-3.5",
            time_elapsed=time.time() - start_time,
            config_snapshot=request.config.model_dump()
        )
    )
    
    
    return response

def build_optimization_instruction(request: OptimizeRequest) -> str:
    """
    根据请求配置构建优化指令
    """
    template = """
    请将以下泛泛而谈的用户提示词转换为精准、具体的描述。根据以下要求重构用户提示：
    
    {role_block}
    {examples_block}
    {cot_block}
    
    ## 原始提示
    {original_prompt}
    
    ## 优化要求
    - 保持原始意图不变
    - 语言清晰专业
    - 输出仅包含优化后的提示词
    - 将抽象概念转换为具体要求，增加针对性和可操作性
    """
    
    # 角色扮演
    role_block = ""
    if request.config.role and request.config.role.enabled:
        role_block = f"角色设定：{request.config.role.role_name},{request.config.role.description}\n"
        # if request.config.role.preset_id:
        #     role = get_preset_role(request.config.role.preset_id)
        #     role_block = f"角色设定：{role['description']}\n"
        # elif request.config.role.description:
        #     role_block = f"角色设定：{request.config.role.description}\n"
    
    # 示例增强
    examples_block = ""
    if request.config.examples and request.config.exam_enabled:
        examples = "\n\n".join(
            f"输入：{ex.input}\n输出：{ex.output}"
            for ex in request.config.examples
        )
        examples_block = f"## 参考示例\n{examples}\n\n"
    
    # 思维链
    cot_block = ""
    if request.config.cot and request.config.cot.enabled:
        if request.config.cot.custom_steps:
            steps = "\n".join(
                f"{i+1}. {step}" for i, step in enumerate(request.config.cot.custom_steps)
            )
            cot_block = f"## 思维链要求\n请按以下步骤思考：\n{steps}\n"
        else:
            cot_template = get_cot_template(request.config.cot.level)
            cot_block = f"## 思维链要求\n{cot_template}\n"
    
    # 填充模板
    return template.format(
        role_block=role_block,
        examples_block=examples_block,
        cot_block=cot_block,
        original_prompt=request.original_prompt
    )

def get_cot_template(level: str):
    """
    返回针对不同复杂度的思维链(CoT)提示词模板
    基于认知阶梯理论设计：具体→抽象→元认知
    """
    if level == 'basic':
        return """
        ## 思维链要求
        请按照以下两步框架思考问题：
        1. **核心分解**：识别问题中最关键的1-2个要素
        2. **直接推导**：基于要素得出最直接的结论
        
        示例推理模式：
        "问题→关键要素→结论"
        """
    
    elif level == 'intermediate':
        return """
        ## 思维链要求
        请遵循四步推理框架：
        1. **问题解析**：拆解问题的核心组成部分
        2. **关系映射**：分析各部分间的相互作用
        3. **模式识别**：寻找类似问题的解决模式
        4. **综合应用**：整合前三步形成解决方案
        
        附加要求：
        - 每个步骤提供具体实例说明
        - 识别可能的知识盲区
        """
    
    elif level == 'advanced':
        return """
        ## 思维链要求
        采用五层元认知推理框架：
        
        🔍 **第一层：问题解构**
        - 识别显性/隐性需求
        - 划定问题边界
        - 拆解为3-5个关键子问题
        
        🧩 **第二层：多维分析**
        - 技术可行性（资源/工具/时间）
        - 人文因素（用户/利益相关者）
        - 系统影响（上下游影响）
        - 风险矩阵（可能性/严重性）
        
        💡 **第三层：创新方案**
        - 脑暴3种替代方案
        - 交叉融合方案优势
        - 设计最小可行原型
        
        ⚖️ **第四层：批判评估**
        - 使用SWOT分析方案
        - 压力测试极端场景
        - 识别二阶/三阶影响
        
        🚀 **第五层：执行规划**
        - 制定阶段路线图
        - 定义成功指标
        - 设计反馈迭代机制
        
        〖输出要求〗
        按以下格式呈现：
        ```
        [层级标题] 
        • 关键洞察
        • 决策依据
        • 实施要点
        ```
        """
    
    elif level == 'creative':
        return """
        ## 创新思维链要求
        采用六顶思考帽法：
        
        ⚪ 白帽（事实）: 收集核心数据
        🔴 红帽（情感）: 识别情感驱动因素
        ⚫ 黑帽（风险）: 预判潜在问题
        🟡 黄帽（价值）: 发掘积极机会
        🟢 绿帽（创造）: 生成创新方案
        🔵 蓝帽（控制）: 整合决策框架
        
        〖输出要求〗
        以对话形式呈现：
        ```
        [帽子图标] [角色]: [观点]
        ```
        """
    
    # 专业领域特定模板
    elif level == 'scientific':
        return """
        ## 科研思维链
        1. 假说构建：可证伪的核心命题
        2. 实验设计：控制变量/对照组
        3. 数据收集：量化测量方法
        4. 统计分析：p值/置信区间
        5. 结论推导：支持/反驳假说
        """
    
    return "未定义的思维链级别"
