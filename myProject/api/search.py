from fastapi import APIRouter, Depends, HTTPException, status, Query
from tortoise.functions import Count
from models import Prompts, Folders, PromptFolders, Tags, PromptTags, Users
from pydantic import BaseModel, Field
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

# 数据模型定义
class TagPromptResponse(BaseModel):
    tag_id: int
    tag_name: str

    class Config:
        orm_mode = True

class UserInfoResponse(BaseModel):
    email: str
    avatar_url: str

    class Config:
        orm_mode = True

class PromptResponse(BaseModel):
    prompt_id: int
    original_content: str
    optimized_content: Optional[str]
    usage_count: int = 0
    is_shared: bool = False
    created_at: str
    like_count: int = 0
    session_id: int
    tags: List[TagPromptResponse] = []
    user_info: UserInfoResponse

    class Config:
        orm_mode = True

# class TagFilterResponse(BaseModel):
#     prompt_id: int
#     original_content: str
#     optimized_content: Optional[str]
#     usage_count: int = 0
#     is_shared: bool = False
#     created_at: str
#     session_id: int
#     tags: List[str] = []
#     user_info: UserInfoResponse

#     class Config:
#         orm_mode = True

# 标签创建请求模型
class TagCreationRequest(BaseModel):
    tag_names: List[str] = Field(
        ...,
        min_items=1,
        max_items=50,
        description="要创建的标签名称列表"
    )

# 标签分配请求模型（更新版）
class TagAssignment(BaseModel):
    tag_ids: List[int] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="要分配的标签ID列表"
    )
    prompt_ids: List[int] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="要关联的提示词ID列表"
    )

# ---- 提示词标签管理 ----
@search_api.get("/tags", response_model=List[TagResponse])
async def get_tags(cur_user: Users = Depends(get_current_active_user)):
    """获取用户创建的所有tag"""
    return await Tags.filter(user_id=cur_user.user_id).all()

@search_api.post("/tags", status_code=status.HTTP_201_CREATED)
async def create_tags(
    tags: TagCreationRequest, 
    cur_user: Users = Depends(get_current_active_user)
):
    """
    创建新标签（不关联提示词）
    - 支持批量创建标签
    - 标签在用户下唯一（重复创建已存在标签将忽略）
    - 返回创建的标签列表（包含已存在的标签）
    """
    created_tags = []
    existing_tags = []
    
    async with in_transaction():
        for tag_name in tags.tag_names:
            # 检查标签是否已存在（用户下唯一）
            tag = await Tags.get_or_none(
                user_id=cur_user.user_id,
                tag_name=tag_name
            )
            
            if tag:
                existing_tags.append(tag)
            else:
                # 创建新标签
                new_tag = await Tags.create(
                    user_id=cur_user.user_id,
                    tag_name=tag_name
                )
                created_tags.append(new_tag)
    
    # 合并结果（包括已存在的标签）
    all_tags = created_tags + existing_tags
    
    return {
        "created_count": len(created_tags),
        "existing_count": len(existing_tags),
        "tags": [
            {"tag_id": tag.tag_id, "tag_name": tag.tag_name}
            for tag in all_tags
        ]
    }

@search_api.post("/prompts/tags/assignments", status_code=status.HTTP_201_CREATED)
async def assign_tags_to_prompts(
    assignment: TagAssignment,
    cur_user: Users = Depends(get_current_active_user)
):
    """
    将已有标签关联到多个提示词
    - 要求标签和提示词必须存在且属于当前用户
    - 支持批量操作（多个标签关联到多个提示词）
    - 已存在的关联关系将自动跳过
    """
    # 验证所有提示词属于当前用户
    prompt_ids = assignment.prompt_ids
    tag_ids = assignment.tag_ids
    
    prompt_count = await Prompts.filter(
        prompt_id__in=prompt_ids,
        user_id=cur_user.user_id
    ).count()
    
    if prompt_count != len(prompt_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="部分提示词不存在或无权操作"
        )
    
    # 验证所有标签属于当前用户
    tag_count = await Tags.filter(
        tag_id__in=tag_ids,
        user_id=cur_user.user_id
    ).count()
    
    if tag_count != len(tag_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="部分标签不存在或无权操作"
        )
    
    created_count = 0
    skipped_count = 0
    
    async with in_transaction():
        # 为每个提示词关联所有标签
        for prompt_id in prompt_ids:
            for tag_id in tag_ids:
                # 检查是否已存在关联
                if not await PromptTags.exists(
                    prompt_id=prompt_id, 
                    tag_id=tag_id
                ):
                    await PromptTags.create(
                        prompt_id=prompt_id, 
                        tag_id=tag_id
                    )
                    created_count += 1
                else:
                    skipped_count += 1
    
    return {
        "message": f"成功创建 {created_count} 个关联，跳过 {skipped_count} 个已存在关联",
        "created_relations": created_count,
        "skipped_relations": skipped_count,
        "prompt_count": len(prompt_ids),
        "tag_count": len(tag_ids)
    }

