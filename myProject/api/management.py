from fastapi import APIRouter, Depends, HTTPException, status
from models import Prompts, Folders, PromptFolders, Users
from pydantic import BaseModel
from typing import List, Optional
from tortoise.transactions import in_transaction
from app.core.security import get_current_active_user

manage_api = APIRouter()

# 基础模型定义
class Cur_user(BaseModel):
    user_id: int
    email: str
    role: str
    avatar_url: str

class PromptBase(BaseModel):
    session_id: int
    original_content: str
    optimized_content: str
    is_shared: bool = False
    usage_count: int = 0

class PromptCreate(PromptBase):
    pass

class PromptUpdate(PromptBase):
    pass


class PromptResponse(PromptBase):
    prompt_id: int
    user_id: int

    class Config:
        orm_mode = True

# 文件夹模型
class FolderBase(BaseModel):
    folder_name: str

class FolderCreate(FolderBase):
    pass

class FolderResponse(FolderBase):
    folder_id: int
    user_id: int

    class Config:
        orm_mode = True



# ---- 提示词管理 ----
@manage_api.get("/prompts", response_model=List[PromptResponse])
async def get_all_prompts(cur_user: Users = Depends(get_current_active_user)):
    """获取当前用户的所有提示词"""

    return await Prompts.filter(user_id=cur_user.user_id).all()


@manage_api.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, cur_user: Users = Depends(get_current_active_user)):
    """获取单个提示词详情"""
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, user_id=cur_user.user_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权访问"
        )
    return prompt

@manage_api.post("/prompts", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(prompt: PromptCreate, cur_user: Users = Depends(get_current_active_user)):
    """创建新提示词"""
    # 在实际应用中，prompt_id 应由数据库自动生成，不应由客户端提供
    prompt_obj = await Prompts.create(
        user_id=cur_user.user_id,
        **prompt.model_dump()
    )
    return prompt_obj

@manage_api.put("/prompts/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int, 
    prompt: PromptUpdate,
    cur_user: Users = Depends(get_current_active_user)
):
    """更新提示词内容"""
    # 验证提示词存在且属于当前用户
    if not await Prompts.exists(prompt_id=prompt_id, user_id=cur_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权修改"
        )
    
    await Prompts.filter(prompt_id=prompt_id).update(**prompt.model_dump())
    return await Prompts.get(prompt_id=prompt_id)

@manage_api.delete("/prompts/{prompt_id}")
async def delete_prompt(prompt_id: int, cur_user: Users = Depends(get_current_active_user)):
    """删除单个提示词"""
    delete_count = await Prompts.filter(prompt_id=prompt_id, user_id=cur_user.user_id).delete()
    if not delete_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权删除"
        )
    return {"message": "提示词删除成功"}

@manage_api.delete("/prompts", status_code=status.HTTP_207_MULTI_STATUS)
async def batch_delete_prompts(
    prompt_ids: List[int], 
    cur_user: Users = Depends(get_current_active_user)
):
    """批量删除提示词"""
    results = {}
    async with in_transaction():
        for pid in prompt_ids:
            delete_count = await Prompts.filter(prompt_id=pid, user_id=cur_user.user_id).delete()
            results[pid] = "删除成功" if delete_count else "未找到或无权操作"
    
    return results


# ---- 文件夹管理 ----
@manage_api.get("/folders", response_model=List[FolderResponse])
async def get_all_folders(cur_user: Users = Depends(get_current_active_user)):
    """获取用户所有文件夹"""
    return await Folders.filter(user_id=cur_user.user_id).all()

@manage_api.post("/folders", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(folder: FolderCreate, cur_user: Users = Depends(get_current_active_user)):
    """创建新文件夹"""
    folder_obj = await Folders.create(
        user_id=cur_user.user_id,
        **folder.model_dump()
    )
    return folder_obj

@manage_api.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: int, 
    folder: FolderCreate,
    cur_user: Users = Depends(get_current_active_user)
):
    """更新文件夹信息"""
    if not await Folders.exists(folder_id=folder_id, user_id=cur_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权修改"
        )
    
    await Folders.filter(folder_id=folder_id).update(**folder.model_dump())
    return await Folders.get(folder_id=folder_id)

