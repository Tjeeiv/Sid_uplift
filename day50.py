from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str
    age: int
    grade: str

app = FastAPI()

students: List[Student] = []

@app.get("/")
def read_root():
    return {"message": "This is the Students API"}

@app.get("/students")
def get_students():
    return students

@app.post("/students")
def create_student(student: Student):
    students.append(student)
    return student

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id < len(students):
        students[student_id] = student
        return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id < len(students):
        deleted_student = students.pop(student_id)
        return deleted_student
    raise HTTPException(status_code=404, detail="Student not found")


#python -m uvicorn day50:app --reload