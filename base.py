
import datetime
import logging
import random
import sqlite3

import settings
from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )





def execute_data_from_base(tablename): 
    conn = sqlite3.connect('list_of_posts_base.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM {tablename}")
    count_items = cursor.fetchone()[0]    
    rand_numb = random.randint(1, int(count_items))
    cursor.execute(f"SELECT post_text, img, post_date, post_to, id FROM {tablename} where rowid = ?", (rand_numb,))
    data = cursor.fetchall()[0] 
    logging.info(f'Успешно достали случайное значение из базы данных: {data}')
    conn.close()      
    return data  


def pass_date_filter(date):
    post_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')    
    today = datetime.datetime.today()
    delta = today - post_date
    if delta.days < settings.DELAY_TERM:        
        return False
    else: return True

    

def pass_filters(data, data_list):
    if data in data_list: # Если уже такой пост есть -- пропускаем
        return False

    if data[2] == None:
        post_date = '2019-01-01 00:00:01'
    else: post_date = data[2]
    
    if pass_date_filter(post_date) == False:
        return False
    else: return True
    # Сюда, возможно, позже добавить фильтр по полю post_to
    # Он проверяет или в какой соцсети или месс был опубликова пост




def handle_data(tablename, number_of_posts):
    # Формируем список уникальных строк из базы
    data_list = []
    while len(data_list) < number_of_posts:
        data = execute_data_from_base(tablename)
        if pass_filters(data, data_list) == False:
            continue
        data_list.append(data)
    logging.info(f'Сформировали список постов. Длина -- {len(data_list)}')
    return data_list


def create_users_table():
    conn = sqlite3.connect('users.db')    
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (chat_id text PRIMARY KEY, phone_number text, name text, 
                    first_name text, last_name text, user_id text, role text)'''    
    )
    conn.commit()
    conn.close()


def write_data_to_base(entry):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()  
    cursor.execute(
        'INSERT OR IGNORE INTO users (chat_id, first_name, last_name, user_id, role) VALUES (?, ?, ?, ?, ?)', 
        entry)    
    
    conn.commit()
    conn.close()   


def get_initial_data(update, user_role):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user_id = update.message.from_user.id
    role = user_role
    initial_user_data = (chat_id, first_name, last_name, user_id, role)
    logging.info('Результат функции get_initial_data: ' + str(initial_user_data))
    return initial_user_data



def write_initial_data_to_base(update, user_role):
    data = get_initial_data(update, user_role)
    write_data_to_base(data)


def list_from_base_column(column): # Возвращает список значений столбца
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {column} FROM users')
    column_list = cursor.fetchall()
    conn.commit()
    conn.close()
    return column_list


def get_admin_list(chatid): # Возвращает список значений столбца
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT {chatid} FROM users WHERE role="admin"')
    admin_list = cursor.fetchall()
    conn.commit()
    conn.close()
    return admin_list


def delete_string_from_base(base, table, column, value):
    conn = sqlite3.connect(base)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table} WHERE {column}=?', (value,))
    conn.commit()
    conn.close()    
    logging.info(f'Удалил из {table} айди {value}')
    print(f'Удалил из {table} айди {value}')


if __name__ == "__main__":   

    #entry = ('5', '5', '5', '5', '5', '5', '5')
    # entry = ('5')

    handle_data('story_holodkova', 5)
    # create_users_table()
    # delete_string_from_base('chat_id', '529133148')
