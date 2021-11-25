import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime, time, random
from agents import agent

class citi:
    def __init__(self):
        self.URL = "https://www.citilink.ru/search/?text="
        self.ROW = 1
        self.DF = pd.DataFrame(columns=['SKU','NAME','BARCODE','URL','PRICE','STARS','REPORTS'])
        self.SKU = {}
        self.session = requests.Session()
        self.session.cookies.clear()
    
    def get_info(self, soup, sku, url):
        ## Название товара
        name = soup.find('h1', class_='Heading Heading_level_1 ProductHeader__title').text.strip()

        # Звёзды и отзывы
        meta = soup.find('div', class_='ProductHeader__icon-count js--ProductHeader__icon-count')
        if meta != None:
            if len(meta) >= 1:
                meta.find_all('span', class_='IconWithCount__count js--IconWithCount__count')
                strip_meta = []
                for i in meta:
                    strip_meta.append(i.text.strip())
            else:
                # print(f'\n\n\nproverit {url}\n\n\n')
                strip_meta = ['0','0']
        else:
            strip_meta = ['0','0']

        # Цена товара
        price = soup.find('span', class_='ProductHeader__price-default_current-price js--ProductHeader__price-default_current-price')
        if price != None:
            price = price.text.strip()
        else:
            price = 0
        print(name, strip_meta, price)
        self.DF.at[self.ROW,'SKU'] = sku
        self.DF.at[self.ROW,'NAME'] = name
        self.DF.at[self.ROW,'BARCODE'] = self.SKU.get(sku)
        self.DF.at[self.ROW,'URL'] = url
        self.DF.at[self.ROW,'PRICE'] = price
        self.DF.at[self.ROW,'STARS'] = strip_meta[0]
        self.DF.at[self.ROW,'REPORTS'] = strip_meta[1]
        self.ROW += 1
        
    def no_data(self, sku):    
        self.DF.at[self.ROW,'SKU'] = sku
        self.DF.at[self.ROW,'NAME'] = 'not found'
        self.DF.at[self.ROW,'BARCODE'] = self.SKU.get(sku)
        self.DF.at[self.ROW,'URL'] = 'not found'
        self.ROW += 1

    def capcha(self, soup):
        redir = soup.find('input', {'name':'redirect_to'})['value']
        time.sleep(5)
        payload = {
            'captcha': 'fdfd',
            'captchaKey':'',
            'limited_action': '11',
            'redirect_to': redir
        }
        response = self.session.post('https://www.citilink.ru/web_firewall/check_captcha/', data=payload)
        return bs(response.text, 'lxml')

    def get_page(self, sku):
        headers = {
            'User-Agent' : random.choice(agent)
        }
        response  = self.session.get(self.URL + sku, headers=headers)
        print(response.status_code, response.url)
        if response.status_code == (200):
            if self.URL not in response.url:
                soup = bs(response.text, 'lxml')
                self.get_info(soup, sku, response.url)
            else:
                self.no_data(sku)
        elif response.status_code == 429:
            soup = bs(response.text, 'lxml')
            soup = self.capcha(soup)
            self.get_info(soup, sku, response.url)
        else:
            print(sku, response.status_code)

    def start(self):
        self.session.get('https://www.citilink.ru')
        df = pd.read_excel('citilink.xlsx')
        for i in range(len(df.sku)):
            self.SKU.update({str(df.iat[i,0]):str(df.iat[i,1])})
        for sku in self.SKU:
            self.get_page(sku)
            time.sleep(2 if i % 5 != 0 else 10)
        self.session.close()
        self.DF.to_excel(f'/opt/reports/citilink/citilink_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def main():
    CL = citi().start()

if __name__ == '__main__':
    CL = citi().start()