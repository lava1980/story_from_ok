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
                    filename = 'bot.log'
                    )


# TODO Изменить клавиатуру, которая приходит юзерам
# TODO Когда админ удаляет сообщение, чтобы удалялась картинка





def main():
    mybot = Updater(settings.TOKEN)

    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается.')

    dp = mybot.dispatcher

    # mybot.job_queue.run_repeating(handlers.send_updates, interval=utils.set_interval(settings.POST_COUNT), first=300)
    mybot.job_queue.run_repeating(handlers.send_updates, interval=300, first=300)
    mybot.job_queue.run_repeating(handlers.admin_handle_posts_to_tg, interval=1800, first=1)
    # mybot.job_queue.run_daily(handlers.admin_handle_posts_to_tg, time=settings.ADMIN_TIME)
    
    admin_mode = ConversationHandler(
        entry_points = [CommandHandler('admin', handlers.admin_start)], 
        states = {
                'admin_passw': [MessageHandler(Filters.text, handlers.admin_get_passw)]
                
                
                     
        },
        fallbacks = [MessageHandler(Filters.text, handlers.dontknow, pass_user_data=True)]
    )
    dp.add_handler(CallbackQueryHandler(handlers.func))
    dp.add_handler(admin_mode)   
    dp.add_handler(CommandHandler('start', handlers.subscribe))
    dp.add_handler(CommandHandler('unsubscribe', handlers.unsubscribe))  
    
    
    
    webhook_domain = 'https://python-developer.ru'
    # webhook_domain = 'https://8a10ec94.ngrok.io'
    PORT = 5000
    
    # Использовать незарезервированный порт, например, 5000. 
    # Если порт зарезервирован, то будет 502 bad gateway
    # Порт сервера и порт в ngrok должны совпадать. В механике разберусь потом. 


    mybot.start_webhook(listen='127.0.0.1',
                    port=PORT,
                    url_path=settings.TOKEN,
                    webhook_url=f'{webhook_domain}/{settings.TOKEN}')
    
    
    mybot.idle()


if __name__ == '__main__':
    main()
