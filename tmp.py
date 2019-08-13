
import datetime
import random
import sqlite3



def execute_data_from_base(tablename): 
    conn = sqlite3.connect('list_of_posts_base.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM {tablename}")
    count_items = cursor.fetchone()[0]
    
    rand_numb = random.randint(1, int(count_items))

    cursor.execute(f"SELECT post_text, img, post_date, post_to FROM {tablename} where rowid = ?", (rand_numb,))
    data = cursor.fetchall()[0] 
    conn.close()      
    return data  


def pass_date_filter(date):
    post_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')    
    today = datetime.datetime.today()
    delta = today - post_date
    if delta.days < 180:        
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
    print(data_list)
    print(len(data_list))
    return data_list







# TODO Проверить или дата старше полугода
# TODO 


handle_data('story_holodkova', 5)
# check_date_filter('2019-02-14 13:01:00')
