import sqlite3

con = sqlite3.connect('./database/image.db')
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Image(
    id integer primary key autoincrement,
    email text,
    image text,
    date date default (datetime('now','localtime'))
)
""")


async def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


async def insertBLOB(email, image):
    try:
        BLOB_image = await convertToBinaryData(image)
        data_tuple = (email, BLOB_image)
        cur.execute("INSERT INTO Image (email, image) VALUES (?, ?)", data_tuple)
        con.commit()
        print("이미지 및 텍스트 DB 저장 완료")

    except sqlite3.Error as error:
        print("테이블 저장 실패", error)


def select_image_by_email(user_email: str):
    cur.execute("select * from Image where email = ? order by date desc limit 1", (user_email,))
    return cur.fetchall()
