import logging
import random
import sqlite3

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from telegram.ext import messagequeue as mq

import settings
from handlers import *






logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'bot.log'
                    )





subscribers = set()
admins = set()



# TODO Что надо сделать?

# TODO 1. Подписку - при подписке попадает в базу юзеров
# TODO 2. Отписку - при отписке удаляется из базы юзеров

# TODO Во время работы: Проверяет или юзер в базе
# TODO Как он будет отправлять сообщения? По какому принципу?
# TODO В базе выбрать 



def select_story_to_post(tablename): 
        conn = sqlite3.connect('list_of_posts_base.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {tablename}")
        pass

        







def my_test(bot, job):
    bot.sendMessage(chat_id=529133148, text='Spam, spam, spam!!!')
    job.interval += 5
    if job.interval > 15:
        bot.sendMessage(chat_id=529133148, text='No more spam for you')
        job.schedule_removal()



def main():
    mybot = Updater(settings.TOKEN)

    # Инициализируем MessageQueue 
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default=True


    logging.info('Бот запускается')

    dp = mybot.dispatcher

    mybot.job_queue.run_repeating(send_updates, interval=5)




    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))

    

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('amin_set', admin_subs))

    
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

      


    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()



