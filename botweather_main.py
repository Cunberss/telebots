import telebot
import time
import json
from telebot import types

import botweather

ZODIAC = {'Овен': 'aries', 'Телец': 'taurus', 'Близнецы': 'gemini', 'Рак': 'cancer', 'Лев': 'leo',
          'Дева': 'virgo', 'Весы': 'libra', 'Скорпион': 'scorpio', 'Стрелец': 'sagittarius',
          'Козерог': 'capricorn', 'Водолей': 'aquarius', 'Рыбы': 'pisces'}

CITY_ID = {'Краснодар': '542420', 'Ростов-на-Дону': '501183', 'Москва': '524901',
           'Санкт-Петербург': '498817'}

TELEGRAM_TOKEN = 'token'
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_json(filename):
    with open(filename, 'r') as file:
        users_json = json.load(file)
    return users_json


def add_userdata(id, zodiac, city):
    try:
        users_json = get_json('test.json')
    except Exception:
        users_json = {}
    users_json[id] = {'zodiac': zodiac, 'city': city}
    with open('test.json', 'w') as file:
        json.dump(users_json, file)
    return True


def delete_userdata(id):
    try:
        users_json = get_json('test.json')
    except Exception:
        users_json = {}
    if len(users_json) > 0:
        del (users_json[str(id)])
        with open('test.json', 'w') as file:
            json.dump(users_json, file)
        return True
    return True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привествую тебя! Вот что я умею: \n'
                                     'Присылать гороскоп и погоду на сегодня в любой момент, а также'
                                     ' по расписанию.\n\nМои команды ты можешь увидеть по синей кнопке'
                                     ' в левом углу экрана.\n\n'
                                     'Чтобы начать выбери "Подписаться"')


@bot.message_handler(commands=['begin'])
def start_message(message):
    try:
        users_data = get_json('test.json')
    except Exception:
        users_data = {}
    if str(message.chat.id) in users_data:
        bot.send_message(message.chat.id, 'Вы уже подписаны')
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион',
                   'Стрелец', 'Козерог', 'Водолей', 'Рыбы')
        msg = bot.reply_to(message, 'Выберите ваш знак зодиака:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)


def process_step(message):
    add_userdata(message.chat.id, ZODIAC[message.text], CITY_ID['Краснодар'])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Краснодар', 'Москва', 'Санкт-Петербург', 'Ростов-на-Дону')
    msg = bot.reply_to(message, 'Знак зодиака установлен. Выберете город:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step2)


def process_step2(message):
    users_json = get_json('test.json')
    users_json[str(message.chat.id)]['city'] = CITY_ID[message.text]
    bot.send_message(message.chat.id, 'Данные успешно сохранены! Рассылка подключена')


@bot.message_handler(commands=['stop'])
def stop_message(message):
    try:
        users_data = get_json('test.json')
    except Exception:
        users_data = {}
    if str(message.chat.id) in users_data:
        delete_userdata(message.chat.id)
        bot.send_message(message.chat.id, 'Вы отписались от рассылки')


@bot.message_handler(commands=['now'])
def now2(message):
    try:
        users_data = get_json('test.json')
    except Exception:
        users_data = {}
    if str(message.chat.id) in users_data:
        msg = botweather.info_message(users_data[str(message.chat.id)]['zodiac'],
                                      users_data[str(message.chat.id)]['city'])
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, 'Сперва заполните свои данные!')


@bot.message_handler(content_types=['text'])
def now(message):
    print(message.text)
    if message.text =='Сейчас':
        try:
            users_data = get_json('test.json')
        except Exception:
            users_data = {}
        if str(message.chat.id) in users_data:
            msg = botweather.info_message(users_data[str(message.chat.id)]['zodiac'],
                                          users_data[str(message.chat.id)]['city'])
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(message.chat.id, 'Сперва заполните свои данные!')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')


bot.infinity_polling()
