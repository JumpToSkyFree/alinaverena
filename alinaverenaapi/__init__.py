import telebot
from django.conf import settings
import asyncio

bot = telebot.TeleBot(settings.TELEGRAM_ACTIVITY_BOT_KEY, parse_mode=None)

loop = asyncio.get_event_loop()

async def send_message(text):
    bot.send_message(settings.TELEGRAM_CHAT_ID, text)
