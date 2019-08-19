import datetime
import logging
import random
import sqlite3

from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters
from telegram.ext import messagequeue as mq

import settings
import handlers
# from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
   

  )






def main():
    mybot = Updater(settings.TOKEN)

    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается')

    dp = mybot.dispatcher

    
    mybot.job_queue.run_repeating(handlers.send_updates, interval=5, first=180)
    mybot.job_queue.run_daily(handlers.admin_handle_posts_to_tg, time=datetime.time(19,6,0))

    dp.add_handler(MessageHandler(Filters.contact, handlers.get_contact))
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
    
    # dp.add_handler(MessageHandler(Filters.text, test_message))
      


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()