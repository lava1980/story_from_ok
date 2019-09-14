import datetime
import json
import logging
import random
import sqlite3

from flask import Flask
from flask import request, redirect
from telegram import Update, Bot
from telegram.ext import Dispatcher, JobQueue, Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, \
        MessageHandler, RegexHandler, Filters
from telegram.ext import messagequeue as mq
from queue import Queue

import settings
import handlers
import utils
# from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )

logger = logging.getLogger(__name__)


bot = Bot(settings.TOKEN)
update_queue = Queue()

dp = Dispatcher(bot, update_queue)
j = JobQueue(bot)

app = Flask(__name__)




# TODO Когда админ удаляет сообщение, чтобы удалялась картинка





def main():


    # Инициализируем MessageQueue 
    dp.bot._msg_queue = mq.MessageQueue()
    dp.bot._is_messages_queued_default=True


    logging.info('Бот запускается.')



    # mybot.job_queue.run_repeating(handlers.send_updates, interval=utils.set_interval(settings.POST_COUNT), first=300)
    j.run_repeating(handlers.send_updates, interval=300, first=300)
    j.run_repeating(handlers.admin_handle_posts_to_tg, interval=1800, first=1)
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
    


main()

@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json(request.get_json(force=True), bot)

        logger.info("Update received! " + update.message.text)
        dp.process_update(update)
        update_queue.put(update)
        return "OK"
    else:
        return redirect("https://telegram.me/links_forward_bot", code=302)





if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True)