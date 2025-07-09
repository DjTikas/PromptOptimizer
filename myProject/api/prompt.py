# app/routers/prompt.py
from fastapi import APIRouter, Depends, HTTPException, status
from models import Prompts, PromptsWithLikes_Pydantic, PromptFolders, Tags, Prompts_Pydantic, CommunityInteractions, CommunityInteractions_Pydantic,PromptTags
from app.core.security import get_current_active_user
from models import Users
from tortoise.functions import Count
from fastapi import Query
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

public_api = APIRouter()


# 创建标签的Pydantic模型
class Tag_Pydantic(BaseModel):
    tag_id: int
    tag_name: str

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 的配置方式

# 用户基本信息模型
class UserBasicInfo(BaseModel):
    email: str
    avatar_url: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

# 创建新的提示词模型，包含标签
class PromptWithTags_Pydantic(PromptsWithLikes_Pydantic):
    tags: List[Tag_Pydantic] = []
    user_info: UserBasicInfo  # 新增用户信息字段

    model_config = ConfigDict(from_attributes=True)  
    
# Pydantic v2 的配置方式
@public_api.get("/public-prompts", response_model=List[PromptWithTags_Pydantic])
async def get_public_prompts():
    # 获取公开提示词并统计点赞数，预加载用户和标签数据
    query = Prompts.filter(is_shared=True).annotate(
        like_count=Count("likes")
    ).prefetch_related(
        "user",  # 预加载用户数据
        "session",  # 预加载会话数据
        "tags__tag"  # 预加载标签数据
    )
    
    # 执行查询
    prompts = await query
    
    # 构建结果
    result = []
    for prompt in prompts:
        # 获取用户基本信息
        user_info = UserBasicInfo(
            email=prompt.user.email,
            avatar_url=prompt.user.avatar_url
        )
        
        # 构建提示词数据
        prompt_data = {
            "prompt_id": prompt.prompt_id,
            "original_content": prompt.original_content,
            "optimized_content": prompt.optimized_content,
            "usage_count": prompt.usage_count,
            "is_shared": prompt.is_shared,
            "created_at": prompt.created_at,
            "like_count": prompt.like_count,  # 使用注解的点赞数
            "tags": [Tag_Pydantic.model_validate(tag.tag) for tag in prompt.tags],  # 使用预加载的标签
            "user_info": user_info,  # 添加用户信息
        }
        
        # 转换为Pydantic模型
        prompt_with_tags = PromptWithTags_Pydantic.model_validate(prompt_data)
        result.append(prompt_with_tags)
    
    return result

# app/routers/prompt.py
@public_api.post("/like-prompt/{prompt_id}", response_model=CommunityInteractions_Pydantic)
async def like_prompt(
    prompt_id: int, 
    current_user: Users = Depends(get_current_active_user)
):
    # 获取提示词
    prompt = await Prompts.get_or_none(
        prompt_id=prompt_id, 
        is_shared=True
    )
    if not prompt:
        raise HTTPException(status_code=404, detail="Public prompt not found")

    # 创建点赞记录
    like, created = await CommunityInteractions.get_or_create(
        prompt=prompt,
        user=current_user
    )
    
    if not created:
        raise HTTPException(status_code=400, detail="You have already liked this prompt")
    
    # 更新提示词的点赞计数
    prompt.like_count = await CommunityInteractions.filter(prompt=prompt).count()
    await prompt.save()
    
    return await CommunityInteractions_Pydantic.from_tortoise_orm(like)

@public_api.delete("/unlike-prompt/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_prompt(
    prompt_id: int, 
    current_user: Users = Depends(get_current_active_user)
):
    # 获取点赞记录
    like = await CommunityInteractions.get_or_none(
        prompt_id=prompt_id,
        user=current_user
    )
    if not like:
        raise HTTPException(status_code=404, detail="Like record not found")
    
    # 删除点赞记录
    await like.delete()
    
    # 更新提示词的点赞计数
    prompt = await Prompts.get(prompt_id=prompt_id)
    prompt.like_count = await CommunityInteractions.filter(prompt=prompt).count()
    await prompt.save()

