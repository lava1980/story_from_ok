import datetime
import logging
import random
import sqlite3

from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters
from telegram.ext import messagequeue as mq

import settings
import handlers
import utils
# from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'tmp.log'
                    )

def send_updates(bot, update):
    logging.info('Функция send_updates корректно отработала.')


def main():
    mybot = Updater(settings.TOKEN)

    # Инициализируем MessageQueue 
    # mybot.bot._msg_queue = mq.MessageQueue()
    # mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается.')

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(send_updates, interval=7212, first=300)
    # mybot.job_queue.run_repeating(handlers.send_updates, interval=300, first=300)
    # mybot.job_queue.run_repeating(handlers.admin_handle_posts_to_tg, interval=1800, first=1)
    # mybot.job_queue.run_daily(handlers.admin_handle_posts_to_tg, time=settings.ADMIN_TIME)

    
    # dp.add_handler(MessageHandler(Filters.text, test_message))
    
    # webhook_domain = 'https://python-developer.ru'
    # webhook_domain = 'https://9dc689bc.ngrok.io'
    # PORT = 88
    
    # mybot.start_webhook(listen='0.0.0.0',
    #                 port=PORT,
    #                 url_path=settings.TOKEN,
    #                 webhook_url=f'{webhook_domain}:{str(PORT)}/{settings.TOKEN}')
    
    mybot.start_polling(poll_interval=5.0)
    mybot.idle()


if __name__ == '__main__':
    main()
