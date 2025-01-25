from typing import List, Optional
from beanie import BackLink, Link, Document
from pydantic import BaseModel, Field


class Student(Document):
    name: str
    age: int
    semester: str
    entry_date: str
    classes: Optional[List[BackLink["Class"]]] = Field(original_field="students")


class CreateStudent(BaseModel):
    name: str
    age: int
    semester: str
    entry_date: str

class Teacher(Document):
    name: str
    age: int
    email: str
    qualification: str
    entry_date: str
    classes: Optional[List[BackLink["Class"]]] = Field(original_field="teacher")

class CreateTeacher(BaseModel):
    name: str
    age: int
    email: str
    qualification: str
    entry_date: str


class Subject(Document):
    name: str
    syllabus: str
    code: str
    workload: int
    prerequisite: str
    classes: Optional[List[BackLink["Class"]]] = Field(original_field="subject")

class CreateSubject(BaseModel):
    name: str
    syllabus: str
    code: str
    workload: int
    prerequisite: str

class Class(Document):
    student_limit: int
    schedule: str
    subject: Link[Subject]
    students: Optional[List[Link["Student"]]]
    teacher: Optional[Link[Teacher]] 

class CreateClass(BaseModel):
    subject: str
    teacher: str
    student_limit: int
    schedule: str
