from bs4 import BeautifulSoup
import os
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('bot start\n')

request = requests.request(method='get', url='https://www.kr.playblackdesert.com/ko-KR/News/Notice?boardType=3')
request.encoding = None
html = request.content
soup = BeautifulSoup(html, 'html.parser')
data = soup.select('#wrap > div > div > article > div.tab_container > div > div.event_area > div.event_list')[0]
table = data.findAll('li')

events = {'events': []}
for event in table:
    title = event.find_next('strong').getText().split(' (최종수정')[0].strip()
    count = event.find_next('span', {'class': 'count'}).getText().replace("  ", " ").strip()
    url = event.find_next('a').get('href')
    thumbnail = event.find_next('img').get('src')
    events['events'].append({'title': title, 'count': count, 'url': url, 'thumbnail': thumbnail})

print(events)

with open(os.path.join(BASE_DIR, 'events.json'), 'w+', encoding='utf-8') as json_file:
    json.dump(events, json_file, ensure_ascii=False, indent='\t')

print('finish\n')
