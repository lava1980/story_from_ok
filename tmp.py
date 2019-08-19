import sqlite3
import random
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
   

  )




def execute_data_from_base(tablename): 
    conn = sqlite3.connect('list_of_posts_base.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM {tablename}")
    count_items = cursor.fetchone()[0]    
    rand_numb = random.randint(1, int(count_items))
    cursor.execute("SELECT post_text, img, post_date, post_to, id FROM {} where rowid = ?".format(tablename), (rand_numb,))
    logging.info(f'Выборка из базы, cursor.fetchall(): {cursor.fetchall()}')
    data = cursor.fetchall()
        
    conn.close()      
    return data  

data = execute_data_from_base('story_holodkova')     
print(data)