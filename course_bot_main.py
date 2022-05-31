import telebot

from course_bot import get_info

TELEGRAM_TOKEN = '5298222398:AAFSj29GXI39jyy7tLS_UoQRvneou173Rvk'

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def add_id(id):
    with open('id.txt', 'r') as f:
        data = f.read()
    if data.find(str(id)) != -1:
        return False
    else:
        with open('id.txt','a') as f:
            f.write(str(id) + ',')
            return True


def del_id(id):
    with open('id.txt', 'r') as f:
        data = f.read()
    print(data)
    print(str(id) + ',')
    new_data = data.replace(str(id) + ',', '')
    print(new_data)
    print('Что то не так')
    with open('id.txt', 'w') as f:
        f.write(new_data.strip())
    return True


@bot.message_handler(commands=['start'])
def start(message):
    if add_id(message.chat.id):
        bot.send_message(message.chat.id, 'Бот активирован.')
    else:
        bot.send_message(message.chat.id, 'Вы уже активировали бота')


@bot.message_handler(commands=['stop'])
def stop(message):
    del_id(message.chat.id)
    bot.send_message(message.chat.id,'Бот деактивирован')


@bot.message_handler(commands=['now'])
def stop(message):
    bot.send_message(message.chat.id,get_info())

bot.infinity_polling()