import base64
import requests
import json

from django.db.models import Q
import jdatetime

from .models import Meta, Index, Exchange
from . import models
import logging
import threading
import time
import concurrent.futures


def feed_index():
    offset = 0
    step = 50
    is_has_next = True

    #  check model is empty or not
    if Index.objects.count() > 0:
        last_index_meta_version = Index.objects.latest('meta__version')
        print(last_index_meta_version.meta.version)
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + 'https://v1.db.api.mabnadp.com/exchange/indexes?' + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + 'https://v1.db.api.mabnadp.com/exchange/indexes?'

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + 'https://v1.db.api.mabnadp.com/exchange/exchanges?' + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + 'https://v1.db.api.mabnadp.com/exchange/exchanges?'

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.meta.version) + '&meta.version_op=gt&'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url

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
                obj_stock = models.Companie.objects.get(id=data['stock']['company']['id'])

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

    feed_instrument()
    sel_obj = models.Instrument.objects.filter(Q(type='share')
                                               & Q(market=1)
                                               & Q(exchange_state=1)
                                               & (Q(board=1) | Q(board=2) | Q(board=4) | Q(board=6))
                                               )
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


def feed_tradedaily(instrument_id, index):
    offset = 0
    step = 50
    # is_has_next = True
    print(instrument_id, index)
    logging.info("Thread %s: starting", index)
    model = models.Tradedetail
    # model.objects.all().delete()
    api_url = 'https://v1.db.api.mabnadp.com/exchange/tradedetails?'
    # return

    last_version_from_delete = -1
    is_error_expand = False

    #  check model is empty or not
    if model.objects.filter(instrument=instrument_id).count() > 0:
        last_index_meta_version = model.objects.filter(instrument=instrument_id).latest('version')

        # check last received item is meta.state == deleted ?
        print(last_version_from_delete, last_version_from_delete != -1)
        if last_version_from_delete != -1:
            last_index_meta_version.version = last_version_from_delete
            print('------------- set delete version --------------- ' + str(last_index_meta_version.version))

        # print(last_index_meta_version.meta.version)
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   'instrument.id=' + instrument_id + '&' + \
                   '_sort=meta.version&meta.version=' + str(
            last_index_meta_version.version) + '&meta.version_op=gt' + '&_count=100&_skip=' + index + '* 100'
        if is_error_expand is False:
            get_data = get_data + '@_expand=trade'
    else:
        # print('empty')
        get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                   'instrument.id=' + instrument_id + '&_sort=meta.version' + '&_count=100&_skip=' + index + '* 100'
        if is_error_expand is False:
            get_data = get_data + '@_expand=trade'


    get_data2 = get_data #+ '_count=' + str(step) + '&_skip=' + str(offset) + '&_expand=trade'
    get_data2 = get_data2.replace("&", "@")  # replace & with @, because of & conflict
    print(get_data2)
    req = requests.get(get_data2)
    print(req.text)
    data1 = req.json()

    if 'error' in data1:
        print(data1['error']['code'] + ' - ' + data1['error']['message'])
        is_error_expand = True

    #  check next pagination
    # if len(data1['data']) == step:
    #     offset = offset + step
    # else:
    #     is_has_next = False

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
            url_trade = 'http://mediadrive.ir/bourse/api-test/?url=' + 'https://v1.db.api.mabnadp.com/exchange/trades?id=' + data['trade']['id']
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

        logging.info("Thread %s: finishing", index)




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
            get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
                       'instrument.stock.company.id=' + company_id + '&' + \
                       'date_time=' + today_date + timee + '&_sort=meta.version=' + str(
                last_index_meta_version.version) + '&date_time_op=gt'
        else:
            get_data = 'http://mediadrive.ir/bourse/api-test/?url=' + api_url + \
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
            continue #break

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
            obj_company = models.Companie.objects.get(id=company_id)
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