import requests
import telebot
import schedule
import time
import json

APP_ID = 'app_token'
TELEGRAM_TOKEN = 'token'
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_horo(sign_zodiac: str):
    response = requests.get('https://ignio.com/r/export/utf/xml/daily/com.xml').text
    horoscope = response[response.find('<{}>'.format(sign_zodiac)):response.find('</{}>'.format(sign_zodiac))]
    today_horoscope = horoscope[horoscope.find('<today>') + 7:horoscope.find('</today>')].strip()
    return today_horoscope


def get_weather(city_id: str):
    data = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                        params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': APP_ID}).json()
    weather_list = []
    for i in range(4):
        weather_list.append(data['list'][i * 2]['dt_txt'] + ' +' + str(data['list'][i * 2]['main']['temp']) + ' ' + str(
            data['list'][i * 2]['weather'][0]['description']).capitalize())
    return weather_list


def get_json(filename):
    with open(filename, 'r') as file:
        try:
            users_json = json.load(file)
        except Exception:
            users_json = {}
    return users_json


def get_course_value():
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text
    dollar_info = response[response.find('R01235'):response.find('R01235') + 128]
    dollar_value = dollar_info[dollar_info.find('<Value>') + 7:dollar_info.find('</Value>')]

    euro_info = response[response.find('R01239'):response.find('R01239') + 128]
    euro_value = euro_info[euro_info.find('<Value>') + 7:euro_info.find('</Value>')]
    return dollar_value,euro_value


def info_message(sign_zodiac: str, city_id: str):
    horoscope = get_horo(sign_zodiac)
    weather = get_weather(city_id)
    usd,eur = get_course_value()
    text = 'Прогноз погоды на сегодня:\n\n' \
           '{}\n' \
           '{}\n' \
           '{}\n' \
           '{}\n' \
           '\n' \
           'Ваш гороскоп на сегодня:\n\n' \
           '{}\n\n'\
           'Курс валюты ЦБ:\n' \
           'USD: {} р.\n'\
           'EUR: {} p.\n'.format(weather[0], weather[1], weather[2], weather[3], horoscope,usd,eur)
    return text


def send_all_user(users_json):
    for user in users_json:
        bot.send_message(user, info_message(users_json[user]['zodiac'], users_json[user]['city']))
    return True


def job():
    return send_all_user(get_json('test.json'))


if __name__ == '__main__':
    schedule.every(10).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
