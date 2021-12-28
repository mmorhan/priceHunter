import threading
from telegram import Update
import BotConfig
from telegram.ext import *
from Homework import VolumeSubject, Observer_Telegram, Observer, Subject, RSISubject,main_design
observersList={}
observersList2={}
def hey(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.sendMessage(chat_id, text=f'{chat_id}, your chat id')


def start(update, context):
    update.message.reply_text("Hello, Welcome!")


def commands(update, context):
    update.message.reply_text("""
        📕 List of Commands you can use:
        /rsi RSI alert for Binance USD Futures
        /volume  Volume alert for Binance USDM
        /cancelrsi to unsubscribe RSI for Binance USDM 
        /cancelvolume to unsubscribe Volume for Binance USDM
    """)


def rsi(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in observersList.keys():
        update.message.reply_text("You subscribed to RSI alerts")
        update.message.reply_text(f'Your chat id is: {chat_id}')
        observer = Observer_Telegram(chat_id)
        observersList[chat_id]=observer
        rsiBot.attach(observer)
    else:
        update.message.reply_text(f'You are not subscribed to RSI alerts')


def volume(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in observersList2.keys():
        update.message.reply_text("You subscribed to Volume alerts")
        update.message.reply_text(f'Your chat id is: {chat_id}')
        observer = Observer_Telegram(chat_id)
        observersList2[chat_id]=observer
        volumeBot.attach(observer)
    else:
        update.message.reply_text(f'You are not subscribed to Volume alerts')


def cancelrsi(update, context):
    chat_id = update.effective_chat.id
    if chat_id in observersList.keys():
        observer = observersList.get(chat_id)
        rsiBot.detach(observer)
        update.message.reply_text(f'you unsubscribed from RSI alerts')
        observersList.pop(chat_id)
    else:
        update.message.reply_text(f'you already unsubscribed from RSI alerts')

def cancelvolume(update, context):
    chat_id = update.effective_chat.id
    if chat_id in observersList2.keys():
        observer = observersList2.get(chat_id)
        volumeBot.detach(observer)
        update.message.reply_text(f'you unsubscribed from Volume alerts')
        observersList2.pop(chat_id)
    else:
        update.message.reply_text(f'you already unsubscribed from Volume alerts')


rsiBot = RSISubject()
volumeBot = VolumeSubject()
updater = Updater(BotConfig.API_KEY, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("commands", commands))
dp.add_handler(CommandHandler("rsi", rsi))
dp.add_handler(CommandHandler("cancelrsi", cancelrsi))
dp.add_handler(CommandHandler("volume", volume))
dp.add_handler(CommandHandler("cancelvolume", cancelvolume))
dp.add_handler(CommandHandler("hey", hey))

def main_telegram():

    updater.start_polling()
    print("Running")
    updater.idle()
    print("idle")


x=threading.Thread(target=main_design)
x.start()
y=threading.Thread(target=main_telegram())
y.start()
print(threading.active_count())
