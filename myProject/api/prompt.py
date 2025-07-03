# app/routers/prompt.py
from fastapi import APIRouter, Depends, HTTPException
from models import Prompts, Tags, Prompts_Pydantic, CommunityInteractions, CommunityInteractions_Pydantic,PromptTags
from app.core.security import get_current_active_user
from models import Users
from tortoise.functions import Count
from fastapi import Query
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from pydantic import BaseModel
from datetime import datetime
from typing import List

public_api = APIRouter()

@public_api.get("/public-prompts", response_model=List[Prompts_Pydantic])
async def get_public_prompts():
    query = Prompts.filter(is_shared=True).prefetch_related("user", "session")
    return await Prompts_Pydantic.from_queryset(query)

# app/routers/prompt.py
@public_api.post("/like-prompt/{prompt_id}", response_model=CommunityInteractions_Pydantic)
async def like_prompt(
    prompt_id: int, 
    current_user: Users = Depends(get_current_active_user)
):
    # 获取提示词（确保存在且公开）
    prompt = await Prompts.get_or_none(
        prompt_id=prompt_id, 
        is_shared=True
    )
    if not prompt:
        raise HTTPException(status_code=404, detail="Public prompt not found")

    # 创建或获取点赞记录 - 使用 get_or_create 方法
    like, created = await CommunityInteractions.get_or_create(
        prompt=prompt,
        user=current_user
    )
    
    if not created:
        raise HTTPException(status_code=400, detail="You have already liked this prompt")

    return await CommunityInteractions_Pydantic.from_tortoise_orm(like)

class HotPrompt(Prompts_Pydantic):
    like_count: int

@public_api.get("/hot-prompts", response_model=List[HotPrompt])
async def get_hot_prompts():
    # 使用正确的 related_name
    hot_prompts = await Prompts.filter(
        is_shared=True
    ).annotate(
        like_count=Count('likes')  # 使用 'likes' 而不是 'community_interactions'
    ).order_by(
        '-like_count',  # 点赞数降序
        '-created_at',  # 最新优先
        '-prompt_id',   # ID大的优先
        '-user_id'      # 用户ID大的优先
    ).limit(5)
    
    # 转换为响应模型
    result = []
    for prompt in hot_prompts:
        prompt_data = await Prompts_Pydantic.from_tortoise_orm(prompt)
        result.append(HotPrompt(
            **prompt_data.model_dump(),
            like_count=prompt.like_count
        ))
    
    return result

@public_api.get("/search-prompts", response_model=List[Prompts_Pydantic])
async def search_public_prompts(
    keyword: str = Query(..., min_length=1, description="搜索关键词（支持中文）")
):
    prompts = Prompts.filter(
        Q(is_shared=True) & 
        Q(original_content__icontains=keyword)
    ).order_by("-created_at")
    
    return await Prompts_Pydantic.from_queryset(prompts)

'''
@public_api.get("/filter-by-tags", response_model=list[Prompts_Pydantic])
async def filter_prompts_by_tags(
    tags: str = Query(..., description="标签列表，用逗号分隔"),
    operator: str = Query("AND", description="逻辑操作符: AND 或 OR"),
):
    # 分割标签字符串
    tag_names = [name.strip() for name in tags.split(',') if name.strip()]
    
    if not tag_names:
        return []
    
    # 获取标签对应的ID
    tags_records = await Tags.filter(tag_name__in=tag_names).all()
    if not tags_records:
        return []
    
    tag_ids = [tag.tag_id for tag in tags_records]
    
    if operator.upper() == "OR":
        # OR 逻辑：包含任意一个标签
        prompts = Prompts.filter(
            is_shared=True,
            prompt_tags__tag_id__in=tag_ids
        ).distinct().prefetch_related("user", "session", "tags")
    elif operator.upper() == "AND":
        # AND 逻辑：包含所有标签
        # 使用子查询确保包含所有标签
        query = Prompts.filter(is_shared=True)
        for tag_id in tag_ids:
            query = query.filter(prompt_tags__tag_id=tag_id)
        prompts = query.distinct().prefetch_related("user", "session", "tags")
    else:
        raise HTTPException(
            status_code=400, 
            detail="Invalid operator. Use 'AND' or 'OR'"
        )
    
    return await Prompts_Pydantic.from_queryset(prompts)
'''

@public_api.get("/filter-by-tags", response_model=List[Prompts_Pydantic])
async def filter_prompts_by_tags(
    tags: str = Query(..., description="标签列表，用逗号分隔"),
    operator: str = Query("AND", description="逻辑操作符: AND 或 OR"),
):
    # 分割标签字符串
    tag_names = [name.strip() for name in tags.split(',') if name.strip()]
    
    if not tag_names:
        return []
    
    # 获取标签对应的ID（不区分大小写）
    tags_records = await Tags.filter(
        tag_name__in=[name.lower() for name in tag_names]
    ).all()
    
    if not tags_records:
        return []
    
    tag_ids = [tag.tag_id for tag in tags_records]
    
    # 构建基础查询（只查询公开提示词）
    base_query = Prompts.filter(is_shared=True)
    
    if operator.upper() == "OR":
        # OR 逻辑：包含任意一个标签
        query = base_query.filter(
            tags__tag_id__in=tag_ids
        ).distinct()
    elif operator.upper() == "AND":
        # AND 逻辑：使用子查询确保包含所有标签
        # 创建子查询：查找包含所有标签的提示词ID
        subquery = PromptTags.filter(
            tag_id__in=tag_ids
        ).group_by('prompt_id').annotate(
            tag_count=Count('tag_id')
        ).filter(
            tag_count=len(tag_ids)
        ).values_list('prompt_id', flat=True)
        
        # 执行子查询并获取结果
        prompt_ids = await subquery
        
        # 应用子查询
        query = base_query.filter(
            prompt_id__in=prompt_ids
        )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Invalid operator. Use 'AND' or 'OR'"
        )
    
    # 预加载相关数据
    query = query.prefetch_related("user", "session", "tags")
    
    return await Prompts_Pydantic.from_queryset(query)
