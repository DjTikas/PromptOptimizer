from fastapi import FastAPI
import uvicorn

""" 迁移数据库的过程
1. 初始化配置，一般只执行一次：
运行本文件之前，要先在终端中运行以下命令：
aerich init -t settings.TORTOISE_ORM

2.初始化数据库，一般只执行一次：
aerich init-db

3.更新模型并迁移：（后面的参数表示标记/命名修改操作）
aerich migrate --name add_column  

4.升级（真正应用修改）：
aerich upgrade

回退、查看历史等功能自行查询
"""

### 用于渲染本地docs，不用管，只需要将static文件夹放到main.py文件同级目录
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
 
app = FastAPI(docs_url=None)  # 禁用默认的 Swagger UI
app.mount("/static", StaticFiles(directory="static"), name="static") 
 
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="API Docs",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )
### 渲染结束

from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from api.management import manage_api
from api.optimizer import optimize_api
from api.newop import optimize_new_api
from api.search import search_api
from api.users import user_api
from api.prompt import public_api
from api.api_keys import key_api
from auth import router
from fastapi.middleware.cors import CORSMiddleware

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=86400,  # 24小时缓存
)

app.include_router(manage_api, prefix="/manage", tags=["01 提示词管理（收藏相关）"])
app.include_router(search_api, prefix="/search", tags=["02 提示词管理（搜索相关）"])
app.include_router(optimize_new_api, prefix="/optimize", tags=["03 提示词优化"])
app.include_router(router, prefix="/auth", tags=["04 登录注册"])
app.include_router(user_api, prefix="/user", tags=["05 用户信息"])
app.include_router(public_api, prefix="/public", tags=["06 公共搜索"])
app.include_router(key_api, prefix="/key", tags=["07 api配置"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
    # print(StaticFiles(directory="apps"))

