import base64
import requests
import jdatetime

today_date = str(jdatetime.date.today())
today_date = today_date.replace('-', '')

shakhes_kol_url = f"https://v1.db.api.mabnadp.com/exchange/indexintradayvalues?index.id=1&date_time={today_date}&date_time_op=gt&_count=100"
shakhes_sanat_url = f"https://v1.db.api.mabnadp.com/exchange/indexintradayvalues?index.id=5&date_time={today_date}&date_time_op=gt&_count=100"
shakhes_hamvazn_url = f"https://v1.db.api.mabnadp.com/exchange/indexintradayvalues?index.id=57&date_time={today_date}&date_time_op=gt&_count=100"
shakhes_farabors_url = f"https://v1.db.api.mabnadp.com/exchange/indexintradayvalues?index.id=60&date_time={today_date}&date_time_op=gt&_count=100"


access_token = b'd19573a3602e9c3c320bd8b3b737f28f'

header_value = base64.b64encode(access_token + b':')

headers = {'Authorization': b'Basic ' + header_value}

kol_req = requests.get(shakhes_kol_url, headers=headers)
sanat_req = requests.get(shakhes_sanat_url, headers=headers)
hamvazn_req = requests.get(shakhes_hamvazn_url, headers=headers)
farabors_req = requests.get(shakhes_farabors_url, headers=headers)

print(kol_req.text)
