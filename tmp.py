import sqlite3



def get_admin_list(chatid): # Возвращает список значений столбца
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE role="admin"')
    admin_list = cursor.fetchall()
    conn.commit()
    conn.close()
    return admin_list

column = ('chat_id')
p = get_admin_list(column)
print(p)

# SELECT * FROM locations WHERE country_id='CA'; # Синтаксис Селект