@search_api.delete(
    "/prompts/{prompt_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_prompt_tag_relation(
    prompt_id: int,
    tag_id: int,
    # cur_user: Users = Depends(get_current_active_user)  # 按需启用认证
):
    """
    删除提示词和标签的关联关系
    
    参数:
    - prompt_id: 提示词ID
    - tag_id: 标签ID
    
    返回:
    - 204: 删除成功
    - 404: 关系不存在
    """
    # 检查关系是否存在
    relation = await PromptTags.get_or_none(
        prompt_id=prompt_id,
        tag_id=tag_id
    )
    
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词与标签的关联关系不存在"
        )
    
    # 删除关系
    await relation.delete()
    
    # 返回204 No Content
    return

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
    # cur_user: Users = Depends(get_current_active_user)
):
    """
    根据提示词ID获取关联的标签列表
    - 返回该提示词的所有标签
    """
    # 验证提示词是否存在
    prompt = await Prompts.get_or_none(prompt_id=prompt_id)
    if not prompt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="提示词不存在"
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
    # cur_user: Users = Depends(get_current_active_user)
):
    """
    批量获取多个提示词的标签列表
    - 返回每个提示词对应的标签集合
    """
    # 验证所有提示词属于当前用户
    valid_prompts = await Prompts.filter(
        prompt_id__in=prompt_ids,
        # user_id=cur_user.user_id
    ).values_list("prompt_id", flat=True)
    
    if len(valid_prompts) != len(prompt_ids):
        invalid_ids = set(prompt_ids) - set(valid_prompts)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"无法访问的提示词ID: {invalid_ids}"
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
    query: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """模糊搜索收藏的提示词（包括自己创建的和收藏的他人提示词）"""
    # 获取用户自己创建的提示词ID
    own_prompts = await Prompts.filter(
        Q(original_content__icontains=query) | 
        Q(optimized_content__icontains=query),
        user_id=cur_user.user_id
    ).prefetch_related("tags__tag", "user")
    
    # 获取用户收藏的他人提示词（通过文件夹关联）
    collected_prompts = await PromptFolders.filter(
        folder__user_id=cur_user.user_id,
        prompt__original_content__icontains=query
    ).prefetch_related("prompt__tags__tag", "prompt__user")
    
    # 合并所有提示词
    all_prompts = []
    prompt_ids = set()
    
    for prompt in own_prompts:
        if prompt.prompt_id not in prompt_ids:
            all_prompts.append(prompt)
            prompt_ids.add(prompt.prompt_id)
    
    for pf in collected_prompts:
        prompt = pf.prompt
        if prompt.prompt_id not in prompt_ids:
            all_prompts.append(prompt)
            prompt_ids.add(prompt.prompt_id)
    
    # 构建响应
    result = []
    for prompt in all_prompts:
        # 获取标签
        tags = []
        for prompt_tag in prompt.tags:
            if prompt_tag.tag:
                tags.append(TagPromptResponse(
                    tag_id=prompt_tag.tag.tag_id,
                    tag_name=prompt_tag.tag.tag_name
                ))
        
        # 获取用户信息
        user_info = UserInfoResponse(
            email=prompt.user.email,
            avatar_url=prompt.user.avatar_url
        )
        
        response = PromptResponse(
            prompt_id=prompt.prompt_id,
            original_content=prompt.original_content,
            optimized_content=prompt.optimized_content,
            usage_count=prompt.usage_count,
            is_shared=prompt.is_shared,
            created_at=prompt.created_at.isoformat(),
            like_count=prompt.like_count,
            session_id=1,
            tags=tags,
            user_info=user_info
        )
        result.append(response)
    
    # 按相关性排序
    def sort_key(p):
        if query.lower() in p.original_content.lower():
            return 0
        if p.optimized_content and query.lower() in p.optimized_content.lower():
            return 1
        return 2
    
    result.sort(key=sort_key)
    
    return result[:limit]

