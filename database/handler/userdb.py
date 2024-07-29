import sqlite3

con = sqlite3.connect('./database/user.db')
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS User(
    id integer primary key autoincrement,
    name text,
    email text unique,
    password text
)
""")


def insert_user(user_data: tuple):
    cur.execute("insert into User (name, email, password) values (?, ?, ?)", user_data)
    con.commit()


def select_all_user():
    cur.execute("select * from User")
    return cur.fetchall()


def delete_user_by_email(user_email: str):
    cur.execute("delete from User where email = ?", (user_email,))
    con.commit()


def select_user_by_email(user_email: str):
    cur.execute("select * from User where email = ?", (user_email,))
    return cur.fetchall()


def delete_all_user():
    cur.execute("delete from User")
    con.commit()


def select_password_by_email(user_email: str):
    cur.execute("select password from User where email =?", (user_email,))
    return cur.fetchone()


if __name__ == '__main__':
    con = sqlite3.connect('../user.db')
    if not select_user_by_email('test@test.com'):
        insert_user(('test', 'test@test.com', 'testpwd'))

    print(select_all_user())

    q = input("clear all user? y/n >> ")
    if q == 'y':
        delete_all_user()