async def get_prompts_with_tags(prompts_query):
    # 获取提示词数据并预加载用户信息
    prompts = await prompts_query.prefetch_related("user")
    prompt_ids = [p.prompt_id for p in prompts]
    
    # 批量获取所有相关标签
    tag_relations = await PromptTags.filter(prompt_id__in=prompt_ids).prefetch_related("tag")
    tags_by_prompt = {}
    for relation in tag_relations:
        if relation.prompt_id not in tags_by_prompt:
            tags_by_prompt[relation.prompt_id] = []
        tags_by_prompt[relation.prompt_id].append(Tag_Pydantic.model_validate(relation.tag))
    
    # 构建结果
    result = []
    for prompt in prompts:
        # 获取用户基本信息
        user_info = UserBasicInfo(
            email=prompt.user.email,
            avatar_url=prompt.user.avatar_url
        )
        
        # 只提取需要的字段
        prompt_data = {
            "prompt_id": prompt.prompt_id,
            "original_content": prompt.original_content,
            "optimized_content": prompt.optimized_content,
            "usage_count": prompt.usage_count,
            "is_shared": prompt.is_shared,
            "created_at": prompt.created_at,
            "like_count": getattr(prompt, "like_count", 0),  # 处理可能的注解字段
            "tags": tags_by_prompt.get(prompt.prompt_id, []),
            "user_info": user_info
        }
        
        prompt_with_tags = PromptWithTags_Pydantic.model_validate(prompt_data)
        result.append(prompt_with_tags)
    
    return result

@public_api.get("/hot-prompts", response_model=List[PromptWithTags_Pydantic])
async def get_hot_prompts():
    # 使用正确的 related_name
    hot_prompts_query = Prompts.filter(
        is_shared=True
    ).annotate(
        like_count=Count('likes')
    ).prefetch_related("user", "session")
    
    # 添加排序和限制
    hot_prompts_query = hot_prompts_query.order_by(
        '-like_count',  # 点赞数降序
        '-created_at',  # 最新优先
        '-prompt_id',   # ID大的优先
        '-user_id'      # 用户ID大的优先
    ).limit(5)
    
    # 获取包含标签的数据
    return await get_prompts_with_tags(hot_prompts_query)

@public_api.get("/search-prompts", response_model=List[PromptWithTags_Pydantic])
async def search_public_prompts(
    keyword: str = Query(..., min_length=1, description="搜索关键词（支持中文）")
):
    # 添加点赞统计
    prompts_query = Prompts.filter(
        Q(is_shared=True) & 
        Q(original_content__icontains=keyword)
    ).annotate(
        like_count=Count('likes')  # 添加点赞统计
    ).order_by("-created_at"
    ).prefetch_related("user")
    
    # 获取包含标签的数据
    return await get_prompts_with_tags(prompts_query)


