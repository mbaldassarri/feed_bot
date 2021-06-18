# Remember: add pics folder into the root project directory and insert some pics

import logging
import telegram
from telegram.ext import Updater, CommandHandler
import os, random
import schedule
import time
import threading
import json
import datetime as dt

PICS_PATH = 'pics/'
BOT_TOKEN = 'your_telegram_bot_token_here'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def help(update, context):
    update.message.reply_text('Fai partire la magia scrivendo /start, se non ne vuoi più sapere cancella la chat e fai \'stop bot\'')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Molto bene, da adesso in poi inizia la magia!")
    threading.Thread(target=start_scheduler, args=(update, context)).start()

def start_scheduler(update, context):
    schedule.every(120).to(144).hours.do(lambda: send_pic_quote(update, context))
    #schedule.every(10).seconds.do(lambda: send_pic_quote(update, context))
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    
def send_pic(update, context):
    file_name = random.choice(os.listdir(PICS_PATH))
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(PICS_PATH + file_name, 'rb'))

def send_quote(update, context):
    with open('compliments/quotes.json') as f:
        data = json.load(f)
    current_hour = dt.datetime.now().hour
    if current_hour in range(8, 13):
        context.bot.send_message(chat_id=update.message.chat_id, text="*" + random.choice(data['compliments']['morning']) + "*", parse_mode=telegram.ParseMode.MARKDOWN)
    elif current_hour in range(13, 19):
        context.bot.send_message(chat_id=update.message.chat_id, text="*" + random.choice(data['compliments']['afternoon']) + "*", parse_mode=telegram.ParseMode.MARKDOWN)
    elif current_hour in range(19, 23):
        context.bot.send_message(chat_id=update.message.chat_id, text="*" + random.choice(data['compliments']['evening']) + "*", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="*" + random.choice(data['compliments']['anytime']) + "*", parse_mode=telegram.ParseMode.MARKDOWN)

pic_or_quote = [send_pic, send_quote]

def send_pic_quote(update, context):
    random.choice(pic_or_quote)(update, context)
    #send_pic(update, context)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
