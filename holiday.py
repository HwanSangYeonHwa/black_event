from bs4 import BeautifulSoup
import os
import requests
import json
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
holidays = {'holidays': []}

print('bot start\n')

dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
for m in range(3):
    target_date = dt_kst + datetime.timedelta(days=30 * m)

    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
    params = {'serviceKey': 'XGcXQ6CekCdNNzumuLbCEo6cPJHbMlzNGiMzeSW7CzaX+I6Ga6/gLlStl7/3G8sdrvsWk0ez+cM4krs6FYvpUw==',
              'solYear': str(target_date.year), 'solMonth': str(target_date.month).zfill(2)}

    response = requests.get(url, params=params)
    xml = response.content
    soup = BeautifulSoup(xml, 'html.parser')
    item = soup.findAll('item')

    for i in item:
        date_name = i.datename.string
        year = i.locdate.string[:4]
        month = i.locdate.string[4:6]
        day = i.locdate.string[-2:]
        if i.isholiday.string == 'Y':
            holidays['holidays'].append({date_name: {'year': year, 'month': month, 'day': day}})

print(holidays)

with open(os.path.join(BASE_DIR, 'holiday.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(holidays, json_file, ensure_ascii=False, indent='\t')

print('finish\n')
