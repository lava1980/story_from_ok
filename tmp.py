import sqlite3
import random



def execute_data_from_base(tablename): 
    conn = sqlite3.connect('list_of_posts_base.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM {tablename}")
    count_items = cursor.fetchone()[0]    
    rand_numb = random.randint(1, int(count_items))
    cursor.execute(f"SELECT post_text, img, post_date, post_to, id FROM {tablename} where rowid = ?", (rand_numb,))
    data = cursor.fetchall()[0] 
    conn.close()      
    return data  

data = execute_data_from_base('story_holodkova')
print(data)
