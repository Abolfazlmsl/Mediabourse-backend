from __future__ import absolute_import, unicode_literals

from celery import shared_task
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError
import jdatetime
from unidecode import unidecode
import asyncio
import aiohttp as aiohttp

from . import feed
from .models import News, Instrumentsel, Tradedetail, Trade, InstrumentInfo

# global var, used in threads
trade_detail_list = list()


@shared_task
def adding(x, y):
    return x + y;


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
        try:
            page = urlopen(url)
        except OSError:
            continue

        html_bytes = page.read()
        html = html_bytes

        soup = BeautifulSoup(html, "html.parser")

        all_news = soup.find('div', {'class': 'faq_accordion'}).find_all('div', {'class': 'item'})
        for news in all_news:
            page_url = news.find('a', href=True).get('href')
            # if 'sena.ir' in page_url:
            #     continue
            print(page_url)
            try:
                page = requests.get(page_url)
                print("passed", page)
            except requests.exceptions.ConnectionError:
                requests.status_code = "Connection refused"

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


async def request_trade_detail(client, url):
    async with client.get(url) as request:
        data1 = await request.json()

        # check error
        if 'error' in data1:
            print(f'error in {url}')
            return

        print(f"receive data of {url}, len = {len(data1['data'])}")

        for data in data1['data']:
            trade_detail_list.append(data)
            # save_tradeDetail(data)


# @database_sync_to_async
def save_tradeDetail(data):
    miss_count = 0
    obj = data

    # print(data)
    # print("--", obj['instrument']['id'])

    # ignore deleted state
    if obj['meta']['state'] == 'deleted':
        return

    try:
        obj_instrument = Instrumentsel.objects.get(id=obj['instrument']['id'])
    except Instrumentsel.DoesNotExist:
        # print('can not find; ', obj['instrument'])
        miss_count += 1
        return
    # print(obj_instrument.short_name, obj_instrument.id)
    obj_trade_detail, otd = Tradedetail.objects.get_or_create(instrument=obj_instrument)
    obj_trade, ot = Trade.objects.get_or_create(instrument=obj_instrument)

    # fill trade
    # print(obj['trade'])
    # print('date= ', obj['trade']['date_time'])
    # print('open_price= ', int(obj['trade']['open_price']))
    if 'date_time' in obj['trade']:
        obj_trade.date_time = obj['trade']['date_time']
    if 'open_price' in obj['trade']:
        obj_trade.open_price = int(obj['trade']['open_price'])
    if 'high_price' in obj['trade']:
        obj_trade.high_price = int(obj['trade']['high_price'])
    if 'low_price' in obj['trade']:
        obj_trade.low_price = int(obj['trade']['low_price'])
    if 'close_price' in obj['trade']:
        obj_trade.close_price = int(obj['trade']['close_price'])
    if 'close_price_change' in obj['trade']:
        obj_trade.close_price_change = int(obj['trade']['close_price_change'])
    if 'real_close_price' in obj['trade']:
        obj_trade.real_close_price = int(obj['trade']['real_close_price'])
    if 'real_close_price_change' in obj['trade']:
        obj_trade.real_close_price_change = int(obj['trade']['real_close_price_change'])
    if 'buyer_count' in obj['trade']:
        obj_trade.buyer_count = int(obj['trade']['buyer_count'])
    if 'trade_count' in obj['trade']:
        obj_trade.trade_count = int(obj['trade']['trade_count'])
    if 'volume' in obj['trade']:
        obj_trade.volume = int(obj['trade']['volume'])
    if 'value' in obj['trade']:
        obj_trade.value = int(obj['trade']['value'])
    obj_trade.save()

    # fill trade_detail
    if 'date_time' in obj:
        obj_trade_detail.date_time = obj['date_time']
    if 'person_buyer_count' in obj:
        obj_trade_detail.person_buyer_count = int(obj['person_buyer_count'])
    if 'company_buyer_count' in obj:
        obj_trade_detail.company_buyer_count = int(obj['company_buyer_count'])
    if 'person_buy_volume' in obj:
        obj_trade_detail.person_buy_volume = int(obj['person_buy_volume'])
    if 'company_buy_volume' in obj:
        obj_trade_detail.company_buy_volume = int(obj['company_buy_volume'])
    if 'person_seller_count' in obj:
        obj_trade_detail.person_seller_count = int(obj['person_seller_count'])
    if 'company_seller_count' in obj:
        obj_trade_detail.company_seller_count = int(obj['company_seller_count'])
    if 'person_sell_volume' in obj:
        obj_trade_detail.person_sell_volume = int(obj['person_sell_volume'])
    if 'company_sell_volume' in obj:
        obj_trade_detail.company_sell_volume = int(obj['company_sell_volume'])

    obj_trade_detail.trade = obj_trade
    obj_trade_detail.save()


@shared_task
def get_trade_detail():

    # today date
    today_date = str(jdatetime.date.today())
    today_date = today_date.replace('-', '')

    timee = "090000"
    dateTime = today_date + timee
    dateTime = "13990912" + timee  # test date
    print(dateTime)

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=-date_time@_expand=trade'
              # f'instrument.id={id_str}@instrument.id_op=in' \

    # print(api_url)

    sites = [
        api_url + '@_skip=0',
        api_url + '@_skip=100',
        api_url + '@_skip=200',
        api_url + '@_skip=300',
        api_url + '@_skip=400',
        api_url + '@_skip=500',
        api_url + '@_skip=600',
        api_url + '@_skip=700',
        api_url + '@_skip=800',
        api_url + '@_skip=900',
        api_url + '@_skip=1000',
        api_url + '@_skip=1100',
    ]

    trade_detail_list.clear()

    # with ThreadPoolExecutor(max_workers=10) as pool:
    #     pool.map(request_trade_detail, sites)
    async def scrap():
        async with aiohttp.ClientSession() as client:
            # start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_trade_detail(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            # total_time = time.time() - start_time
            # print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    #TODO: save in tradedetail model
    for itm in trade_detail_list:
        save_tradeDetail(itm)

    # print(f'successful; missied instrument {miss_count}')
    return 'successful'


@shared_task
def update_timeframe_candles():
    instruments_id = Instrumentsel.objects.all().values_list('id', flat=True)
    # host = request.get_host()
    host = ['127.0.0.1:8000'] * len(instruments_id)  # local
    # host = ['bourse-api.ir'] * len(instruments_id)  # server
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.map(feed.second_feed_tradedaily_thread, instruments_id, host)