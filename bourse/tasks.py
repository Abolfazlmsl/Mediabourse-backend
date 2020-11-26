from __future__ import absolute_import, unicode_literals

from celery import shared_task
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
from unidecode import unidecode

from .models import News


@shared_task
def scrap_news():
    print('start scraping news')
    urls = [
        'http://www.fipiran.ir/News?Cat=1&Feeder=0',
        'http://www.fipiran.ir/News?Cat=2&Feeder=0',
        'http://www.fipiran.ir/News?Cat=4&Feeder=0',
        'http://www.fipiran.ir/News?Cat=5&Feeder=0',
    ]
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
                    # print(text_list)
                    # text_list.pop()
                    # text_list.pop()
                    # text = list()
                    # for i, j in enumerate(text_list):
                    #     text.append(j)
                    # short_title = soup.find('div', {'class': 'short-title'}).get_text()

                    json_list = {
                        "title": title,
                        "image": image,
                        # 'short_title': short_title,
                        "summary": summary,
                        "text": text_list,
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
                        News.objects.get_or_create(
                            title=title,
                            short_description=summary,
                            description=text_list,
                            pic=image,
                            date=unidecode(date_str + time_str),
                            reference='بورس پرس'
                        )
                    except IntegrityError:
                        continue
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
                    # print(text, 'sfaeqefefewf')
                    text.pop()
                    text.pop()
                    text.pop()
                    # print(text, 'bah bha')
                    json_list = {
                        "title": title,
                        "image": image,
                        "summary": summary,
                        "text": text,
                        "date": date,
                    }
                    # print(json_list)
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
                        date[0] = '0' + str(date[0])
                    date_str = date[2] + date[1] + date[0]
                    datetime_str = unidecode(date_str + time_str).replace(" ", "")
                    # print('daaaaaaaaaaaaaaaaaaaate', date_str, time_str, datetime_str)

                    try:
                        News.objects.get_or_create(
                            title=title,
                            short_description=summary,
                            description=text,
                            pic=image,
                            date=datetime_str,
                            reference='ایسنا'
                        )
                    except IntegrityError:
                        continue

                except AttributeError:
                    continue
    return 'successful'
