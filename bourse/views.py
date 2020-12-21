import concurrent
import logging
import secrets
import string
import base64
import requests
import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import mixins, viewsets, generics, status
from rest_framework import filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import pandas as pd
from django.conf import settings
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required, user_passes_test

import jdatetime
from persiantools.jdatetime import JalaliDate
from rest_framework_simplejwt.authentication import JWTAuthentication

from mediabourse.settings import KAVENEGAR_APIKEY
from .serializers import \
    NewsListSerializer, \
    NewsRetrieveSerializer, \
    UserTechnicalSerializer, \
    TechnicalListSerializer, \
    TechnicalRetrieveSerializer, \
    WebinarSerializer, \
    FundamentalSerializer, \
    BazaarSerializer, \
    TutorialListSerializer, \
    TutorialRetrieveSerializer, \
    FileRepositorySerializer, \
    UserForgetSerializer, \
    WatchListSerializer, \
    WatchListItemSerializer, InstrumentSerializer, NotificationListSerializer, \
    NotificationDetailSerializer, TechnicalJSONUserSerializer, BugReportSerializer, NewsPodcastListSerializer, \
    NewsPodcastDetailSerializer, ArticleListSerializer, ArticleRetrieveSerializer, CommentListSerializer, \
    TradedetailSerializer, InstrumentInfoSerializer, TradedetailCurrentSerializer


from .models import Company, \
    News, \
    UserTechnical, \
    Technical, \
    Webinar, \
    HitCount, \
    Fundamental, \
    Bazaar, Tutorial, FileRepository, User, Meta, Index, \
    WatchList, WatchListItem, Instrumentsel, UserComment, Notification, TechnicalJSONUser, NewsPodcast, InstrumentInfo, \
    Article, Tradedetail, TradedetailCurrent

from .permissions import AdminAuthenticationPermission

from . import models

from . import feed

from . import candle

from . import trade_midday

from . import news_scraper


def index(request):
    return render(request, 'bourse/index.html')


def room(request, room_name):
    return render(request, 'bourse/room.html', {
        'room_name': room_name
    })


def news_scraper_view(request):
    news_scraper.scrap()
    return HttpResponse(("Text only, please."), content_type="text/plain")

    # urls = [
    #     'http://www.fipiran.com/News?Cat=1&Feeder=0',
    #     'http://www.fipiran.com/News?Cat=2&Feeder=0',
    #     'http://www.fipiran.com/News?Cat=4&Feeder=0',
    #     'http://www.fipiran.com/News?Cat=5&Feeder=0',
    # ]
    # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    #     executor.map(news_scraper.scraper, urls)
    # return HttpResponse(("Text only, please."), content_type="text/plain")


def list_trade_detail(request):
    instrument_list = request.GET.get('instrument')
    print(instrument_list)
    list = instrument_list.split("_")
    # print(list)

    instrument_db = []
    ids = []

    # get iobjects from db
    for itm in list:
        try:
            instrument_db.append(models.Instrumentsel.objects.get(short_name__iexact=itm))

        except Instrumentsel.DoesNotExist:
            pass
    # print(instrument_db)
    for itm in instrument_db:
        ids.append(itm.id)
    id_str = ','.join(str(x) for x in ids)
    # print(id_str)

    today_date = str(jdatetime.date.today())
    today_date = today_date.replace('-', '')
    timee = "090000"
    dateTime = today_date + timee
    # print(dateTime)

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?' \
              f'instrument.id={id_str}@instrument.id_op=in' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=-date_time'
    # print(api_url)

    req = requests.get(api_url)
    # # print(req.text)
    data1 = req.json()
    # print(data1)
    cntr = 0
    for itm in data1['data']:
        data1['data'][cntr]['instrument']['short_name'] = models.Instrumentsel.objects.get(
            id=itm['instrument']['id']).short_name
        print(itm['instrument']['id'])
        cntr += 1

    # print(data1)
    if 'error' in data1:
        # print(data1['error']['code'] + ' - ' + data1['error']['message'])
        return HttpResponse((data1['error']['message']), content_type="text/plain")

    return JsonResponse(data1, safe=False)


