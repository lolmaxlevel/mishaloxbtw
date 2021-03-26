# -*- coding: utf-8 -*-
import datetime
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

token = '913737436:AAGmZ9TkmNaMjPATRRChaYI0XBk3hFIEWbU'  # bot constants
bot = telebot.TeleBot(token)

# users = {}  # constants for db
# with open('users.txt', "r") as json_file:
#     users = json.load(json_file)
#     print(users.keys())


# def save_users(users):
#     with open('users.txt', 'w') as outfile:
#         json.dump(users, outfile)


def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––")
            print(f'{m.chat.first_name}[{m.chat.id}][{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}]: {m.text}')
            with open('logs.txt', 'a', encoding='utf-8') as logs_file:
                logs_file.write("––––––––––––––––––––––––––––––––––––––––––––––––––––––\n")
                logs_file.write(
                    f'{m.chat.first_name}[{m.chat.id}][{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")}]: {m.text}\n')


bot.set_update_listener(listener)


def menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    settings = InlineKeyboardButton("Настройки", callback_data="settings")
    statistic = InlineKeyboardButton("Статистика", callback_data="statistic")
    statistic_by_location = InlineKeyboardButton("Статистика региона по вашей локации",
                                                 callback_data="statistic_by_location")
    news = InlineKeyboardButton("Сводка новостей", callback_data="news")
    markup.add(settings, statistic, statistic_by_location, news)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе узнать актуальную информацию о коронавирусе в "
                                      "твоем районе.\nВыбери действие:",
                     reply_markup=menu())
    if str(message.chat.id) not in users:
        users[str(message.chat.id)] = [None, False]
        save_users(users)


@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'contact'])
def error(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    print(type(message.chat.id))
    bot.send_message(message.chat.id, 'Воспользуйтесь предложенными кнопками. '
                                      'Если кнопки исчезли, введите команду /start')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "settings":
            bot.edit_message_text("Настройки:",
                                  call.message.chat.id,
                                  call.message.message_id, reply_markup=menu())

        bot.answer_callback_query(call.id)

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            print('bolt')
            time.sleep(5)
