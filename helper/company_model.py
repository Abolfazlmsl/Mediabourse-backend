# import base64
#
# import requests
#
# index = 0
# while True:
#
#     url = f"https://v1.db.api.mabnadp.com/exchange/instruments?_expand=market,board,group,stock&_count=100&_skip={100 * index}"
#     access_token = b'd19573a3602e9c3c320bd8b3b737f28f'
#
#     header_value = base64.b64encode(access_token + b':')
#
#     headers = {'Authorization': b'Basic ' + header_value}
#
#     req = requests.get(url, headers=headers)
#
#     # text_file = open("Output.txt", "a")
#     # text_file.write(req.text)
#     # text_file.close()
#
#     index += 1
#     # print(req.json())
#
#     data_list = req.json()['data']
#     for data in data_list:
#         print(data)
#         break
#
#     break