# get all instrument real-time data
def instrument_info(request):
    res = feed.get_instrument_info(request)

    cntr = 0
    for itm in res:

        # print(itm)

        #  ignore deleted items
        # if itm['meta']['state'] == 'deleted':
        #     cntr += 1
        #     continue

        isIgnore = False

        # add instrument short name
        try:
            # print(itm['instrument']['id'])
            res[cntr]['instrument']['short_name'] = Instrumentsel.objects.get(id=itm['instrument']['id']).short_name
        except Instrumentsel.DoesNotExist:
            isIgnore = True
            # print(f"2----An exception occurred in ")
            res[cntr]['instrument']['short_name'] = "صندوق سرمایه گذاری"
            # print(f'instrument {itm["instrument"]["id"]} dose not exist')
        except:
            isIgnore = True
            # print(f"1----An exception occurred in ")
        if isIgnore is True:
            cntr += 1
            continue

        # print(f"4----cont {isIgnore}")

        # print(itm)
        # add instrument info
        try:
            obj_insIfno = InstrumentInfo.objects.get(instrument_id=itm['instrument']['id'])
            res[cntr]['VolumeAvg1M'] = obj_insIfno.volAvg1M
            res[cntr]['VolumeAvg3M'] = obj_insIfno.volAvg3M
            res[cntr]['VolumeAvg12M'] = obj_insIfno.volAvg12M
        except InstrumentInfo.DoesNotExist:
            res[cntr]['VolumeAvg1M'] = -1
            res[cntr]['VolumeAvg3M'] = -1
            res[cntr]['VolumeAvg12M'] = -1
        except:
            print(f"3----An exception occurred in ")
        cntr += 1

    return JsonResponse(res, safe=False)


# get all instrument real-time data
# @login_required
# @user_passes_test(lambda u: u.is_superuser)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminAuthenticationPermission])
def ai_trade_detail(request):

    user_date = request.GET.get('date')
    is_update_daily = request.GET.get('updateDaily')

    # update one day
    if is_update_daily is not None:
        # today date
        td = jdatetime.date.today()
        td = td - timedelta(days=1)
        today_date = str(td)
        # print('today_date: ', today_date)
        today_date = today_date.replace('-', '')
        if user_date is not None:
            today_date = user_date
        timee = "090000"
        dateTime = today_date + timee
        # dateTime = "13990912" + timee
        feed.get_trade_detail_oneDay(request, dateTime)
        feed.get_trade_oneDay(request, dateTime)
    # update from first date (all data)
    else:
        list_of_instruments = models.Instrumentsel.objects.all()
        count = list_of_instruments.count()

        counter = 0
        for ins in list_of_instruments:
            print(f'-- start to scrap {counter} of {count} - {ins.short_name} --')
            feed.get_trade_detail(request, ins)
            feed.get_trade(request, ins)
            counter += 1

    # update month average values
    if True: #False:
        list_of_instruments = models.Instrumentsel.objects.all()
        counter = 0

        # one month
        td = jdatetime.date.today()
        td_date30 = td - timedelta(days=30)
        td_date30 = str(td_date30)
        td_date30 = td_date30.replace('-', '')
        timee = "090000"
        td_date30 = td_date30 + timee

        # three month
        td_date90 = td - timedelta(days=90)
        td_date90 = str(td_date90)
        td_date90 = td_date90.replace('-', '')
        td_date90 = td_date90 + timee

        # 12 month
        td_date365 = td - timedelta(days=365)
        td_date365 = str(td_date365)
        td_date365 = td_date365.replace('-', '')
        td_date365 = td_date365 + timee

        count = list_of_instruments.count()
        for ins in list_of_instruments:
            print(f'-- start to cal. avg {counter} of {count} - {ins.short_name} --')
            counter += 1

            # one month
            avg = models.Trade.objects.filter(date_time__gt=td_date30).aggregate(Avg('volume'))
            obj_info, crt = models.InstrumentInfo.objects.get_or_create(instrument=ins)
            obj_info.volAvg1M = avg['volume__avg']
            print(f'volAvg1M: {avg}')

            # three month
            avg = models.Trade.objects.filter(date_time__gt=td_date90).aggregate(Avg('volume'))
            obj_info.volAvg3M = avg['volume__avg']
            print(f'volAvg3M: {avg}')

            # 12 month
            avg = models.Trade.objects.filter(date_time__gt=td_date365).aggregate(Avg('volume'))
            obj_info.volAvg12M = avg['volume__avg']
            print(f'volAvg12M: {avg}')

            obj_info.save()

    return JsonResponse({'status': 'successful'}, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AdminAuthenticationPermission])
