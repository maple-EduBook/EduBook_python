import sqlite3

con = sqlite3.connect('./database/result.db')
cur = con.cursor()

cur.execute("""
    create table if not exists Result(
        email text primary key ,
        description text,
        image text,
        date date default (datetime('now','localtime'))
    )
""")


async def save_result(save_res):
    cur.execute("insert into Result (email, description, image) values (?, ?, ?)", (save_res,))
    con.commit()


async def get_result(email):
    cur.execute("select * from Result where email = ?", (email,))
    con.commit()
