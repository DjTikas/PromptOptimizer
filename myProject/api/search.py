from fastapi import APIRouter, Depends, HTTPException, status, Query
from tortoise.functions import Count
from models import Prompts, Folders, Tags, PromptTags, Users
from pydantic import BaseModel
from typing import List, Optional
from tortoise.transactions import in_transaction
from tortoise.expressions import Q
from collections import defaultdict
from app.core.security import get_current_active_user

search_api = APIRouter()

# ---- 数据模型定义 ----
class Cur_user(BaseModel):
    user_id: int
    email: str
    role: str
    avatar_url: str

class TagBase(BaseModel):
    tag_name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    tag_id: int
    user_id: int

    class Config:
        orm_mode = True

class TagAssignment(BaseModel):
    prompt_ids: List[int]
    tag_names: List[str]  # 支持创建新标签或使用现有标签

class FolderResponse(BaseModel):
    folder_id: int
    user_id: int
    folder_name: str

    class Config:
        orm_mode = True

class PromptResponse(BaseModel):
    prompt_id: int
    user_id: int
    session_id: int
    original_content: str
    optimized_content: Optional[str]
    usage_count: int
    is_shared: bool
    created_at: str
    tags: List[str] = []  # 标签名称列表

    class Config:
        orm_mode = True

# ---- 提示词标签管理 ----
@search_api.get("/tags", response_model=List[TagResponse])
async def get_tags(cur_user: Users = Depends(get_current_active_user)):
    """获取用户创建的所有tag"""
    return await Tags.filter(user_id=cur_user.user_id).all()

@search_api.post("/tags", status_code=status.HTTP_201_CREATED)
async def create_tags(assignment: TagAssignment, cur_user: Users = Depends(get_current_active_user)):
    """
    用户给提示词批量创建并分配tag
    - 支持创建新标签名或使用现有标签
    - 批量关联到多个提示词
    """
    # 验证所有提示词属于当前用户
    prompt_count = await Prompts.filter(
        prompt_id__in=assignment.prompt_ids,
        user_id=cur_user.user_id
    ).count()
    
    if prompt_count != len(assignment.prompt_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="部分提示词不存在或无权操作"
        )
    
    async with in_transaction():
        # 处理每个标签
        for tag_name in assignment.tag_names:
            # 查找或创建标签（确保用户标签名唯一）
            tag, created = await Tags.get_or_create(
                user_id=cur_user.user_id,
                tag_name=tag_name,
                defaults={'user_id': cur_user.user_id, 'tag_name': tag_name}
            )
            
            # 为每个提示词关联标签
            for prompt_id in assignment.prompt_ids:
                # 检查是否已存在关联
                if not await PromptTags.exists(prompt_id=prompt_id, tag_id=tag.tag_id):
                    await PromptTags.create(prompt_id=prompt_id, tag_id=tag.tag_id)
    
    return {"message": f"成功为{len(assignment.prompt_ids)}个提示词添加{len(assignment.tag_names)}个标签"}

@search_api.put("/tag/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int, 
    tag_update: TagCreate, 
    cur_user: Users = Depends(get_current_active_user)
):
    """用户根据id修改tag内容"""
    # 验证标签存在且属于当前用户
    tag = await Tags.get_or_none(tag_id=tag_id, user_id=cur_user.user_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在或无权修改"
        )
    
    # 检查新标签名是否已存在
    existing_tag = await Tags.get_or_none(
        user_id=cur_user.user_id, 
        tag_name=tag_update.tag_name
    )
    if existing_tag and existing_tag.tag_id != tag_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="标签名称已存在"
        )
    
    tag.tag_name = tag_update.tag_name
    await tag.save()
    return tag

