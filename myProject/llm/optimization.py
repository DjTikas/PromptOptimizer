# llm/optimization.py
from models import Roles
from tortoise.exceptions import DoesNotExist

async def apply_role_enhancement(
    original_content: str, 
    role_enhancement: str,
    user_id: int
) -> str:
    """
    应用角色强化到提示词
    :param original_content: 原始提示词内容
    :param role_enhancement: 角色增强配置（角色ID或自定义内容）
    :param user_id: 当前用户ID（用于验证自定义角色）
    :return: 优化后的提示词
    """
    # 如果role_enhancement是数字，尝试作为角色ID处理
    if role_enhancement.isdigit():
        try:
            role_id = int(role_enhancement)
            # 查询角色 - 优先查询系统预置角色
            role = await Roles.get_or_none(role_id=role_id, is_preset=True)
            
            # 如果找不到预置角色，尝试查询用户的自定义角色
            if not role:
                role = await Roles.get(role_id=role_id, user_id=user_id)
                
            return f"{role.content}\n\n{original_content}"
        
        except DoesNotExist:
            # 如果角色ID不存在，回退到直接使用输入内容
            return f"{role_enhancement}\n\n{original_content}"
    
    # 如果role_enhancement不是数字，直接作为角色内容使用
    return f"{role_enhancement}\n\n{original_content}"
