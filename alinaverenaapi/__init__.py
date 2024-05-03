from django.conf import settings
import telebot
import asyncio

bot = telebot.TeleBot(settings.TELEGRAM_ACTIVITY_BOT_KEY, parse_mode=None)

def send_message(text):
    bot.send_message(settings.TELEGRAM_CHAT_ID, text)