def ai_trade_detail_current(request):
    res = feed.get_instrument_info(request)
    if len(res) == 0:
        return JsonResponse({'status': 'LIST_EMPTY'}, safe=False)

    return JsonResponse({'status': 'successful'}, safe=False)


def get_Selected_instrument_info(request):
    instrument_id = request.GET.get('instrument')
    back_test_day = request.GET.get('day')

    # instruments_obj= models.InstrumentInfo.objects.get(ins)

    if instrument_id is None:
        return JsonResponse({'error': 'enter instrument id'}, safe=False)

    # back test day limitation
    back_test_day = int(back_test_day)
    if back_test_day > 100:
        back_test_day = 100

    # today date
    td = jdatetime.date.today()
    if back_test_day is not None:
        td = td - timedelta(days=back_test_day)

    today_date = str(td)
    today_date = today_date.replace('-', '')
    timee = "090000"
    dateTime = today_date + timee
    print(dateTime)
    # return JsonResponse({}, safe=False)

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?' \
              f'instrument.id={instrument_id}' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=-date_time@_expand=trade'

    with requests.get(api_url) as request:
        data1 = request.json()
        # print(data1)
        print(f"receive data of {api_url}, len = {len(data1['data'])}")
        # for data in data1['data']:
        # print(data)
        # instrument_info_list.append(data)

    res = data1['data']
    cntr = 0
    for itm in res:
        # add instrument short name
        try:
            # print(itm['instrument']['id'])
            res[cntr]['instrument']['short_name'] = Instrumentsel.objects.get(id=itm['instrument']['id']).short_name
        except Instrumentsel.DoesNotExist:
            res[cntr]['instrument']['short_name'] = "صندوق سرمایه گذاری"
            # print(f'instrument {itm["instrument"]["id"]} dose not exist')
        except:
            print(f"An exception occurred in ")

        # add instrument info
        try:
            obj_insIfno = InstrumentInfo.objects.get(instrument_id=itm['instrument']['id'])
            res[cntr]['VolumeAvg1M'] = obj_insIfno.volAvg1M
            res[cntr]['VolumeAvg3M'] = obj_insIfno.volAvg3M
            res[cntr]['VolumeAvg12M'] = obj_insIfno.volAvg12M
            res[cntr]['val_support'] = obj_insIfno.val_support
            res[cntr]['val_resistance'] = obj_insIfno.val_resistance
            res[cntr]['val_candleCount'] = obj_insIfno.val_candleCount
            res[cntr]['InstrumentInfo_id'] = obj_insIfno.id
        except InstrumentInfo.DoesNotExist:
            res[cntr]['VolumeAvg1M'] = -1
            res[cntr]['VolumeAvg3M'] = -1
            res[cntr]['VolumeAvg12M'] = -1
            res[cntr]['val_support'] = -1
            res[cntr]['val_resistance'] = -1
            res[cntr]['val_candleCount'] = -1
            res[cntr]['InstrumentInfo_id'] = -1
        except:
            print(f"An exception occurred in ")
        cntr += 1

    return JsonResponse(res, safe=False)


