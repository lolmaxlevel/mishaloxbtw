import datetime
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import LSTEP, WYearTelegramCalendar
from geopy.geocoders import Nominatim
import json
import requests
import os

geolocator = Nominatim(user_agent="tg_bot")
url = 'https://tools.emailmatrix.ru/event-generator/'
myobj = {
    "apikey": "64ZFRFZAF57t3sdGsZK6102090589",
    "start": "2021-09-28 00:00",
    "end": "2021-09-28 01:00",
    "timezone": "Europe/Moscow",
    "title": "Событие",
    "url": "http://emailmatrix.ru",
    "location": "г. Рязань, 390010, ул. Октябрьская, д. 65, H264",
    "description": "Описание события",
    "remind": "2",
    "remind_unit": "h"
}
url_keys = {"sport": "Спорт",
            "education": "Образование",
            "roflxdlmao": "Развлечение",
            "public_govno": "Общественная деаятельность",
            "Спорт": "sport",
            "Образование": "education",
            "Развлечение": "roflxdlmao",
            "Общественная деаятельность": "public_govno"}

x = (requests.post(url, json=myobj)).json()
ics, google = x['ics'], x['google']

token = '1701768134:AAE8pHbVTKLTM2PdKHRqRmLkgo8ticpV3gg'  # bot constants
bot = telebot.TeleBot(token)
users = {}  # constants for db
with open('users.txt', "r") as json_file:
    users = json.load(json_file)
    # print(users.keys())


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
    settings = InlineKeyboardButton("Настройки 🛠", callback_data="settings")
    markup.add(events, organization, meme, settings)
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
    roflxdlmao = InlineKeyboardButton('Развлечения 🎬', callback_data='roflxdlmao')
    public_govno = InlineKeyboardButton('Общественная деаятельность 🦽', callback_data='public_govno')
    back = InlineKeyboardButton('Назад ◀', callback_data='back_to_menu')
    markup.add(sport, education, roflxdlmao, public_govno, back)
    return markup


def no(n=False):
    markup = InlineKeyboardMarkup(row_width=1)
    if n:
        subs = InlineKeyboardButton('Подписаться ✅ ', callback_data='subs')
    else:
        subs = InlineKeyboardButton('Отписаться ❌', callback_data='unsub')
    setup_tags = InlineKeyboardButton('Настроить тэги ✅ ', callback_data='setup_tags')
    back_to_menu = InlineKeyboardButton('Назад ◀ ', callback_data='back_to_menu')
    markup.add(subs, setup_tags, back_to_menu)
    return markup


def add_events(message):
    if str(message.chat.id) in os.listdir(path="users"):
        pathlist = os.listdir(
                        path=f"users\\{message.chat.id}")
        if f'{message.text}.txt'.lower() not in [i.lower() for i in pathlist]:
            with open(f'users\\{message.chat.id}\\{message.text}.txt',
                    'w') as f:
                print(f'{message.text}.txt'.lower(), [i.lower() for i in pathlist])
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    a = bot.edit_message_text('Укажите адрес: ', cmcd, cmmi)
                    bot.register_next_step_handler(a, lambda m: proverka(m, message.text))
                except Exception as e:
                    pass
        else:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                pass
            a = bot.edit_message_text('У вас уже есть ивент с таким названием!\nПридумайте другое: ', cmcd, cmmi)
            bot.register_next_step_handler(a, add_events)
    else:
        os.mkdir(f'users\\{message.chat.id}')
        with open(f'users\\{message.chat.id}\\{message.text}.txt', 'w') as f:
            if message.text not in os.listdir(
                    path=f"users\\{message.chat.id}"):
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                except Exception as e:
                    pass
                a = bot.edit_message_text('Укажите адрес: ', cmcd, cmmi)
                bot.register_next_step_handler(a, lambda m: proverka(m, message.text))


def proverka(message, text):
    global m1
    global t1
    try:
        location = geolocator.geocode(message.text)
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text(f'Это верный адрес?(Да/Нет)\n\n{location.address}', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_adress(m, text, message.text))
    except:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Этот адрес неверен!\nУкажите достоверный адрес: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: proverka(m, text))


def add_adress(message, text, location):
    global m1
    global t1
    m1 = message
    t1 = text
    if message.text == 'Да' or message.text == 'да':
        with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
            f.write('{adress: "' + location + '", ')
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Укажите дату: ', cmcd, cmmi)
        # bot.register_next_step_handler(a, lambda m: add_date(m, text))
        calendar, step = WYearTelegramCalendar(locale="ru").build()
        bot.edit_message_text("Выберите дату", cmcd, cmmi,
                              reply_markup=calendar)
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Укажите достоверный адрес: ', cmcd, cmmi)

        bot.register_next_step_handler(a, lambda m: proverka(m, text))


def add_date(message, text):
    with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
        f.write('date: "' + message.text + '", ')
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        pass
    a = bot.edit_message_text('Укажите время(Пример: 14:40): ', cmcd, cmmi)
    bot.register_next_step_handler(a, lambda m: add_time(m, text))


def add_time(message, text):
    try:
        time.strptime(message.text, '%H:%M')
        with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
            f.write('time: "' + message.text + '", ')
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Укажите длительность в часах: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_duration(m, text))
    except ValueError:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Укажите время в верном формате(Пример: 14:40): ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_time(m, text))


def add_duration(message, text):
    if (message.text).isdigit():
        with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
            f.write('duration: "' + message.text + '", ')
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Укажите количество мест: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_place_left(m, text))
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Вы ввели не число!\nУкажите длительность в часах: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_duration(m, text))


