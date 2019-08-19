from glob import glob
import logging
import os
import pprint
import sqlite3
from random import choice

from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq
from telegram import User


from utils import *
import settings, base

def get_contact(bot, update):
    print(update.message.contact)    
    
  


        
def subscribe(bot, update):
    base.write_initial_data_to_base(update, 'user')
    update.message.reply_text('Вы подписались!', reply_markup=get_keyboard())


def unsubscribe(bot, update):
    user_list = base.list_from_base_column('chat_id')
    for chat_id in user_list:
        if str(update.message.chat_id) in chat_id[0]:
            base.delete_string_from_base('users.db', 'users', 'chat_id', str(update.message.chat_id))            
            update.message.reply_text('Вы отписались.')
    


def admin_start(bot, update):
    update.message.reply_text('Введите пароль админа:')
    return 'admin_passw'


def admin_get_passw(bot, update):
    if update.message.text == settings.ADMIN_PASS: 
        update.message.reply_text('Вы авторизованы как админ')
        base.write_initial_data_to_base(update, 'admin') # Сделать, чтобы запись об админе обновлялась, если он сперва авторизовался под юзером, а потом под админом
        return ConversationHandler.END # Завершаем разговор, т.к. цель достигнута -- он ввёл пароль
    else:
        update.message.reply_text('Неверный пароль')
        return 'admin_passw' # Замыкаем на том же ключе, т.е. пароль ввёл неправильно




def send_one_post_to_admin(bot, post, chat_id):
    text = handle_text(post[0])
    images = post[1]
    post_id = post[4]            
    if images != None:   
        # Передаём только первое изображение            
        bot.send_photo(chat_id=chat_id, photo=get_image(images.split(', ')[0], 'story_holodkova'))        
    else: images = ''
    if len(text) < 4096:
        bot.sendMessage(
                chat_id=chat_id, text=text, 
                reply_markup=get_inline_keyboard(bot, images + ', ' + post_id)
                )
    else: 
        tg_text = create_telegraph_page('Ещё одна история...', text_to_html(text))
        bot.sendMessage(
                chat_id=chat_id, text=tg_text, 
                reply_markup=get_inline_keyboard(bot, images + ', ' + post_id)
                )
    

def send_posts_to_admin(bot, job, chat_id):
    aproved_post_list = []
    post_list = base.handle_data('story_holodkova', 5)
    for post in post_list:
        try:
            send_one_post_to_admin(bot, post, chat_id)
            aproved_post_list.append(post)
        except TelegraphException:
            new_data = base.execute_data_from_base('story_holodkova')
            send_one_post_to_admin(bot, new_data, chat_id)
            aproved_post_list.append(new_data)

    print(aproved_post_list)
    print(len(aproved_post_list))

            

def get_aproved_list():
    pass


def admin_handle_posts_to_tg(bot, job):    
    admin_list = base.get_admin_list('chat_id')    
    for admin in admin_list:
        chat_id = admin[0]
        send_posts_to_admin(bot, job, chat_id) 


def func(bot, update):
    query = update.callback_query # Можно вывести на печать и посмотреть его
    if query.data != '1':    # В query.data хранится айди истории        
        post_id, images_list = parse_inline_data(query.data)     
        bot.delete_message(chat_id = query.message.chat_id , message_id=query.message.message_id)
        
        base.delete_string_from_base('list_of_posts_base.db', 'story_holodkova', 'id', post_id)                    
        remove_item_from_post_list(aproved_post_list, post_id)
        
        if images_list != '':
            delete_images(images_list, 'story_holodkova')
        new_data = base.execute_data_from_base('story_holodkova')
        send_one_post_to_admin(bot, new_data, query.message.chat_id)

        
# TODO По нажатию НЕТ должно:

# TODO 3. Отобрать из базы случайную историю и прислать её в чат на модерацию


def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       




@mq.queuedmessage
def send_updates(bot, job):
    users_list = base.list_from_base_column('chat_id')
    for chat_id in users_list:
        bot.sendMessage(chat_id=chat_id[0], text='Buzz!') # Вставить текст сообщений              
    