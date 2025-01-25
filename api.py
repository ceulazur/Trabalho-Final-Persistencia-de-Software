import fastapi
from beanie import init_beanie
from model import CreateClass, CreateStudent, CreateSubject, CreateTeacher, Student, Teacher, Subject, Class
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import os


load_dotenv(".env")

async def init():
    connection_string = os.getenv("DBURL")
    client = AsyncIOMotorClient(connection_string)
    await init_beanie(database=client["school_db"], document_models=[Student, Teacher, Subject, Class])

async def lifespan(app: FastAPI):
    await init()
    yield
    # await Student.delete_all()
    # await Teacher.delete_all()
    # await Subject.delete_all()
    # await Class.delete_all()

app = fastapi.FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/student")
async def create_student(_student: CreateStudent):
    student = Student(**_student.dict())
    student.classes =[]
    await Student.insert_one(student)
    return JSONResponse(content=jsonable_encoder(student))

@app.get("/student")
async def get_students():
    students = await Student.all().to_list()
    students = [student.dict(exclude={"classes"}) for student in students]
    for student in students:
        student.update({"id": str(student.get("id"))})
    return JSONResponse(content=jsonable_encoder(students))

@app.get("/student/classes")
async def get_student_classes():
    students = await Student.all().to_list()
    for student in students:
        student.fill_back_refs(["classes"])

        classes = []
        for _class in student.classes:
            print(_class.to_dict())
            classes.append(_class.to_dict())
        student.update({"classes": classes})
        student.update({"id": str(student.get("id"))})

    return students

@app.post("/teacher")
async def create_teacher(teacher: CreateTeacher):
    teacher_ = Teacher(**teacher.dict())
    teacher_.classes = []
    await Teacher.insert_one(teacher_)
    return JSONResponse(content=jsonable_encoder(teacher_))

@app.get("/teacher")
async def get_teachers():
    teachers = await Teacher.all(nesting_depth=0).to_list()
    teachers = [teacher.dict(exclude={"classes"}) for teacher in teachers]
    for teacher in teachers:
        teacher.update({"id": str(teacher.get("id"))})
    return teachers

@app.post("/subject")
async def create_subject(subject: CreateSubject):
    subject_ = Subject(**subject.dict())
    subject_.classes = []
    await Subject.insert_one(subject_)
    return JSONResponse(content=jsonable_encoder(subject_))

@app.get("/subject")
async def get_subjects():
    subjects = await Subject.all().to_list()
    subjects = [subject.dict(exclude={"classes"}) for subject in subjects]
    for subject in subjects:
        subject.update({"id": str(subject.get("id"))})
    return jsonable_encoder(subjects)

@app.post("/class")
async def create_class(_class: CreateClass):
    class_ = Class(**_class.dict())
    await Class.insert_one(class_)
    return

@app.get("/class")
async def get_classes():
    classes = await Class.all().to_list()
    classes = [class_.dict(exclude={"students", "teacher", "subject"}) for class_ in classes]
    for class_ in classes:
        class_.update({"id": str(class_.get("id"))})
    return classes