def bazaar_info(request):
    res = {}
    sites = 'http://www.tsetmc.com/Loader.aspx?ParTree=15'

    bourse_bazaar_status = ""  # وضعیت بازار
    bourse_index_total = ""  # شاخص کل
    bourse_index_total_Equal_weight = ""  # شاخص كل (هم وزن)
    bourse_bazaar_value = ""  # ارزش بازار
    bourse_date = ""  # اطلاعات قیمت
    bourse_transaction_count = ""  # تعداد معاملات
    bourse_transaction_value = ""  # ارزش معاملات
    bourse_transaction_volume = ""  # حجم معاملات

    farabourse_bazaar_status = ""  # وضعیت بازار
    farabourse_index_total = ""  # شاخص کل
    farabourse_bazaar_value = ""  # ارزش بازار اول و دوم
    farabourse_date = ""  # اطلاعات قیمت
    farabourse_transaction_count = ""  # تعداد معاملات
    farabourse_transaction_value = ""  # ارزش معاملات
    farabourse_transaction_volume = ""  # حجم معاملات

    with requests.get(sites) as request:
        data1 = request
        # print(data1)
        # print(f"receive data of {sites}, len = {(data1)}")
        res = str(data1)

        html_bytes = data1.text
        html = html_bytes

        soup = BeautifulSoup(html, "html.parser")
        res2 = soup.find_all('div', {'class': 'box1 blue tbl z1_4 h210'})
        for itm in res2:
            print('--------------------------')
            header = itm.find('div', {'class': 'header'})
            isBourse = False
            if header.get_text() == 'بازار نقدی بورس در یک نگاه':
                isBourse = True
            print(f'header: {header.get_text()} - {isBourse}')
            all_td = itm.find_all('td')
            cntr = 0
            for td in all_td:
                # bourse
                if isBourse:
                    if td.get_text() == 'وضعیت بازار':
                        bourse_bazaar_status = all_td[cntr + 1].get_text()
                    if td.get_text() == 'شاخص کل':
                        bourse_index_total = all_td[cntr + 1].get_text()
                    if td.get_text() == 'شاخص كل (هم وزن)':
                        bourse_index_total_Equal_weight = all_td[cntr + 1].get_text()
                    if td.get_text() == 'ارزش بازار':
                        bourse_bazaar_value = all_td[cntr + 1].get_text()
                    if td.get_text() == 'اطلاعات قیمت':
                        bourse_date = all_td[cntr + 1].get_text()
                    if td.get_text() == 'تعداد معاملات':
                        bourse_transaction_count = all_td[cntr + 1].get_text()
                    if td.get_text() == 'ارزش معاملات':
                        bourse_transaction_value = all_td[cntr + 1].get_text()
                    if td.get_text() == 'حجم معاملات':
                        bourse_transaction_volume = all_td[cntr + 1].get_text()
                # faraBourse
                else:
                    if td.get_text() == 'وضعیت بازار':
                        farabourse_bazaar_status = all_td[cntr + 1].get_text()
                    if td.get_text() == 'شاخص کل':
                        farabourse_index_total = all_td[cntr + 1].get_text()
                    if td.get_text() == 'ارزش بازار اول و دوم':
                        farabourse_bazaar_value = all_td[cntr + 1].get_text()
                    if td.get_text() == 'اطلاعات قیمت':
                        farabourse_date = all_td[cntr + 1].get_text()
                    if td.get_text() == 'تعداد معاملات':
                        farabourse_transaction_count = all_td[cntr + 1].get_text()
                    if td.get_text() == 'ارزش معاملات':
                        farabourse_transaction_value = all_td[cntr + 1].get_text()
                    if td.get_text() == 'حجم معاملات':
                        farabourse_transaction_volume = all_td[cntr + 1].get_text()
                cntr += 1

    info = {
        'bourse_bazaar_status': bourse_bazaar_status,
        'bourse_index_total': bourse_index_total,
        'bourse_index_total_Equal_weight': bourse_index_total_Equal_weight,
        'bourse_bazaar_value': bourse_bazaar_value,
        'bourse_date': bourse_date,
        'bourse_transaction_count': bourse_transaction_count,
        'bourse_transaction_value': bourse_transaction_value,
        'bourse_transaction_volume': bourse_transaction_volume,
        'farabourse_bazaar_status': farabourse_bazaar_status,
        'farabourse_index_total': farabourse_index_total,
        'farabourse_bazaar_value': farabourse_bazaar_value,
        'farabourse_date': farabourse_date,
        'farabourse_transaction_count': farabourse_transaction_count,
        'farabourse_transaction_value': farabourse_transaction_value,
        'farabourse_transaction_volume': farabourse_transaction_volume,
    }
    rr = {}

    return JsonResponse(info, safe=False)


def save_csv_candle(request):
    candle.feed_candle()
    return HttpResponse(("Text only, please."), content_type="text/plain")


import socket
import time
from . import tasks


