from concurrent.futures import ThreadPoolExecutor
import datetime

import jdatetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from bourse import models


def get_trade_midday(sites):
    data = requests.get(sites).json()
    print(data)


def main():
    symbols_id = [
        9879,
        9991,
        9963
    ]
    now_date = datetime.datetime.now().date()
    now_time = datetime.datetime.now().time()
    jalali_date = jdatetime.date.fromgregorian(
        day=now_date.day,
        month=now_date.month,
        year=now_date.year
    )
    now_date_str = str(jalali_date).replace('-', '')
    print(now_date_str)
    now_time_str = str(now_time).split('.')[0].replace(':', '')

    now_datetime = now_date_str + now_time_str

    last_minute = str(now_time.minute - 1)
    now_time_str = str(now_time).split('.')[0].split(':')
    if len(last_minute) == 1:
        last_minute = '0' + last_minute
        now_time_str = now_time_str[0] + last_minute + now_time_str[2]
    else:
        now_time_str = now_time_str[0] + last_minute + now_time_str[2]

    one_minute_ago = now_date_str + now_time_str

    base_url = 'http://bourse-api.ir/bourse/api-test/?url='
    sites = []
    for s_id in symbols_id:
        try:
            obj = models.Instrumentsel.objects.get(id=s_id)
            company_id = obj.stock_id
            api_url = base_url + 'https://v1.db.api.mabnadp.com/exchange/intradaytrades?' + \
                      'instrument.stock.company.id=' + str(company_id) + \
                      '@date_time=' + one_minute_ago + ',' + now_datetime + '@date_time_op=bw' + '@_count=100'
            sites.append(api_url)
            print(api_url)
        except IntegrityError:
            print('Instrument not found!')
            return
        except ObjectDoesNotExist:
            print('Instrument Does Not Exist')

    with ThreadPoolExecutor(max_workers=3) as pool:
        pool.map(get_trade_midday, sites)
