from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()
conn = sqlite3.connect('library.db')

def create_table():
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        price REAL
        )
        '''
    )
    conn.commit()
    conn.close()
create_table()
class Book(BaseModel):
    title: str
    author: str
    price: float

@app.post('/books')
def insert_books(book: Book):
    row = conn.execute(
            "INSERT INTO books (title , author, price) Values(?, ?,?)",
            (book.title, book.author, book.price)
        )
    conn.commit()
    newid = row.lastrowid
    conn.close()
    return {"id": newid, **book.model_dump()}

@app.get('/books')
def select_all():
    rows = conn.execute(
                "SELECT * FROM books"
                    )
    conn.commit()
    conn.close()
    return [dict(row) for row in rows]

@app.get('/books/{book_id}')
def select_one(book_id: int):
    row = conn.execute(
                "SELECT * FROM books WHERE id = ?", (book_id,)
            )
    conn.commit()
    conn.close()
    return [dict(row) ]

@app.put('/books/{book_id}')
def update_book(book: Book, book_id: int):
    row = conn.execute(
            "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?" , (book.title , book.author , book.price ,book_id)
                )
    conn.commit()
    if row.rowcount == 0:
            raise HTTPException(status_code=404)
    conn.close()
    return {"id": book_id, **book.model_dump()}

@app.delete('/books/{book_id}')
def delete_book(book_id: int):
    row = conn.execute(
            "DELETE FROM books WHERE id = ?" , (book_id,)
                )
    conn.commit()
    if row.rowcount == 0:
        raise HTTPException(status_code=404)
    conn.close()
    return {"message": f"Book with ID {book_id} deleted successfully."}