@search_api.delete("/tags", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(
    tag_ids: List[int] = Query(..., description="要删除的标签ID列表"),
    cur_user: Users = Depends(get_current_active_user)
):
    """用户根据id列表批量删除tag内容"""
    # 验证所有标签属于当前用户
    tags_count = await Tags.filter(
        tag_id__in=tag_ids,
        user_id=cur_user.user_id
    ).count()
    
    if tags_count != len(tag_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="部分标签不存在或无权删除"
        )
    
    async with in_transaction():
        # 删除标签关联
        await PromptTags.filter(tag_id__in=tag_ids).delete()
        # 删除标签本身
        await Tags.filter(tag_id__in=tag_ids).delete()
    
    return

# 新增的响应模型和接口
class PromptTagItem(BaseModel):
    tag_id: int
    tag_name: str

class PromptTagsResponse(BaseModel):
    prompt_id: int
    tags: List[PromptTagItem]

@search_api.get("/prompts/{prompt_id}/tags", response_model=List[PromptTagItem])
async def get_tags_by_prompt_id(
    prompt_id: int,
    cur_user: Users = Depends(get_current_active_user)
):
    """
    根据提示词ID获取关联的标签列表
    - 验证提示词属于当前用户
    - 返回该提示词的所有标签
    """
    # 验证提示词是否存在且属于当前用户
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, user_id=cur_user.user_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在或无权访问"
        )
    
    # 查询关联的标签
    tag_relations = await PromptTags.filter(prompt_id=prompt_id).prefetch_related('tag')
    
    # 构建响应数据
    return [
        PromptTagItem(tag_id=rel.tag.tag_id, tag_name=rel.tag.tag_name)
        for rel in tag_relations
    ]

# 批量获取多个提示词的标签接口
@search_api.get("/prompts/tags", response_model=List[PromptTagsResponse])
async def get_tags_for_prompts(
    prompt_ids: List[int] = Query(..., alias="prompt_ids"),
    cur_user: Users = Depends(get_current_active_user)
):
    """
    批量获取多个提示词的标签列表
    - 验证所有提示词属于当前用户
    - 返回每个提示词对应的标签集合
    """
    # 验证所有提示词属于当前用户
    valid_prompts = await Prompts.filter(
        prompt_id__in=prompt_ids,
        user_id=cur_user.user_id
    ).values_list("prompt_id", flat=True)
    
    if len(valid_prompts) != len(prompt_ids):
        invalid_ids = set(prompt_ids) - set(valid_prompts)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"无权访问的提示词ID: {invalid_ids}"
        )
    
    # 查询所有关联的标签
    tag_relations = await PromptTags.filter(
        prompt_id__in=prompt_ids
    ).prefetch_related('tag')
    
    # 按提示词ID分组
    tags_by_prompt = defaultdict(list)
    for rel in tag_relations:
        tags_by_prompt[rel.prompt_id].append(
            PromptTagItem(tag_id=rel.tag.tag_id, tag_name=rel.tag.tag_name)
        )
    
    # 构建响应数据（包括没有标签的提示词）
    return [
        PromptTagsResponse(
            prompt_id=pid,
            tags=tags_by_prompt.get(pid, [])
        )
        for pid in prompt_ids
    ]

