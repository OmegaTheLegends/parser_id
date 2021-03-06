from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime, os, json, time

class dns_main:
    def __init__(self):
        if os.name == 'nt':
            self.GECKO = 'C:\\TEMP\\geckodriver.exe' # windows
            self.SAVE_FOLDER = 'C:\\TEMP\\' # windows
            self.url_file_url = 'dns_sku_id.txt'
        else:
            self.GECKO = '/opt/geckodriver' # linux
            self.SAVE_FOLDER = '/opt/reports/dns/' #linux
            self.url_file_url = '/opt/parser_id/dns_sku_id.txt'
        self.ROW = 1
        self.url_data = {}

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            # 'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


        self.options = webdriver.FirefoxOptions()
        # user-agent
        self.options.binary_location = "/usr/bin/firefox"
        self.options.headless = True
        # disable webdriver mode
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("permissions.default.image", 2)


    def start(self):
        self.DF = pd.DataFrame()
        driver = webdriver.Firefox(executable_path=self.GECKO, options=self.options, firefox_profile=self.profile)
        driver.get('https://www.dns-shop.ru')

        if not os.path.exists(self.url_file_url):
            with open(self.url_file_url, 'w', encoding='utf8') as f:
                f.write('')

        with open(self.url_file_url, 'r', encoding='utf8') as f:
            for line in f.readlines():
                if len(line) > 2:
                    data = line.strip().split(':')
                    self.url_data.update({str(data[0]):data[1]})

        with open('dns_sku.txt', 'r', encoding='utf8') as f:
            sku_list = f.read().split('\n')

        for id in sku_list:
            if self.url_data.get(str(id)):
                eid = self.url_data.get(str(id))
                driver.get(f'https://www.dns-shop.ru/product/microdata/{eid}/')
                # print(driver.current_url)
                response = driver.page_source
            else:
                driver.get(f'https://www.dns-shop.ru/search/?q={str(id)}')
                # print(driver.current_url)
                source = driver.page_source
                soup = bs(source, 'lxml')
                eid = soup.find('div', class_='container product-card').get('data-product-card')
                with open(self.url_file_url, 'a', encoding='utf8') as f:
                    f.write(f'{id}:{eid}\n')
                driver.get(f'https://www.dns-shop.ru/product/microdata/{eid}/')
                response = driver.page_source
            soup = bs(response, 'lxml')
            try:
                json_info = soup.find('div', id='json').text
                data = json.loads(json_info)
                self.DF.at[self.ROW,'SKU'] = str(id)
                self.DF.at[self.ROW,'NAME'] = data['data']['name']
                if 'offers' in data['data']:
                    self.DF.at[self.ROW,'PRICE'] = int(data['data']['offers']['price'])
                else:
                    self.DF.at[self.ROW,'PRICE'] = 0
                if 'aggregateRating' in data['data']:
                    self.DF.at[self.ROW,'STARTS'] = data['data']['aggregateRating']['ratingValue']
                    self.DF.at[self.ROW,'REPORTS'] = data['data']['aggregateRating']['reviewCount']
                # if 'offers' in data['data']:
                #     self.DF.at[self.ROW,'URL'] = data['data']['offers']['url']
                self.DF.at[self.ROW,'DESCRIPTION'] = data['data']['description']
            except:
                print(f'JSON not found {id=}')
                list_data = soup.find('tbody').find_all('tr')
                for i in list_data:
                    y = i.get('id')
                    if y == '/data/name':
                        self.DF.at[self.ROW,'NAME'] = i.find(class_='objectBox').text
                    if y == '/data/offer/price':
                        self.DF.at[self.ROW,'PRICE'] = int(i.find(class_='objectBox').text)
                    else:
                        self.DF.at[self.ROW,'PRICE'] = 0
                    if y == '/data/aggregateRating/ratingValue':
                        self.DF.at[self.ROW,'STARTS'] = i.find(class_='objectBox').text
                    if y == '/data/aggregateRating/reviewCount':
                        self.DF.at[self.ROW,'REPORTS'] = i.find(class_='objectBox').text
                    if y == '/data/description':
                        self.DF.at[self.ROW,'DESCRIPTION'] = i.find(class_='objectBox').text
            self.ROW += 1
            time.sleep(1)

        driver.close()
        driver.quit()
        self.DF.to_excel(f'{self.SAVE_FOLDER}dns_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def main():
    DNS = dns_main()
    DNS.start()


if __name__ == '__main__':
    DNS = dns_main()
    DNS.start()
