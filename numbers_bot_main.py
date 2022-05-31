import telebot
from telebot import types
import numbers_bot

TELEGRAM_TOKEN = 'token'
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Проверить номер', 'Добавить номер', 'Добавить ссылку')
    bot.send_message(message.chat.id,'Приветствую тебя! Я могу проверить номер телефона в своей базе'
                                     ' и показать его странички в социальных сетях!\n'
                                     'Ты можешь помочь мне собирать базу! Для этого отправь мне номер и его страницу'
                                     ,reply_markup=markup)
    print(message.text)


@bot.message_handler(func=lambda message: message.text == 'Проверить номер')
def start(message):
    msg = bot.reply_to(message, 'Введите номер без плюса и доп. символов, номер должен начинаться с 7')
    bot.register_next_step_handler(msg, process_check)


def process_check(message):
    info = numbers_bot.check_number(message.text)
    if info:
        vk = info[0]
        inst = info[1]
        bot.send_message(message.chat.id, 'Ссылки на страницу ВКонтакте:')
        for url in vk:
            bot.send_message(message.chat.id,url)
        bot.send_message(message.chat.id, 'Ссылки на Инстаграм:')
        for url in inst:
            bot.send_message(message.chat.id,url)
        bot.send_message(message.chat.id, 'Внимание! Ссылки могут не соответствовать действительности!')
    else:
        bot.send_message(message.chat.id, 'Информации нет или номер введен некорректно')


@bot.message_handler(func=lambda message: message.text == 'Добавить номер')
def start(message):
    msg = bot.reply_to(message, 'Введите номер без плюса и доп. символов, номер должен начинаться с 7')
    bot.register_next_step_handler(msg, process_add_number)


def process_add_number(message):
    if numbers_bot.add_number(message.text):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('VK', 'Instagram')
        msg = bot.reply_to(message, 'Добавить ссылку на соц.сеть:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_add_site,message.text)
    else:
        bot.send_message(message.chat.id,'Номер введен некорректно или он уже есть в базе')


def process_add_site(message,number):
    print(message.text)
    if message.text == 'VK' or message.text == 'Instagram':
        msg = bot.reply_to(message, 'Введите ссылку без https:')
        bot.register_next_step_handler(msg, process_add_site_two, message.text,number)
    else:
        bot.send_message(message.chat.id,'Не понимаю тебя')


def process_add_site_two(message,site,number):
    print(message.text,site,number)
    site = 'vk.com' if site == 'VK' else 'instagram.com'
    if numbers_bot.check_valid(site,message.text):
        numbers_bot.add_url(number,site,message.text)
        bot.send_message(message.chat.id,'Ссылка успешно добавлена к данному номеру')
    else:
        bot.send_message(message.chat.id,'Ссылка некорректна!')


@bot.message_handler(func=lambda message: message.text == 'Добавить ссылку')
def start(message):
    msg = bot.reply_to(message, 'Введите номер без плюса и доп. символов, номер должен начинаться с 7')
    bot.register_next_step_handler(msg, process_add_url)


def process_add_url(message):
    if numbers_bot.check_number_in_data(message.text):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('VK', 'Instagram')
        msg = bot.reply_to(message, 'Добавить ссылку на соц.сеть:', reply_markup=markup)
        bot.register_next_step_handler(msg, process_add_site, message.text)
    else:
        bot.send_message(message.chat.id,'Данного номера нет в базе, вы можете его добавить!')


bot.infinity_polling()