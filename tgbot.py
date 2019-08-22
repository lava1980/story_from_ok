import datetime
import logging
import random
import sqlite3

from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters
from telegram.ext import messagequeue as mq

import settings
from handlers import *
from utils import *


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


    logging.info('Бот запускается')

    dp = mybot.dispatcher

    # Интервал: 8640
    mybot.job_queue.run_repeating(send_updates, interval=set_interval(settings.POST_COUNT), first=180)
    # mybot.job_queue.run_repeating(send_updates, interval=20, first=180)
    mybot.job_queue.run_daily(admin_handle_posts_to_tg, time=datetime.time(9,0,0))

    dp.add_handler(MessageHandler(Filters.contact, get_contact))
    admin_mode = ConversationHandler(
        entry_points = [CommandHandler('admin', admin_start)], 
        states = {
                'admin_passw': [MessageHandler(Filters.text, admin_get_passw)]                                       
        },
        fallbacks = [MessageHandler(Filters.text, dontknow, pass_user_data=True)]
    )
    dp.add_handler(CallbackQueryHandler(func))
    dp.add_handler(admin_mode)   
    dp.add_handler(CommandHandler('start', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))  
    
    # dp.add_handler(MessageHandler(Filters.text, test_message))
    
    # webhook_domain = 'https://python-developer.ru'
    # webhook_domain = 'https://9dc689bc.ngrok.io'
    # PORT = 88
    
    # mybot.start_webhook(listen='0.0.0.0',
    #                 port=PORT,
    #                 url_path=settings.TOKEN,
    #                 webhook_url=f'{webhook_domain}:{str(PORT)}/{settings.TOKEN}')
    
    # mybot.bot.setWebhook('https://api.telegram.org/bot924321187:AAF2e8Cb051Xv-x9VySJGAkAK1An6tOimOE/setWebhook?url=https://python-developer.ru/924321187:AAF2e8Cb051Xv-x9VySJGAkAK1An6tOimOE')
    # https://api.telegram.org/bot924321187:AAF2e8Cb051Xv-x9VySJGAkAK1An6tOimOE/setWebhook?url=https://9dc689bc.ngrok.io:88/924321187:AAF2e8Cb051Xv-x9VySJGAkAK1An6tOimOE

# https://api.telegram.org/bot924321187:AAF2e8Cb051Xv-x9VySJGAkAK1An6tOimOE/getWebhookInfo
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()