def fill_data(request):
    # candle.feed_candle()
    # feed.update_timeframe_candles()
    # tasks.update_timeframe_candles()

    return HttpResponse(f"Table processed", content_type="text/plain")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
    # Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
    # For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
    # So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
    # Thanks to @stevenreddie
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SO_REUSEPORT

    # Enable broadcasting mode
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # SO_REUSEPORT

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    message = b"dariush very important message"
    count = 0
    while count < 10:
        server.sendto(message, ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)
        count = count + 1

    # table = request.GET.get('table')
    # print(f"feed {table} table")
    #
    # if table == "index":
    #     feed.feed_index()
    # elif table == "exchange":
    #     feed.feed_exchange()
    # elif table == "market":
    #     feed.feed_market()
    # elif table == "board":
    #     feed.feed_board()
    # elif table == "instrumentgroup":
    #     feed.feed_instrumentgroup()
    # elif table == "instrumentexchangestate":
    #     feed.feed_instrumentexchangestate()
    # elif table == "assettype":
    #     feed.feed_assettype()
    # elif table == "assetstate":
    #     feed.feed_assetstate()
    # elif table == "fund":
    #     feed.feed_fund()
    # elif table == "category":
    #     feed.feed_category()
    # elif table == "asset":
    #     feed.feed_asset()
    # elif table == "company":
    #     feed.feed_company()
    # elif table == "instrument":
    #     # feed.feed_instrument()
    #     feed.feed_instrument_thread()
    # elif table == "feed_trademidday":
    #     feed.feed_trademidday("164")
    # elif table == "instrumentsel":
    feed.feed_instrumentsel()
    # elif table == "search_rahavard_instruments":
    #     feed.search_rahavard_instruments()

    # feed.second_feed_tradedaily_thread(3312, '127.0.0.1:8000')
    # feed.update_timeframe_candles()
    # candle.feed_candle()
    # feed.update_candlesDay_thread(3312)

    return HttpResponse(f"Table processed", content_type="text/plain")


def test_data(request):
    print("tes test")

    url = request.GET.get('url')
    print(url)

    url = url.replace("@", "&")
    # url = 'https://v1.db.api.mabnadp.com/exchange/indexes?_sort=meta.version&meta.version=4736142543&meta.version_op=gt&_count=100&_skip=0'
    # if version is not None:
    #     url = url + '&_sort=meta.version&meta.version='+version+'&meta.version_op=gt'
    access_token = b'd19573a3602e9c3c320bd8b3b737f28f'
    header_value = base64.b64encode(access_token + b':')
    headers = {'Authorization': b'Basic ' + header_value}
    req = requests.get(url, headers=headers)
    data = req.json()
    # print(req)

    # return HttpResponse(("test only, please." ), content_type="text/plain")
    # return JsonResponse(data, safe=False)
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                        content_type="application/json")


def trade_daily(request):
    print("trade_daily")

    # 9975, 15698

    # obj = models.Instrument.objects.filter(short_name__icontains="بین")
    # print(obj)
    # for itm in obj:
    #     print(itm.short_name
    #           , ' - ', itm.id
    #           , ' - ', itm.type
    #           , ' - ', itm.market
    #           , ' - ', itm.exchange_state
    #           , ' - ', itm.board)
    #
    # return JsonResponse({}, safe=False)

    instrument = request.GET.get('instrument')
    version = request.GET.get('version')
    print(instrument, version)

    # get index candles whiout thread
    # feed.feed_tradedaily(instrument)

    # get selected instrument
    obj = models.Instrumentsel.objects.get(id=instrument)

    if obj.index is not None:
        # threading to get index candles
        feed.feed_indexdaily_thread(obj.index_id)
    else:
        # threading to get instrument candles
        feed.feed_tradedaily_thread(instrument)

    # get result candles
    trade = models.Tradedetail.objects.filter(instrument=instrument).order_by('date_time').values()

    return JsonResponse(list(trade), safe=False)