@manage_api.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, cur_user: Users = Depends(get_current_active_user)):
    """删除文件夹（同时移除关联）"""
    async with in_transaction():
        # 删除文件夹关联关系
        await PromptFolders.filter(folder_id=folder_id).delete()
        # 删除文件夹本身
        delete_count = await Folders.filter(folder_id=folder_id, user_id=cur_user.user_id).delete()
    
    if not delete_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权删除"
        )
    return {"message": "文件夹删除成功"}

# ---- 文件夹与提示词关联管理 ----
@manage_api.get("/folders/{folder_id}/prompts", response_model=List[PromptResponse])
async def get_folder_prompts(folder_id: int, cur_user: Users = Depends(get_current_active_user)):
    """获取文件夹内的所有提示词"""
    # 验证文件夹属于当前用户
    if not await Folders.exists(folder_id=folder_id, user_id=cur_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权访问"
        )
    
    # 通过 PromptFolders 表获取关联的提示词
    prompts = await PromptFolders.filter(folder_id=folder_id).select_related("prompt").all()
    
    # 将 Prompts 对象转换为 PromptResponse 模型
    prompt_responses = [
        PromptResponse(
            prompt_id=prompt.prompt.prompt_id,
            user_id=prompt.prompt.user_id,
            session_id=prompt.prompt.session_id,
            original_content=prompt.prompt.original_content,
            optimized_content=prompt.prompt.optimized_content,
            usage_count=prompt.prompt.usage_count,
            is_shared=prompt.prompt.is_shared,
            created_at=prompt.prompt.created_at
        )
        for prompt in prompts
    ]
    
    return prompt_responses

class FolderOperation(BaseModel):
    prompt_ids: List[int]
    cur_folder_id: int = 0 # 如果是移动，则要从提示词所在的当前文件夹移除
    move: bool = True  # True=移动, False=复制

@manage_api.post("/folders/{folder_id}/prompts")
async def add_prompts_to_folder(
    folder_id: int,
    operation: FolderOperation,
    cur_user: Users = Depends(get_current_active_user)
):
    """添加提示词到文件夹（移动或复制）"""
    # 验证文件夹属于当前用户
    if not await Folders.exists(folder_id=folder_id, user_id=cur_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权访问"
        )
    
    # 验证所有提示词属于当前用户
    # prompt_count = await Prompts.filter(
    #     prompt_id__in=operation.prompt_ids,
    #     user_id=cur_user.user_id
    # ).count()
    
    # if prompt_count != len(operation.prompt_ids):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="部分提示词不存在或无权操作"
    #     )
    
    # 执行添加操作
    # folder = await Folders.get(folder_id=folder_id)
    async with in_transaction():
        for pid in operation.prompt_ids:
            # 移动操作：先删除现在的关联
            if operation.move:
                await PromptFolders.filter(prompt_id=pid, folder_id=operation.cur_folder_id).delete()
            
            # 添加新关联（如果不存在）
            if not await PromptFolders.exists(prompt_id=pid, folder_id=folder_id):
                await PromptFolders.create(prompt_id=pid, folder_id=folder_id)
    
    return {"message": "操作成功"}

@manage_api.delete("/folders/{folder_id}/prompts")
async def remove_prompts_from_folder(
    folder_id: int,
    prompt_ids: List[int],
    cur_user: Users = Depends(get_current_active_user)
):
    """从文件夹中移除提示词"""
    # 验证文件夹属于当前用户
    if not await Folders.exists(folder_id=folder_id, user_id=cur_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权访问"
        )
    
    # 删除关联关系
    delete_count = await PromptFolders.filter(
        folder_id=folder_id,
        prompt_id__in=prompt_ids
    ).delete()
    
    if not delete_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到匹配的关联关系"
        )
    
    return {"message": f"成功移除{delete_count}个提示词"}