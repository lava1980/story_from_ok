from glob import glob
import logging
import os
import pprint
from random import choice

from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq

from utils import get_keyboard
from bot import subscribers, admins
import settings

def get_contact(bot, update):
    print(update.message.contact)    
    
  


        
def subscribe(bot, update):
    subscribers.add(update.message.chat_id)    
    update.message.reply_text('Вы подписались!', reply_markup=get_keyboard())
    print(subscribers)


def unsubscribe(bot, update):
    if update.message.chat_id in subscribers:
        subscribers.remove(update.message.chat_id)
        update.message.reply_text('Вы отписались.')
    else:
        update.message.reply_text('Вы не подписаны. Нажмите /subscibe чтобы подписаться')



def admin_start(bot, update):
    update.message.reply_text('Введите пароль админа:')
    return 'admin_passw'


def admin_get_passw(bot, update):
    if update.message.text == settings.ADMIN_PASS: 
        print(update.message)        
        # Надо добавить в базу    
        update.message.reply_text('Вы авторизованы как админ')
        return ConversationHandler.END # Завершаем разговор, т.к. цель достигнута -- он ввёл пароль
    else:
        update.message.reply_text('Неверный пароль')
        return 'admin_passw' # Замыкаем на том же ключе, т.е. пароль ввёл неправильно



''' 

{'message_id': 130, 'date': 1565881392, 'chat': {'id': 529133148, 'type': 'private', 'username': 'alex_belocki', 'first_name': 'Aleksey', 'last_name': 'Belocki'}, 'text': 'blekey88', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 529133148, 'first_name': 'Aleksey', 'is_bot': False, 'last_name': 'Belocki', 'username': 'alex_belocki', 'language_code': 'ru'}}

'''
    

def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       


@mq.queuedmessage
def send_updates(bot, job):
    for chat_id in subscribers:
        bot.sendMessage(chat_id=chat_id, text='Buzz!') # Вставить текст сообщений
