from glob import glob
import logging
import os
import pprint
import sqlite3
from random import choice

from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq
from telegram import User

from utils import get_keyboard, get_initial_data
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


def admin_handle_posts_to_tg(bot, job):
    post_list = base.handle_data('story_holodkova', 5)
    
    admin_list = base.get_admin_list('chat_id')
    for admin in admin_list:
        bot.sendMessage(chat_id=admin[0], text='Сообщения для админа')


def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       


@mq.queuedmessage
def send_updates(bot, job):
    users_list = base.list_from_base_column('chat_id')
    for chat_id in users_list:
        bot.sendMessage(chat_id=chat_id[0], text='Buzz!') # Вставить текст сообщений              
    