# -*- coding: utf-8 -*-

import requests, bs4, sqlite3, getpostdata



def get_data(soup, page_type, name_of_table):

    list_of_blocks = soup.select('.feed-w') # <class 'bs4.element.Tag'>
    data_to_base = []

    if 'page' in page_type:
        search_part_of_url = '/statuses/'
    elif 'community' in page_type:
        search_part_of_url = '/topic/'

    for block in list_of_blocks:
        try:
            search_full_link = block.find_all('a', class_='')[0].get('href')

        except:
            try:
                search_full_link = block.select('.media-text_a')[0].get('href')
            except:
                search_full_link = '/chtoto/' # лишь бы что -- чтобы в следующей строке
                # при сравнении выбило False и блок не отработал



        if search_part_of_url in search_full_link:
            link = 'https://ok.ru' + search_full_link
            date = getpostdata.get_valid_date(block.select('.feed_date')[0].get_text())
            id = link[-14:]

            count_of_comments, count_of_share, count_of_likes = getpostdata.get_list_of_metadata(block=block)
            post_text = getpostdata.post_text(link)
            get_images = getpostdata.get_images(block=block, id=id, folder=name_of_table)

            data_to_base.append(
                (id, date, link, count_of_comments, count_of_share, count_of_likes, post_text, get_images))

    print(len(data_to_base))

    return data_to_base



def create_database(data, name_of_table):
    conn = sqlite3.connect("list_of_posts_base.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name_of_table}
                      (id text PRIMARY KEY, date text, url text, comments integer,
                       shares integer, likes integer, post_text text, img text)
                   """)

    # Вставляем данные в таблицу
    cursor.executemany(f"INSERT INTO {name_of_table} VALUES (?,?,?,?,?,?,?,?)", data)

    # Сохраняем изменения
    conn.commit()
    conn.close()



def update_base(data, name_of_table):
    conn = sqlite3.connect("list_of_posts_base.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    try:
        # Создание таблицы
        cursor.execute(f"""CREATE TABLE {name_of_table}
                              (id text PRIMARY KEY, date text, url text, comments integer,
                               shares integer, likes integer, post_text text, img text)
                           """)

        # Вставляем данные в таблицу
        cursor.executemany(f"INSERT INTO {name_of_table} VALUES (?,?,?,?,?,?,?,?)", data)
        

    except:
        pass



    cursor.execute(f"SELECT id FROM {name_of_table}")



    id_list = cursor.fetchall()

    count_of_update = 0
    count_of_insert = 0

    for data_id in data:
        for table_id in id_list:
            if data_id[0] == table_id[0]:
                cursor.execute(f"UPDATE {name_of_table} SET comments=?, shares=?, likes=? WHERE id=?",
                               (data_id[3], data_id[4], data_id[5], data_id[0]))
                count_of_update += 1
                break

        if data_id[0] != table_id[0]:
            cursor.execute(f"INSERT INTO {name_of_table} VALUES (?,?,?,?,?,?,?,?)", data_id)
            count_of_insert += 1

    print('Добавлено ' + str(count_of_insert) + '.\nОбновлено ' + str(count_of_update) + '.')

    # Сохраняем изменения
    conn.commit()
    conn.close()





def main():

    for initial_data in getpostdata.parsing_data:
        parsing_url, page_type, name_of_table = initial_data
        resp = requests.get(parsing_url)

        story_soup = bs4.BeautifulSoup(resp.text, features='lxml')

        data_to_base = get_data(soup=story_soup, page_type=page_type, name_of_table=name_of_table)

        update_base(data_to_base, name_of_table)




if __name__ == '__main__':
    main()