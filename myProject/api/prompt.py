# app/routers/prompt.py
from fastapi import APIRouter, Depends, HTTPException, status
from models import Prompts, PromptsWithLikes_Pydantic, Tags, Prompts_Pydantic, CommunityInteractions, CommunityInteractions_Pydantic,PromptTags
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

@public_api.get("/public-prompts", response_model=List[PromptsWithLikes_Pydantic])
async def get_public_prompts():
    # 使用annotate添加点赞数统计
    query = Prompts.filter(is_shared=True).annotate(
        like_count=Count("likes")  # 统计关联的点赞数量
    ).prefetch_related("user", "session")
    
    return await PromptsWithLikes_Pydantic.from_queryset(query)

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

@public_api.get("/hot-prompts", response_model=List[Prompts_Pydantic])
async def get_hot_prompts():
    # 使用正确的 related_name
    hot_prompts_query = Prompts.filter(
        is_shared=True
    ).annotate(
        like_count=Count('likes')  # 使用 'likes' 而不是 'community_interactions'
    ).prefetch_related("user", "session")  # 在查询执行前添加 prefetch_related
    
    # 添加排序和限制
    hot_prompts_query = hot_prompts_query.order_by(
        '-like_count',  # 点赞数降序
        '-created_at',  # 最新优先
        '-prompt_id',   # ID大的优先
        '-user_id'      # 用户ID大的优先
    ).limit(5)
    
    # 执行查询
    hot_prompts = await hot_prompts_query
    
    # 直接使用 from_queryset 转换
    return await Prompts_Pydantic.from_queryset(hot_prompts_query)


@public_api.get("/search-prompts", response_model=List[Prompts_Pydantic])
async def search_public_prompts(
    keyword: str = Query(..., min_length=1, description="搜索关键词（支持中文）")
):
    # 添加点赞统计
    prompts = Prompts.filter(
        Q(is_shared=True) & 
        Q(original_content__icontains=keyword)
    ).annotate(
        like_count=Count('likes')  # 添加点赞统计
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
    limit: int = Query(100, ge=1, le=500, description="返回结果数量"),
    offset: int = Query(0, ge=0, description="分页偏移量")
):
    """
    根据标签名称筛选公共提示词
    - 基于标签名称匹配而不是标签ID
    - 支持 AND/OR 两种筛选逻辑
    - 返回匹配的提示词
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
    )
    
    # 添加分页
    query = query.limit(limit).offset(offset)
    
    # 预加载相关数据
    query = query.prefetch_related("user", "session", "tags__tag")
    
    return await Prompts_Pydantic.from_queryset(query)