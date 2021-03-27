import datetime
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import requests
import os

url = 'https://tools.emailmatrix.ru/event-generator/'
myobj = {
"apikey" : "64ZFRFZAF57t3sdGsZK6102090589",
"start" : "2021-09-28 00:00",
"end" : "2021-09-28 01:00",
"timezone" : "Europe/Moscow",
"title" : "Событие",
"url" : "http://emailmatrix.ru",
"location" : "г. Рязань, 390010, ул. Октябрьская, д. 65, H264",
"description" : "Описание события",
"remind" : "2",
"remind_unit" : "h"
}
x = (requests.post(url, json= myobj)).json()
ics, google = x['ics'], x['google']

token = '1701768134:AAE8pHbVTKLTM2PdKHRqRmLkgo8ticpV3gg'  # bot constants
bot = telebot.TeleBot(token)
users = {}  # constants for db
with open('users.txt', "r") as json_file:
    users = json.load(json_file)
    #print(users.keys())

def calendar(message):
    calendar, step = DetailedTelegramCalendar(locale="ru").build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)

def save_users(users):
    with open('users.txt', 'w') as outfile:
        json.dump(users, outfile)


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
    events = InlineKeyboardButton("Мои мероприятия", callback_data="events")
    organization = InlineKeyboardButton("Организация", callback_data="organization")
    meme = InlineKeyboardButton("Мем", callback_data="meme")
    rassilka = InlineKeyboardButton("Рассылка", callback_data="rassilka")
    markup.add(events, organization, meme, rassilka)
    return markup


def organisator():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    add_event = InlineKeyboardButton('Добавить событие', callback_data='add_event')
    edit_event = InlineKeyboardButton("Редактировать событие", callback_data='edit_event')
    markup.add(add_event, edit_event)
    return markup


def tags():
    markup = InlineKeyboardMarkup(row_width=1)
    sport = InlineKeyboardButton('Спорт', callback_data='sport')
    education = InlineKeyboardButton('Образование', callback_data='education')
    roflxdlmao = InlineKeyboardButton('Меме)', callback_data = 'roflxdlmao')
    public_govno = InlineKeyboardButton('Общественная деаятельность', callback_data='public_govno')
    markup.add(sport, education, roflxdlmao, public_govno)
    return markup


def add_events(message):
    if str(message.chat.id) in os.listdir(path="users"):
        with open(f'users/{message.chat.id}/{message.text}.txt', 'w') as f:
            f.write('huy')
        print('vse')
    else:
        os.mkdir(f'users/{message.chat.id}')
        with open(f'users/{message.chat.id}/{message.text}.txt', 'w') as f:
            f.write('huy')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Привет! Пошел нахуй!\nВыбери действие:", reply_markup=menu())
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
        if call.data == "organization":
            bot.edit_message_text(f"<a href='{ics}'>apple calendar</a>\n<a href='{google}'>google calendar</a>\nВыберите действие: ",
                                  call.message.chat.id,
                                  call.message.message_id, parse_mode='HTML', reply_markup=organisator())

        if call.data == 'add_event':
            a = bot.edit_message_text('Введите название события: ',
                                  call.message.chat.id,
                                  call.message.message_id)
            bot.register_next_step_handler(a, add_events)
        bot.answer_callback_query(call.id)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)
