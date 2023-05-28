import requests
from datetime import datetime, date, time, timedelta
from hashlib import sha256
import zoneinfo


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


def generate_wash_dates():
    dates = []
    for day in range(7):
        current_date = timedelta(days=+day) + date.today()
        if day > 0 and current_date.strftime('%a') == 'Mon':
            break
        if current_date.strftime('%a') in ['Wed', 'Sun']:
            for start_hour in range(10, 23, 3):
                dates.append(
                    datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=start_hour,
                             minute=0, second=0, tzinfo=zoneinfo.ZoneInfo('Asia/Yekaterinburg')))
        else:
            for start_hour in range(12, 22, 3):
                dates.append(
                    datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=start_hour,
                             minute=0, second=0, tzinfo=zoneinfo.ZoneInfo('Asia/Yekaterinburg')))
    return dates


def get_auth_url():
    client_id = 51659704
    client_secret = 'IYAadzoAGaIxkmsEv14a'
    redirect_uri = 'https://www.11student.site/profile'
    response_type = 'code'
    auth = f'https://oauth.vk.com/authorize?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&response_type={response_type}&v=5.131'
    return auth


def get_access_token(code):
    client_id = 51659704
    client_secret = 'IYAadzoAGaIxkmsEv14a'
    redirect_uri = 'https://www.11student.site/profile'
    return requests.get('https://oauth.vk.com/access_token',
                        params={'client_id': client_id, 'client_secret': client_secret, 'redirect_uri': redirect_uri,
                                'code': code}).json()


def get_user_info(access_token, user_id):
    return requests.get('https://api.vk.com/method/users.get',
                        params={'user_ids': user_id, 'fields': 'first_name,last_name,domain',
                                'access_token': access_token, 'v': '5.131'}).json()


def format_people(people):
    if people % 10 in [0, 1, 5, 6, 7, 8, 9] or people in [11, 12, 13, 14]:
        return 'человек'
    return 'человека'


def format_washing_machines(washing_machines):
    if washing_machines % 10 in [2, 3, 4] and washing_machines not in [12, 13, 14]:
        return 'машинки'
    elif washing_machines % 10 in [0, 5, 6, 7, 8, 9] or washing_machines in [12, 13, 14]:
        return 'машинок'
    return 'машинка'
