import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException


# import base


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )



def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)    
    my_keyboard = ReplyKeyboardMarkup([                                     
                                    [contact_button]                                   
                                    
                                    ], resize_keyboard=True)

    return my_keyboard


def get_inline_keyboard(bot, inline_data):
    inlinekeyboard = [[InlineKeyboardButton('Да', callback_data='1'),
                        InlineKeyboardButton('Нет', callback_data=inline_data)]]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup


def handle_admin_keyboard(bot, post):
    images = post[1]      
    if images == None:
        images = ''        
    post_id = post[4]            
    kb = get_inline_keyboard(bot, images + ', ' + post_id)
    return kb


def get_user_inline_keyboard():
    inlinekeyboard = []
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup



def parse_inline_data(data):
    images_list = data.split(', ')
    post_id = images_list.pop(-1)
    if len(images_list) == 0:
        images_list = ''
    return post_id, images_list
    



def handle_text(text):
    text1 = text.replace('\n\n', '<rrrr>')
    text2 = text1.replace('\n \n', '<rrrr>')   
    text3 = text2.replace(' \n \n', '<rrrr>')
    text4 = text3.replace('\n', '\n\n')
    text5 = text4.replace('<rrrr>', '\n\n')    
    return text5


def text_to_html(text):
    html_text = text.replace('\n', '<br />')    
    return html_text



def create_telegraph_page(headline, html_content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='14021980')
    response = telegraph.create_page(
        headline, html_content=html_content
    )
    logging.info('Создали страницу в Телеграф: https://telegra.ph/{}'.format(response['path']))
    return 'https://telegra.ph/{}'.format(response['path'])


def get_image(filename, foldername):
    path = os.getcwd() + '/images/' + foldername + '/' + filename
    try:
        image = open(path, 'rb')
    except FileNotFoundError:
        image = open(os.getcwd() + '/images/' + foldername + '/noimage.gif', 'rb')
        return image
    return image


def delete_images(images_list, foldername):
    for image in images_list:
        path = path = os.getcwd() + '/images/' + foldername + '/' + image
        if os.path.exists(path):
            try:
                os.remove(path)
            except IsADirectoryError:
                logging.info('История в базе без изображения. Удалять нечего.')
        else: logging.info('Нет такого изображения: ' + image)
    

def remove_item_from_post_list(post_list, del_id):
    for post in post_list:
        post_id = post[4]
        if post_id == del_id:
            del post_list[post_list.index(post)]
            logging.info(f'Удалили строку с айди {post_id}')
    return post_list

        
def set_interval(post_count):
    interval = 11 / post_count * 3600
    return interval







if __name__ == "__main__":
    pass