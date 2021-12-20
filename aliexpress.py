import requests, json, pandas as pd
from bs4 import BeautifulSoup as bs
import time, datetime

class alibaba:
    def __init__(self) -> None:
        self.headers = {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
        }
        self.DF = pd.DataFrame(columns=['SKU','NAME','BARCODE','PRICE','DISCOUNT','MAXPRICE','STARS','REPORTS','LIKES','TRADE','DESCRIPTION'])
        self.ROW = 1
        self.SKU = {}

    def get_info_from_page(self,id):
        response = requests.get(f'https://aliexpress.ru/item/{str(id)}')
        soup = bs(response.text, 'lxml')
        data = json.loads(soup.find('script', id="__AER_DATA__").text)

        if 'children' in data['widgets'][0]:
            self.DF.at[self.ROW,'SKU'] = id
            self.DF.at[self.ROW,'BARCODE'] = self.SKU.get(id)
            self.DF.at[self.ROW,'NAME'] = data['widgets'][0]['children'][7]['children'][0]['props']['name']
            self.DF.at[self.ROW,'DESCRIPTION'] = data['widgets'][0]['children'][7]['children'][0]['props']['description']
            self.DF.at[self.ROW,'LIKES'] = data['widgets'][0]['children'][7]['children'][0]['props']['likes']
            self.DF.at[self.ROW,'DISCOUNT'] = data['widgets'][0]['children'][7]['children'][0]['props']['price']['discount']
            self.DF.at[self.ROW,'PRICE'] = data['widgets'][0]['children'][7]['children'][0]['props']['price']['formattedActivityPrice']
            self.DF.at[self.ROW,'MAXPRICE'] = data['widgets'][0]['children'][7]['children'][0]['props']['price']['formattedPrice']
            self.DF.at[self.ROW,'STARS'] = data['widgets'][0]['children'][7]['children'][0]['props']['rating']['middle']
            #all_stars  = data['widgets'][0]['children'][7]['children'][0]['props']['rating']['middle']['stars']
            #banner  = data['widgets'][0]['children'][7]['children'][0]['props']['banner']
            self.DF.at[self.ROW,'TRADE'] = data['widgets'][0]['children'][7]['children'][0]['props']['tradeInfo']['tradeCount']
            self.DF.at[self.ROW,'REPORTS'] = data['widgets'][0]['children'][7]['children'][0]['props']['reviews']
        else:
            self.DF.at[self.ROW,'SKU'] = id
            self.DF.at[self.ROW,'BARCODE'] = self.SKU.get(id)

    def start(self):
        xlsx = pd.read_excel('/opt/parser_id/aliexpress.xlsx')
        for i in range(len(xlsx.ШК)):
                sku = str(xlsx.iat[i,4])
                if len(sku) > 2:
                    self.SKU.update({str(sku):str(xlsx.iat[i,3])})
                    # print(sku)
                    time.sleep(1 if i % 15 != 0 else 5)
                    self.get_info_from_page(sku)
                else:
                    self.DF.at[self.ROW,'SKU'] = sku
                    self.DF.at[self.ROW,'BARCODE'] = str(xlsx.iat[i,3])
                self.ROW += 1
                # if self.ROW == 10:
                #     break
        self.DF.to_excel(f'/opt/reports/aliexpress/aliexpress_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def main():
    alibaba().start()

if __name__ == '__main__':
    main()