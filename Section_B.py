from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import sqlite3

def get_connection():
    conn = sqlite3.connect("student.db")
    return conn

def create_table():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        course TEXT,
        city TEXT,
        marks INTEGER)
        '''
    )
    conn.commit()
    conn.close()

create_table()
class Student(BaseModel):
    name: str
    course: str
    city : str
    marks : int

def createstudent(student : Student):
    conn = get_connection()
    cursor = conn.execute(
        " INSERT INTO student (name, course, city, marks) VALUES (?,?,?,?)",
        (student.name,student.course,student.city,student.marks),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id,**student.model_dump()}

Aman = Student(name='Aman', course='BSc', city='Jaipur', marks=78)
Priya = Student(name='Priya', course='BCA', city='Pali', marks=88)
Rahul = Student(name='Rahul', course='BSc', city='Jodhpur', marks=78)
Sneha = Student(name='Sneha', course='BSc', city='Pali', marks=92)
Karan = Student(name='Karan', course='BCA', city='Jaipur', marks=30)

createstudent(Aman)
createstudent(Priya)
createstudent(Rahul)
createstudent(Sneha)
createstudent(Karan)

def get_students():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM students").fetchall
    conn.close
    return [dict(row) for row in rows]

#Section B
#B1:
def get_smart():
    conn = get_connection()
    rows = conn.execute("SELECT name, marks FROM students WHERE marks >? order DESC" , (80)).fetchall
    conn.close
    return [dict(row) for row in rows]

get_smart()
#B2:

def add_vikram():
    conn = get_connection()
    cursor = conn.execute(
            " INSERT INTO student (name, course, city, marks) VALUES (?, ? , ?, ?)",
            ('Vikram', 'BCA' , 'Udaipur',67),
        )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"hno": new_id}

add_vikram() # RETURNS THE NEW ID which Vikram gets (6)

#B3 : CRUD Stands for create read update delete the four Standard api calls for any backend of an application.  below are all the sql commands and http methods used in FastAPI API

app = FastAPI()

@app.post('/students')    #CREATE
def add_student(student : Student):
    conn = get_connection()
    cursor = conn.execute(
        " INSERT INTO student (name, course, city, marks) VALUES (?,?,?,?)",
        (student.name,student.course,student.city,student.marks),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id,**student.model_dump()}



@app.get('/students/{student_id}')    # READ
def get_one_students(student_id:int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM students WHERE id= ?" , (student_id)).fetchone()
    conn.close
    return dict(row) 


@app.put('/student/update/{student_id}') # UPDATE
def update_student(student:Student,student_id:int):
    conn = get_connection()
    conn.execute("UPDATE students SET name = ?, course = ?, city = ?, marks =? WHERE id = ?" , (student.name , student.course , student.city , student.marks ,student_id))
    conn.close
    return {"id": student_id ,**student.model_dump()}

@app.delete('/students/{student_id}')  #DELETE
def delete_student(student_id:int):
    conn = get_connection()
    conn.execute("DELETE FROM student WHERE id = ?" , (student_id))
    conn.close
    return f"Student with id :{student_id} removed from db"

#B4:

@app.get('/hellow/{name}')
def say_hello(student_name:str):
    return {"message" : "Hello student_name"}

#B5: in line 5 inside the conn.execute () block placeholder ? was not used , and in the same line student_id is written as + student_id and a ',' was not used as well
# the corrected code would be "SELECT * FROM students WHERE id = ?", (student_id,)

