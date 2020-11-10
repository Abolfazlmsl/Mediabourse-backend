import json

from django.db import IntegrityError

from .models import News
from pprint import pprint
from urllib.error import HTTPError
from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

urls = [
    'http://www.fipiran.com/News?Cat=1&Feeder=0',
    'http://www.fipiran.com/News?Cat=2&Feeder=0',
    'http://www.fipiran.com/News?Cat=4&Feeder=0',
    'http://www.fipiran.com/News?Cat=5&Feeder=0',
]


def scraper():
    for url in urls:
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes

        soup = BeautifulSoup(html, "html.parser")

        all_news = soup.find('div', {'class': 'faq_accordion'}).find_all('div', {'class': 'item'})
        for news in all_news:
            page_url = news.find('a', href=True).get('href')
            if 'sena.ir' in page_url:
                continue
            print(page_url)
            page = requests.get(page_url)

            soup = BeautifulSoup(page.content, "html.parser")

            json_list = {}
            if 'boursepress.ir' in page_url:
                try:
                    image = soup.find('div', {'class': 'news-img'}).find('img', src=True).get('src')
                    date = soup.find('div', {'class': 'news-map'}).find_all('div')[2].get_text()
                    title = soup.find('h1').get_text()
                    summary = soup.find('div', {'class': 'news-lead'}).get_text()
                    text_list = soup.find('div', {'class': 'news-text'}).find_all('p')
                    print(text_list)
                    text_list.pop()
                    text_list.pop()
                    text = list()
                    for i, j in enumerate(text_list):
                        text.append(j)
                    # short_title = soup.find('div', {'class': 'short-title'}).get_text()

                    json_list = {
                        "title": title,
                        "image": image,
                        # 'short_title': short_title,
                        "summary": summary,
                        "text": text,
                        "date": date,
                    }
                    time, date = date.split('-')
                    time_str = ''.join(time.split(':'))
                    date = date.split('/')
                    date_str = ''
                    for i, x in enumerate(date):
                        if i > 0:
                            if len(x) < 2:
                                date[i] = '0' + date[i]
                        date_str += date[i]
                    try:
                        News.objects.create(
                            title=title,
                            short_description=summary,
                            description=text,
                            pic=image,
                            date=unidecode(date_str+time_str)
                        )
                    except IntegrityError:
                        return
                    # with open('data1.json', 'w', encoding='utf-8') as f:
                    #     json.dump(json_list, f, ensure_ascii=False)
                except AttributeError:
                    continue

            elif 'isna.ir' in page_url:
                try:
                    date = soup.select_one('span.text-meta').get_text()
                    title = soup.find('div', {'class': 'item-title'}).find('h1', {'class': 'first-title'}).get_text()
                    image = soup.find('figure', {'class': 'item-img'}).find('img')['src']
                    summary = soup.find('p', {'class': 'summary'}).get_text()
                    text = soup.find('div', {'class': 'item-text'}).find_all('p')
                    print(text, 'sfaeqefefewf')
                    text.pop()
                    text.pop()
                    text.pop()
                    print(text, 'bah bha')
                    json_list = {
                        "title": title,
                        "image": image,
                        "summary": summary,
                        "text": text,
                        "date": date,
                    }
                    print(json_list)
                    date, time = date.split('/')
                    time_str = ''.join(time.split(':'))
                    date = date.split(' ')
                    date = date[0:3]
                    month_number = {
                        'فروردین': '01',
                        'اردیبهشت': '02',
                        'خرداد': '03',
                        'تیر': '04',
                        'مرداد': '05',
                        'شهریور': '06',
                        'مهر': '07',
                        'آبان': '08',
                        'آذر': '09',
                        'دی': '10',
                        'بهمن': '11',
                        'اسفند': '12',
                    }
                    date[1] = month_number[date[1]]
                    if len(date[0]) == 1:
                        date[0] = '0'+str(date[0])
                    date_str = date[2]+date[1]+date[0]
                    datetime_str = unidecode(date_str+time_str).replace(" ", "")
                    # print('daaaaaaaaaaaaaaaaaaaate', date_str, time_str, datetime_str)

                    try:
                        News.objects.create(
                            title=title,
                            short_description=summary,
                            description=text,
                            pic=image,
                            date=datetime_str
                        )
                    except IntegrityError:
                        return

                except AttributeError:
                    continue

        # pprint(json_list)
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


