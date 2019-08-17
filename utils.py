import os

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegraph import Telegraph

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)    
    my_keyboard = ReplyKeyboardMarkup([                                     
                                    [contact_button]                                   
                                    
                                    ], resize_keyboard=True)

    return my_keyboard


def get_initial_data(update, user_role):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user_id = update.message.from_user.id
    role = user_role
    initial_user_data = (chat_id, first_name, last_name, user_id, role)
    return initial_user_data

def admin_aprove():
    pass


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
    image = open(path, 'rb')
    return image




if __name__ == "__main__":
    #main()
    get_image('1.jpg', 'story_holodkova')