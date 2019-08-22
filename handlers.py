from glob import glob
import logging
import os
import pprint
import sqlite3
from random import choice

from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq
from telegram import User

from telegraph.exceptions import TelegraphException


from utils import *
import settings, base


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )



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




def send_one_post(bot, post, chat_id, keyboard):
    logging.info(f'Отправляем пост для: {chat_id}')
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
                reply_markup=keyboard
                )
        logging.info(f'Отправили сообщение в Телеграм: {post_id}, {text[:50]}...')
    elif len(text) > 32798:
        logging.info('Не удалось отправить пост в Телеграф. Пост слишком большой.')
    else:         
        tg_text = create_telegraph_page('Ещё одна история...', text_to_html(text))
        # TODO Разбить на отдельные функции -- отправку в Телеграм и в Телеграф
        # TODO Проверку что слать делать снаружи
        bot.sendMessage(
                chat_id=chat_id, text=tg_text, 
                reply_markup=keyboard                
                )
        logging.info(f'Отправили сообщение в Телеграф: {post_id}, {text[:50]}...')

post_list = base.handle_data('story_holodkova', 5)     


def send_posts_to_admin(bot, job, chat_id):    
    for post in post_list:   
        kb = handle_admin_keyboard(bot, post)
        try:
            send_one_post(bot, post, chat_id, kb)
        except TelegraphException:
            remove_item_from_post_list(post_list, post[4])
            new_data = base.execute_data_from_base('story_holodkova')
            send_one_post(bot, new_data, chat_id, kb)
            post_list.append(new_data)

       


def admin_handle_posts_to_tg(bot, job):    
    admin_list = base.get_admin_list('chat_id')    
    for admin in admin_list:
        chat_id = admin[0]
        send_posts_to_admin(bot, job, chat_id) 


def func(bot, update):
    query = update.callback_query # Можно вывести на печать и посмотреть его
    if query.data != '1':    # В query.data хранится айди истории
        logging.info('******** АДМИН НАЖАЛ НЕТ **********')        
        post_id, images_list = parse_inline_data(query.data) 

        bot.delete_message(chat_id = query.message.chat_id , message_id=query.message.message_id)        
        base.delete_string_from_base('list_of_posts_base.db', 'story_holodkova', 'id', post_id)                    
        remove_item_from_post_list(post_list, post_id)
        logging.info(f'Удалили из списка постов неподходящее значение: {post_id}')        
        if images_list != '':
            delete_images(images_list, 'story_holodkova')        
        new_data = base.execute_data_from_base('story_holodkova')
        logging.info('Длина списка постов: ' + str(len(post_list)))
        post_list.append(new_data)
        
        kb = handle_admin_keyboard(bot, new_data)
        send_one_post(bot, new_data, query.message.chat_id, kb)        
        logging.info('После добавления новых постов длина списка: ' + str(len(post_list)))

        


def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       



def info_about_post_list_for_logging():
    post_list_for_logging = []
    for post in post_list:
        post_list_for_logging.append(post[0][:50])
    return post_list_for_logging


@mq.queuedmessage
def send_updates(bot, job):
    global post_list
    # Переменная для удобного просмотра списка постов. Только для логинга
    post_list_for_logging = info_about_post_list_for_logging()
    logging.info(f'Всего будет отправлено {str(len(post_list_for_logging))}.')
    logging.info(f'Список постов для отправки юзерам: {str(post_list_for_logging)}')
    users_list = base.list_from_base_column('chat_id')
    for user in users_list:         
        try:                
            post = post_list[0]
            logging.info(f'НОВЫЙ СПИСОК ПОСТОВ для отправки юзерам: {str(post_list_for_logging)}')
            chat_id = user[0]
            logging.info(f'Отправляем сообщения пользователю {chat_id}')  
            kb = get_user_inline_keyboard()
            send_one_post(bot, post, chat_id, kb)
        except IndexError:
            print('В списке постов нет данных. Пользователи получили все сообщения.')
            logging.info('В списке постов нет данных. Пользователи получили все сообщения.')
    if len(post_list) != 0:
        del post_list[0]
        del post_list_for_logging[0]
