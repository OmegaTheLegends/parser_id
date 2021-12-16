import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import datetime, time, os

class citi:
    def __init__(self):
        self.URL = "https://www.citilink.ru/search/?text="
        if os.name == 'nt':
            self.GECKO = 'C:\\TEMP\\geckodriver.exe' # windows
        else:
            self.GECKO = '/opt/geckodriver' # linux
        self.ROW = 1
        self.DF = pd.DataFrame(columns=['SKU','NAME','BARCODE','URL','PRICE','STARS','REPORTS'])
        self.SKU = {}
        self.session = requests.Session()
        self.session.cookies.clear()
        self.options = webdriver.FirefoxOptions()
        # user-agent
        self.options.binary_location = "/usr/bin/firefox"
        self.options.headless = True
        # disable webdriver mode
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("permissions.default.image", 2)
    
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
        # print(name, strip_meta, price)
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
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive',
            #'Cookie' : r'old_design=0; _tuid=e085c28cca7b29e4ac59b326f38a3ea471087fea; _space=msk_cl%3A; ab_test=90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A6%7Cnew_designv13%3A1%7Cproduct_card_design%3A3%7Cdummy%3A20; ab_test_analytics=90x10v4%3A1%7Creindexer%3A2%7Cnew_designv10%3A6%7Cnew_designv13%3A1%7Cproduct_card_design%3A3%7Cdummy%3A20; _dy_ses_load_seq=55481%3A1638186600431; _dy_c_exps=; _dy_soct=1036728.1078892.1637142086*1017570.1030352.1638186579*1015299.1026209.1638186579*1015300.1026211.1638186580*1033770.1068198.1638…19543844%3Bv%3A1448806%3A1638090294484%3Bv%3A397588%3A1637148709118%3Bv%3A1587166%3A1637146817226%3Bv%3A1070048%3A1637146454053%3Bv%3A1400534%3A1637142653885; _ym_uid=1637144890615923855; _ym_d=1637144890; _hjSessionUser_1592904=eyJpZCI6ImI3MTkxOTUxLTc1OTEtNTYwNy04MTc2LWZjNTJjYWFiNmRiZCIsImNyZWF0ZWQiOjE2MzcyMTk1NDMyNDIsImV4aXN0aW5nIjp0cnVlfQ==; mindboxDeviceUUID=b402dc2f-1ae2-47f7-98d3-5b6a2373a1c1; directCrm-session=%7B%22deviceGuid%22%3A%22b402dc2f-1ae2-47f7-98d3-5b6a2373a1c1%22%7D; _pcl=eW5hpkNB+ULlrA==',
            'Host': 'www.citilink.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'TE': 'trailers',
            'Upgrade-Insecure-Requests': '1',
            "Keep-Alive" : "timeout=10, max=5",
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
        }
        response  = self.session.get(self.URL + sku, headers=headers)
        # print(response.status_code, response.url)
        if response.status_code == (200):
            if self.URL not in response.url:
                soup = bs(response.text, 'lxml')
                self.get_info(soup, sku, response.url)
            else:
                self.no_data(sku)
        elif response.status_code == 429:
            soup = bs(response.text, 'lxml')
            try:
                soup = self.capcha(soup)
                print('capcha passed')
            except:
                pass
            self.get_info(soup, sku, response.url)
        else:
            print(sku, response.status_code)

    def start(self):
        driver = webdriver.Firefox(executable_path=self.GECKO, options=self.options, firefox_profile=self.profile)
        driver.get('https://www.citilink.ru')
        time.sleep(3)
        driver.close()
        driver.quit()
        df = pd.read_excel('citilink.xlsx')
        for i in range(len(df.sku)):
            self.SKU.update({str(df.iat[i,0]):str(df.iat[i,1])})
        for sku in self.SKU:
            time.sleep(2 if i % 5 != 0 else 10)
            self.get_page(sku)
        self.session.close()
        self.DF.to_excel(f'/opt/reports/citilink/citilink_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def main():
    CL = citi().start()

if __name__ == '__main__':
    CL = citi().start()