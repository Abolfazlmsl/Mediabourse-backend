import asyncio
import json

import aiohttp as aiohttp
from django.db import IntegrityError
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor
import jdatetime
import requests
import time
import pandas as pd
from django.utils import timezone

from .models import Meta, Index, Exchange
from . import models
from django.conf import settings
from datetime import date, timedelta, datetime
from persiantools.jdatetime import JalaliDate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .Utils import UtilFunc
from channels.db import database_sync_to_async

base_url = 'http://bourse-api.ir/bourse/api-test/?url='


def feed_index():
    offset = 0
    step = 50
    is_has_next = True

    #  check model is empty or not
    if Index.objects.count() > 0:
        last_index_meta_version = Index.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + 'https://v1.db.api.mabnadp.com/exchange/indexes?' + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + 'https://v1.db.api.mabnadp.com/exchange/indexes?'

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        print(req)
        data1 = req.json()
        print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        for data in data1['data']:
            print(data)
        # return

        for data in data1['data']:
            print(data)
            print('check: ', int(data['meta']['version']))
            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            insert_date_time=data['meta']['insert_date_time'], type=data['meta']['type'])
            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']

            ch = Meta.objects.filter(version=obj_meta.version)
            print("ch,", len(ch))
            if len(ch) > 0:
                print('duplicate')
                print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj_index = Index(meta=obj_meta, code=data['code'], name=data['name'], english_name=data['english_name'],
                              short_name=data['short_name'], english_short_name=data['english_short_name'],
                              fingilish_name=data['fingilish_name'], fingilish_short_name=data['fingilish_short_name'],
                              id=data['id'])
            obj_index.save()
            # print('saved ', obj_meta.version)
            # break


def feed_exchange():
    offset = 0
    step = 50
    is_has_next = True

    #  check model is empty or not
    if Exchange.objects.count() > 0:
        last_index_meta_version = Exchange.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + 'https://v1.db.api.mabnadp.com/exchange/exchanges?' + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + 'https://v1.db.api.mabnadp.com/exchange/exchanges?'

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        print(req)
        data1 = req.json()
        print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        for data in data1['data']:
            print(data)
        # return

        for data in data1['data']:
            print(data)
            print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            insert_date_time=data['meta']['insert_date_time'], type=data['meta']['type'])
            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']

            ch = Meta.objects.filter(version=obj_meta.version)
            print("ch,", len(ch))
            if len(ch) > 0:
                print('duplicate')
                print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj_exchange = Exchange(meta=obj_meta, title=data['title'], english_title=data['english_title'],
                                    code=data['code'], id=data['id'])
            obj_exchange.save()


def feed_market():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Market
    api_url = 'https://v1.db.api.mabnadp.com/exchange/markets?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        # print(req)
        data1 = req.json()
        # print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        for data in data1['data']:
            print(data)
        # return

        for data in data1['data']:
            print(data)
            print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            ch = Meta.objects.filter(version=obj_meta.version)
            print("ch,", len(ch))
            if len(ch) > 0:
                print('duplicate')
                print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], english_title=data['english_title'],
                        code=data['code'], id=data['id'])
            obj.save()


def feed_board():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Board
    api_url = 'https://v1.db.api.mabnadp.com/exchange/boards?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        # print(req)
        data1 = req.json()
        # print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        for data in data1['data']:
            print(data)
        # return

        for data in data1['data']:
            print(data)
            print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            ch = Meta.objects.filter(version=obj_meta.version)
            print("ch,", len(ch))
            if len(ch) > 0:
                print('duplicate')
                print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], english_title=data['english_title'],
                        code=data['code'], id=data['id'])
            obj.save()


def feed_instrumentgroup():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Instrumentgroup
    api_url = 'https://v1.db.api.mabnadp.com/exchange/instrumentgroups?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        # print(req)
        data1 = req.json()
        # print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        for data in data1['data']:
            print(data)
        # return

        for data in data1['data']:
            print(data)
            print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            ch = Meta.objects.filter(version=obj_meta.version)
            print("ch,", len(ch))
            if len(ch) > 0:
                print('duplicate')
                print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], code=data['code'], id=data['id'])
            if 'english_title' in data:
                obj.english_title = data['english_title']
            obj.save()


def feed_instrumentexchangestate():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Instrumentexchangestate
    api_url = 'https://v1.db.api.mabnadp.com/exchange/instrumentexchangestates?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        # print(req)
        data1 = req.json()
        # print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        # for data in data1['data']:
        #     print(data)
        # return

        for data in data1['data']:
            # print(data)
            # print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # ch = Meta.objects.filter(version=obj_meta.version)
            # print("ch,", len(ch))
            # if len(ch) > 0:
            #     print('duplicate')
            #     print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], id=data['id'])
            obj.save()


def feed_assettype():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Assettype
    api_url = 'https://v1.db.api.mabnadp.com/exchange/assettypes?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        # print('--------------- ', offset, ' ------------------------- ', offset)
        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''

        # print("check update ", get_data)

        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict

        req = requests.get(get_data2)
        # print(req)
        data1 = req.json()
        # print(data1)

        # print(len(data1['data']))
        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
            # print("offset: ", offset)
        else:
            is_has_next = False

        # print(data1['data'])
        # for data in data1['data']:
        #     print(data)
        # return

        for data in data1['data']:
            # print(data)
            # print('check: ', int(data['meta']['version']))

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # ch = Meta.objects.filter(version=obj_meta.version)
            # print("ch,", len(ch))
            # if len(ch) > 0:
            #     print('duplicate')
            #     print(ch[0].version)

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], code=data['code'], id=data['id'])
            if 'english_title' in data:
                obj.english_title = data['english_title']
            obj.save()


def feed_assetstate():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Assetstate
    api_url = 'https://v1.db.api.mabnadp.com/exchange/assetstates?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta, title=data['title'], id=data['id'])
            if 'english_title' in data:
                obj.english_title = data['english_title']
            obj.save()


def feed_fund():
    offset = 0
    step = 50
    is_has_next = True

    model = models.Fund
    api_url = 'https://v1.db.api.mabnadp.com/fund/funds?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])
            obj_state = models.Assetstate.objects.get(id=data['state']['id'])
            if 'exchange' in data:
                obj_exchange = models.Exchange.objects.get(id=data['exchange']['id'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , state=obj_state
                        , id=data['id']
                        , name=data['name']
                        , short_name=data['short_name']
                        , inception_date=data['inception_date']

                        )
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            if 'english_name' in data:
                obj.english_name = data['english_name']
            if 'website' in data:
                obj.website = data['website']
            if 'trade_symbol' in data:
                obj.trade_symbol = data['trade_symbol']
            if 'custodian' in data:
                obj.custodian_name = data['custodian']['name']
            if 'investment_manager' in data:
                obj.investment_manager_name = data['investment_manager']['name']
            if 'liquidity_guarantor' in data:
                obj.liquidity_guarantor_name = data['liquidity_guarantor']['name']
            if 'manager' in data:
                obj.manager_name = data['manager']['name']
            if 'exchange' in data:
                obj.exchange = obj_exchange
            if 'code' in data:
                obj.code = data['code']
            obj.save()


def feed_category():
    offset = 0
    step = 100
    is_has_next = True

    model = models.Category
    api_url = 'https://v1.db.api.mabnadp.com/exchange/categories?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + ''
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , id=data['id']
                        , name=data['name']
                        )
            if 'short_name' in data:
                obj.short_name = data['short_name']
            if 'english_name' in data:
                obj.english_name = data['english_name']
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            if 'code' in data:
                obj.code = data['code']
            if 'parent' in data:
                obj.parent_id = data['parent']['id']

            obj.save()


