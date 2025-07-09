# app/routers/api_keys.py
from fastapi import APIRouter, Depends, HTTPException, Query
from models import APIKeys, APIKeys_Pydantic, APIKeysIn_Pydantic
from app.core.security import get_current_active_user, encrypt_api_key
from models import Users
from tortoise.transactions import atomic
from typing import List

key_api = APIRouter()

@atomic()  # 启用事务保证数据一致性
@key_api.post("/", response_model=APIKeys_Pydantic)
async def create_api_key(
    api_key_data: APIKeysIn_Pydantic,
    current_user: Users = Depends(get_current_active_user)
):
    # 直接存储明文 API 密钥
    new_api_key = await APIKeys.create(
        user=current_user,
        api_key=api_key_data.api_key,  # 直接使用原始值，不加密
        api_name=api_key_data.api_name,
        api_address=api_key_data.api_address,
        api_type=api_key_data.api_type
    )
    return await APIKeys_Pydantic.from_tortoise_orm(new_api_key)
@key_api.get("/", response_model=List[APIKeys_Pydantic])
async def get_user_api_keys(
    current_user: Users = Depends(get_current_active_user),
    is_active: bool = Query(None, description="过滤激活状态")
):
    """获取当前用户的所有API密钥（支持激活状态过滤）"""
    query = APIKeys.filter(user=current_user)
    if is_active is not None:
        query = query.filter(is_active=is_active)
    
    return await APIKeys_Pydantic.from_queryset(query)

@key_api.get("/{key_id}", response_model=APIKeys_Pydantic)
async def get_api_key(
    key_id: int,
    current_user: Users = Depends(get_current_active_user)
):
    """获取单个API密钥（通过key_id）"""
    api_key = await APIKeys.get_or_none(
        key_id=key_id, 
        user=current_user
    ).prefetch_related("user")
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API密钥不存在")
    return await APIKeys_Pydantic.from_tortoise_orm(api_key)

@atomic()
@key_api.put("/{key_id}", response_model=APIKeys_Pydantic)
async def update_api_key(
    key_id: int,
    api_key_data: APIKeysIn_Pydantic,
    current_user: Users = Depends(get_current_active_user)
):
    """更新API密钥信息"""
    api_key = await APIKeys.get_or_none(
        key_id=key_id, 
        user=current_user
    )
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API密钥不存在")
    
    # 获取更新数据，不进行加密处理
    updated_data = api_key_data.dict(exclude_unset=True)
    
    # 更新数据
    await api_key.update_from_dict(updated_data)
    await api_key.save()
    return await APIKeys_Pydantic.from_tortoise_orm(api_key)

@atomic()
@key_api.delete("/{key_id}")
async def delete_api_key(
    key_id: int,
    current_user: Users = Depends(get_current_active_user)
):
    """删除API密钥记录"""
    deleted_count = await APIKeys.filter(
        key_id=key_id, 
        user=current_user
    ).delete()
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="API密钥不存在")
    return {"message": "API密钥已删除"}
