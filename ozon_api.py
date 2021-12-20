import requests, json, datetime, pandas
import myapi

class OZON:
    def __init__(self):
        self.xlsx = pandas.read_excel('all_sku.xlsx')
        self.xlsx['OZ'] = self.xlsx['OZ'].fillna(0)
        self.url = 'http://api-seller.ozon.ru/v2/product/info'
        self.headers = {
            'Content-Type': 'application/json',
            'Host': 'api-seller.ozon.ru',
            'Client-Id': myapi.azet.get('client'),
            'Api-Key': myapi.azet.get('key')
            }
        self.DF = pandas.DataFrame()
        self.ROW = 1

    def search(self, sku):
        payload = {
            "sku": sku,
            "language":"RU"
        }
        res = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        data = json.loads(res.text)
        try:
            self.DF.at[self.ROW,'SKU'] = int(sku)
            self.DF.at[self.ROW,'BARCODE'] = data['result']['barcode']
            self.DF.at[self.ROW,'NAME'] = data['result']['name']
            self.DF.at[self.ROW,'PRICE'] = data['result']['marketing_price']
            self.DF.at[self.ROW,'OLD_PRICE'] = data['result']['old_price']
            self.DF.at[self.ROW,'FOTOS'] = len(data['result']['images']) + 1
            self.DF.at[self.ROW,'STOCK'] = data['result']['stocks']['present']
            self.DF.at[self.ROW,'URL'] = 'https://www.ozon.ru/product/' + str(sku)
        except:
            pass
        finally:
            self.ROW += 1


    def main(self):
        for sku in self.xlsx.OZ:
            if sku != 0 and sku != '0':
                self.search(int(sku))
        self.DF.to_excel(f'/opt/reports/ozon/Ozon_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def start():
    OZON().main()

if __name__ == '__main__':
    start()
