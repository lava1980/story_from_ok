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


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )



# TODO Чтобы все сообщения сперва приходили админу
# TODO Чтобы всем остальным приходили только те сообщения, которые одобрит админ



def select_story_to_post(tablename): 
        conn = sqlite3.connect('list_of_posts_base.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {tablename}")
        pass

        







def main():
    mybot = Updater(settings.TOKEN)

    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается')

    dp = mybot.dispatcher

    if admin_aprove() == True:
        mybot.job_queue.run_repeating(send_updates, interval=5)
    mybot.job_queue.run_daily(admin_handle_posts_to_tg, time=datetime.time(18,33,0))

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
      


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()