# def get_news_text(news_url):
#     page = urlopen(news_url)
#
#     html_bytes = page.read()
#     html = html_bytes
#
#     soup = BeautifulSoup(html, "html.parser")
#     json_list = {}
#     if 'sena.ir' in news_url:
#         sub_title = soup.find('div',  {'class': 'item-title'}).find('h4').get_text()
#         title = soup.find('div',  {'class': 'item-title'}).find('h1').get_text()
#         summary = soup.find('p',  {'class': 'summary'}).get_text()
#         body = soup.find('div',  {'class': 'item-body'}).get_text()
#         image = soup.find('figure', {'class': 'item-img'}).find('img')['src']
#         date = soup.find('div', {'class': 'item-date'}).find('span').get_text()
#
#         json_list = {
#             "sub_title": sub_title,
#             "title": title,
#             "summary": summary,
#             "body": body,
#             "image": image,
#             "date": date
#         }
#
#         with open('data_detail.json', 'w', encoding='utf-8') as f:
#             json.dump(json_list, f, ensure_ascii=False)
#     elif 'boursenews.ir' in news_url:
#         sub_title = soup.find('div',  {'class': 'rutitr'}).get_text()
#         title = soup.find('div',  {'class': 'title'}).find('a').get_text()
#         date = soup.find('div',  {'class': 'news_pdate_c'}).get_text()
#         summmary = soup.find('div', {'class': 'subtitle'}).get_text()
#         paragraph_dict = {}
#         paragraphs = soup.find('div', {'class': 'body'}).find_all('p')
#         for i, x in enumerate(paragraphs):
#             try:
#                 content = x.find('img')['src']
#                 paragraph_dict[i + 1] = 'boursenews.ir'+content
#             except TypeError:
#                 content = x.get_text()
#                 paragraph_dict[i + 1] = content
#
#         json_list = {
#             'sub_title': sub_title,
#             'title': title,
#             'date': date,
#             'summary': summmary,
#             'paragraphs': paragraph_dict
#         }
#         with open('data2.json', 'w', encoding='utf-8') as f:
#             json.dump(json_list, f, ensure_ascii=False)
#
#     elif 'boursepress.ir' in news_url:
#         image = soup.find('div', {'class': 'news-img'}).find('img')['src']
#         date = soup.find('div', {'class': 'news-map'}).find_all('div')[2].get_text()
#         title = soup.find('h1').get_text()
#         summary = soup.find('div', {'class': 'news-lead'}).get_text()
#         text_list = soup.find('div', {'class': 'news-text'}).find_all('p')
#         text_list.pop()
#         text_list.pop()
#         text = {}
#         for i, j in enumerate(text_list):
#             text[i + 1] = j.get_text()
#         short_title = soup.find('div', {'class': 'short-title'}).get_text()
#
#         json_list = {
#             "title": title,
#             "image": image,
#             'short_title': short_title,
#             "summary": summary,
#             "text": text,
#             "date": date,
#         }
#
#         with open('data1.json', 'w', encoding='utf-8') as f:
#             json.dump(json_list, f, ensure_ascii=False)
#
#
#     elif 'isna.ir' in news_url:
#         date = soup.find('li').find('span', {'class': 'text-meta'})
#         title = soup.find('div', {'class': 'item-title'}).find('h1', {'class': 'first-title'}).get_text()
#         image = soup.find('figure', {'class': 'item-img'}).find('img')['src']
#         summary = soup.find('p', {'class': 'summary'}).get_text()
#         text = soup.find('div', {'class': 'item-text'}).get_text()
#
#         json_list = {
#             "title": title,
#             "image": image,
#             "summary": summary,
#             "text": text,
#             "date": date,
#         }
#
#         with open('data3.json', 'w', encoding='utf-8') as f:
#             json.dump(json_list, f, ensure_ascii=False)
#
#     pprint(json_list)

# get_news_text('https://www.isna.ir/news/98112014886/%D8%A8%D8%A7%D9%82%DB%8C%D9%85%D8%A7%D9%86%D8%AF%D9%87-%D8%A7%DB%8C%D9%86%D8%AA%D8%B1%D9%86%D8%AA-%D9%BE%D8%B1%D8%B3%D8%B1%D8%B9%D8%AA-%D9%85%D8%B4%D8%AA%D8%B1%DB%8C%D8%A7%D9%86-%D8%AA%D8%B9%DB%8C%DB%8C%D9%86-%D8%AA%DA%A9%D9%84%DB%8C%D9%81-%D8%B4%D8%AF')
