from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from typing import Optional
import os
from models import Users
from pytz import utc

# 从环境变量获取配置，如果环境变量未设置，则使用默认值
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# 创建密码哈希和验证的上下文，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 定义OAuth2密码认证方案，指定token的获取URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# 验证密码函数，比较明文密码和哈希密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 获取密码哈希值的函数
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 认证用户函数，根据邮箱和密码验证用户
async def authenticate_user(email: str, password: str) -> Optional[Users]:
    # 根据邮箱查找用户
    try:
        user = await Users.get(email=email)
    except DoesNotExist:
        # 如果用户不存在，返回 None
        return None
    
    # 如果密码验证失败，返回 None
    if not verify_password(password, user.password_hash):
        return None
    
    return user

# 创建访问令牌的函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        # 如果指定了过期时间，计算过期时间点
        expire = datetime.now(utc) + expires_delta  # 使用 utc 时区
    else:
        # 默认过期时间为15分钟
        expire = datetime.now(utc) + timedelta(minutes=15)  # 使用 utc 时区
    # 将过期时间添加到要编码的数据中
    to_encode.update({"exp": expire})
    # 使用JWT库编码数据，生成访问令牌
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 获取当前用户的函数，根据令牌验证用户身份
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Users:
    # 定义认证失败的异常
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从令牌中获取用户邮箱
        email: str = payload.get("sub")
        if email is None:
            # 如果邮箱为空，抛出认证失败异常
            raise credentials_exception
    except JWTError:
        # 如果解码失败，抛出认证失败异常
        raise credentials_exception
    
    # 根据邮箱查找用户
    user = await Users.get_or_none(email=email)
    if user is None:
        # 如果用户不存在，抛出认证失败异常
        raise credentials_exception
    return user

# 获取当前活跃用户的函数，依赖于get_current_user函数
async def get_current_active_user(current_user: Users = Depends(get_current_user)) -> Users:
    return current_user


from models import UserRole

async def get_current_admin_user(current_user: Users = Depends(get_current_user)) -> Users:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
