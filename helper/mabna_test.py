import base64
import io
import json

import requests

url = 'https://v1.db.api.mabnadp.com/bond/bonds'

access_token = b'd19573a3602e9c3c320bd8b3b737f28f'

header_value = base64.b64encode(access_token + b':')

headers = {'Authorization': b'Basic ' + header_value}

req = requests.get(url, headers=headers)

with open('data1.json', 'w', encoding='utf-8') as f:
    json.dump(req.json(), f, ensure_ascii=False)
