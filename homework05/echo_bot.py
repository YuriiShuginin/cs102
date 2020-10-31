import requests
import telebot
import config

from telebot import apihelper

apihelper.proxy = {'https': '{}'.format(config.proxy)}

bot = telebot.TeleBot(config.access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)