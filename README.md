# PromptOptimizer

## 实训项目

记得提前安装postgreSQL，并新建数据库。
数据库连接的配置在myProject/settings.py里面。

## 迁移数据库的过程
    - 1. 初始化配置，一般只执行一次：
    - 运行main.py文件之前，要先在终端中运行以下命令：
    - aerich init -t settings.TORTOISE_ORM

    - 2.初始化数据库，一般只执行一次：
    - aerich init-db
    - 
    - 3.更新模型并迁移：（后面的参数表示标记/命名修改操作）
    - aerich migrate --name add_column  
    - 
    - 4.升级（真正应用修改）：
    - aerich upgrade
    - 
    - 回退、查看历史等功能自行查询



# 运行方法：
## 1.创建并进入虚拟环境。
    - # 以Windows系统为例
    - cd myProject
    - python -m venv venv
    - .\venv\Scripts\activate

## 2.安装依赖
    - pip install -r requirements.txt

## 3.找到main.py文件，运行。
    - # 可以右键->运行python->在终端中运行python文件
    - # 终端出现类似以下内容即可
    - INFO:     Started server process [14524]
    - INFO:     Waiting for application startup.
    - INFO:     Application startup complete.

# 接口文档页面
在运行成功后，fastapi会自动渲染出接口文档：
http://localhost:8080/docs#/