# ---- 提示词智能搜索管理 ----
@search_api.get("/fuzzy/prompts", response_model=List[PromptResponse])
async def get_fuzzy_prompts(
    query: str = Query(..., min_length=2, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """模糊搜索提示词（标题和内容）"""
    # 查询时直接获取外键值
    prompts = await Prompts.filter(
        Q(original_content__icontains=query) | 
        Q(optimized_content__icontains=query),
        user_id=cur_user.user_id
    ).limit(limit).prefetch_related("tags__tag").values(
        "prompt_id",
        "user_id",  # 直接获取外键ID
        "session_id",  # 直接获取外键ID
        "original_content",
        "optimized_content",
        "usage_count",
        "is_shared",
        "created_at"
    )
    
    # 获取所有提示词的标签
    prompt_ids = [p["prompt_id"] for p in prompts]
    tags_map = {}
    if prompt_ids:
        tag_relations = await PromptTags.filter(
            prompt_id__in=prompt_ids
        ).prefetch_related("tag")
        
        for rel in tag_relations:
            if rel.prompt_id not in tags_map:
                tags_map[rel.prompt_id] = []
            tags_map[rel.prompt_id].append(rel.tag.tag_name)
    
    # 构建响应
    result = []
    for prompt in prompts:
        response = PromptResponse(
            prompt_id=prompt["prompt_id"],
            user_id=prompt["user_id"],
            session_id=prompt["session_id"],
            original_content=prompt["original_content"],
            optimized_content=prompt["optimized_content"],
            usage_count=prompt["usage_count"],
            is_shared=prompt["is_shared"],
            created_at=prompt["created_at"].isoformat(),
            tags=tags_map.get(prompt["prompt_id"], [])
        )
        result.append(response)
    
    return result

@search_api.get("/fuzzy/tags", response_model=List[TagResponse])
async def get_fuzzy_tags(
    query: str = Query(..., min_length=2, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """模糊搜索标签"""
    return await Tags.filter(
        tag_name__icontains=query,
        user_id=cur_user.user_id
    ).limit(limit).all()

@search_api.get("/fuzzy/folders", response_model=List[FolderResponse])
async def get_fuzzy_folders(
    query: str = Query(..., min_length=2, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """模糊搜索文件夹"""
    return await Folders.filter(
        folder_name__icontains=query,
        user_id=cur_user.user_id
    ).limit(limit).all()

class TagFilterResponse(PromptResponse):
    """扩展响应模型，包含匹配信息（可选）"""
    pass

@search_api.get("/filter/tags", response_model=List[TagFilterResponse])
async def filter_prompts_by_tags(
    tags: List[str] = Query(..., description="要筛选的标签列表"),
    mode: str = Query("and", description="筛选模式：'and' 表示必须包含所有标签, 'or' 表示包含任一标签"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """
    根据标签筛选提示词
    - 支持 AND/OR 两种筛选逻辑
    - 返回匹配的提示词及其所有标签
    """
    # 获取当前用户的标签ID
    user_tags = await Tags.filter(
        tag_name__in=tags,
        user_id=cur_user.user_id
    ).values_list("tag_id", flat=True)
    
    tag_ids = list(user_tags)
    
    if not tag_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到匹配的标签"
        )
    
    # 根据模式构建查询
    if mode.lower() == "and":
        # AND 模式：必须包含所有标签
        # 使用分组计数确保包含所有标签
        prompt_ids = await PromptTags.filter(
            tag_id__in=tag_ids
        ).group_by("prompt_id").annotate(
            count=Count("tag_id")
        ).filter(count=len(tag_ids)).values_list("prompt_id", flat=True)
    elif mode.lower() == "or":
        # OR 模式：包含任一标签
        prompt_ids = await PromptTags.filter(
            tag_id__in=tag_ids
        ).distinct().values_list("prompt_id", flat=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的筛选模式，仅支持 'and' 或 'or'"
        )
    
    # 获取提示词详情
    prompts = await Prompts.filter(
        prompt_id__in=prompt_ids,
        user_id=cur_user.user_id
    ).limit(limit).values(
        "prompt_id",
        "user_id",
        "session_id",
        "original_content",
        "optimized_content",
        "usage_count",
        "is_shared",
        "created_at"
    )
    
    # 获取所有提示词的标签
    prompt_ids = [p["prompt_id"] for p in prompts]
    tags_map = {}
    if prompt_ids:
        tag_relations = await PromptTags.filter(
            prompt_id__in=prompt_ids
        ).prefetch_related("tag")
        
        for rel in tag_relations:
            if rel.prompt_id not in tags_map:
                tags_map[rel.prompt_id] = []
            tags_map[rel.prompt_id].append(rel.tag.tag_name)
    
    # 构建响应
    result = []
    for prompt in prompts:
        response = TagFilterResponse(
            prompt_id=prompt["prompt_id"],
            user_id=prompt["user_id"],
            session_id=prompt["session_id"],
            original_content=prompt["original_content"],
            optimized_content=prompt["optimized_content"],
            usage_count=prompt["usage_count"],
            is_shared=prompt["is_shared"],
            created_at=prompt["created_at"].isoformat(),
            tags=tags_map.get(prompt["prompt_id"], [])
        )
        result.append(response)
    
    return result