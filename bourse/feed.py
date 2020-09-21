import base64
import requests
import json
from .models import Meta, Index


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
