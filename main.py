from bs4 import BeautifulSoup
import os
import requests
import json
import datetime


def get_meta(event_url):
    meta_request = requests.request(method='get', url=event_url)
    requests.encoding = None
    meta_html = meta_request.content
    meta_soup = BeautifulSoup(meta_html, 'html.parser')
    meta_data = meta_soup.find('meta', {'name': 'description'}).get('content')
    return meta_data


print('get event bot start\n')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

request = requests.request(method='get', url='https://www.kr.playblackdesert.com/ko-KR/News/Notice?boardType=3')
request.encoding = None
html = request.content
soup = BeautifulSoup(html, 'html.parser')
data = soup.select('#wrap > div > div > article > div.tab_container > div > div.event_area > div.event_list')[0]
table = data.findAll('li')

today = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
events = {'events': [], 'last_update': today.strftime('%Y-%m-%d %H:%M:%S')}
for event in table:
    title = event.find_next('strong').getText().split(' (최종수정')[0].strip()
    count = event.find_next('span', {'class': 'count'}).getText().replace("  ", " ").strip()
    if count == "상시":
        deadline = "-"
    else:
        deadline = (today + datetime.timedelta(days=int(count.split(' ')[0])) - 1).strftime('%Y-%m-%d')
    url = event.find_next('a').get('href')
    thumbnail = event.find_next('img').get('src')
    meta = get_meta(url)
    events['events'].append({'title': title, 'deadline': deadline, 'count': count, 'url': url, 'thumbnail': thumbnail, 'meta': meta})

with open(os.path.join(BASE_DIR, 'events.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(events, json_file, ensure_ascii=False, indent='\t')

print('finish\n')
