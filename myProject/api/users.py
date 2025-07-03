from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from models import Users, User_Pydantic
from app.core.security import get_current_active_user
from pydantic import BaseModel

import os
import uuid


user_api = APIRouter()
class AvatarSelectRequest(BaseModel):
    avatar_name: str


# 配置头像路径
BASE_URL = "http://localhost:8000"  # 访问静态文件的域名
AVATAR_UPLOAD_DIR = "./uploads/avatars/user"     # 用户上传
AVATAR_SYSTEM_DIR = "./uploads/avatars/system"   # 系统头像

# 获取当前登录用户信息
@user_api.get("/me", response_model=User_Pydantic)
async def get_current_user_info(current_user: Users = Depends(get_current_active_user)):
    return current_user

# 上传头像（文件）
@user_api.post("/avatar/upload")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: Users = Depends(get_current_active_user)
):
    # 限制类型
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="仅支持 JPG/PNG 格式")

    # 自动创建目录
    os.makedirs(AVATAR_UPLOAD_DIR, exist_ok=True)

    # 保存文件
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(AVATAR_UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    # 设置头像 URL
    avatar_url = f"{BASE_URL}/avatars/user/{filename}"
    current_user.avatar_url = avatar_url
    await current_user.save()

    return {"avatar_url": avatar_url, "message": "头像上传成功"}

# 使用系统默认头像
@user_api.post("/avatar/select")
async def select_system_avatar(
    req: AvatarSelectRequest,
    current_user: Users = Depends(get_current_active_user)
):
    avatar_name = req.avatar_name
    avatar_path = os.path.join(AVATAR_SYSTEM_DIR, avatar_name)
    if not os.path.exists(avatar_path):
        raise HTTPException(status_code=404, detail="系统头像不存在")

    avatar_url = f"{BASE_URL}/avatars/system/{avatar_name}"
    current_user.avatar_url = avatar_url
    await current_user.save()

    return {"avatar_url": avatar_url, "message": "系统头像设置成功"}

