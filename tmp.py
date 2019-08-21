import sqlite3
import random
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'base.log'
                    )




def execute_data_from_base(tablename): 
    while True:
        conn = sqlite3.connect('list_of_posts_base.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT count(*) FROM {tablename}")
        count_items = cursor.fetchone()[0]    
        rand_numb = random.randint(1, int(count_items))
        cursor.execute(f"SELECT post_text, img, post_date, post_to, id FROM {tablename} where rowid = ?", (rand_numb,))
        try:
            data = cursor.fetchall()[0] 
            logging.info(f'Успешно достали случайное значение из базы данных: {data}')
            conn.close()      
            return data  
        except IndexError:
            logging.info('Не удалось достать случайное значение из базы.')
            conn.close()

data = execute_data_from_base('story_holodkova')
print(data)
print(len(data))
