import requests
import json
from pprint import pprint
from myapi import ozon

url = 'http://api-seller.ozon.ru/v2/product/info'

headers = {
        'Content-Type': 'application/json',
        'Host': 'api-seller.ozon.ru',
        'Client-Id': ozon.get('client'),
        'Api-Key': ozon.get('key')
    }

data = {
    "sku": 160678400,
    "language":"RU"
}

res = requests.post(url, headers=headers, data=json.dumps(data))
pprint(res.text)
