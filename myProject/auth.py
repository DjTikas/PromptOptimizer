from pydantic import BaseModel

class Cur_user(BaseModel):
    user_id: int
    email: str
    role: str
    avatar_url: str

# async def get_current_user():

#     return Cur_user(
#         user_id=1,
#         email="emma.tech@example.com",
#         role="user",
#         avatar_url="https://avatarhub.com/emma_profile.jpg",
#     )


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import IntegrityError
from datetime import timedelta
from pydantic import BaseModel
from app.core.security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
import os
from models import Users, Folders
from models import User_Pydantic, UserIn_Pydantic
from app.core.email_code_service import EmailCodeService
from app.core.email_utils import send_email
from app.core.email_template import generate_email_code_template

# 创建认证路由的APIRouter实例
router = APIRouter()

# 定义令牌模型，包含访问令牌和令牌类型
class Token(BaseModel):
    access_token: str
    token_type: str

# 定义登录路由，使用OAuth2密码认证表单接收用户输入
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        # 如果认证失败，抛出401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 获取访问令牌的过期时间
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    # 调用创建访问令牌函数生成令牌
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 定义用户注册路由，接收用户注册信息
@router.post("/register", response_model=User_Pydantic)
async def register(user: UserIn_Pydantic):
    """
    用户注册路由，接收用户注册信息并创建新用户。为新用户创建默认收藏夹。
    """
    # 检查邮箱是否已注册
    existing_user = await Users.get_or_none(email=user.email)
    if existing_user:
        # 如果邮箱已注册，抛出400错误请求异
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 获取密码的哈希值
    hashed_password = get_password_hash(user.password_hash)
    try:
        # 创建新用户
        new_user = await Users.create(
            email=user.email,
            password_hash=hashed_password,
        )
        
        # 为新用户创建默认收藏夹
        default_folder = await Folders.create(
            user_id=new_user.user_id,
            folder_name="默认收藏夹"
        )
        
        return await User_Pydantic.from_tortoise_orm(new_user)
    
    except IntegrityError as e:
        # 处理可能的数据库唯一约束错误
        raise HTTPException(
            status_code=400,
            detail="Failed to create default folder"
        )

# 定义获取当前用户信息的路由，依赖于get_current_active_user函数
@router.get("/me", response_model=User_Pydantic)
async def read_me(current_user: Users = Depends(get_current_active_user)):
    return current_user

# 定义忘记密码请求的模型
class ForgotPasswordRequest(BaseModel):
    email: str

# 定义发送邮箱验证码的路由
@router.post("/getEmailCode")
async def send_email_code(request: ForgotPasswordRequest):
    # 生成并存储验证码
    code = EmailCodeService.generate_code()
    EmailCodeService.store_code(request.email, code)

    # 清理过期验证码
    EmailCodeService.cleanup_expired()

    # 发送邮件
    email_data = generate_email_code_template(email_to=request.email, code=code)
    try:
        send_email(
            email_to=request.email,
            subject=email_data.subject,
            html_content=email_data.html_content
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    return {"code": 0}

# 定义重置密码请求的模型
class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str

# 定义重置密码的路由
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    # 验证验证码
    if not EmailCodeService.verify_code(request.email, request.code):
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    # 查找用户
    user = await Users.get_or_none(email=request.email)
    if not user:
        raise HTTPException(status_code=400, detail="user not found")

    # 更新用户密码
    hashed_password = get_password_hash(request.new_password)
    user.password_hash = hashed_password
    await user.save()

    return {"message": "Password has been reset successfully."}