@search_api.get("/fuzzy/tags", response_model=List[TagResponse])
async def get_fuzzy_tags(
    query: str = Query(..., min_length=2, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """模糊搜索创建的标签"""
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
    """模糊搜索创建的文件夹"""
    return await Folders.filter(
        folder_name__icontains=query,
        user_id=cur_user.user_id
    ).limit(limit).all()


@search_api.get("/filter/tags", response_model=List[PromptResponse])
async def filter_prompts_by_tags(
    tags: List[str] = Query(..., description="要筛选的标签列表"),
    mode: str = Query("and", description="筛选模式：'and' 表示必须包含所有标签, 'or' 表示包含任一标签"),
    limit: int = Query(10, ge=1, le=100, description="返回结果数量"),
    cur_user: Users = Depends(get_current_active_user)
):
    """根据标签名称筛选用户私有提示词库中的提示词"""
    # 获取用户私有提示词库中的所有提示词
    own_prompts = await Prompts.filter(
        user_id=cur_user.user_id
    ).prefetch_related("tags__tag", "user", "session")
    
    collected_prompts = await PromptFolders.filter(
        folder__user_id=cur_user.user_id
    ).prefetch_related("prompt__tags__tag", "prompt__user", "prompt__session")
    
    # 合并提示词
    all_prompts = []
    prompt_ids = set()
    
    for prompt in own_prompts:
        if prompt.prompt_id not in prompt_ids:
            all_prompts.append(prompt)
            prompt_ids.add(prompt.prompt_id)
    
    for pf in collected_prompts:
        prompt = pf.prompt
        if prompt.prompt_id not in prompt_ids:
            all_prompts.append(prompt)
            prompt_ids.add(prompt.prompt_id)
    
    # 根据标签筛选
    filtered_prompts = []
    
    for prompt in all_prompts:
        prompt_tags = [pt.tag.tag_name for pt in prompt.tags if pt.tag]
        
        if mode.lower() == "and":
            # 必须包含所有标签
            if all(tag in prompt_tags for tag in tags):
                filtered_prompts.append(prompt)
        elif mode.lower() == "or":
            # 包含任一标签
            if any(tag in prompt_tags for tag in tags):
                filtered_prompts.append(prompt)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的筛选模式，仅支持 'and' 或 'or'"
            )
    
    # 构建响应
    result = []
    for prompt in filtered_prompts:
        # 获取标签详细信息
        tag_responses = [
            TagPromptResponse(
                tag_id=pt.tag.tag_id,
                tag_name=pt.tag.tag_name
            )
            for pt in prompt.tags if pt.tag
        ]
        
        # 获取用户信息
        user_info = UserInfoResponse(
            email=prompt.user.email,
            avatar_url=prompt.user.avatar_url
        )
        
        response = PromptResponse(
            prompt_id=prompt.prompt_id,
            original_content=prompt.original_content,
            optimized_content=prompt.optimized_content,
            usage_count=prompt.usage_count,
            is_shared=prompt.is_shared,
            created_at=prompt.created_at.isoformat(),
            like_count=prompt.like_count,
            session_id=prompt.session.session_id,  # 确保session_id正确获取
            tags=tag_responses,  # 使用TagPromptResponse列表
            user_info=user_info
        )
        result.append(response)
    
    # 按创建时间排序
    result.sort(key=lambda x: x.created_at, reverse=True)
    
    return result[:limit]