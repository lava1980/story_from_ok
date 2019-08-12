import requests, bs4, datetime, os


############ SETTINGS ##########################

parsing_data = [['https://ok.ru/profile/566394142643', 'page', 'story_holodkova'],
                ['https://ok.ru/shizofren', 'community', 'shiza_vozrozhd'],
                ['https://ok.ru/shizokhren', 'community', 'shizohrenia']#

                ]





################################################


def post_text(post_url):

    response = requests.get(post_url)
    post_soup = bs4.BeautifulSoup(response.text, features='lxml')
    list_of_text_blocks = post_soup.find_all('div', class_='media-text_cnt_tx emoji-tx textWrap')
    for text_block in list_of_text_blocks:
        text_of_post = None

        param = text_block.get('data-tid')
        id = post_url[-14:]
        if param == id:
            text_of_post = text_block.get_text()


    return text_of_post



def get_list_of_metadata(block):
    span_tags = block.find_all('span')
    list_of_metadata = []
    for span in span_tags:
        if span.has_attr('class'):
            class_value = span.get('class')
            if ('widget_count' in class_value and '__empty' not in class_value) or \
                    ('widget_count' in class_value and '__empty' in class_value):

                if '\xa0' in span.get_text():
                    span_no_spaces = span.get_text().replace('\xa0', '')
                    list_of_metadata.append(span_no_spaces)
                else:
                    list_of_metadata.append(span.get_text())

    list_of_metadata = list_of_metadata[-3:]

    return list_of_metadata



def get_valid_date(date): # преобразовывает дату в формат sqlite3

    if 'вчера' in date:
        post_time = date.replace('вчера ', '') + ':00'
        post_date = str(datetime.date.today() - datetime.timedelta(days=1))

    else:
        post_time = date + ':00'
        post_date = str(datetime.date.today())

    date_to_sql = post_date + ' ' + post_time

    return date_to_sql



def get_images(block, id, folder):
    #block = bs4.BeautifulSoup(block, features='lxml') # убрать после теста
    PATH_TO_IMG = os.getcwd() + '/images/' + folder + '/'
    if os.path.exists(PATH_TO_IMG):
        pass
    else:
        try:
            os.mkdir(PATH_TO_IMG)
        except OSError:
            print("Создать директорию %s не удалось" % PATH_TO_IMG)


    list_of_images = block.find_all('img', class_='collage_img')
    list_of_gif = block.find_all('div', class_='gif ovr-menu_soh h-mod js-gif')

    # задаём переменные, которые будут меняться в цикле for
    if len(list_of_images) != 0:
        list_images_or_gif_or_video = list_of_images
        ext = '.webp'
        img_attr = 'src'
    elif len(list_of_gif) != 0:
        list_images_or_gif_or_video = list_of_gif
        ext = '.mp4'
        img_attr = 'data-mp4src'
    else:
        list_images_or_gif_or_video = []


    if len(list_images_or_gif_or_video) != 0:

        number_of_image = 1

        list_of_images_to_base = []

        for img in list_images_or_gif_or_video:
            image = 'http://' + img.get(img_attr)[2:]

            res = requests.get(image)
            res.raise_for_status()

            i_file_name = id + '-' + str(number_of_image) + ext

            image_file = open(PATH_TO_IMG + i_file_name, 'wb')

            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()

            list_of_images_to_base.append(i_file_name)
            number_of_image += 1

        string_of_files = (', ').join(list_of_images_to_base)

        return string_of_files

    else:
        return None


