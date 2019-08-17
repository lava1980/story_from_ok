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
            base.delete_string_from_base('chat_id', str(update.message.chat_id))            
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



def get_post_to_tg(bot, job, admin):
    post_list = base.handle_data('story_holodkova', 5)
    for post in post_list:
        text = handle_text(post[0])
        image = post[1]            
        if image != None:               
            bot.send_photo(chat_id=admin[0], photo=get_image(image, 'story_holodkova'))        
        if len(text) < 4096:
            bot.sendMessage(chat_id=admin[0], text=text, reply_markup=get_inline_keyboard())
        else: 
            tg_text = create_telegraph_page('Ещё одна история...', text_to_html(text))
            bot.sendMessage(chat_id=admin[0], text=tg_text, reply_markup=get_inline_keyboard())
# Передавать в клавиатуру разные цифры, чтобы можно было отследить,
# что именно он нажал. Через переменные

def get_aproved_list():
    pass


def admin_handle_posts_to_tg(bot, job):    
    admin_list = base.get_admin_list('chat_id')    
    for admin in admin_list:
        get_post_to_tg(bot, job, admin) 


def func(bot, update):
    query = update.callback_query
    if query.data == '1':
        print('Вы выбрали ДА')



def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       




@mq.queuedmessage
def send_updates(bot, job):
    users_list = base.list_from_base_column('chat_id')
    for chat_id in users_list:
        bot.sendMessage(chat_id=chat_id[0], text='Buzz!') # Вставить текст сообщений              
    