def chart_timeframes(request):
    # print("trade_daily")

    instrument = request.GET.get('instrument')
    last_date = request.GET.get('date')
    # print(instrument, last_date)

    if instrument is None:
        return JsonResponse({}, safe=False)

    host = request.get_host()

    #  update candles
    feed.second_feed_tradedaily_thread(instrument, host)

    symbol_timeframes = models.Chart.objects.filter(instrument=instrument)
    url = settings.MEDIA_ROOT.replace('\\', '/')
    parts = url.split('/')
    parts = parts[:-1]
    url = '/'.join(parts)
    res = []
    for itm in symbol_timeframes:
        # print(itm.instrument, itm.timeFrame)
        # print(itm.instrument, itm.data)
        # url2 = url + itm.data.url
        # url2 = url2.replace('/media//', '/') #diffrenet in server
        url2 = url + itm.data.url
        if host != '127.0.0.1:8000':
            url2 = url2.replace('/media/media/', '/media/')
        df = pd.read_csv(url2)  # read csv
        # json_data = df.to_json(r'./New_Products.json')

        if last_date is not None:
            # df['<DTYYYYMMDD>'] = pd.to_datetime(df['<DTYYYYMMDD>'])
            mask = (df['<DTYYYYMMDD>'] > int(last_date))
            # print("ressss")
            df = df.loc[mask]
            # print(df.loc[mask])

        json_data = df.to_json(orient='values')

        # return JsonResponse(res, safe=False)
        res.append({
            'data': json_data,
            'timeframe': itm.timeFrame,
            'instrument': itm.instrument.id
        })

    return JsonResponse(res, safe=False)
    # get index candles whiout thread
    feed.feed_tradedaily(instrument)

    # get selected instrument
    obj = models.Instrumentsel.objects.get(id=instrument)

    if obj.index is not None:
        # threading to get index candles
        feed.feed_indexdaily_thread(obj.index_id)
    else:
        # threading to get instrument candles
        feed.feed_tradedaily_thread(instrument)

    # get result candles
    trade = models.Tradedetail.objects.filter(instrument=instrument).order_by('date_time').values()

    return JsonResponse(list(trade), safe=False)


def instrument_list(request):
    print("instrument_list")

    instrument = request.GET.get('instrument')
    version = request.GET.get('version')
    print(instrument, version)

    if instrument is not None:
        trade = models.Instrumentsel.objects.filter(short_name__icontains=instrument).values('id', 'name', 'short_name')
    else:
        trade = models.Instrumentsel.objects.all().values('id', 'name', 'short_name')

    return JsonResponse(list(trade), safe=False)


