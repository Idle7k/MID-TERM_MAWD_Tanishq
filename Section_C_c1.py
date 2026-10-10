#C1:
import sqlite3

#(a)
conn = sqlite3.connect('library.db')

#(b)
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

#(c)

def insert_books():
    conn.executemany(
            "INSERT INTO books (title , author, price) Values(?, ?,?)",
            [
                ('Python Basics','Rao' ,250),
                ('SQL Guide' ,'Mehta' , 180),
                ('Web Dev' ,'Khan', 400),
            ]
            
        )
    conn.commit()
    conn.close()

insert_books()

#(d)

def increase_id2():
    row = conn.execute(
        "UPDATE books SET  price = price + price* 0.1 where id = 2"
            )
    conn.commit()
    conn.close()
    return print(len(row))

increase_id2()

#(e)

def delete_under():
    conn.execute(
            "DELETE FROM books WHERE price < ?" , (200)
                )
    conn.commit()
    conn.close()

delete_under()

def select_all():
    rows = conn.execute(
                "SELECT * FROM books"
                    )
    conn.commit()
    conn.close()
    return [dict(row) for row in rows]
