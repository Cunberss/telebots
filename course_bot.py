import requests
import telebot
import datetime
import schedule
import time

TELEGRAM_TOKEN = 'token'

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_info():
    res = requests.get('https://bcs-express.ru/kotirovki-i-grafiki').text

    brent_info = res[res.find('data-secur-code="BRENT"'):res.find('data-secur-code="BRENT"') + 450]
    brent_value = brent_info[
                  brent_info.find('<span class="quote-value _updated js-quote-value">') + 50:brent_info.find('</span>')]

    gold_info = res[res.find('data-secur-code="Gold"'):res.find('data-secur-code="Gold"') + 450]
    gold_value = gold_info[
                 gold_info.find('<span class="quote-value _updated js-quote-value">') + 50:gold_info.find('</span>')]

    usd_info = res[res.find('data-secur-code="USD000UTSTOM"'):res.find('data-secur-code="USD000UTSTOM"') + 450]
    usd_value = usd_info[
                usd_info.find('<span class="quote-value _updated js-quote-value">') + 50:usd_info.find('</span>')]

    time = datetime.datetime.now().strftime('%H:%M %d.%m')

    text = 'Текущее время: {}\n' \
           'Курс: \n\n' \
           'Нефть BRENT: {}$\n' \
           'Золото: {} US$|OZ\n' \
           'Доллар: {} RUR\n'.format(time, brent_value, gold_value, usd_value)
    return text


def send_message():
    with open('id.txt', 'r') as f:
        users = f.read()
    users_list = users.replace(',', ' ').strip().split(' ')
    for user in users_list:
        bot.send_message(user, get_info())
    return True


if __name__ == '__main__':
    schedule.every().day.at('09:02').do(send_message)
    schedule.every().day.at('12:02').do(send_message)
    schedule.every().day.at('15:02').do(send_message)
    schedule.every().day.at('18:02').do(send_message)
    schedule.every().day.at('03:19').do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)
