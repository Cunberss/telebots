import requests
import json


def check_valid(site:str, url: str):
    if site in url:
        try:
            resp = requests.get('https://' + url).status_code
        except Exception:
            resp = None
        return resp == 200
    return False


def get_data():
    with open('numbers.json', 'r') as file:
        data = json.load(file)
    return data


def add_url(numbers: str, site: str, url: str):
    data = get_data()
    list_url = data[numbers][site]
    if len(list_url) == 5:
        list_url.pop(0)
    list_url.append(url)
    data[numbers][site] = list_url
    with open('numbers.json','w') as file:
        json.dump(data,file)
    return True


def add_number(number: str):
    data = get_data()
    if number not in data and number.isdigit() and len(number) > 7 and number[0] == '7':
        data[number] = {'vk.com': [], 'instagram.com': []}
        with open('numbers.json','w') as file:
            json.dump(data,file)
        return True
    return False


def check_number_in_data(number:str):
    data = get_data()
    return number in data


def check_number(number:str):
    if number.isdigit() and len(number) > 7:
        data = get_data()
        if number in data:
            return data[number]['vk.com'],data[number]['instagram.com']
        else:
            return False