def watchlist(request):
    print("watchlist")
    print(request.user)

    return JsonResponse({'error': 'enter watchlist name'}, safe=False)
    watchlist = request.POST.get('watchlist')

    if request.method == 'POST':

        watchlist = request.POST.get('watchlist')
        if watchlist is not None:
            obj_watchlist = models.WatchList(user=request.user, name=watchlist)
            obj_watchlist.save()
            return JsonResponse(list(obj_watchlist), safe=False)
        else:
            return JsonResponse({'error': 'enter watchlist name'}, safe=False)

    else:
        watchlist = request.GET.get('watchlist')
        print(watchlist)

        if watchlist is not None:
            obj_watchlist = models.WatchList.objects.filter(name__icontains=watchlist).values('id', 'name', 'user')
        else:
            obj_watchlist = models.WatchList.objects.all().values('id', 'name', 'user')

        return JsonResponse(list(obj_watchlist), safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


"""
-- Watchlist class --
"""


class WatchlistAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = WatchList.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class WatchlistRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return WatchList.objects.all()


"""
-- BugReport class --
"""


class BugReportAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BugReportSerializer
    permission_classes = []  # [IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = models.BugReport.objects.all()
        query = self.request.GET.get("q")
        query_email = self.request.GET.get("email")
        if query is not None:
            qs = qs.filter(Q(text__icontains=query)).distinct()
        if query_email is not None:
            qs = qs.filter(Q(email=query_email)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save()

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class BugReportRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BugReportSerializer
    permission_classes = []  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return models.BugReport.objects.all()


"""
-- User Json Technical class --
"""


class UserJsonTechnicalAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TechnicalJSONUserSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = TechnicalJSONUser.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        query_instrument = self.request.GET.get("instrument")
        query_share = self.request.GET.get("share")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query)).distinct()
        # fetch global share files
        if query_share is not None:
            qs = TechnicalJSONUser.objects.all()
            flag = True
            if query_share is "false":
                flag = False
            qs = qs.filter(Q(isShare=flag)).distinct()
        if query_instrument is not None:
            qs = qs.filter(Q(instrument=query_instrument)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class UserJsonTechnicalRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = TechnicalJSONUserSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return TechnicalJSONUser.objects.filter(user=self.request.user)


class instrumentTechnicaInfoAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = InstrumentInfoSerializer
    permission_classes = [] #[IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):

        qs = InstrumentInfo.objects.all()
        query = self.request.GET.get("q")
        query_instrument = self.request.GET.get("instrument")

        if query is not None:
            qs = qs.filter(Q(instrument__name__icontains=query)).distinct()

        if query_instrument is not None:
            qs = qs.filter(Q(instrument=query_instrument)).distinct()
        return qs

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class instrumentTechnicaInfoRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = InstrumentInfoSerializer
    permission_classes = [] #[IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return InstrumentInfo.objects.all()


class TradeDetailAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TradedetailSerializer
    permission_classes = [] #[IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = Tradedetail.objects.all().order_by('date_time')
        query = self.request.GET.get("q")                       # filter certain instrument based on short_name
        query_instrument = self.request.GET.get("instrument")   # filter certain instrument based on id
        query_date = self.request.GET.get("date")               # get grater than date info
        query_one_date = self.request.GET.get("oneDate")        # get certain day info
        if query is not None:
            qs = qs.filter(Q(instrument__short_name__icontains=query)).distinct()
        if query_instrument is not None:
            qs = qs.filter(Q(instrument=query_instrument)).distinct()
        if query_date is not None:
            qs = qs.filter(Q(date_time__gt=query_date)).distinct()
        if query_one_date is not None:
            qs = qs.filter(Q(date_time__icontains=query_one_date)).distinct()
        return qs


class CurrentTradeDetailAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TradedetailCurrentSerializer
    permission_classes = [] #[IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = TradedetailCurrent.objects.all()
        query = self.request.GET.get("instrument")
        if query is not None:
            qs = qs.filter(Q(instrument__id=query)).distinct()
        return qs


"""-------------------------------------------------------------------------------"""


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000



"""
-- Watchlist item class --
"""


class WatchlistItemAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListItemSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = WatchListItem.objects.filter(watch_list__user=self.request.user)
        return qs

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class WatchlistItemRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListItemSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return WatchListItem.objects.all()


class CompanyListRetrieveApiView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """List and retrieve company"""

    serializer_class = InstrumentSerializer
    queryset = Company.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['name']
    search_fields = ['name', 'short_name', 'short_english_name']
    ordering_fields = ['hit_count']
    ordering = ['-hit_count']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_instrument = Instrumentsel.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        instrument_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_instrument.hit_count = current_instrument.hit_count + 1
                    current_instrument.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        company_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Instrumentsel.DoesNotExist:
                pass

        return self.queryset


class NewsListRetrieveApiView(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    """List and retrieve news"""

    serializer_class = NewsListSerializer
    queryset = News.objects.filter(is_approved=True)
    # pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category', 'is_important', 'instrument']
    search_fields = ['instrument__name', 'title', 'tag']
    ordering_fields = ['date', 'hit_count']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return NewsRetrieveSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_news = News.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        news_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_news.hit_count = current_news.hit_count + 1
                    current_news.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        news_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except News.DoesNotExist:
                pass
        return self.queryset


class ArticleListRetrieveApiView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """List and retrieve articles"""

    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category']
    search_fields = ['title', 'tag']
    ordering_fields = ['date', 'hit_count']
    ordering = ['-date']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return ArticleRetrieveSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_article = Article.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        article_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_article.hit_count = current_article.hit_count + 1
                    current_article.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        article_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Article.DoesNotExist:
                pass
        return self.queryset


class UserTechnicalListRetrieveApiView(viewsets.GenericViewSet,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin):
    """List and retrieve technical user"""

    serializer_class = UserTechnicalSerializer
    queryset = UserTechnical.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['instrument']
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_queryset(self):
        return self.queryset.filter(is_share=True)


class TechnicalListRetrieveApiView(viewsets.GenericViewSet,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin):
    """List and retrieve technical"""

    serializer_class = TechnicalListSerializer
    queryset = Technical.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['instrument']
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_technical = Technical.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        technical_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_technical.hit_count = current_technical.hit_count + 1
                    current_technical.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        technical_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Technical.DoesNotExist:
                pass

        video = self.request.GET.get('video')
        if video == 'true':
            queryset = queryset.exclude(video__exact='')
        elif video == 'false':
            queryset = queryset.filter(video__exact='')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TechnicalRetrieveSerializer
        return self.serializer_class


class WebinarListRetrieveApiView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """List and retrieve webinar"""

    serializer_class = WebinarSerializer
    queryset = Webinar.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_webinar = Webinar.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        webinar_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_webinar.hit_count = current_webinar.hit_count + 1
                    current_webinar.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        webinar_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Webinar.DoesNotExist:
                pass

        return self.queryset


class FundamentalListRetrieveApiView(viewsets.GenericViewSet,
                                     mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin):
    """List and retrieve fundamental"""

    serializer_class = FundamentalSerializer
    queryset = Fundamental.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_fundamental = Fundamental.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        fundamental_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_fundamental.hit_count = current_fundamental.hit_count + 1
                    current_fundamental.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        fundamental_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Fundamental.DoesNotExist:
                pass

        return self.queryset


class BazaarListRetrieveApiView(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
    """List and retrieve bazaar"""

    serializer_class = BazaarSerializer
    queryset = Bazaar.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_bazaar = Bazaar.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        bazaar_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_bazaar.hit_count = current_bazaar.hit_count + 1
                    current_bazaar.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        bazaar_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Bazaar.DoesNotExist:
                pass

        return self.queryset


class TutorialListRetrieveApiView(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin):
    """List and retrieve tutorial"""

    serializer_class = TutorialListSerializer
    queryset = Tutorial.objects.filter(free=False)

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_tutorial = Tutorial.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_tutorial.hit_count = current_tutorial.hit_count + 1
                    current_tutorial.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Tutorial.DoesNotExist:
                pass

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TutorialRetrieveSerializer
        return self.serializer_class


class FreeTutorialListRetrieveApiView(viewsets.GenericViewSet,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin):
    """List and retrieve free tutorial"""

    serializer_class = TutorialListSerializer
    queryset = Tutorial.objects.filter(free=True)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['sub_category']
    search_fields = ['sub_category__title', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_tutorial = Tutorial.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_tutorial.hit_count = current_tutorial.hit_count + 1
                    current_tutorial.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk'],
                        date=date.today()
                    )
            except Tutorial.DoesNotExist:
                pass

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TutorialRetrieveSerializer
        return self.serializer_class


class FileRepositoryViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):
    serializer_class = FileRepositorySerializer
    queryset = FileRepository.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = ['type']
    ordering_fields = ['created_on']
    ordering = ['-created_on']


class ForgetPasswordAPIView(generics.CreateAPIView):
    serializer_class = UserForgetSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        phone_number = self.request.POST.get('phone_number')
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        try:
            user = get_user_model().objects.get(phone_number=phone_number)
        except get_user_model().DoesNotExist:
            return Response(
                {
                    'message': 'شماره مورد نظر یافت نشد',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        user.set_password(password)
        user.save()
        try:
            api = KavenegarAPI(KAVENEGAR_APIKEY)
            params = {'sender': '10006000660600', 'receptor': phone_number,
                      'message': 'مدیابورس\n' + 'رمزعبور جدید شما:' + password}
            api.sms_send(params)
            return Response(
                {
                    'message': 'رمز عبور به شماره موبایل وارد شده ارسال گردید',
                },
                status=status.HTTP_200_OK
            )
        except APIException:
            return Response(
                {
                    'error': 'ارسال رمز عبور با مشکل مواجه شده است',
                    'type': 'APIException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except HTTPException:
            return Response(
                {
                    'error': 'ارسال رمز عبور با مشکل مواجه شده است',
                    'type': 'HTTPException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserCommentViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin):
    """
        List, retrieve, and create user comment
    """
    serializer_class = CommentListSerializer
    queryset = UserComment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'technical',
        'fundamental',
        'company',
        'webinar',
        'news'
    ]
    ordering_fields = ['created_on', 'like']
    ordering = ['-created_on']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InstrumentListRetrieveViewSet(viewsets.GenericViewSet,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin):
    """
        List and retrieve instruments
    """

    serializer_class = InstrumentSerializer
    queryset = Instrumentsel.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['market', 'group']
    search_fields = ['name']
    ordering_fields = ['created_on', 'hit_count']


class NotificationListRetrieveViewSet(viewsets.GenericViewSet,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin):
    """
        List and retrieve notification
    """
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['company']
    search_fields = ['title']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return self.serializer_class


class NewsPodcastListRetrieveAPIView(viewsets.GenericViewSet,
                                     mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin):
    """
        List and retrieve news podcast
    """
    serializer_class = NewsPodcastListSerializer
    queryset = NewsPodcast.objects.all()
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsPodcastDetailSerializer
        return self.serializer_class


def trade_midday_function(request):
    trade_midday.main()
    return HttpResponse(("Text only, please."), content_type="text/plain")
