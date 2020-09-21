
import base64
import requests
import json
from .models import Meta, Index


def feed_index():
    # json_data = open('D:/projects/mediabourse/git_projects/mbna-api data/index.json', encoding='utf-8')
    # data1 = json.load(json_data)  # deserialises it
    # data2 = json.dumps(data1)  # json formatted string

    url = 'https://v1.db.api.mabnadp.com/exchange/indexes?_count=100&_skip=0'

    access_token = b'd19573a3602e9c3c320bd8b3b737f28f'
    header_value = base64.b64encode(access_token + b':')
    headers = {'Authorization': b'Basic ' + header_value}
    req = requests.get(url, headers=headers)
    data1 = req.json()

    # data_list = data2['data']
    print(data1['data'][0])
    print(data1['data'][0]['name'])

    for data in data1['data']:
        print(data)
        print('check: ' , int(data['meta']['version']))
        obj_meta = Meta(version=int(data['meta']['version']), state=data['meta']['state'], insert_date_time=data['meta']['insert_date_time'], type=data['meta']['type'])
        if 'update_date_time' in data['meta']:
            obj_meta.update_date_time = data['meta']['update_date_time']

        ch = Meta.objects.filter(version=obj_meta.version)
        print("ch," , len(ch))
        if len(ch) > 0:
            print('duplicate')
            print(ch[0].version)

        print(obj_meta.version)
        obj_meta.save()
        obj_index = Index(meta=obj_meta, code=data['code'], name=data['name'], english_name=data['english_name'], short_name=data['short_name'], english_short_name=data['english_short_name'], fingilish_name=data['fingilish_name'], fingilish_short_name=data['fingilish_short_name'], id=data['id'])
        obj_index.save()
        print('saved ', obj_meta.version)
        # break

    # json_data.close()


def test_index():
    json_data = open('D:/projects/mediabourse/git_projects/mbna-api data/index.json', encoding='utf-8')
    data1 = json.load(json_data)  # deserialises it

    cntr = 0
    for data in data1['data']:
        obj = Index.objects.get(id=data['id'])
        if obj.meta.version != int(data['meta']['version']):
            print(data)
            print(obj.meta.version , '??' , int(data['meta']['version']))
            print("false------")
            cntr = cntr + 1
    print("false count = " , cntr)

    json_data.close()


def check_update_index():
    pass