def feed_company():
    offset = 0
    step = 100
    is_has_next = True

    model = models.Company
    api_url = 'https://v1.db.api.mabnadp.com/stock/companies?'  # state.id=1

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + '&_expand=state'
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            print(data)
            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            # check company state
            company_state_list = models.Companystate.objects.filter(id=data['state']['id'])
            if len(company_state_list) > 0:
                obj_state = company_state_list[0]
            else:
                obj_company_meta = Meta(version=int(data['state']['meta']['version']),
                                        state=data['state']['meta']['state']
                                        , type=data['state']['meta']['type'])
                if 'update_date_time' in data['state']['meta']:
                    obj_company_meta.update_date_time = data['state']['meta']['update_date_time']
                if 'insert_date_time' in data['state']['meta']:
                    obj_company_meta.insert_date_time = data['state']['meta']['insert_date_time']
                obj_company_meta.save()
                obj_state = models.Companystate(id=data['state']['id'], meta=obj_company_meta,
                                                title=data['state']['title'])
                obj_state.save()

            if 'exchange' in data:
                obj_exchange = models.Exchange.objects.get(id=data['exchange']['id'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , id=data['id']
                        , name=data['name']
                        )
            if 'short_name' in data:
                obj.short_name = data['short_name']
            if 'english_name' in data:
                obj.english_name = data['english_name']
            if 'english_trade_symbol' in data:
                obj.english_trade_symbol = data['english_trade_symbol']
            if 'trade_symbol' in data:
                obj.trade_symbol = data['trade_symbol']
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            if 'description' in data:
                obj.description = data['description']
            if 'fiscalyear' in data:
                obj.fiscalyear = data['fiscalyear']
            if 'exchange' in data:
                obj.exchange = obj_exchange
            if 'state' in data:
                obj.state = obj_state

            obj.save()


def feed_asset():
    offset = 0
    step = 100
    is_has_next = True

    model = models.Asset
    api_url = 'https://v1.db.api.mabnadp.com/exchange/assets?'

    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + '&_expand=state'
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            print(data)
            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])
            obj_state = models.Assetstate.objects.get(id=data['state']['id'])
            obj_assetType = models.Assettype.objects.get(id=data['type']['id'])

            if 'exchange' in data:
                obj_exchange = models.Exchange.objects.get(id=data['exchange']['id'])
            if 'entity' in data:
                # obj_entity = models.Company.objects.get(id=data['entity']['id'])
                obj_entity_list = models.Company.objects.filter(id=data['entity']['id'])
                if len(obj_entity_list) == 0:
                    continue
                obj_entity = obj_entity_list[0]
            if 'fund' in data:
                # obj_fund = models.Fund.objects.get(id=data['fund']['id'])
                obj_fund_list = models.Fund.objects.filter(id=data['fund']['fund']['id'])
                if len(obj_fund_list) == 0:
                    continue
                obj_fund = obj_fund_list[0]
            if 'categories' in data:
                obj_categories = models.Category.objects.get(id=data['categories'][0]['id'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , id=data['id']
                        , name=data['name']
                        , assetType=obj_assetType
                        , state=obj_state
                        )
            if 'trade_symbol' in data:
                obj.trade_symbol = data['trade_symbol']
            if 'english_trade_symbol' in data:
                obj.english_trade_symbol = data['english_trade_symbol']
            if 'short_name' in data:
                obj.short_name = data['short_name']
            if 'english_name' in data:
                obj.english_name = data['english_name']
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            if 'fingilish_name' in data:
                obj.fingilish_name = data['fingilish_name']
            if 'fingilish_short_name' in data:
                obj.fingilish_short_name = data['fingilish_short_name']
            if 'fingilish_trade_symbol' in data:
                obj.fingilish_trade_symbol = data['fingilish_trade_symbol']
            if 'state_change_date' in data:
                obj.state_change_date = data['state_change_date']
            if 'state_description' in data:
                obj.state_description = data['state_description']
            if 'english_state_description' in data:
                obj.english_state_description = data['english_state_description']

            if 'entity' in data:
                obj.entity = obj_entity
            if 'exchange' in data:
                obj.exchange = obj_exchange
            if 'fund' in data:
                obj.fund = obj_fund
            if 'categories' in data:
                obj.categories = obj_categories

            obj.save()


##-----------------------------------------


def get_instrument_all(sites):
    model = models.Instrument
    with requests.get(sites) as request:
        data1 = request.json()
        # print(data1)
        print(f"recive data of {sites}, len = {len(data1['data'])}")
        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            # print(data)
            # print(int(data['meta']['version']))
            # print(data['meta']['state'])
            # print(data['meta']['type'])
            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'exchange' in data:
                obj_exchange = models.Exchange.objects.get(id=data['exchange']['id'])
            else:
                obj_exchange = None

            # print(obj_exchange)
            if 'exchange_state' in data:
                obj_exchange_state_list = models.Instrumentexchangestate.objects.filter(id=data['exchange_state']['id'])
                if len(obj_exchange_state_list) == 0:
                    obj_exchange_state = None
                obj_exchange_state = obj_exchange_state_list[0]
            else:
                obj_exchange_state = None
            # print(obj_exchange_state)
            if 'market' in data:
                obj_market = models.Market.objects.get(id=data['market']['id'])
            else:
                obj_market = None
            # print(obj_market)
            if 'group' in data:
                obj_group = models.Instrumentgroup.objects.get(id=data['group']['id'])
            else:
                obj_group = None
            # print(obj_group)
            if 'board' in data:
                obj_board = models.Board.objects.get(id=data['board']['id'])
            else:
                obj_board = None
            # print(f'obj_board - {obj_board}')
            if 'index' in data:
                obj_index = models.Index.objects.get(id=data['index']['id'])
            else:
                obj_index = None
            # print(f'obj_index - {obj_index}')
            if 'asset' in data:
                # obj_asset = models.Asset.objects.get(id=data['asset']['id'])
                obj_asset_list = models.Asset.objects.filter(id=data['asset']['id'])
                if len(obj_asset_list) == 0:
                    obj_asset = None
                else:
                    obj_asset = obj_asset_list[0]
            else:
                obj_asset = None
            # print(f'obj_asset - {obj_asset}')
            if 'stock' in data:
                obj_stock = models.Company.objects.get(id=data['stock']['company']['id'])
            else:
                obj_stock = None

            # print(f'obj_stock - {obj_stock}')
            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            else:
                obj_meta.update_date_time = None
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']
            else:
                obj_meta.insert_date_time = None

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , id=data['id']
                        , code=data['code']
                        , isin=data['isin']
                        , name=data['name']
                        , type=data['type']
                        )
            if 'value_type' in data:
                obj.value_type = data['value_type']
            else:
                obj.value_type = None
            if 'nominal_price' in data:
                obj.nominal_price = data['nominal_price']
            else:
                obj.nominal_price = None
            if 'price_tick' in data:
                obj.price_tick = data['price_tick']
            else:
                obj.price_tick = None
            if 'trade_tick' in data:
                obj.trade_tick = data['trade_tick']
            else:
                obj.trade_tick = None
            if 'base_volume' in data:
                obj.base_volume = data['base_volume']
            else:
                obj.base_volume = None
            if 'bbs_code' in data:
                obj.bbs_code = data['bbs_code']
            else:
                obj.bbs_code = None
            if 'english_name' in data:
                obj.english_name = data['english_name']
            else:
                obj.english_name = None
            if 'short_name' in data:
                obj.short_name = data['short_name']
            else:
                obj.short_name = None
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            else:
                obj.english_short_name = None
            if 'payment_delay' in data:
                obj.payment_delay = data['payment_delay']
            else:
                obj.payment_delay = None
            if 'minimum_volume_permit' in data:
                obj.minimum_volume_permit = data['minimum_volume_permit']
            else:
                obj.minimum_volume_permit = None
            if 'maximum_volume_permit' in data:
                obj.maximum_volume_permit = data['maximum_volume_permit']
            else:
                obj.maximum_volume_permit = None
            if 'listing_date' in data:
                obj.listing_date = data['listing_date']
            else:
                obj.listing_date = None

            if 'exchange' in data:
                obj.exchange = obj_exchange
            if 'exchange_state' in data:
                obj.exchange_state = obj_exchange_state
            if 'market' in data:
                obj.market = obj_market
            if 'group' in data:
                obj.group = obj_group
            if 'board' in data:
                obj.board = obj_board
            if 'index' in data:
                obj.index = obj_index
            if 'asset' in data:
                obj.asset = obj_asset
            if 'stock' in data:
                obj.stock = obj_stock

            obj.save()
            # print(obj)


# thread version of get instrument
def feed_instrument_thread():
    num_of_threads = 10

    model = models.Instrument
    # model.objects.all().delete()
    # return

    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/instruments?'

    sites = [
        # api_url + '@_count=100@_skip=0',
    ]

    for i in range(400):
        sites.append(f'{api_url}@_count=100@_skip={(i * 100)}')

    #  check model is empty or not
    if model.objects.all().count() > 0:
        last_index_meta_version = model.objects.all().latest('meta__version')
        print(last_index_meta_version)
        print(last_index_meta_version.meta_id)
        # print(last_index_meta_version.version)
        api_url = base_url \
                  + 'https://v1.db.api.mabnadp.com/exchange/instruments?' + \
                  '_sort=meta.version@meta.version=' + str(
            last_index_meta_version.meta_id) + '@meta.version_op=gt@'

        sites = []

        for i in range(20):
            sites.append(f'{api_url}_count=100@_skip={(i * 100)}')

    # print(sites)
    # return

    # add missed instruments
    # url = 'http://mediadrive.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/instruments?short_name=%D8%AF%D8%B3%D8%A8%D8%AD%D8%A7%D9%86,%DA%A9%D8%AF%D9%85%D8%A7,%D8%AE%D9%BE%D9%88%DB%8C%D8%B4,%D8%AE%D8%B2%D8%A7%D9%85%DB%8C%D8%A7,%D8%AA%DA%A9%D9%86%D9%88,%D9%88%D8%AF%D8%A7%D9%86%D8%A7@short_name_op=in'
    # sites = [url]

    start_time = time.time()
    # download_all_sites(sites)
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_instrument_all, sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


def feed_instrument():
    offset = 0
    step = 100
    is_has_next = True

    model = models.Instrument
    # model.objects.all().delete()
    api_url = 'https://v1.db.api.mabnadp.com/exchange/instruments?'
    # return
    #  check model is empty or not
    if model.objects.count() > 0:
        last_index_meta_version = model.objects.latest('meta__version')
        # print(last_index_meta_version.meta.version)
        get_data = base_url + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = base_url + api_url

    # iterate for collect pagination data
    while is_has_next:

        get_data2 = get_data + '_count=' + str(step) + '&_skip=' + str(offset) + '&_expand=state'
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            # print(data)
            obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'],
                            type=data['meta']['type'])

            if 'exchange' in data:
                obj_exchange = models.Exchange.objects.get(id=data['exchange']['id'])
            if 'exchange_state' in data:
                obj_exchange_state_list = models.Instrumentexchangestate.objects.filter(id=data['exchange_state']['id'])
                if len(obj_exchange_state_list) == 0:
                    continue
                obj_exchange_state = obj_exchange_state_list[0]
            if 'market' in data:
                obj_market = models.Market.objects.get(id=data['market']['id'])
            if 'group' in data:
                obj_group = models.Instrumentgroup.objects.get(id=data['group']['id'])
            if 'board' in data:
                obj_board = models.Board.objects.get(id=data['board']['id'])
            if 'index' in data:
                obj_index = models.Index.objects.get(id=data['index']['id'])
            if 'asset' in data:
                # obj_asset = models.Asset.objects.get(id=data['asset']['id'])
                obj_asset_list = models.Asset.objects.filter(id=data['asset']['id'])
                if len(obj_asset_list) == 0:
                    continue
                obj_asset = obj_asset_list[0]
            if 'stock' in data:
                obj_stock = models.Company.objects.get(id=data['stock']['company']['id'])

            if 'update_date_time' in data['meta']:
                obj_meta.update_date_time = data['meta']['update_date_time']
            if 'insert_date_time' in data['meta']:
                obj_meta.insert_date_time = data['meta']['insert_date_time']

            # print(obj_meta.version)
            obj_meta.save()
            obj = model(meta=obj_meta
                        , id=data['id']
                        , code=data['code']
                        , isin=data['isin']
                        , name=data['name']
                        , type=data['type']
                        )
            if 'value_type' in data:
                obj.value_type = data['value_type']
            if 'nominal_price' in data:
                obj.nominal_price = data['nominal_price']
            if 'price_tick' in data:
                obj.price_tick = data['price_tick']
            if 'trade_tick' in data:
                obj.trade_tick = data['trade_tick']
            if 'base_volume' in data:
                obj.base_volume = data['base_volume']
            if 'bbs_code' in data:
                obj.bbs_code = data['bbs_code']
            if 'english_name' in data:
                obj.english_name = data['english_name']
            if 'short_name' in data:
                obj.short_name = data['short_name']
            if 'english_short_name' in data:
                obj.english_short_name = data['english_short_name']
            if 'payment_delay' in data:
                obj.payment_delay = data['payment_delay']
            if 'minimum_volume_permit' in data:
                obj.minimum_volume_permit = data['minimum_volume_permit']
            if 'maximum_volume_permit' in data:
                obj.maximum_volume_permit = data['maximum_volume_permit']
            if 'listing_date' in data:
                obj.listing_date = data['listing_date']

            if 'exchange' in data:
                obj.exchange = obj_exchange
            if 'exchange_state' in data:
                obj.exchange_state = obj_exchange_state
            if 'market' in data:
                obj.market = obj_market
            if 'group' in data:
                obj.group = obj_group
            if 'board' in data:
                obj.board = obj_board
            if 'index' in data:
                obj.index = obj_index
            if 'asset' in data:
                obj.asset = obj_asset
            if 'stock' in data:
                obj.stock = obj_stock

            obj.save()


def feed_instrumentsel():
    # models.Instrumentsel.objects.all().delete()

    # feed_instrument()
    sel_obj = models.Instrument.objects.filter((Q(type='share') | Q(type='warrant') | Q(type='commodity')
                                                | Q(type='portfoy') | Q(type='index'))
                                               & (Q(market=1) | Q(market=5))
                                               & Q(exchange_state=1)
                                               & (Q(board=1) | Q(board=2) | Q(board=4) | Q(board=5) | Q(board=6) | Q(
        board=8))
                                               )
    # add missed instruments
    sel_obj = models.Instrument.objects.filter(Q(short_name='دارا یکم'))
    for itm in sel_obj:
        obj = models.Instrumentsel(id=itm.id
                                   , code=itm.code
                                   , bbs_code=itm.bbs_code
                                   , isin=itm.isin
                                   , name=itm.name
                                   , english_name=itm.english_name
                                   , short_name=itm.short_name
                                   , english_short_name=itm.english_short_name
                                   , type=itm.type
                                   , value_type=itm.value_type
                                   , base_volume=itm.base_volume
                                   , nominal_price=itm.nominal_price
                                   , price_tick=itm.price_tick
                                   , trade_tick=itm.trade_tick
                                   , payment_delay=itm.payment_delay
                                   , minimum_volume_permit=itm.minimum_volume_permit
                                   , maximum_volume_permit=itm.maximum_volume_permit
                                   , listing_date=itm.listing_date
                                   , meta=itm.meta
                                   , exchange=itm.exchange
                                   , exchange_state=itm.exchange_state
                                   , market=itm.market
                                   , group=itm.group
                                   , board=itm.board
                                   , index=itm.index
                                   , asset=itm.asset
                                   , stock=itm.stock)
        obj.save()


