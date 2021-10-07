import requests
import json
from pprint import pprint

url = 'http://api-seller.ozon.ru/v2/product/info'

headers = {
        'Content-Type': 'application/json',
        'Host': 'api-seller.ozon.ru',
        'Client-Id': '1657',
        'Api-Key': '69f150e7-9ef5-430a-96b8-b0881999273e'
    }

data = {
    "sku": 160678400,
    "language":"RU"
}

res = requests.post(url, headers=headers, data=json.dumps(data))
pprint(res.text)
