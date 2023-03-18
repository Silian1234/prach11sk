import os

import pytz
import requests
from datetime import datetime, date, time, timedelta
from hashlib import sha256
from django.utils import timezone


# def keyGenerator(keyCount):
#     chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#     fullPassword = []
#     for n in range(keyCount):
#         password = ''
#         for i in range(16):
#             password += random.choice(chars)
#         if password not in fullPassword:
#             fullPassword.append(password)
#     return fullPassword


def check_code(unique_code):
    seller_id = 1115984
    api_key = '7B147C6B96084B36AC66CD2AB05F57D8'
    timestamp = int(datetime.timestamp(datetime.now()))
    get_token = {
        'seller_id': str(seller_id),
        'timestamp': timestamp,
        'sign': str(sha256(str(api_key).encode('utf-8') + str(timestamp).encode('utf-8')).hexdigest())
    }
    json = requests.post('https://api.digiseller.ru/api/apilogin', json=get_token).json()
    token = json['token']
    json = requests.get(f'https://api.digiseller.ru/api/purchases/unique-code/{unique_code}?token={token}').json()
    return json


def generate_dates():
    dates = []
    for day in range(7):
        current_date = timedelta(days=+day) + date.today()
        if day > 0 and current_date.strftime('%a') == 'Mon':
            break
        if current_date.strftime('%a') in ['Wed', 'Sun']:
            for start_hour in range(10, 23, 3):
                dates.append(
                    datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=start_hour,
                             minute=0, second=0, tzinfo=timezone.get_current_timezone()))
        else:
            for start_hour in range(12, 22, 3):
                dates.append(
                    datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=start_hour,
                             minute=0, second=0, tzinfo=timezone.get_current_timezone()))
    return dates


def get_auth_url():
    app_id = 51584619
    secure_key = '0Xmd2fuaeybsFcGplK8y'
    url = 'http://127.0.0.1:8000/profile'
    response_type = 'code'
    auth = f'https://oauth.vk.com/authorize?client_id={app_id}&client_secret={secure_key}&redirect_uri={url}&response_type={response_type}&v=5.131'
    return auth


def get_access_token(code):
    app_id = 51584619
    secure_key = '0Xmd2fuaeybsFcGplK8y'
    url = 'http://127.0.0.1:8000/profile'
    return requests.get('https://oauth.vk.com/access_token',
                        params={'client_id': app_id, 'client_secret': secure_key, 'redirect_uri': url,
                                'code': code}).json()


def get_user_info(access_token, user_id):
    return requests.get('https://api.vk.com/method/users.get',
                        params={'user_ids': user_id, 'fields': 'first_name,last_name,domain',
                                'access_token': access_token, 'v': '5.131'}).json()