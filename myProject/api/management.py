from fastapi import APIRouter, Depends, HTTPException, status
from models import Prompts, Folders, PromptFolders, Users
from pydantic import BaseModel
from typing import List, Optional
from tortoise.transactions import in_transaction
from app.core.security import get_current_active_user
from datetime import datetime

manage_api = APIRouter()

# Tag model
class TagResponse(BaseModel):
    tag_id: int
    tag_name: str

    class Config:
        orm_mode = True

# User info model
class UserInfoResponse(BaseModel):
    email: str
    avatar_url: Optional[str]

    class Config:
        orm_mode = True

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

# Updated Prompt Response model
class PromptResponse(BaseModel):
    prompt_id: int
    original_content: str
    optimized_content: str
    usage_count: int = 0
    is_shared: bool = False
    created_at: datetime
    like_count: int = 0
    session_id: int
    tags: List[TagResponse] = []
    user_info: UserInfoResponse

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
    """获取当前用户创建的所有提示词"""
    prompts = await Prompts.filter(user_id=cur_user.user_id).prefetch_related("tags__tag", "user").all()
    
    prompt_responses = []
    for prompt in prompts:
        # Get tags through the junction table
        tags = []
        for prompt_tag in prompt.tags:  # This accesses PromptTags instances
            if prompt_tag.tag:  # Ensure the tag exists
                tags.append(TagResponse(
                    tag_id=prompt_tag.tag.tag_id,
                    tag_name=prompt_tag.tag.tag_name
                ))
        
        prompt_responses.append(
            PromptResponse(
                prompt_id=prompt.prompt_id,
                original_content=prompt.original_content,
                optimized_content=prompt.optimized_content,
                usage_count=prompt.usage_count,
                is_shared=prompt.is_shared,
                created_at=prompt.created_at,
                like_count=prompt.like_count,
                session_id=prompt.session_id,
                tags=tags,
                user_info=UserInfoResponse(
                    email=prompt.user.email,
                    avatar_url=prompt.user.avatar_url
                )
            )
        )
    
    return prompt_responses


@manage_api.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: int, cur_user: Users = Depends(get_current_active_user)):
    """获取用户创建的单个提示词详情"""
    prompt = await Prompts.get_or_none(
        prompt_id=prompt_id, 
        user_id=cur_user.user_id
    ).prefetch_related("tags__tag", "user")
    
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权访问"
        )
    
    # Get tags through the junction table
    tags = []
    for prompt_tag in prompt.tags:  # This accesses PromptTags instances
        if prompt_tag.tag:  # Ensure the tag exists
            tags.append(TagResponse(
                tag_id=prompt_tag.tag.tag_id,
                tag_name=prompt_tag.tag.tag_name
            ))
    
    return PromptResponse(
        prompt_id=prompt.prompt_id,
        original_content=prompt.original_content,
        optimized_content=prompt.optimized_content,
        usage_count=prompt.usage_count,
        is_shared=prompt.is_shared,
        created_at=prompt.created_at,
        like_count=prompt.like_count,
        session_id=1,  # Access session_id through the session relationship
        tags=tags,
        user_info=UserInfoResponse(
            email=prompt.user.email,
            avatar_url=prompt.user.avatar_url
        )
    )

@manage_api.post("/prompts", status_code=status.HTTP_201_CREATED)
async def create_prompt(prompt: PromptCreate, cur_user: Users = Depends(get_current_active_user)):
    """创建新提示词"""
    # 检查数据库中是否已存在相同用户、相同原始内容和优化内容的提示词
    existing_prompt = await Prompts.filter(
        user_id=cur_user.user_id,
        original_content=prompt.original_content,
        optimized_content=prompt.optimized_content
    ).first()
    
    if existing_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已存在内容完全相同的提示词"
        )
    
    # 在实际应用中，prompt_id 应由数据库自动生成，不应由客户端提供
    prompt_obj = await Prompts.create(
        user_id=cur_user.user_id,
        **prompt.model_dump()
    )
    return prompt_obj
    

@manage_api.put("/prompts/{prompt_id}" , status_code=status.HTTP_200_OK)
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
    return 

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
    """创建新文件夹（自动检查重名）"""
    # 检查当前用户是否已有同名文件夹
    existing_folder = await Folders.filter(
        user_id=cur_user.user_id,
        folder_name=folder.folder_name
    ).exists()
    
    if existing_folder:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件夹名称 '{folder.folder_name}' 已存在"
        )
    
    # 创建新文件夹
    folder_obj = await Folders.create(
        user_id=cur_user.user_id,
        folder_name=folder.folder_name
    )
    return folder_obj

@manage_api.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: int, 
    folder: FolderCreate,
    cur_user: Users = Depends(get_current_active_user)
):
    """更新文件夹信息（自动检查重名）"""
    # 检查文件夹是否存在且属于当前用户
    folder_obj = await Folders.get_or_none(folder_id=folder_id, user_id=cur_user.user_id)
    if not folder_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件夹不存在或无权修改"
        )
    
    # 检查新名称是否与当前名称不同（避免不必要的检查）
    if folder_obj.folder_name != folder.folder_name:
        # 检查当前用户是否已有其他同名文件夹
        # 正确方式：直接检查是否存在同名文件夹（排除当前文件夹）
        exists = await Folders.filter(
            user_id=cur_user.user_id,
            folder_name=folder.folder_name
        ).exclude(folder_id=folder_id).exists()
        
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件夹名称 '{folder.folder_name}' 已存在"
            )
        
    # 默认收藏夹不可修改
    if folder_obj.folder_name == "默认收藏夹":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="默认收藏夹名称不可修改"
        )
    
    # 执行更新
    folder_obj.folder_name = folder.folder_name
    await folder_obj.save()
    
    return folder_obj

@manage_api.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, cur_user: Users = Depends(get_current_active_user)):
    """删除文件夹（同时移除关联）"""
    # 默认收藏夹不可删除
    folder_obj = await Folders.get_or_none(folder_id=folder_id, user_id=cur_user.user_id)
    if folder_obj.folder_name == "默认收藏夹":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="默认收藏夹不可删除"
        )
    
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
    prompt_folders = await PromptFolders.filter(folder_id=folder_id).prefetch_related(
        "prompt__tags__tag", 
        "prompt__user"
    ).all()
    
    prompt_responses = []
    for pf in prompt_folders:
        prompt = pf.prompt
        # Get tags through the junction table
        tags = []
        for prompt_tag in prompt.tags:  # This accesses PromptTags instances
            if prompt_tag.tag:  # Ensure the tag exists
                tags.append(TagResponse(
                    tag_id=prompt_tag.tag.tag_id,
                    tag_name=prompt_tag.tag.tag_name
                ))
        
        prompt_responses.append(
            PromptResponse(
                prompt_id=prompt.prompt_id,
                original_content=prompt.original_content,
                optimized_content=prompt.optimized_content,
                usage_count=prompt.usage_count,
                is_shared=prompt.is_shared,
                created_at=prompt.created_at,
                like_count=prompt.like_count,
                session_id=1,  # Access session_id through the session relationship
                tags=tags,
                user_info=UserInfoResponse(
                    email=prompt.user.email,
                    avatar_url=prompt.user.avatar_url
                )
            )
        )
    
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