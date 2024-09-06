import sqlite3

def search_db_telegram(cell):
    filename="telegram_id.db"
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("select * from telegramdb WHERE id={}".format(cell))


    data=cursor.fetchone()
    print(data)
    return data