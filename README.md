# 实训项目：PromptOptimizer

## 基于fastapi+vue的提示词助手

myProject文件夹里面是后端文件
另一个文件夹是前端的文件

# 后端

## 运行方法：

### 0.配置数据库
记得提前安装postgreSQL，并新建数据库，导入PromptOptimizer.sql。
数据库连接的配置在myProject/settings.py里面，记得更改。

### 1.创建并进入虚拟环境。
    - # 以Windows系统为例
    - cd myProject
    - python -m venv venv
    - .\venv\Scripts\activate

### 2.安装依赖
    - pip install -r requirements.txt

### 3.找到main.py文件，运行。
    - # 在vscode可以右键->运行python->在终端中运行python文件
    - # 终端出现类似以下内容即可
    - INFO:     Started server process [14524]
    - INFO:     Waiting for application startup.
    - INFO:     Application startup complete.

## 接口文档页面
在运行成功后，fastapi会自动渲染出接口文档：
http://localhost:8080/docs#/