def add_place_left(message, text):
    if (message.text).isdigit():
        with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
            f.write('place_left: "' + message.text + '", ')
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text(
            'Выберите теги:\n1. Спорт\n2. Образование\n3. Развлечения\n4. Общественная деятельность\n\nПример: 134', cmcd,
            cmmi)
        bot.register_next_step_handler(a, lambda m: add_teg(m, text))
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text('Вы ввели не число!\nУкажите количество мест: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_place_left(m, text))


def add_teg(message, text):
    if (message.text).isdigit():
        with open('users.txt', "r") as json_file:
            users = json.load(json_file)
        tegs = ["Спорт", "Образование", "Развлечения", "Общественная деятельность"]
        tegi = []
        teg_ids = list(message.text)
        try:
            for i in teg_ids:
                tegi.append(tegs[int(i) - 1])
            with open(f'users\\{message.chat.id}\\{text}.txt', 'a') as f:
                f.write('tags: ' + str(tegi) + '}')
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                pass
            bot.edit_message_text('Ваше событие готово!\nВыберите действие:', cmcd, cmmi, reply_markup=menu())
            #for i in tegi:
            #   for j in users:
            #       if url_keys[i] in j[2]: #TODO доделать спам после нового ивента"""
        except:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                pass
            a = bot.edit_message_text(
            'Попробуйте снова!\nВыберите теги:\n1. Спорт\n2. Образование\n3. Развлечения\n4. Общественная деятельность\n\nПример: 134', cmcd,
            cmmi)
            bot.register_next_step_handler(a, lambda m: add_teg(m, text))
    else:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            pass
        a = bot.edit_message_text(
            'Вы ввели не число!\nВыберите теги:\n1. Спорт\n2. Образование\n3. Развлечения\n4. Общественная деятельность\n\nПример: 134', cmcd,
            cmmi)
        bot.register_next_step_handler(a, lambda m: add_teg(m, text))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "🐽Привет!\nВыбери действие:", reply_markup=menu())
    if str(message.chat.id) not in users:
        users[str(message.chat.id)] = [[], [], False]
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


@bot.callback_query_handler(func=WYearTelegramCalendar.func())
def cal(c):
    result, key, step = WYearTelegramCalendar(locale="ru").process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        with open(f'users\\{m1.chat.id}\\{t1}.txt', 'a') as f:
            f.write('date: "' + str(result) + '", ')
        a = bot.edit_message_text('Укажите время: ', cmcd, cmmi)
        bot.register_next_step_handler(a, lambda m: add_time(m, t1))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        global cmcd, cmmi
        cmcd = call.message.chat.id
        cmmi = call.message.message_id
        print(call.message.chat.id, call.data)
        with open(f"users.txt") as json_file:
            users = json.load(json_file)

        if call.data == "organization":
            bot.edit_message_text("Выберите действие:",
                cmcd, cmmi, reply_markup=organisator())

        elif call.data == 'add_event':
            a = bot.edit_message_text('Введите название события(название не может содержать символов: <> | \ /: " *): ',
                                      cmcd, cmmi)
            bot.register_next_step_handler(a, add_events)

        elif call.data == "settings":
            if users[str(call.message.chat.id)][2]:
                bot.edit_message_text(
                    'Ваша подписка активна! 🔔' + f"\nВаши тэги: {f', '.join([url_keys[i] for i in users[str(call.message.chat.id)][1]])}",
                    call.message.chat.id, call.message.message_id,
                    reply_markup=no())
            else:
                bot.edit_message_text(
                    'Ваша подписка не активна 🔕' + f"\nВаши тэги: {f', '.join([url_keys[i] for i in users[str(call.message.chat.id)][1]])}",
                    call.message.chat.id, call.message.message_id,
                    reply_markup=no(True))
        elif call.data == 'back_to_menu':
            bot.edit_message_text('Выберите действие:', call.message.chat.id, call.message.message_id, reply_markup=menu())

        elif call.data == 'events':
            ans = ""
            for i in range(users[str(call.message.chat.id)]):
                ans += events[i]["name"] + "Время " + events[i]["time"] + "\n"
            bot.edit_message_text(ans, call.message.chat.id, call.message_id, reply_markup=menu())
        elif call.data == "edit_event":
            bot.edit_message_text("Выберите объект для редактирования:", call.message.chat.id, call.message_id,
                                  reply_markup=event_edit())

        elif call.data == 'subs':
            bot.edit_message_text('Теперь Вы подписаны ✅', call.message.chat.id, call.message.message_id,
                                  reply_markup=menu())
            users[str(call.message.chat.id)][2] = True
            save_users(users)
        elif call.data == 'unsub':
            bot.edit_message_text('Вы больше не подписаны ❌', call.message.chat.id, call.message.message_id,
                                  reply_markup=menu())
            users[str(call.message.chat.id)][2] = False
            save_users(users)
        elif call.data == "setup_tags":
            bot.edit_message_text(f"в данный момент у вас включены такие тэги как"
                                  f" {', '.join([url_keys[i] for i in users[str(call.message.chat.id)][1]])}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=tags())
        elif str(call.data) not in users[str(call.message.chat.id)][1]:
            users[str(call.message.chat.id)][1].append(str(call.data))
            save_users(users)
            bot.edit_message_text(f"{url_keys[str(call.data)]} добавлен, теперь уведомления приходят о "
                                  f"{', '.join([url_keys[i] for i in users[str(call.message.chat.id)][1]])}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=tags())
        else:
            users[str(call.message.chat.id)][1].remove(str(call.data))
            save_users(users)
            bot.edit_message_text(f"{url_keys[str(call.data)]} убран, уведомления больше не будут приходить, остались"
                                  f" {', '.join([url_keys[i] for i in users[str(call.message.chat.id)][1]])}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=tags())

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
