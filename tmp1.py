from telegram.ext import messagequeue as mq
from telegram.ext import Updater

updater = Updater('TOKEN')

# Инициализируем MessageQueue 
updater.bot._msg_queue = mq.MessageQueue()
updater.bot._is_messages_queued_default=True

dp = updater.dispatcher

@mq.queuedmessage
def send_updates(bot, job):
    print('Message send')

