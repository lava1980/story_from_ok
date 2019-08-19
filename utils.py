import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException


import base

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


def parse_inline_data(data):
    images_list = data.split(', ')
    post_id = images_list.pop(-1)
    if len(images_list) == 0:
        images_list = ''
    return post_id, images_list
    



def get_initial_data(update, user_role):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user_id = update.message.from_user.id
    role = user_role
    initial_user_data = (chat_id, first_name, last_name, user_id, role)
    logging.info('Результат функции get_initial_data: ' + initial_user_data)
    return initial_user_data

def admin_aprove():
    pass

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
    print('https://telegra.ph/{}'.format(response['path']))
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
                print('История в базе без изображения. Удалять нечего.')
        else: print('Нет такого изображения: ' + image)
    

def remove_item_from_post_list(post_list, del_id):
    for post in post_list:
        post_id = post[4]
        if post_id == del_id:
            del post_list[post_list.index(post)]
            print(f'Удалили строку с айди {post_id}')
    return post_list

        
    


if __name__ == "__main__":
    #main()
    # data = '777778887699-1.webp, 777778887699-2.webp, 777778887699'
    # parse_inline_data(data)
    aproved_post_list = [('Больше другого в на...Дегтерева', None, None, None, '70712314820019'), ('СЁМУШКА \n\n-Сёмушк...ндр Гутин', None, None, None, '70698537448883'), ('... Если долго смот...лакала...', '70760910288307-1.webp', None, None, '70760910288307'), ('"Старушечка \nСтару...я Иванова', None, None, None, '70520225985971'), ('Стою я сейчас за на...nРаевская', '70625861039539-1.webp', None, None, '70625861039539')]    
    remove_item_from_post_list(aproved_post_list, '70698537448883')