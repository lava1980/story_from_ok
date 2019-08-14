from glob import glob
import logging
import os
from random import choice

from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq

# from utils import get_keyboard, get_user_emo, is_cat
from bot import subscribers, admins
import settings

  


        
def subscribe(bot, update):
    subscribers.add(update.message.chat_id)
    update.message.reply_text('Вы подписались!')
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
        # Надо добавить в базу    update.message.reply_text('Вы авторизованы как админ')
        update.message.reply_text('Вы авторизованы как админ')
        return ConversationHandler.END # Завершаем разговор, т.к. цель достигнута -- он ввёл пароль
    else:
        update.message.reply_text('Неверный пароль')
        return 'admin_passw' # Замыкаем на том же ключе, т.е. пароль ввёл неправильно
    

def dontknow(bot, update, user_data):
    update.message.reply_text('Не понимаю')       


@mq.queuedmessage
def send_updates(bot, job):
    for chat_id in subscribers:
        bot.sendMessage(chat_id=chat_id, text='Buzz!') # Вставить текст сообщений