def feed_tradedaily(instrument_id):
    offset = 0
    step = 50
    is_has_next = True

    model = models.Tradedetail
    # model.objects.all().delete()
    api_url = 'https://v1.db.api.mabnadp.com/exchange/tradedetails?'
    # return

    last_version_from_delete = -1
    is_error_expand = False

    start_time = time.time()

    # iterate for collect pagination data
    while is_has_next:

        #  check model is empty or not
        if model.objects.filter(instrument=instrument_id).count() > 0:
            last_index_meta_version = model.objects.filter(instrument=instrument_id).latest('version')

            # check last recived item is meta.state == deleted ?
            print(last_version_from_delete, last_version_from_delete != -1)
            if last_version_from_delete != -1:
                last_index_meta_version.version = last_version_from_delete
                print('------------- set delete version --------------- ' + str(last_index_meta_version.version))

            # print(last_index_meta_version.meta.version)
            get_data = base_url + api_url + \
                       'instrument.id=' + instrument_id + '&' + \
                       '_sort=meta.version&meta.version=' + str(
                last_index_meta_version.version) + '&meta.version_op=gt'
            if is_error_expand is False:
                get_data = get_data + '@_expand=trade'
        else:
            # print('empty')
            get_data = base_url + api_url + \
                       'instrument.id=' + instrument_id + '&_sort=meta.version'
            if is_error_expand is False:
                get_data = get_data + '@_expand=trade'

        get_data2 = get_data  # + '_count=' + str(step) + '&_skip=' + str(offset) + '&_expand=trade'
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        # print(get_data2)
        req = requests.get(get_data2)
        # print(req.text)
        data1 = req.json()

        if 'error' in data1:
            print(data1['error']['code'] + ' - ' + data1['error']['message'])
            is_error_expand = True
            continue  # break

        #  check next pagination
        if len(data1['data']) == step:
            offset = offset + step
        else:
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                last_version_from_delete = int(data['meta']['version'])
                print('------------- set delete ' + str(last_version_from_delete))
                continue

            last_version_from_delete = -1  # clear delete version
            # print(data)

            obj_trade = models.Tradedetail(version=int(data['meta']['version']), date_time=data['date_time'])
            obj_instrument = models.Instrumentsel.objects.get(id=data['instrument']['id'])
            obj_trade.instrument = obj_instrument
            val = ''

            # if get trade alone
            if is_error_expand is True:
                is_error_expand = False
                url_trade = base_url + 'https://v1.db.api.mabnadp.com/exchange/trades?id=' + \
                            data['trade']['id']
                req_trade = requests.get(url_trade)
                obj_trade_single_t = req_trade.json()
                obj_trade_single = obj_trade_single_t['data'][0]

                if 'open_price' in obj_trade_single:
                    val = val + str(obj_trade_single['open_price']) + ','
                else:
                    val = val + '-1,'
                if 'high_price' in obj_trade_single:
                    val = val + str(obj_trade_single['high_price']) + ','
                else:
                    val = val + '-1,'
                if 'low_price' in obj_trade_single:
                    val = val + str(obj_trade_single['low_price']) + ','
                else:
                    val = val + '-1,'
                if 'close_price' in obj_trade_single:
                    val = val + str(obj_trade_single['close_price']) + ','
                else:
                    val = val + '-1,'
                if 'close_price_change' in obj_trade_single:
                    val = val + str(obj_trade_single['close_price_change']) + ','
                else:
                    val = val + '-1,'
                if 'real_close_price' in obj_trade_single:
                    val = val + str(obj_trade_single['real_close_price']) + ','
                else:
                    val = val + '-1,'
                if 'buyer_count' in obj_trade_single:
                    val = val + str(obj_trade_single['buyer_count']) + ','
                else:
                    val = val + '-1,'
                if 'trade_count' in obj_trade_single:
                    val = val + str(obj_trade_single['trade_count']) + ','
                else:
                    val = val + '-1,'
                if 'volume' in obj_trade_single:
                    val = val + str(obj_trade_single['volume']) + ','
                else:
                    val = val + '-1,'
                if 'value' in obj_trade_single:
                    val = val + str(obj_trade_single['value']) + ','
                else:
                    val = val + '-1,'
            else:

                if 'open_price' in data['trade']:
                    val = val + str(data['trade']['open_price']) + ','
                else:
                    val = val + '-1,'
                if 'high_price' in data['trade']:
                    val = val + str(data['trade']['high_price']) + ','
                else:
                    val = val + '-1,'
                if 'low_price' in data['trade']:
                    val = val + str(data['trade']['low_price']) + ','
                else:
                    val = val + '-1,'
                if 'close_price' in data['trade']:
                    val = val + str(data['trade']['close_price']) + ','
                else:
                    val = val + '-1,'
                if 'close_price_change' in data['trade']:
                    val = val + str(data['trade']['close_price_change']) + ','
                else:
                    val = val + '-1,'
                if 'real_close_price' in data['trade']:
                    val = val + str(data['trade']['real_close_price']) + ','
                else:
                    val = val + '-1,'
                if 'buyer_count' in data['trade']:
                    val = val + str(data['trade']['buyer_count']) + ','
                else:
                    val = val + '-1,'
                if 'trade_count' in data['trade']:
                    val = val + str(data['trade']['trade_count']) + ','
                else:
                    val = val + '-1,'
                if 'volume' in data['trade']:
                    val = val + str(data['trade']['volume']) + ','
                else:
                    val = val + '-1,'
                if 'value' in data['trade']:
                    val = val + str(data['trade']['value']) + ','
                else:
                    val = val + '-1,'

            if 'person_buyer_count' in data:
                val = val + str(data['person_buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'company_buyer_count' in data:
                val = val + str(data['company_buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'person_buy_volume' in data:
                val = val + str(data['person_buy_volume']) + ','
            else:
                val = val + '-1,'
            if 'company_buy_volume' in data:
                val = val + str(data['company_buy_volume']) + ','
            else:
                val = val + '-1,'
            if 'person_seller_count' in data:
                val = val + str(data['person_seller_count']) + ','
            else:
                val = val + '-1,'
            if 'company_seller_count' in data:
                val = val + str(data['company_seller_count']) + ','
            else:
                val = val + '-1,'
            if 'person_sell_volume' in data:
                val = val + str(data['person_sell_volume']) + ','
            else:
                val = val + '-1,'
            if 'company_sell_volume' in data:
                val = val + str(data['company_sell_volume']) + ','
            else:
                val = val + '-1,'

            obj_trade.value = val
            obj_trade.save()

    duration = time.time() - start_time
    print(f"Downloaded {instrument_id} in {duration} seconds")


##-----------------------------------------


def get_index_values(sites):
    """ return candel info for selected index"""
    with requests.get(sites) as request:
        data1 = request.json()
        # print(data1)
        print(f"recive data of {sites}, len = {len(data1['data'])}")
        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_trade = models.Tradedetail(version=int(data['meta']['version']), date_time=data['date_time'])
            obj_instrument = models.Instrumentsel.objects.get(index__id=data['index']['id'])
            obj_trade.instrument = obj_instrument
            val = ''

            if 'open_value' in data:
                val = val + str(data['open_value']) + ','
            else:
                val = val + '-1,'
            if 'high_value' in data:
                val = val + str(data['high_value']) + ','
            else:
                val = val + '-1,'
            if 'low_value' in data:
                val = val + str(data['low_value']) + ','
            else:
                val = val + '-1,'
            if 'close_value' in data:
                val = val + str(data['close_value']) + ','
            else:
                val = val + '-1,'
            if 'close_value_change' in data:
                val = val + str(data['close_value_change']) + ','
            else:
                val = val + '-1,'
            if 'close_value' in data:
                val = val + str(data['close_value']) + ','
            else:
                val = val + '-1,'

            val = val + '-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,'

            obj_trade.value = val
            obj_trade.save()


def get_instrument(sites):
    """ return candel info for selected instrument"""
    with requests.get(sites) as request:
        data1 = request.json()
        # print(data1, 'error' in data1)
        print(f"-recive data of {sites}, len = {len(data1['data'])}")
        # print('error' in data1)

        if 'error' in data1:
            print(data1['error']['code'] + ' - ' + data1['error']['message'])
            is_error_expand = True
            # req = requests.get(sites)
            # print('request.url')
            # print(request.url)
            return

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue

            obj_trade = models.Tradedetail(version=int(data['meta']['version']), date_time=data['date_time'])
            obj_instrument = models.Instrumentsel.objects.get(id=data['instrument']['id'])
            obj_trade.instrument = obj_instrument
            val = ''

            if 'open_price' in data['trade']:
                val = val + str(data['trade']['open_price']) + ','
            else:
                val = val + '-1,'
            if 'high_price' in data['trade']:
                val = val + str(data['trade']['high_price']) + ','
            else:
                val = val + '-1,'
            if 'low_price' in data['trade']:
                val = val + str(data['trade']['low_price']) + ','
            else:
                val = val + '-1,'
            if 'close_price' in data['trade']:
                val = val + str(data['trade']['close_price']) + ','
            else:
                val = val + '-1,'
            if 'close_price_change' in data['trade']:
                val = val + str(data['trade']['close_price_change']) + ','
            else:
                val = val + '-1,'
            if 'real_close_price' in data['trade']:
                val = val + str(data['trade']['real_close_price']) + ','
            else:
                val = val + '-1,'
            if 'buyer_count' in data['trade']:
                val = val + str(data['trade']['buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'trade_count' in data['trade']:
                val = val + str(data['trade']['trade_count']) + ','
            else:
                val = val + '-1,'
            if 'volume' in data['trade']:
                val = val + str(data['trade']['volume']) + ','
            else:
                val = val + '-1,'
            if 'value' in data['trade']:
                val = val + str(data['trade']['value']) + ','
            else:
                val = val + '-1,'
            if 'person_buyer_count' in data:
                val = val + str(data['person_buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'company_buyer_count' in data:
                val = val + str(data['company_buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'person_buy_volume' in data:
                val = val + str(data['person_buy_volume']) + ','
            else:
                val = val + '-1,'
            if 'company_buy_volume' in data:
                val = val + str(data['company_buy_volume']) + ','
            else:
                val = val + '-1,'
            if 'person_seller_count' in data:
                val = val + str(data['person_seller_count']) + ','
            else:
                val = val + '-1,'
            if 'company_seller_count' in data:
                val = val + str(data['company_seller_count']) + ','
            else:
                val = val + '-1,'
            if 'person_sell_volume' in data:
                val = val + str(data['person_sell_volume']) + ','
            else:
                val = val + '-1,'
            if 'company_sell_volume' in data:
                val = val + str(data['company_sell_volume']) + ','
            else:
                val = val + '-1,'

            obj_trade.value = val
            obj_trade.save()


# thread version of get instrument
def feed_tradedaily_thread(instrument_id):
    num_of_threads = 10

    model = models.Tradedetail
    # model.objects.filter(instrument=instrument_id).delete()
    # return

    x = jdatetime.date.today()
    print(x.strftime("%Y%m%d"))

    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/tradedetails?' + \
              'instrument.id=' + instrument_id + '@_sort=meta.version' + '@_expand=trade'

    # sites = [f'{api_url}@_count=100', f'{api_url}@_count=100']
    sites = []

    for i in range(21):
        sites.append(f'{api_url}@_count=100@_skip={(i * 100)}')

    # print(sites)
    #  check model is empty or not
    if model.objects.filter(instrument=instrument_id).count() > 0:
        model.objects.filter(date_time__icontains=x.strftime("%Y%m%d")).delete()
        last_index_meta_version = model.objects.filter(instrument=instrument_id).latest('version')
        api_url = base_url \
                  + 'https://v1.db.api.mabnadp.com/exchange/tradedetails?' + \
                  'instrument.id=' + instrument_id + '@_sort=meta.version@meta.version=' + str(
            last_index_meta_version.version) + '@meta.version_op=gt' + '@_expand=trade'
        sites = [
            api_url + '@_count=100@_skip=0',
            api_url + '@_count=100@_skip=100',
        ]

    start_time = time.time()
    # download_all_sites(sites)
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_instrument, sites)
        # audiolists = pool.map(get_audio_link, sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


candle_list = list()
instrument_info_list = list()
intraday_list = list()


def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(json['date_time'])
    except KeyError:
        return 0


# last request have not any data
skip_num = -1


def get_intraday(sites, skip):
    global skip_num
    print('-=-=-sites: ', skip, skip_num)
    if skip_num is not -1:
        print('retrun---')
        return
    with requests.get(sites) as request:
        data1 = request.json()
        # print(data1)
        print(f"receive data of {sites}, len = {len(data1['data'])}")
        if len(data1['data']) < 100:
            skip_num = skip
        for data in data1['data']:
            intraday_list.append(data)


def update_candlesDay_thread(instrument_id):
    num_of_threads = 10
    try:
        # company_id = models.Instrumentsel.objects.get(id=instrument_id).stock_id
        company_id = models.Instrumentsel.objects.get(id=instrument_id).id
    except IntegrityError:
        print('Instrument not found!')
        return
    except ObjectDoesNotExist:
        print('Instrument Does Not Exist')
        return

    x = jdatetime.date.today()
    print(x.strftime("%Y%m%d"))
    last_candle_date = models.Chart.objects.get(Q(instrument=instrument_id) & Q(timeFrame='D1')).last_candle_date
    print(f'last_candle_date: {last_candle_date}')

    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/trades?' + \
              'instrument.id=' + company_id + '@date_time=13990722110000' + \
              '@date_time_op=gt'
    # 'instrument.stock.company.id=' + company_id + '@date_time=' + last_candle_date + \

    sites = []
    skip = []
    skip_num = -1
    for i in range(100):
        sites.append(f'{api_url}@_count=100@_skip={(i * 100)}')
        skip.append(i * 100)

    # print(f'sites {sites}')
    intraday_list.clear()
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_intraday, sites, skip)
    intraday_list.sort(key=extract_time, reverse=False)
    if len(intraday_list) > 0:
        max_val = max(intraday_list, key=lambda item: item['real_close_price'])
        min_val = min(intraday_list, key=lambda item: item['real_close_price'])
        print('intraday_list: ', intraday_list)
        print('len: ', len(intraday_list))
        print('max_val: ', max_val['real_close_price'])
        print('min_val: ', min_val['real_close_price'])
    # for itm in intraday_list:
    #     print(itm['id'], itm['date_time'], itm['real_close_price'])


def update_candles_thread(instrument_id):
    num_of_threads = 10
    model = models.Tradedetail
    try:
        # company_id = models.Instrumentsel.objects.get(id=instrument_id).stock_id
        company_id = models.Instrumentsel.objects.get(id=instrument_id).id
    except IntegrityError:
        print('Instrument not found!')
        return
    except ObjectDoesNotExist:
        print('Instrument Does Not Exist')
        return

    x = jdatetime.date.today()
    print(x.strftime("%Y%m%d"))
    last_candle_date = models.Chart.objects.get(Q(instrument=instrument_id) & Q(timeFrame='D1')).last_candle_date
    print(f'last_candle_date: {last_candle_date}')

    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/intradaytrades?' + \
              'instrument.id=' + company_id + '@date_time=13990722110000,13990722120000' + \
              '@date_time_op=bw'
    # 'instrument.stock.company.id=' + company_id + '@date_time=' + last_candle_date + \

    sites = []
    skip = []
    skip_num = -1
    for i in range(100):
        sites.append(f'{api_url}@_count=100@_skip={((i * 100) + 2000)}')
        skip.append(((i * 100) + 2000))

    # sites = [
    #     api_url + '@_count=100@_skip=5000',
    #     api_url + '@_count=100@_skip=5100',
    # ]
    # skip = [
    #     5000,
    #     5100
    # ]

    # print(f'sites {sites}')
    intraday_list.clear()
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_intraday, sites, skip)
    intraday_list.sort(key=extract_time, reverse=False)
    if len(intraday_list) > 0:
        max_val = max(intraday_list, key=lambda item: item['real_close_price'])
        min_val = min(intraday_list, key=lambda item: item['real_close_price'])
        print('intraday_list: ', intraday_list)
        print('len: ', len(intraday_list))
        print('max_val: ', max_val['real_close_price'])
        print('min_val: ', min_val['real_close_price'])
    # for itm in intraday_list:
    #     print(itm['id'], itm['date_time'], itm['real_close_price'])


def second_get_instrument(sites):
    with requests.get(sites) as request:
        data1 = request.json()
        # print(data1)
        print(f"receive data of {sites}, len = {len(data1['data'])}")
        for data in data1['data']:
            val = ''
            print(data)
            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                continue
            if 'date_time' in data:
                val = val + str(data['date_time']) + ','
            else:
                val = val + '-1,'
            if 'open_price' in data:
                val = val + str(data['open_price']) + ','
            elif 'open_value' in data:
                val = val + str(data['open_value']) + ','
            else:
                val = val + '-1,'
            if 'high_price' in data:
                val = val + str(data['high_price']) + ','
            elif 'high_value' in data:
                val = val + str(data['high_value']) + ','
            else:
                val = val + '-1,'
            if 'low_price' in data:
                val = val + str(data['low_price']) + ','
            elif 'low_value' in data:
                val = val + str(data['low_value']) + ','
            else:
                val = val + '-1,'
            if 'real_close_price' in data:
                val = val + str(data['real_close_price']) + ','
            elif 'close_value' in data:
                val = val + str(data['close_value']) + ','
            else:
                val = val + '-1,'
            if 'volume' in data:
                val = val + str(data['volume']) + ','
            else:
                val = val + '-1,'
            print(val)
            candle_list.append(val)


def second_feed_tradedaily_thread(instrument_id, host):
    # print('start update candles info')
    num_of_threads = 10
    model = models.Tradedetail
    # model.objects.filter(instrument=instrument_id).delete()
    try:
        obj = models.Instrumentsel.objects.get(id=instrument_id)

    except IntegrityError:
        print('Instrument not found!')
        return
    except ObjectDoesNotExist:
        print('Instrument Does Not Exist')
        return

    last_candle_date = models.Chart.objects.get(Q(instrument=instrument_id) & Q(timeFrame='D1')).last_candle_date
    print(f'last_candle_date: {last_candle_date}')

    api_url = ''
    if obj.index is None:
        # company_id = obj.stock_id
        company_id = obj.id
        print('company_id: ', company_id)
        api_url = base_url + 'https://v1.db.api.mabnadp.com/exchange/trades?' + 'instrument.id=' + company_id + \
                  '@date_time=' + last_candle_date + '@date_time_op=gt'
    else:
        company_id = obj.index_id
        api_url = base_url + 'https://v1.db.api.mabnadp.com/exchange/indexvalues?' + \
                  'index.id=' + company_id + '@date_time=' + last_candle_date + \
                  '@date_time_op=gt'

    sites = [
        api_url + '@_count=100@_skip=0',
        api_url + '@_count=100@_skip=100',
        api_url + '@_count=100@_skip=200',
    ]

    print(f'sites {sites}')
    candle_list.clear()
    # download_all_sites(sites)
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(second_get_instrument, sites)

    # check result length
    if len(candle_list) == 0:

        # # Update instrument info for first time
        # candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='D1').data
        # # find candle file url
        # url2 = UtilFunc.findCsvFileUrl(candle.url, host)
        # # read csv file
        # df = pd.read_csv(url2)
        # # update average of instrumentInfo model
        # obj_info, crt = models.InstrumentInfo.objects.get_or_create(instrument_id=instrument_id)
        # obj_info.volAvg1M = df.iloc[-30:, -1].mean()
        # obj_info.volAvg3M = df.iloc[-90:, -1].mean()
        # obj_info.volAvg12M = df.iloc[-360:, -1].mean()
        # obj_info.created_on = timezone.now()  # df.iloc[-1:, 0]
        # obj_info.save()

        return

    print("candle_list:", candle_list)

    # read daily candle csv file and update it
    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='D1').data
        # instrument_name = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='D1').instrument.short_name

        # find candle file url
        url2 = UtilFunc.findCsvFileUrl(candle.url, host)
        # read csv file
        df = pd.read_csv(url2)
        # iterate new candles and add to csv file
        for item in candle_list:
            print(item)
            # date conversion
            candle_parts = item.split(",")
            jalali_date = JalaliDate(int(candle_parts[0][:4]), int(candle_parts[0][4:6]),
                                     int(candle_parts[0][6:8])).to_gregorian()
            jalali_date = str(jalali_date).replace('-', '')
            print(jalali_date)
            # find similar row and replace or append new entry
            index = df['<DTYYYYMMDD>'].searchsorted(int(jalali_date), 'left')
            print('length: ', len(df))
            print('index: ', index)
            if index != len(df):
                # to_append = [int(jalali_date),
                #              max(int(candle_parts[0][8:]), int(df.iloc[index][1])),
                #              # int(candle_parts[0][8:]),
                #              int(float(candle_parts[1])),
                #              max(int(float(candle_parts[2])), df.iloc[index]['<HIGH>']),
                #              min(int(float(candle_parts[3])), df.iloc[index]['<LOW>']),
                #              int(float(candle_parts[4])),
                #              max(float(candle_parts[5]), float(df.iloc[index]['<VOL>']))]
                # print("to_append!=", to_append)
                to_append = [int(jalali_date), int(candle_parts[0][8:]), int(float(candle_parts[1])),
                             int(float(candle_parts[2])), int(float(candle_parts[3])), int(float(candle_parts[4])),
                             float(candle_parts[5])]
                df.loc[index, :] = to_append
            else:
                to_append = [int(jalali_date), int(candle_parts[0][8:]), int(float(candle_parts[1])),
                             int(float(candle_parts[2])), int(float(candle_parts[3])), int(float(candle_parts[4])),
                             float(candle_parts[5])]
                print("to_append=", to_append)
                df.loc[index, :] = to_append

        # print(df)
        df['<DTYYYYMMDD>'] = df['<DTYYYYMMDD>'].astype(int)
        # df['<TIME>'] = df['<TIME>'].astype(int)
        df['<OPEN>'] = df['<OPEN>'].astype(int)
        df['<HIGH>'] = df['<HIGH>'].astype(int)
        df['<LOW>'] = df['<LOW>'].astype(int)
        df['<CLOSE>'] = df['<CLOSE>'].astype(int)
        # df['<VOL>'] = df['<VOL>'].astype(int)
        str_lst_date = str(df['<DTYYYYMMDD>'].iloc[-1])
        jl_date = jdatetime.date.fromgregorian(
            day=int(str_lst_date[6:]),
            month=int(str_lst_date[4:6]),
            year=int(str_lst_date[:4])
        )
        jl_date = str(jl_date).replace('-', '')
        models.Chart.objects.filter(instrument_id=instrument_id, timeFrame='D1').update(last_candle_date=jl_date)

        # print("df:", df)
        df.to_csv(url2, index=False)

        # update average of instrumentInfo model
        obj_info, crt = models.InstrumentInfo.objects.get_or_create(instrument_id=instrument_id)
        obj_info.volAvg1M = df.iloc[-30:, -1].mean()
        obj_info.volAvg3M = df.iloc[-90:, -1].mean()
        obj_info.volAvg12M = df.iloc[-360:, -1].mean()
        obj_info.created_on = timezone.now()  # df.iloc[-1:, 0]
        obj_info.save()

    except IntegrityError:
        print('candle nadarim')
        return
    # return

    # todo: update week csv
    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='W1').data
        # find candle file url
        url2 = UtilFunc.findCsvFileUrl(candle.url, host)
        # read csv file
        df_week = pd.read_csv(url2)
        # read las item
        print(len(df_week))
        # last candle date in weekly dataframe
        last_entry_date = df_week['<DTYYYYMMDD>'][len(df_week) - 1]
        # last candle date in daily dataframe
        last_day_date = df['<DTYYYYMMDD>'][len(df) - 1]
        print(last_entry_date, last_day_date)
        d_last = datetime.strptime(str(last_entry_date), "%Y%m%d").date()
        day_last = datetime.strptime(str(last_day_date), "%Y%m%d").date()
        day_last = day_last + timedelta(weeks=1)
        print('date,', d_last, day_last)
        # previous week date
        week_prior = d_last - timedelta(weeks=1)
        # next week date
        week_next = d_last + timedelta(weeks=1)
        print('three', week_prior, d_last, week_next)
        # check it is the first iterate in while
        is_first_iterate = True
        while day_last > week_next:
            print('------------------------------------ checking', d_last)
            d_last_str = str(d_last).replace('-', '')
            week_next_str = str(week_next).replace('-', '')
            # find start day of week
            index_start_day = df['<DTYYYYMMDD>'].searchsorted(int(d_last_str), 'left')
            # find stop day  of week
            index_stop_day = df['<DTYYYYMMDD>'].searchsorted(int(week_next_str), 'left')
            print('week: ', d_last_str, week_next_str)
            print('index: ', index_start_day, index_stop_day)
            df_days_of_week = df[:][index_start_day:index_stop_day]

            # sum of volume
            vol = 0
            for i in range(len(df_days_of_week)):
                print('vol', df_days_of_week['<VOL>'][index_start_day + i])
                if df_days_of_week['<VOL>'][index_start_day + i] < 0:
                    vol = vol + (df_days_of_week['<VOL>'][index_start_day + i] * -1)
                else:
                    vol = vol + df_days_of_week['<VOL>'][index_start_day + i]

            print(int(d_last_str), int(0), index_start_day)
            candle_week = [int(d_last_str), int(0), int(df_days_of_week['<OPEN>'][index_start_day])
                , int(df_days_of_week['<HIGH>'].max())
                , int(df_days_of_week['<LOW>'].min())
                , int(df_days_of_week['<CLOSE>'][index_start_day + len(df_days_of_week) - 1])
                , vol
                           ]
            # print('candle_week: ', candle_week)

            # checks if it is first iterate for update or create candle
            if is_first_iterate:
                df_week.loc[len(df_week) - 1, :] = candle_week
                is_first_iterate = False
            else:
                df_week.loc[len(df_week), :] = candle_week

            df_week['<DTYYYYMMDD>'] = df_week['<DTYYYYMMDD>'].astype(int)
            # df_week['<TIME>'] = df_week['<TIME>'].astype(int)
            df_week['<OPEN>'] = df_week['<OPEN>'].astype(int)
            df_week['<HIGH>'] = df_week['<HIGH>'].astype(int)
            df_week['<LOW>'] = df_week['<LOW>'].astype(int)
            df_week['<CLOSE>'] = df_week['<CLOSE>'].astype(int)
            # df_week['<VOL>'] = df_week['<VOL>'].astype(int)

            d_last = d_last + timedelta(weeks=1)
            week_next = week_next + timedelta(weeks=1)

        # print(df_week.tail())
        df_week.to_csv(url2, index=False)
        models.Chart.objects.filter(instrument_id=instrument_id, timeFrame='W1').update(
            last_candle_date=df_week['<DTYYYYMMDD>'][len(df_week) - 1])
        # print(df)
    except IntegrityError:
        print('candle nadarim')

    # todo: update month csv
    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='MN1').data
        # find candle file url
        url2 = UtilFunc.findCsvFileUrl(candle.url, host)
        # read csv file
        df_month = pd.read_csv(url2)
        # read las item
        print(len(df_month))
        # last_entry_date = df_week.loc[len(df_week)-1:,:]['<DTYYYYMMDD>']
        last_entry_date = df_month['<DTYYYYMMDD>'][len(df_month) - 1]
        last_day_date = df['<DTYYYYMMDD>'][len(df) - 1]
        print(last_entry_date, last_day_date)
        d_last = datetime.strptime(str(last_entry_date), "%Y%m%d").date()
        day_last = datetime.strptime(str(last_day_date), "%Y%m%d").date()
        day_last = day_last + timedelta(days=30)
        print('date,', d_last, day_last)
        month_prior = d_last - timedelta(days=30)
        month_next = d_last + timedelta(days=30)
        print('three', month_prior, d_last, month_next)
        # check is the first iterate
        is_first_iterate = True
        while day_last > month_next:
            print('-----------------checking month-------------------', d_last)
            d_last_str = str(d_last).replace('-', '')
            month_next_str = str(month_next).replace('-', '')
            # find start day of week
            index_start_day = df['<DTYYYYMMDD>'].searchsorted(int(d_last_str), 'left')
            # find stop day  of week
            index_stop_day = df['<DTYYYYMMDD>'].searchsorted(int(month_next_str), 'left')
            print('month: ', d_last_str, month_next_str)
            print('index: ', index_start_day, index_stop_day)
            df_days_of_month = df[:][index_start_day:index_stop_day]
            print(df_days_of_month)

            # sum of volume
            vol = 0
            for i in range(len(df_days_of_month)):
                print('vol', df_days_of_month['<VOL>'][index_start_day + i])
                if df_days_of_month['<VOL>'][index_start_day + i] < 0:
                    vol = vol + (df_days_of_month['<VOL>'][index_start_day + i] * -1)
                else:
                    vol = vol + df_days_of_month['<VOL>'][index_start_day + i]

            candle_month = [int(d_last_str), int(0), int(df_days_of_month['<OPEN>'][index_start_day])
                , int(df_days_of_month['<HIGH>'].max())
                , int(df_days_of_month['<LOW>'].min())
                , int(df_days_of_month['<CLOSE>'][index_start_day + len(df_days_of_month) - 1])
                , vol]
            print('candle_month: ', candle_month)

            # checks if it is first iterate for update or create candle
            if is_first_iterate:
                df_month.loc[len(df_month) - 1, :] = candle_month
                is_first_iterate = False
            else:
                df_month.loc[len(df_month), :] = candle_month

            df_month['<DTYYYYMMDD>'] = df_month['<DTYYYYMMDD>'].astype(int)
            # df_month['<TIME>'] = df_month['<TIME>'].astype(int)
            df_month['<OPEN>'] = df_month['<OPEN>'].astype(int)
            df_month['<HIGH>'] = df_month['<HIGH>'].astype(int)
            df_month['<LOW>'] = df_month['<LOW>'].astype(int)
            df_month['<CLOSE>'] = df_month['<CLOSE>'].astype(int)
            # df_month['<VOL>'] = df_month['<VOL>'].astype(int)

            d_last = d_last + timedelta(days=30)
            month_next = month_next + timedelta(days=30)

        print(df_month.tail())
        df_month.to_csv(url2, index=False)
        models.Chart.objects.filter(instrument_id=instrument_id, timeFrame='MN1').update(
            last_candle_date=df_month['<DTYYYYMMDD>'][len(df_month) - 1])
        # print(df)
    except IntegrityError:
        print('candle nadarim')


def update_timeframe_candles():
    instruments_id = models.Instrumentsel.objects.all().values_list('id', flat=True)
    # host = request.get_host()
    host = ['127.0.0.1:8000'] * len(instruments_id)
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.map(second_feed_tradedaily_thread, instruments_id, host)


async def request_instrumentInfo(client, url):
    async with client.get(url) as request:
        data1 = await request.json()

        # check error
        if 'error' in data1:
            print(f'error in {url}')
            return

        print(f"receive data of {url}, len = {len(data1['data'])}")

        for data in data1['data']:
            instrument_info_list.append(data)
            # save_tradeDetail(data)


# @database_sync_to_async
def save_tradeDetailCurrent(data):
    miss_count = 0
    obj = data

    # print(data)
    # print("--", obj['instrument']['id'])

    # ignore deleted state
    if obj['meta']['state'] == 'deleted':
        return

    try:
        obj_instrument = models.Instrumentsel.objects.get(id=obj['instrument']['id'])
    except models.Instrumentsel.DoesNotExist:
        # print('can not find; ', obj['instrument'])
        miss_count += 1
        return
    # print(obj_instrument.short_name, obj_instrument.id)
    obj_trade_detail, otd = models.TradedetailCurrent.objects.get_or_create(instrument=obj_instrument)
    obj_trade, ot = models.TradeCurrent.objects.get_or_create(instrument=obj_instrument)

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


def get_instrument_info(request):

    # instruments_id = models.InstrumentInfo.objects.all().values_list('instrument__id', flat=True)
    # host = request.get_host()
    # host = [request.get_host()] * len(instruments_id)
    # print(instruments_id)

    # id_str = ','.join(str(x) for x in instruments_id)
    # print('list: ', id_str)

    # today date
    user_date = request.GET.get('date')
    today_date = str(jdatetime.date.today())
    today_date = today_date.replace('-', '')
    if user_date is not None:
        today_date = user_date
    timee = "090000"
    dateTime = today_date + timee
    # dateTime = "13990912" + timee
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

    instrument_info_list.clear()

    # with ThreadPoolExecutor(max_workers=10) as pool:
    #     pool.map(request_instrumentInfo, sites)
    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_instrumentInfo(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()
    for itm in instrument_info_list:
        save_tradeDetailCurrent(itm)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return instrument_info_list


# -------------------------------------------
# ------- trade detail functions ------------

trade_detail_list = list()


# ger url
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


# save single data
def save_single_trade_detail(data, obj_instrument):

    obj = data

    # ignore deleted state
    if obj['meta']['state'] == 'deleted':
        models.Tradedetail.objects.filter(id=obj['id']).delete()
        return

    obj_trade_detail, otd = models.Tradedetail.objects.get_or_create(id=obj['id'])
    obj_trade, ot = models.Trade.objects.get_or_create(id=obj['trade']['id'])

    obj_trade_detail.instrument = obj_instrument
    obj_trade.instrument = obj_instrument

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
    # print('obj_trade_detail: ', obj_trade_detail)


# fill all data
def get_trade_detail(request, instrument):

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?' \
              f'instrument.id={instrument.id}@_count=100'  # @_expand=trade'

    sites = []
    for cntr in range(30):
        sites.append(f'{api_url}@_skip={cntr*100}')

    # print('site: ', sites)

    trade_detail_list.clear()

    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_trade_detail(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()

    cnt = 0
    for itm in trade_detail_list:
        save_single_trade_detail(itm, instrument)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return trade_detail_list


# fill custom data
def get_trade_detail_oneDay(request, dateTime):

    print(dateTime)

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/tradedetails?' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=date_time' #@_expand=trade'

    sites = []
    for cntr in range(30):
        sites.append(f'{api_url}@_skip={cntr*100}')

    trade_detail_list.clear()

    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_trade_detail(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()

    for itm in trade_detail_list:
        # print('--- ', itm)
        if itm['meta']['state'] == 'deleted':
            continue
        try:
            instrument = models.Instrumentsel.objects.get(id=itm['instrument']['id'])
        except models.Instrumentsel.DoesNotExist:
            continue
        save_single_trade_detail(itm, instrument)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return trade_detail_list

# ------- end of trade detail functions -------
# ---------------------------------------------


# -------------------------------------------
# ------- trade functions ------------

trade_list = list()


# ger url
async def request_trade(client, url):
    async with client.get(url) as request:
        try:
            data1 = await request.json()

            # check error
            if 'error' in data1:
                print(f'error in {url}')
                return

            print(f"receive data of {url}, len = {len(data1['data'])}")

            for data in data1['data']:
                trade_list.append(data)
                # save_tradeDetail(data)
        except aiohttp.client_exceptions.ContentTypeError:
            print(aiohttp.client_exceptions.ContentTypeError)


# save single data
def save_single_trade(data, obj_instrument):

    obj = data

    # ignore deleted state
    if obj['meta']['state'] == 'deleted':
        return

    obj_trade, ot = models.Trade.objects.get_or_create(id=obj['id'])

    obj_trade.instrument = obj_instrument

    if obj_instrument.type == 'index':
        if 'date_time' in obj:
            obj_trade.date_time = obj['date_time']
        if 'open_value' in obj:
            obj_trade.open_price = int(obj['open_value'])
        if 'high_value' in obj:
            obj_trade.high_price = int(obj['high_value'])
        if 'low_value' in obj:
            obj_trade.low_price = int(obj['low_value'])
        if 'close_value' in obj:
            obj_trade.close_price = int(obj['close_value'])
            obj_trade.real_close_price = int(obj['close_value'])
        if 'close_value_change' in obj:
            obj_trade.close_price_change = int(obj['close_value_change'])
    else:

        # fill trade
        # print(obj['trade'])
        # print('date= ', obj['trade']['date_time'])
        # print('open_price= ', int(obj['trade']['open_price']))
        if 'date_time' in obj:
            obj_trade.date_time = obj['date_time']
        if 'open_price' in obj:
            obj_trade.open_price = int(obj['open_price'])
        if 'high_price' in obj:
            obj_trade.high_price = int(obj['high_price'])
        if 'low_price' in obj:
            obj_trade.low_price = int(obj['low_price'])
        if 'close_price' in obj:
            obj_trade.close_price = int(obj['close_price'])
        if 'close_price_change' in obj:
            obj_trade.close_price_change = int(obj['close_price_change'])
        if 'real_close_price' in obj:
            obj_trade.real_close_price = int(obj['real_close_price'])
        if 'real_close_price_change' in obj:
            obj_trade.real_close_price_change = int(obj['real_close_price_change'])
        if 'buyer_count' in obj:
            obj_trade.buyer_count = int(obj['buyer_count'])
        if 'trade_count' in obj:
            obj_trade.trade_count = int(obj['trade_count'])
        if 'volume' in obj:
            obj_trade.volume = int(obj['volume'])
        if 'value' in obj:
            obj_trade.value = int(obj['value'])
    obj_trade.save()
    # print('obj_trade: ', obj_trade)


# fill all data
def get_trade(request, instrument):

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/trades?' \
              f'instrument.id={instrument.id}@_count=100@_expand=trade'

    if instrument.type == 'index':
        api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/indexvalues?' \
                 f'index.id={instrument.index.id}@_count=100'  # @_expand=trade'

    sites = []
    for cntr in range(30):
        sites.append(f'{api_url}@_skip={cntr*100}')

    # print('site: ', sites)

    trade_list.clear()

    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_trade(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()

    cnt = 0
    for itm in trade_list:
        save_single_trade(itm, instrument)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return trade_list


# fill custom data
def get_trade_oneDay(request, dateTime):

    sites = []
    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/trades?' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=date_time' #@_expand=trade'
    for cntr in range(16):
        sites.append(f'{api_url}@_skip={cntr*100}')

    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/exchange/indexvalues?' \
              f'@date_time={dateTime}@date_time_op=gt' \
              f'@_count=100@_sort=date_time'

    for cntr in range(2):
        sites.append(f'{api_url}@_skip={cntr*100}')

    # print('site: ', sites)

    trade_list.clear()

    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_trade(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()

    cnt = 0
    for itm in trade_list:
        if itm['meta']['state'] == 'deleted':
            continue
        try:
            if 'index' in itm:
                instrument = models.Instrumentsel.objects.get(index__id=itm['index']['id'])
            else:
                instrument = models.Instrumentsel.objects.get(id=itm['instrument']['id'])
        except models.Instrumentsel.DoesNotExist:
            continue
        # print(f'start save {instrument} - {itm}')
        save_single_trade(itm, instrument)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return trade_list

# ------- end of trade detail functions -------
# ---------------------------------------------


# ---------------------------------------------
# ------- start of capital change functions -------

capital_change_list = list()


# ger url
async def request_capital_change(client, url):
    async with client.get(url) as request:
        data1 = await request.json()

        # check error
        if 'error' in data1:
            print(f'error in {url}')
            return

        print(f"receive data of {url}, len = {len(data1['data'])}")

        for data in data1['data']:
            capital_change_list.append(data)
            # save_tradeDetail(data)


# save capital change data
def save_capital_change(data, obj_company):

    obj = data

    # ignore deleted state
    if obj['meta']['state'] == 'deleted':
        return

    obj_capital, ot = models.Capitalchange.objects.get_or_create(id=obj['id'])

    obj_capital.company = obj_company

    if 'date' in obj:
        obj_capital.date = obj['date']
    if 'previous_capital' in obj:
        obj_capital.previous_capital = float(obj['previous_capital'])
    if 'new_capital' in obj:
        obj_capital.new_capital = float(obj['new_capital'])
    if 'contribution_percent' in obj:
        obj_capital.contribution_percent = float(obj['contribution_percent'])
    if 'reserve_percent' in obj:
        obj_capital.reserve_percent = int(obj['reserve_percent'])
    if 'premium_percent' in obj:
        obj_capital.premium_percent = int(obj['premium_percent'])
    # if 'underwriting_end_date' in obj:
    #     obj_capital.underwriting_end_date = int(obj['underwriting_end_date'])
    if 'registration_date' in obj:
        obj_capital.registration_date = obj['registration_date']
    if 'stock_certificate_receive_date' in obj:
        obj_capital.stock_certificate_receive_date = obj['stock_certificate_receive_date']
    if 'comments' in obj:
        obj_capital.comments = obj['comments']


    obj_capital.save()
    # print('obj_capital: ', obj_capital)


# fill capital change data
def get_capital_change(request):

    sites = []
    api_url = f'https://bourse-api.ir/bourse/api-test/?url=https://v1.db.api.mabnadp.com/stock/capitalchanges?' \
              f'@_count=100' #@_expand=trade'
    for cntr in range(20): #65
        # cntr = cntr + 60
        sites.append(f'{api_url}@_skip={cntr*100}')


    # print('site: ', sites)

    capital_change_list.clear()

    async def scrap():
        async with aiohttp.ClientSession() as client:
            start_time = time.time()
            tasks = []
            for url in sites:
                task = asyncio.ensure_future(request_capital_change(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            print('scrapped in', total_time, 'seconds')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrap())
    loop.close()

    start_time = time.time()

    cnt = 0
    for itm in capital_change_list:
        # print(itm)
        # continue
        if itm['meta']['state'] == 'deleted':
            continue
        try:
            company = models.Company.objects.get(id=itm['company']['id'])
        except models.Company.DoesNotExist:
            continue
        # print(f'start save {company} - {itm}')
        save_capital_change(itm, company)

    total_time = time.time() - start_time
    print('save in DB in', total_time, 'seconds')

    # return instrument_info_list
    return trade_list

# ------- end of capital change functions -------
# ---------------------------------------------

def test():
    print('man')
    print('no')


# thread version of get index candle
def feed_indexdaily_thread(index_id):
    num_of_threads = 10

    model = models.Tradedetail

    x = jdatetime.date.today()
    print(x.strftime("%Y%m%d"))

    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/indexvalues?' + \
              'index.id=' + index_id + '@_sort=meta.version'

    sites = []

    for i in range(21):
        sites.append(f'{api_url}@_count=100@_skip={(i * 100)}')

    #  check model is empty or not
    if model.objects.filter(instrument__index=index_id).count() > 0:
        model.objects.filter(date_time__icontains=x.strftime("%Y%m%d")).delete()
        last_index_meta_version = model.objects.filter(instrument__index=index_id).latest('version')
        api_url = base_url \
                  + 'https://v1.db.api.mabnadp.com/exchange/indexvalues?' + \
                  'index.id=' + index_id + '@_sort=meta.version@meta.version=' + str(
            last_index_meta_version.version) + '@meta.version_op=gt'
        sites = [
            api_url + '@_count=100@_skip=0',
            api_url + '@_count=100@_skip=100',
        ]

    start_time = time.time()
    # download_all_sites(sites)
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_index_values, sites)
        # audiolists = pool.map(get_audio_link, sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


def feed_trademidday(company_id):
    offset = 0
    step = 100
    is_has_next = True

    today_date = str(jdatetime.date.today())
    today_date = today_date.replace('-', '')
    timee = "090000"

    model = models.Trademidday
    # model.objects.all().delete()
    api_url = 'https://v1.db.api.mabnadp.com/exchange/intradaytrades?'

    last_version_from_delete = -1

    # iterate for collect pagination data
    while is_has_next:
        #  check model is empty or not
        if model.objects.filter(company=company_id).count() > 0:
            last_index_meta_version = model.objects.filter(company=company_id).latest('version')

            # check last recived item is meta.state == deleted ?
            print(last_version_from_delete, last_version_from_delete != -1)
            if last_version_from_delete != -1:
                last_index_meta_version.version = last_version_from_delete
                print('------------- set delete version --------------- ' + str(last_index_meta_version.version))

            # print(last_index_meta_version.meta.version)
            get_data = base_url + api_url + \
                       'instrument.stock.company.id=' + company_id + '&' + \
                       'date_time=' + today_date + timee + '&_sort=meta.version=' + str(
                last_index_meta_version.version) + '&date_time_op=gt'
        else:
            get_data = base_url + api_url + \
                       'instrument.stock.company.id=' + company_id + '&' + \
                       'date_time=' + today_date + timee + '&' + 'date_time_op=gt'
            # print(get_data)

        get_data2 = get_data + '&_count=' + str(step) + '&_skip=' + str(offset)
        get_data2 = get_data2.replace("&", "@")  # replace & with @, becuase of & confilict
        req = requests.get(get_data2)
        data1 = req.json()

        if 'error' in data1:
            print(data1['error']['code'] + ' - ' + data1['error']['message'])
            is_error_expand = True
            continue  # break

        #  check next pagination
        if len(data1['data']) == step:
            print(1)
            offset = offset + step
        else:
            print(2)
            is_has_next = False

        for data in data1['data']:

            #  ignore deleted items
            if data['meta']['state'] == 'deleted':
                last_version_from_delete = int(data['meta']['version'])
                print('------------- set delete ' + str(last_version_from_delete))
                continue

            last_version_from_delete = -1  # clear delete version
            # print(data)

            obj_trade = models.Trademidday(version=int(data['meta']['version']), date_time=data['date_time'])
            obj_instrument = models.Instrumentsel.objects.get(id=data['instrument']['id'])
            obj_company = models.Company.objects.get(id=company_id)
            obj_trade.instrument = obj_instrument
            obj_trade.company = obj_company
            val = ''

            if 'open_price' in data['trade']:
                val = val + str(data['trade']['open_price']) + ','
            else:
                val = val + '-1,'
            if 'high_price' in data['trade']:
                val = val + str(data['trade']['high_price']) + ','
            else:
                val = val + '-1,'
            if 'low_price' in data['trade']:
                val = val + str(data['trade']['low_price']) + ','
            else:
                val = val + '-1,'
            if 'close_price' in data['trade']:
                val = val + str(data['trade']['close_price']) + ','
            else:
                val = val + '-1,'
            if 'close_price_change' in data['trade']:
                val = val + str(data['trade']['close_price_change']) + ','
            else:
                val = val + '-1,'
            if 'real_close_price' in data['trade']:
                val = val + str(data['trade']['real_close_price']) + ','
            else:
                val = val + '-1,'
            if 'buyer_count' in data['trade']:
                val = val + str(data['trade']['buyer_count']) + ','
            else:
                val = val + '-1,'
            if 'trade_count' in data['trade']:
                val = val + str(data['trade']['trade_count']) + ','
            else:
                val = val + '-1,'
            if 'volume' in data['trade']:
                val = val + str(data['trade']['volume']) + ','
            else:
                val = val + '-1,'
            if 'value' in data['trade']:
                val = val + str(data['trade']['value']) + ','
            else:
                val = val + '-1,'
            if 'id' in data:
                val = val + str(data['id']) + ','
            else:
                val = val + '-1,'
            if 'close_price' in data:
                val = val + str(data['close_price']) + ','
            else:
                val = val + '-1,'
            if 'real_close_price' in data:
                val = val + str(data['real_close_price']) + ','
            else:
                val = val + '-1,'
            if 'volume' in data:
                val = val + str(data['volume']) + ','
            else:
                val = val + '-1,'
            if 'value' in data:
                val = val + str(data['value']) + ','
            else:
                val = val + '-1,'

            obj_trade.value = val
            obj_trade.save()


# search in valid instrument and add to DataBase
def search_rahavard_instruments():
    # valid instrument list (fetched from rahavard)
    ins = ["آ س پ",
           "آبادا",
           "آبین",
           "آپ",
           "اپرداز",
           "اتکام",
           "اخابر",
           "ارفع",
           "آرمان",
           "آریا",
           "آریان",
           "آسیا",
           "اعتلا",
           "افرا",
           "افق",
           "امید",
           "امین",
           "انرژی3",
           "آینده",
           "بالاس",
           "بالبر",
           "بایکا",
           "بپاس",
           "بپیوند",
           "بترانس",
           "بتک",
           "بجهرم",
           "بخاور",
           "برکت",
           "بزاگرس",
           "بساما",
           "بسویچ",
           "بشهاب",
           "بفجر",
           "بکاب",
           "بکام",
           "بگیلان",
           "بمپنا",
           "بموتو",
           "بمیلا",
           "بنو",
           "بنیرو",
           "بهپاک",
           "بورس",
           "پارتا",
           "پارس",
           "پارسان",
           "پارسیان",
           "پاسا",
           "پاکشو",
           "پتایر",
           "پترول",
           "پخش",
           "پرداخت",
           "پردیس",
           "پسهند",
           "پکرمان",
           "پکویر",
           "پلاست",
           "پلاسک",
           "پلوله",
           "پیزد",
           "تاپکیش",
           "تاپیکو",
           "تاصیکو",
           "تایرا",
           "تبرک",
           "تپمپی",
           "تپولا",
           "تشتاد",
           "تفیرو",
           "تکشا",
           "تکمبا",
           "تکنار",
           "تماوند",
           "تملت",
           "تنوین",
           "توریل",
           "تیپیکو",
           "ثاباد",
           "ثاخت",
           "ثاژن",
           "ثاصفا",
           "ثالوند",
           "ثامان",
           "ثامید",
           "ثباغ",
           "ثبهساز",
           "ثپردیس",
           "ثتران",
           "ثتوسا",
           "ثجوان",
           "ثرود",
           "ثزاگرس",
           "ثشاهد",
           "ثشرق",
           "ثعتما",
           "ثعمرا",
           "ثغرب",
           "ثفارس",
           "ثقزوی",
           "ثمسکن",
           "ثنام",
           "ثنظام",
           "ثنور",
           "ثنوسا",
           "جم",
           "جم پیلن",
           "جهرم",
           "چافست",
           "چدن",
           "چفیبر",
           "چکاپا",
           "چکارن",
           "چکاوه",
           "حاریا",
           "حآسا",
           "حبندر",
           "حپارسا",
           "حپترو",
           "حتاید",
           "حتوکا",
           "حخزر",
           "حرهشا",
           "حریل",
           "حسیر",
           "حسینا",
           "حفارس",
           "خاذین",
           "خاهن",
           "خبهمن",
           "خپارس",
           "ختراک",
           "ختور",
           "ختوقا",
           "خچرخش",
           "خدیزل",
           "خراسان",
           "خریخت",
           "خرینگ",
           "خزر",
           "خساپا",
           "خشرق",
           "خصدرا",
           "خعمرا",
           "خفنر",
           "خفولا",
           "خکار",
           "خکاوه",
           "خکرمان",
           "خکمک",
           "خگستر",
           "خلنت",
           "خمحرکه",
           "خمحور",
           "خمهر",
           "خموتور",
           "خنصیر",
           "خودرو",
           "دابور",
           "داراب",
           "دارو",
           "داسوه",
           "دالبر",
           "دامین",
           "دانا",
           "داوه",
           "دبالک",
           "دپارس",
           "دتماد",
           "دتوزیع",
           "دتولید",
           "دجابر",
           "ددام",
           "درهآور",
           "دروز",
           "دزهراوی",
           "دسانکو",
           "دسبحا",
           "دسینا",
           "دشیری",
           "دشیمی",
           "دعبید",
           "دفرا",
           "دقاضی",
           "دکپسول",
           "دکوثر",
           "دکیمی",
           "دلر",
           "دلقما",
           "دماوند",
           "دی",
           "دیران",
           "ذوب",
           "رافزا",
           "رانفور",
           "رتاپ",
           "رتکو",
           "رکیش",
           "رمپنا",
           "رنیک",
           "ریشمک",
           "زاگرس",
           "زبینا",
           "زپارس",
           "زدشت",
           "زشریف",
           "زشگزا",
           "زفکا",
           "زقیام",
           "زکشت",
           "زکوثر",
           "زگلدشت",
           "زماهان",
           "زمگسا",
           "زملارد",
           "زنجان",
           "زنگان",
           "ساراب",
           "ساروج",
           "ساروم",
           "ساوه",
           "سایرا",
           "ساینا",
           "سباقر",
           "سبجنو",
           "سبهان",
           "سپ",
           "سپاها",
           "ستران",
           "سجام",
           "سخاش",
           "سخزر",
           "سخواف",
           "سخوز",
           "سدبیر",
           "سدور",
           "سرچشمه",
           "سرود",
           "سشرق",
           "سشمال",
           "سصفها",
           "سصوفی",
           "سغرب",
           "سفار",
           "سفارس",
           "سفارود",
           "سفاسی",
           "سفانو",
           "سقاین",
           "سکارون",
           "سکرد",
           "سکرما",
           "سلار",
           "سمازن",
           "سمتاز",
           "سمگا",
           "سنوین",
           "سنیر",
           "سهرمز",
           "سهگمت",
           "سیتا",
           "سیدکو",
           "سیستم",
           "سیلام",
           "سیمرغ",
           "شاراک",
           "شاروم",
           "شاملا",
           "شاوان",
           "شبریز",
           "شبصیر",
           "شبندر",
           "شبهرن",
           "شپارس",
           "شپاس",
           "شپاکسا",
           "شپترو",
           "شپدیس",
           "شپلی",
           "شتهران",
           "شتوکا",
           "شتولی",
           "شجم",
           "شخارک",
           "شدوص",
           "شراز",
           "شرانل",
           "شرنگی",
           "شزنگ",
           "شسپا",
           "شسم",
           "شسینا",
           "شصدف",
           "شصفها",
           "شغدیر",
           "شفا",
           "شفارا",
           "شفارس",
           "شفن",
           "شکبیر",
           "شکربن",
           "شکف",
           "شکلر",
           "شگل",
           "شگویا",
           "شلرد",
           "شلعاب",
           "شمواد",
           "شنفت",
           "شوینده",
           "شیراز",
           "شیران",
           "صبا",
           "غاذر",
           "غالبر",
           "غبشهر",
           "غبهار",
           "غبهنوش",
           "غپآذر",
           "غپاک",
           "غپونه",
           "غپینو",
           "غچین",
           "غدام",
           "غدشت",
           "غزر",
           "غسالم",
           "غشاذر",
           "غشصفا",
           "غشهد",
           "غشهداب",
           "غشوکو",
           "غفارس",
           "غگرجی",
           "غگز",
           "غگل",
           "غگلپا",
           "غگلستا",
           "غگیلا",
           "غمارگ",
           "غمهرا",
           "غمینو",
           "غنوش",
           "غنیلی",
           "غویتا",
           "غیوان",
           "فاراک",
           "فارس",
           "فاسمین",
           "فافزا",
           "فالوم",
           "فاما",
           "فایرا",
           "فباهنر",
           "فبیرا",
           "فپنتا",
           "فجام",
           "فجر",
           "فخاس",
           "فخوز",
           "فرابورس",
           "فرآور",
           "فروس",
           "فروی",
           "فزرین",
           "فسا",
           "فسازان",
           "فسپا",
           "فسدید",
           "فسرب",
           "فلات",
           "فلوله",
           "فمراد",
           "فملی",
           "فن آوا",
           "فنرژی",
           "فنفت",
           "فنوال",
           "فنورد",
           "فوکا",
           "فولاد",
           "فولاژ",
           "فولای",
           "قاسم",
           "قپیرا",
           "قثابت",
           "قچار",
           "قرن",
           "قزوین",
           "قشرین",
           "قشکر",
           "قشهد",
           "قشیر",
           "قصفها",
           "قلرست",
           "قمرو",
           "قنیشا",
           "قهکمت",
           "کابگن",
           "کاذر",
           "کاسپین",
           "کالا",
           "کاما",
           "کاوه",
           "کایتا",
           "کبافق",
           "کپارس",
           "کپرور",
           "کپشیر",
           "کترام",
           "کتوکا",
           "کچاد",
           "کحافظ",
           "کخاک",
           "کرازی",
           "کرماشا",
           "کرمان",
           "کروی",
           "کساپا",
           "کسرا",
           "کسعدی",
           "کشرق",
           "کصدف",
           "کطبس",
           "کفرا",
           "کفرآور",
           "کقزوی",
           "کگاز",
           "کگل",
           "کگهر",
           "کلر",
           "کلوند",
           "کماسه",
           "کمرجان",
           "کمنگنز",
           "کمینا",
           "کنور",
           "کهرام",
           "کهمدا",
           "کوثر",
           "کویر",
           "کی بی سی",
           "کیا",
           "کیسون",
           "کیمیا",
           "گپارس",
           "گدنا",
           "گشان",
           "گکوثر",
           "گکیش",
           "گوهران",
           "لازما",
           "لبوتان",
           "لپارس",
           "لپیام",
           "لخانه",
           "لخزر",
           "لسرما",
           "لوتوس",
           "ما",
           "مادیرا",
           "مارون",
           "مبین",
           "مداران",
           "مرقام",
           "معیار ",
           "مفاخر",
           "ملت",
           "میدکو",
           "میهن",
           "نتوس",
           "نطرین",
           "نمرینو",
           "نوری",
           "نوین",
           "نیرو",
           "هجرت",
           "هرمز",
           "همراه",
           "وآتوس",
           "واتی",
           "واحصا",
           "واحیا",
           "وآذر",
           "وارس",
           "وآرین",
           "واعتبار",
           "وآفری",
           "والبر",
           "وامید",
           "وآوا",
           "وایرا",
           "وایران",
           "وآیند",
           "وبانک",
           "وبرق",
           "وبشهر",
           "وبصادر",
           "وبملت",
           "وبهمن",
           "وبوعلی",
           "وبیمه",
           "وپارس",
           "وپاسار",
           "وپترو",
           "وپخش",
           "وپسا",
           "وپست",
           "وپویا",
           "وتجارت",
           "وتعاون",
           "وتوس",
           "وتوسم",
           "وتوشه",
           "وتوصا",
           "وتوکا",
           "وثخوز",
           "وثنو",
           "وثوق",
           "وجامی",
           "وحافظ",
           "وخارزم",
           "وخاور",
           "ودی",
           "ورازی",
           "ورنا",
           "وزمین",
           "وساپا",
           "وساخت",
           "وساربیل",
           "وسالت",
           "وسبحان",
           "وسپه",
           "وسپهر",
           "وسخراج",
           "وسخراش",
           "وسرمد",
           "وسزنجان",
           "وسقم",
           "وسکاب",
           "وسکرشا",
           "وسگلستا",
           "وسمرکز",
           "وسنا",
           "وسیلام",
           "وسینا",
           "وشمال",
           "وشهر",
           "وصنا",
           "وصندوق",
           "وصنعت",
           "وغدیر",
           "وکادو",
           "وگردش",
           "وگستر",
           "ولانا",
           "ولبهمن",
           "ولپارس",
           "ولتجار",
           "ولساپا",
           "ولشرق",
           "ولصنم",
           "ولغدر",
           "ولملت",
           "ولیز",
           "ومشان",
           "ومعلم",
           "وملل",
           "وملی",
           "ومهان",
           "ونفت",
           "ونوین",
           "ونیرو",
           "ونیکی",
           "وهنر",
           "وهور"]

    # fill instrumentSel by Instrument entries
    feed_instrumentsel()

    # url for get instruments from mabna api
    api_url = base_url \
              + 'https://v1.db.api.mabnadp.com/exchange/instruments?'

    # list of missed instrument url
    sites = []

    # missed instrument counter (InstrumentSel)
    cntr = 0
    for itm in ins:
        # search instrument item
        res = models.Instrumentsel.objects.filter(short_name=itm)

        # check missed in instrumentSel
        if len(res) is 0:
            print("---")
            print(itm)
            cntr = cntr + 1

            # search instrument item in Instrument models
            res2 = models.Instrument.objects.filter(short_name=itm)
            print(res2)

            # check missed in instrument
            if len(res2) is 0:
                sites.append(f'{api_url}short_name={itm}@name_op=like')
            else:
                print(res2[0].id)

    print(f"missed files counr in instrumentSel: {cntr}")
    print(sites)

    # --- get missed instruments --//
    num_of_threads = 10
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_instrument_all, sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


# update all instrument candles
def daily_candle_update_thread(instrument_id, host):
    num_of_threads = 10

    model = models.Tradedetail
    # model.objects.filter(instrument=instrument_id).delete()
    try:
        obj = models.Instrumentsel.objects.get(id=instrument_id)

    except IntegrityError:
        print('Instrument not found!')
        return
    except ObjectDoesNotExist:
        print('Instrument Does Not Exist')
        return
    x = jdatetime.date.today()
    # print(x.strftime("%Y%m%d"))

    last_candle_date = models.Chart.objects.get(Q(instrument=instrument_id) & Q(timeFrame='D1')).last_candle_date
    print(f'last_candle_date: {last_candle_date}')

    api_url = ''
    if obj.index is None:
        # company_id = obj.stock_id
        company_id = obj.id
        print('company_id: ', company_id)
        api_url = base_url + 'https://v1.db.api.mabnadp.com/exchange/trades?' + 'instrument.id=' + company_id + \
                  '@date_time=' + last_candle_date + '@date_time_op=gt'
    else:
        company_id = obj.index_id
        api_url = base_url + 'https://v1.db.api.mabnadp.com/exchange/indexvalues?' + \
                  'index.id=' + company_id + '@date_time=' + last_candle_date + \
                  '@date_time_op=gt'

    sites = [
        api_url + '@_count=100@_skip=0',
        api_url + '@_count=100@_skip=100',
        api_url + '@_count=100@_skip=200',
    ]

    print(f'sites {sites}')
    # download_all_sites(sites)
    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(second_get_instrument, sites)

    # check result length
    if len(candle_list) == 0:
        return

    # read candle csv file and update it
    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='D1').data
        # find candle file url
        url = settings.MEDIA_ROOT.replace('\\', '/')
        parts = url.split('/')
        parts = parts[:-1]
        url = '/'.join(parts)
        url2 = url + candle.url
        print(url2)
        # url2 = 'http://127.0.0.1:8000' + candle.url
        # if host != '127.0.0.1:8000':
        #     url2 = url2.replace('/media/media/', '/media/')
        # read csv file
        df = pd.read_csv(url2)
        # iterate new candles and add to csv file
        for item in candle_list:
            print(item)
            # date conversion
            candle_parts = item.split(",")
            jalali_date = JalaliDate(int(candle_parts[0][:4]), int(candle_parts[0][4:6]),
                                     int(candle_parts[0][6:8])).to_gregorian()
            jalali_date = str(jalali_date).replace('-', '')
            print(jalali_date)
            # find similar row and replace or append new entry
            index = df['<DTYYYYMMDD>'].searchsorted(int(jalali_date), 'left')
            # print('index: ', index)
            to_append = [int(jalali_date), int(candle_parts[0][8:])
                , int(float(candle_parts[1])), int(float(candle_parts[2])), int(float(candle_parts[3]))
                , int(float(candle_parts[4])), int(float(candle_parts[5]))]
            df.loc[index, :] = to_append

        # print(df)
        df['<DTYYYYMMDD>'] = df['<DTYYYYMMDD>'].astype(int)
        # df['<TIME>'] = df['<TIME>'].astype(int)
        df['<OPEN>'] = df['<OPEN>'].astype(int)
        df['<HIGH>'] = df['<HIGH>'].astype(int)
        df['<LOW>'] = df['<LOW>'].astype(int)
        df['<CLOSE>'] = df['<CLOSE>'].astype(int)
        df['<VOL>'] = df['<VOL>'].astype(int)
        str_lst_date = str(df['<DTYYYYMMDD>'].iloc[-1])
        jl_date = jdatetime.date.fromgregorian(
            day=int(str_lst_date[6:]),
            month=int(str_lst_date[4:6]),
            year=int(str_lst_date[:4])
        )
        jl_date = str(jl_date).replace('-', '')
        models.Chart.objects.filter(instrument_id=instrument_id, timeFrame='D1').update(last_candle_date=jl_date)
        df.to_csv(url2, index=False)
    except IntegrityError:
        print('candle nadarim')
        return

    return
    # todo: update week csv
    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='W1').data
        # find candle file url
        url2 = url + candle.url
        # read csv file
        df_week = pd.read_csv(url2)
        # read las item
        print(len(df_week))
        # last_entry_date = df_week.loc[len(df_week)-1:,:]['<DTYYYYMMDD>']
        last_entry_date = df_week['<DTYYYYMMDD>'][len(df_week) - 1]
        last_day_date = df['<DTYYYYMMDD>'][len(df) - 1]
        print(last_entry_date, last_day_date)
        d_last = datetime.strptime(str(last_entry_date), "%Y%m%d").date()
        day_last = datetime.strptime(str(last_day_date), "%Y%m%d").date()
        day_last = day_last + timedelta(weeks=1)
        print('date,', d_last, day_last)
        week_prior = d_last - timedelta(weeks=1)
        d_last = d_last + timedelta(weeks=1)
        week_next = d_last + timedelta(weeks=1)
        print('three', week_prior, d_last, week_next)
        while day_last > week_next:
            d_last_str = str(d_last).replace('-', '')
            week_next_str = str(week_next).replace('-', '')
            # find start day of week
            index_start_day = df['<DTYYYYMMDD>'].searchsorted(int(d_last_str), 'left')
            # find stop day  of week
            index_stop_day = df['<DTYYYYMMDD>'].searchsorted(int(week_next_str), 'left')
            print('week: ', d_last_str, week_next_str)
            print('index: ', index_start_day, index_stop_day)
            df_days_of_week = df[:][index_start_day:index_stop_day]
            print(df_days_of_week)

            # sum of volume
            vol = 0
            for i in range(len(df_days_of_week)):
                print('vol', df_days_of_week['<VOL>'][index_start_day + i])
                if df_days_of_week['<VOL>'][index_start_day + i] < 0:
                    vol = vol + (int(df_days_of_week['<VOL>'][index_start_day + i]) * -1)
                else:
                    vol = vol + int(df_days_of_week['<VOL>'][index_start_day + i])
                print('after plus vol', vol)

            candle_week = [int(d_last_str), int(0), int(df_days_of_week['<OPEN>'][index_start_day])
                , int(df_days_of_week['<HIGH>'].max())
                , int(df_days_of_week['<LOW>'].min())
                , int(df_days_of_week['<CLOSE>'][index_start_day + len(df_days_of_week) - 1])
                , vol
                           ]
            print('candle_week: ', candle_week)

            df_week.loc[len(df_week) - 1, :] = candle_week

            df_week['<DTYYYYMMDD>'] = df_week['<DTYYYYMMDD>'].astype(int)
            # df_week['<TIME>'] = df_week['<TIME>'].astype(int)
            df_week['<OPEN>'] = df_week['<OPEN>'].astype(int)
            df_week['<HIGH>'] = df_week['<HIGH>'].astype(int)
            df_week['<LOW>'] = df_week['<LOW>'].astype(int)
            df_week['<CLOSE>'] = df_week['<CLOSE>'].astype(int)
            df_week['<VOL>'] = df_week['<VOL>'].astype(int)
            df_week.to_csv(url2, index=False)

            d_last = datetime.strptime(str(d_last_str), "%Y%m%d").date()
            week_next = datetime.strptime(str(week_next_str), "%Y%m%d").date()

            d_last = d_last + timedelta(weeks=1)
            week_next = d_last + timedelta(weeks=2)
        models.Chart.objects.filter(instrument_id=instrument_id, timeFrame='W1').update(
            last_candle_date=df_week['<DTYYYYMMDD>'][len(df_week) - 1])
        # print(df)
    except IntegrityError:
        print('candle nadarim')

    # todo: update month csv
    return

    # old method
    cndl_list = [''] * len(candle_list)
    for i in range(len(candle_list)):
        print('shomare', i)
        # check duplication candles
        if i > 0:
            lst = candle_list[i].split(",")
            lst_prv = candle_list[i - 1].split(",")
            if int(float(lst[0][:8])) == int(float(lst_prv[0][:8])):
                jalali_date = JalaliDate(int(lst[0][:4]), int(lst[0][4:6]), int(lst[0][6:8])).to_gregorian()
                jalali_date = str(jalali_date).replace('-', '')
                lstt = [jalali_date, lst_prv[0][8:], lst_prv[1], max(lst_prv[2], lst[2]), min(lst_prv[3], lst[3]),
                        lst[4], lst_prv[5]]
                str1 = ','.join(lstt)
                cndl_list[i] = str1
                cndl_list[i - 1] = 'deleted'
            else:
                jalali_date = JalaliDate(int(lst[0][:4]), int(lst[0][4:6]), int(lst[0][6:8])).to_gregorian()
                jalali_date = str(jalali_date).replace('-', '')
                lstt = [jalali_date, lst[0][8:], lst[1], lst[2], lst[3],
                        lst[4], lst[5]]
                str1 = ','.join(lstt)
                cndl_list[i] = str1
        else:
            # add first row
            lst = candle_list[i].split(",")
            jalali_date = JalaliDate(int(lst[0][:4]), int(lst[0][4:6]), int(lst[0][6:8])).to_gregorian()
            jalali_date = str(jalali_date).replace('-', '')
            lstt = [jalali_date, lst[0][8:], lst[1], lst[2], lst[3], lst[4], lst[5]]
            str1 = ','.join(lstt)
            cndl_list[i] = str1
    new_candle_list = [x for x in cndl_list if x != 'deleted']
    print('new_candle_list: ', len(new_candle_list))

    try:
        candle = models.Chart.objects.get(instrument_id=instrument_id, timeFrame='D1').data
        candle_name = str(candle).split('/')[-1]
        # find candle file url
        url = settings.MEDIA_ROOT.replace('\\', '/')
        parts = url.split('/')
        parts = parts[:-1]
        url = '/'.join(parts)
        url2 = url + candle.url
        # read csv file
        df = pd.read_csv(url2)
        i = 0
        for item in new_candle_list:
            print(i)
            i += 1
            lst = item.split(",")
            print('sdfsdf', item)
            print('sdfsdf', lst)
            to_append = [int(float(lst[0])), int(float(lst[1])), int(float(lst[2])),
                         int(float(lst[3])), int(float(lst[4])), int(float(lst[5])), int(float(lst[6]))]
            df.loc[len(df), :] = to_append
        print(df.tail())
        df.to_csv(url2, index=False)
    except IntegrityError:
        print('candle nadarim')
    print(f"Downloaded {len(sites)} in {duration} seconds")
