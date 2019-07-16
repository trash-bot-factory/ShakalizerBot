#!/usr/bin/env python3

import telebot
import tempfile
import os
from PIL import Image

API_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(API_TOKEN)
cache = {}


@bot.message_handler(commands=['shakalize', 'shakal'])
def handle_reply(message):
    reply_to_message = message.reply_to_message
    if reply_to_message is not None and reply_to_message.content_type == 'photo':
        shakalize(bot, reply_to_message)
    elif message.chat.id in cache:
        shakalize(bot, cache[message.chat.id])
    else:
        bot.reply_to(message, "Я не помню, чтобы в этом чатике были какие-то пикчи =(")


@bot.message_handler(commands=['start'])
def log_start(message):
    print("Initialized at chat {}".format(message.chat.id))


def cache_photo(message):
    cache[message.chat.id] = message


@bot.message_handler(content_types=['photo'])
def handle_photo_tpye(message):
    cache_photo(message)
    if message.caption == None:
        return
    caption = message.caption.lower()
    if not ("шакал" in caption or "shakal" in caption):
        return
    shakalize(bot, message)


def shakalize(bot, message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    _, file_path = tempfile.mkstemp(suffix='.' + file_info.file_path.split('.')[-1])
    try:
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        image = Image.open(file_path)
        original_size = image.size
        rate = 1 / 3
        image = image.resize(map(lambda e: int(e * rate), image.size))
        image = image.resize(original_size)
        image.save(file_path, optimize=True, quality=5)
        bot.send_photo(message.chat.id, open(file_path, 'rb'),
                       reply_to_message_id=message.message_id)
    finally:
        os.remove(file_path)


if __name__ == '__main__':
    bot.polling(none_stop=True)
