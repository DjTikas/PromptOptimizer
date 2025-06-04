from fastapi import APIRouter
from models import *
from pydantic import BaseModel, field_validator
from typing import List
from fastapi.exceptions import HTTPException

student_api = APIRouter()

# 用于粘贴的文件，不参与项目运行

@student_api.get("/")
async def getAllStudent():
    # 01 查询所有 all方法
    # students = await Student.all() # Queryset
    # for stu in students :
    #     print(stu.name)
    #     pass

    # 02 过滤查询 filter , 返回的也是列表
    # students = await Student.filter(name="张三") # Queryset

    # 03 get方法，返回模型类对象
    # stu = await Student.get(id=4) # Student()

    # 04 模糊查询
    # students = await Student.filter(sno__gt=2001)
    # students = await Student.filter(sno__in=[2001, 2002, 2009])
    # students = await Student.filter(sno__range=[1, 10000])

    # 05 values查询
    # students = await Student.all().values("name", "sno")   # 从Queryset中获取values字典（键值对）

    # 06 一对多查询 多对多查询
    amiya = await Student.get(name="amiya")
    # 跨表获取班级名称 {'name': '一年级二班'}
    print(await amiya.clas.values("name"))  
    # 所有学生获取班级名称和课程名称 
    students = await Student.all().values("name", "clas__name", "course__name") 

    # 跨表获取课程名称和老师名称 [{'name': '语文', 'teacher__name': '李老师'}, {'name': '英语', 'teacher__name': '王老师'}]
    print(await amiya.course.all().values("name", "teacher__name"))  

    return{
        "查看所有学生":students
    }

class StudentIn(BaseModel):
    name : str
    pwd : str
    sno : int
    clas_id : int
    courses : List[int] = []   # 课程id列表

    @field_validator("name") # 该装饰器用于验证字段的值
    def check_name(cls, v):
        if len(v) < 2:
            raise ValueError("姓名长度不能小于2")
        return v

@student_api.post("/")
async def addStudent(student_in: StudentIn):
    # 插入到数据库中
    # 01
    # student = Student(name=student_in.name, pwd=student_in.pwd, sno=student_in.sno, clas_id=student_in.clas_id)
    # await student.save()
    # 02
    student = await Student.create(
        name=student_in.name,
        pwd=student_in.pwd,
        sno=student_in.sno,
        clas_id=student_in.clas_id
    )
    # 多对多的关系绑定
    chosen_courses = await Course.filter(id__in=student_in.courses) # 过滤，保证课程id存在
    await student.course.add(*chosen_courses)  # 绑定课程，注意打星号
    return student

@student_api.get("/{student_id}")
async def getOneStudent(student_id: int):
    student = await Student.get(id=student_id)
    return student


@student_api.put("/{student_id}")
async def updateStudent(student_id: int, student_in: StudentIn):
    data = student_in.model_dump() # 获取数据，转换为字典
    courses =  data.pop("courses") # 提取多对多关系

    await Student.filter(id=student_id).update(**data)  # 更新数据

    # 更新多对多关系
    edit_student = await Student.get(id=student_id)  # 获取学生对象
    chosen_courses = await Course.filter(id__in=courses) # 过滤，保证课程id存在
    await edit_student.course.clear()  # 清空多对多关系
    await edit_student.course.add(*chosen_courses)  # 绑定新的多对多关系

    return edit_student


@student_api.delete("/{student_id}")
async def deleteOneStudent(student_id: int):
    deleteCount =  await Student.filter(id=student_id).delete()
    if not deleteCount:
        raise HTTPException(status_code=404, detail="没有找到该学生")
    return{}