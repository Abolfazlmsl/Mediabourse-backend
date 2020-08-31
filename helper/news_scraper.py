import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

# url = "http://www.fipiran.com/News?Cat=2&Feeder=0"
#
# page = urlopen(url)
#
# html_bytes = page.read()
# html = html_bytes
#
# soup = BeautifulSoup(html, "html.parser")
#
# news_elements = soup.find_all('div', {"class": "line_last_news_inner"})
#
# news_list = []
#
# for news in news_elements:
#     a_classes = news.find_all('a', {"class": "news"})
#     title = a_classes[0].find('b').get_text()
#     text = a_classes[1].get_text()
#     href = news.find('a', href=True).get('href')
#     date = news.find('span', {'class': 'date-news'}).get_text()
#     source = news.find(
#         'span',
#         {
#             'class': 'type-news'
#         }
#     ).find('span').find('span').get_text()
#
#     # print(news)
#
#     temp = {
#         "title": title,
#         "text": text,
#         "href": href,
#         "date": date,
#         "source": source
#     }
#     news_list.append(temp)
#
# # print(news_list)
# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(news_list, f, ensure_ascii=False)
#


def get_news_text(news_url):
    page = urlopen(news_url)

    html_bytes = page.read()
    html = html_bytes

    soup = BeautifulSoup(html, "html.parser")

    if 'sena.ir' in news_url:
        sub_title = soup.find('div',  {'class': 'item-title'}).find('h4').get_text()
        title = soup.find('div',  {'class': 'item-title'}).find('h1').get_text()
        summary = soup.find('p',  {'class': 'summary'}).get_text()
        body = soup.find('div',  {'class': 'item-body'}).get_text()
        image = soup.find('figure', {'class': 'item-img'}).find('img')['src']
        date = soup.find('div', {'class': 'item-date'}).find('span').get_text()

        json_list = {
            "sub_title": sub_title,
            "title": title,
            "summary": summary,
            "body": body,
            "image": image,
            "date": date
        }

        with open('data_detail.json', 'w', encoding='utf-8') as f:
            json.dump(json_list, f, ensure_ascii=False)
    elif 'boursenews.ir' in news_url:
        sub_title = soup.find('div',  {'class': 'rutitr'}).get_text()
        title = soup.find('div',  {'class': 'title'}).find('a').get_text()
        date = soup.find('div',  {'class': 'news_nav'}).get_text()
        summmary = soup.find('div', {'class': 'subtitle'}).get_text()



    pprint(json_list)


