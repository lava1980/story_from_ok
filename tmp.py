import sqlite3



def list_from_base_column(column): # Возвращает список значений столбца
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users WHERE role=admin')
    column_list = cursor.fetchall()
    conn.commit()
    conn.close()
    return column_list

column = ('chat_id')
p = list_from_base_column(column)
print(p)

# SELECT * FROM locations WHERE country_id='CA'; # Синтаксис Селект
