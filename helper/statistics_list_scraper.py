import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://www.fipiran.com/News?Cat=1&Feeder=0"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes

soup = BeautifulSoup(html, "html.parser")

news_elements = soup.find_all('div', {"class": "line_last_news_inner"})

news_list = []

for news in news_elements:
    a_classes = news.find_all('a', {"class": "news"})
    title = a_classes[0].find('b').get_text()
    text = a_classes[1].get_text()
    href = news.find('a', href=True).get('href')
    date = news.find('span', {'class': 'date-news'}).get_text()
    source = news.find(
        'span',
        {
            'class': 'type-news'
        }
    ).find('span').find('span').get_text()

    # print(news)

    temp = {
        "title": title,
        "text": text,
        "href": href,
        "date": date,
        "source": source
    }
    news_list.append(temp)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(news_list, f, ensure_ascii=False)