@public_api.get("/filter-by-tags", response_model=List[PromptWithTags_Pydantic])
async def filter_prompts_by_tags(
    tags: str = Query(..., description="标签列表，用逗号分隔"),
    operator: str = Query("AND", description="逻辑操作符: AND 或 OR"),
    limit: int = Query(100, ge=1, le=500, description="返回结果数量"),
    offset: int = Query(0, ge=0, description="分页偏移量")
):
    """
    根据标签名称筛选公共提示词
    - 基于标签名称匹配而不是标签ID
    - 支持 AND/OR 两种筛选逻辑
    - 返回匹配的提示词及其标签信息
    """
    # 1. 分割标签字符串并转换为小写
    tag_names = [name.strip().lower() for name in tags.split(',') if name.strip()]
    
    if not tag_names:
        return []
    
    # 2. 获取所有公开提示词的ID
    public_prompt_ids = await Prompts.filter(
        is_shared=True
    ).values_list("prompt_id", flat=True)
    
    if not public_prompt_ids:
        return []  # 没有公开提示词
    
    # 3. 根据模式构建标签名称筛选查询
    operator = operator.upper()
    if operator == "OR":
        # OR 模式：包含任一标签名称
        filtered_prompt_ids = await PromptTags.filter(
            tag__tag_name__in=tag_names,
            prompt_id__in=public_prompt_ids
        ).distinct().values_list("prompt_id", flat=True)
        filtered_prompt_ids = set(filtered_prompt_ids)
    elif operator == "AND":
        # AND 模式：提示词必须包含所有标签名称
        filtered_prompt_ids = set(public_prompt_ids)  # 初始化为所有公开提示词
        
        for tag_name in tag_names:
            # 对于每个标签名称，筛选出拥有该标签的提示词
            tagged_prompt_ids = await PromptTags.filter(
                tag__tag_name=tag_name,
                prompt_id__in=filtered_prompt_ids
            ).values_list("prompt_id", flat=True)
            
            # 更新筛选结果
            filtered_prompt_ids = set(tagged_prompt_ids)
            
            # 如果已经没有匹配的提示词，提前退出
            if not filtered_prompt_ids:
                break
    else:
        raise HTTPException(
            status_code=400, 
            detail="无效的操作符，仅支持 'AND' 或 'OR'"
        )
    
    # 4. 获取提示词详情
    if not filtered_prompt_ids:
        return []  # 没有匹配的提示词
    
    # 构建查询
    query = Prompts.filter(
        prompt_id__in=filtered_prompt_ids,
        is_shared=True
    ).annotate(
        like_count=Count('likes')  # 添加点赞统计
    ).prefetch_related("user")
    
    # 添加分页和排序
    query = query.order_by("-created_at").limit(limit).offset(offset)
    
    # 预加载相关数据
    query = query.prefetch_related("user", "session", "tags__tag")
    
    # 使用之前定义的公共方法获取包含标签的数据
    return await get_prompts_with_tags(query)


# 新增：用户点赞状态检查接口
@public_api.get("/prompts/{prompt_id}/like-status", response_model=dict)
async def check_user_like_status(
    prompt_id: int,
    current_user: Users = Depends(get_current_active_user)
):
    """
    检查当前用户是否对指定提示词点过赞
    - 返回: { "liked": boolean }
    """
    # 检查提示词是否存在且是公开的
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, is_shared=True)
    if not prompt:
        raise HTTPException(status_code=404, detail="Public prompt not found")
    
    # 检查用户是否点过赞
    liked = await CommunityInteractions.exists(
        prompt_id=prompt_id,
        user_id=current_user.user_id
    )
    
    return {"liked": liked}

# 新增：用户收藏状态检查接口
@public_api.get("/prompts/{prompt_id}/collect-status", response_model=dict)
async def check_user_collect_status(
    prompt_id: int,
    current_user: Users = Depends(get_current_active_user)
):
    """
    检查当前用户是否收藏过指定提示词及收藏到哪些文件夹
    - 返回: { 
        "collected": boolean,
        "folders": [
            {"folder_id": int, "folder_name": str},
            ...
        ]
    }
    """
    # 检查提示词是否存在且是公开的
    prompt = await Prompts.get_or_none(prompt_id=prompt_id, is_shared=True)
    if not prompt:
        raise HTTPException(status_code=404, detail="Public prompt not found")
    
    # 查询用户收藏该提示词的所有文件夹
    folder_relations = await PromptFolders.filter(
        prompt_id=prompt_id,
        folder__user_id=current_user.user_id  # 确保文件夹属于当前用户
    ).prefetch_related("folder")
    
    # 提取文件夹信息
    folders = [
        {
            "folder_id": relation.folder.folder_id,
            "folder_name": relation.folder.folder_name
        }
        for relation in folder_relations
    ]
    
    return {
        "collected": len(folders) > 0,
        "folders": folders
    }