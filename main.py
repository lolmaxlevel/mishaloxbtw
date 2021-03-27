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
    events = InlineKeyboardButton("Мои мероприятия 📃", callback_data="events")
    organization = InlineKeyboardButton("Организация 🗿", callback_data="organization")
    meme = InlineKeyboardButton("Мем 🛐", callback_data="meme")
    rassilka = InlineKeyboardButton("Рассылка 📩", callback_data="rassilka")
    markup.add(events, organization, meme, rassilka)
    return markup


def organisator():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    add_event = InlineKeyboardButton('Добавить событие 📎', callback_data='add_event')
    edit_event = InlineKeyboardButton("Редактировать событие ✂", callback_data='edit_event')
    back_to_menu = InlineKeyboardButton('Назад ◀', callback_data='back_to_menu')
    markup.add(add_event, edit_event, back_to_menu)
    return markup


def tags():
    markup = InlineKeyboardMarkup(row_width=1)
    sport = InlineKeyboardButton('Спорт ⚽', callback_data='sport')
    education = InlineKeyboardButton('Образование 📝', callback_data='education')
    roflxdlmao = InlineKeyboardButton('Развлечения 🎬', callback_data = 'roflxdlmao')
    public_govno = InlineKeyboardButton('Общественная деаятельность 🦽', callback_data='public_govno')
    markup.add(sport, education, roflxdlmao, public_govno)
    return markup


def yes():
    markup = InlineKeyboardMarkup()
    subs = InlineKeyboardButton('Подписаться ✅ ', callback_data='subs')
    back_to_menu = InlineKeyboardButton('Назад ◀', callback_data='back_to_menu')
    markup.add(subs, back_to_menu)
    return markup


def no():
    markup = InlineKeyboardMarkup()
    subs = InlineKeyboardButton('Отписаться ❌', callback_data='unsub')
    back_to_menu = InlineKeyboardButton('Назад ◀ ', callback_data='back_to_menu')
    markup.add(subs, back_to_menu)
    return markup


def add_events(message):
    if str(message.chat.id) in os.listdir(path="C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users"):
        with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{message.text}.txt', 'w') as f:
            if message.text not in os.listdir(path=f"C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}"):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except Exception as e:
                    pass
                a = bot.edit_message_text('Укажите адрес: ', cmcd, cmmi)
                bot.register_next_step_handler(a, lambda m: add_adress(m, message.text))
    else:
        os.mkdir(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}')
        with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{message.text}.txt', 'w') as f:
            if message.text not in os.listdir(path=f"C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}"):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except Exception as e:
                    pass
                a = bot.edit_message_text('Укажите адрес: ', cmcd, cmmi)
                bot.register_next_step_handler(a, lambda m: add_adress(m, message.text))

def add_adress(message, text):
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('{adress: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Укажите дату: ', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_date(m, text))

def add_date(message, text):
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('date: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Укажите время: ', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_time(m, text))

def add_time(message, text):
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('time: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Укажите длительность в часах: ', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_duration(m, text))

def add_duration(message, text):
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('duration: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Укажите количество мест: ', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_place_left(m, text))

def add_place_left(message, text):
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('place_left: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Выберите теги:\n1. Спорт\n2. Образование\n3. Развлечения\n4. Общественная деятельность\n\nПример: 134', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_teg(m, text))

def add_teg(message, text):
    tegs = ["Спорт", "Образование", "Развлечения", "Общественная деятельность"]
    tegi = []
    teg_ids = list(message.text)
    for i in teg_ids:
        tegi.append(tegs[int(i)-1])
    with open(f'C:\\Users\\User\\Desktop\\mishaloxbtw-main\\users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('tags: "' + str(tegi) + '"}')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    bot.edit_message_text('Ваше событие готово!\nВыберите действие:', cmcd, cmmi, reply_markup=menu())


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "🐽Привет! Пошел нахуй!🐽\nВыбери действие:", reply_markup=menu())
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
        global cmcd, cmmi
        cmcd = call.message.chat.id
        cmmi = call.message.message_id
        if call.data == "organization":
            bot.edit_message_text(f"<a href='{ics}'>apple calendar</a>\n<a href='{google}'>google calendar</a>\nВыберите действие: ",
                                  cmcd, cmmi, parse_mode='HTML', reply_markup=organisator())
        if call.data == 'add_event':
            a = bot.edit_message_text('Введите название события: ',
                                  cmcd, cmmi)
            bot.register_next_step_handler(a, add_events)

        elif call.data == 'back_to_menu':
            bot.edit_message_text('Пошел нахуй', call.message.chat.id, call.message.message_id, reply_markup=menu())

        if call.data == 'events':
            ans = ""
            with open('users.txt', "r") as json_file:
                users = json.load(json_file)
                for i in range(users[call.message.chat.id]):
                    ans += events[i]["name"] + "Время " + events[i]["time"] + "\n"
            bot.edit_message_text(ans, call.message.chat.id, call.message_id, reply_markup=menu())
        if call.data == "edit_event":
            bot.edit_message_text("Что редактировать будем епта?)", call.message.chat.id, call.message_id, reply_markup=event_edit())

        if call.data == 'rassilka':
            if users[str(call.message.chat.id)][1]:
                bot.edit_message_text('Ваша подписка активна! 🔔', call.message.chat.id, call.message.message_id, reply_markup=no())
            else:
                bot.edit_message_text('Ваша подписка не активна 🔕', call.message.chat.id, call.message.message_id, reply_markup=yes())

        if call.data == 'subs':
                bot.edit_message_text('Вы подписаны ✅', call.message.chat.id, call.message.message_id, reply_markup=menu())
                users[str(call.message.chat.id)][1] = True
        if call.data == 'unsub':
                bot.edit_message_text('Вы не подписаны ❌', call.message.chat.id, call.message.message_id, reply_markup=menu())
                users[str(call.message.chat.id)][1] = False


        bot.answer_callback_query(call.id)
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f'i sleep   {e}')
            time.sleep(5)
