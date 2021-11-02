# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup as bs
import pandas
import time, datetime, random
import capcha


class ozon:
    def __init__(self):
        # self.console = Console()
        self.URL = 'https://www.ozon.ru/product/'
        self.xlsx = pandas.read_excel('all_sku.xlsx')
        self.xlsx['OZ'] = self.xlsx['OZ'].fillna(0)
        self.GECKO = '/opt/geckodriver' # linux
        self.SAVE_FOLDER = '/opt/reports/ozon/' #linux
        # self.GECKO = 'C:\\temp\\geckodriver.exe' # windows
        # self.SAVE_FOLDER = 'C:\\TEMP\\' # windows
        self.main_url = 'https://www.ozon.ru'

        self.DF = pandas.DataFrame()

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


        self.options = Options()
        # user-agent
        self.options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        self.options.headless = True
        self.options.set_preference("http.response.timeout", 30)
        self.options.binary_location = "/usr/bin/firefox"
        # disable webdriver mode
        self.options.set_preference("dom.webdriver.enabled", False)
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("permissions.default.image", 2)

    def GET_UA(self):
        uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                    ]

        return random.choice(uastrings)

    def get_info_from_page(self,IDS):
        for i in range(len(IDS)):  # len(IDS)
            if self.xlsx.iat[i,3] != 0 and self.xlsx.iat[i,3] != '0':
                t_id = int(self.xlsx.iat[i,3])
                try:
                    self.drive.get(self.URL + str(t_id))
                except TimeoutException:
                    self.drive.get(self.URL + str(t_id))
                    continue
                time.sleep(2.2)
                if self.drive.current_url == 'https://www.ozon.ru/product/' + str(t_id):
                    time.sleep(0.3)
                    html = self.drive.page_source
                    soup = bs(html, 'lxml')
                    try:
                        if self.drive.find_element_by_class_name('page-503'):
                            print('page 503')
                            self.drive.refresh()
                            time.sleep(1)
                    except:
                        pass
                    try:
                        if soup.find('div',class_='a3q6').get('data-widget') == 'error':
                            self.DF.at[self.ROW,'SKU'] = str(IDS[i])
                            # self.DF.at[self.ROW,'URL'] = str(None)
                            self.DF.at[self.ROW,'NAME'] = str('Товар не найден')
                            # self.DF.at[self.ROW,'PRICE'] = str(None)
                            # self.DF.at[self.ROW,'STARS'] = str(None)
                            # self.DF.at[self.ROW,'REPORTS'] = str(None)
                            # self.DF.at[self.ROW,'FOTOS'] = str(None)
                            try:
                                self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i,1])
                            except:
                                # self.DF.at[self.ROW,'BARCODE'] = None
                                pass
                            try:
                                self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i,0])
                            except:
                                pass

                            self.ROW += 1
                            # print(IDS[i], 'Товар не найден')
                            continue
                    except Exception as e:
                        pass
                        # self.console.print_exception(show_locals=True)
                    try:
                        if 'Товар закончился' in soup.find('div',class_='c2e2').text:
                            self.DF.at[self.ROW,'SKU'] = str(IDS[i])
                            # self.DF.at[self.ROW,'URL'] = str(None)
                            self.DF.at[self.ROW,'NAME'] = str('Товар закончился')
                            # self.DF.at[self.ROW,'PRICE'] = str(None)
                            # self.DF.at[self.ROW,'STARS'] = str(None)
                            # self.DF.at[self.ROW,'REPORTS'] = str(None)
                            # self.DF.at[self.ROW,'FOTOS'] = str(None)
                            try:
                                self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i,1])
                            except:
                                # self.DF.at[self.ROW,'BARCODE'] = None
                                pass
                            try:
                                self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i,0])
                            except:
                                pass

                            self.ROW += 1
                            # print(IDS[i], 'Товар закончился')
                            continue
                    except Exception as e:
                        pass
                        # self.console.print_exception(show_locals=True)
                    try:
                        html = self.drive.page_source
                        soup = bs(html, 'lxml')
                        iframe = soup.find('iframe').get('id')
                        if iframe == 'main-iframe':
                            fin = capcha.start_cap(self.drive)
                            if fin == False:
                                time.sleep(300)
                                self.drive.refresh()
                            else:
                                self.drive = fin

                    except Exception as e:
                        # self.console.print_exception(show_locals=True)
                        time.sleep(20)
                        self.drive.refresh()
                        time.sleep(1)
                        if self.drive.current_url == 'https://www.ozon.ru/product/' + str(t_id):
                            print('PIZDEC')
                            self.drive.quit()
                            quit()
                time.sleep(1)
                html = self.drive.page_source
                soup = bs(html, 'lxml')
                try:
                    href = self.drive.current_url
                except:
                    href = None
                try:
                    fotos = soup.find('div', class_='e8w7').find_all('div', class_='e9q6')
                    fotos = len(fotos)
                except:
                    fotos = None
                try:
                    price = soup.find('span', class_='c2h5 c2h6').text
                    price = price.strip().replace(' ','').replace('₽','').replace('\u2009','')
                    # print(price)
                except:
                    # try:
                    #     price = str(soup.find('h2', class_='e7z1').text.replace('\n','').strip())
                    # except:
                    price = 0
                try:
                    name = soup.find('h1', class_='e8j2').text
                except:
                    name = None
                try:
                    main_stars = soup.find('div', class_='_3OTE k0ds _2Ji0 e7y9')
                    stars = main_stars.find('div', class_='_3xol').get('style')
                    stars = stars.replace('width:','').replace(';','').replace('%','')
                    stars = float(stars) / 20
                except:
                    stars = 0
                try:
                    reports = soup.find('a', class_='_1-6r _3UDF').get('title')
                    if 'ставить' in reports:
                        self.drive.refresh()
                        time.sleep(1.5)
                        html = self.drive.page_source
                        soup = bs(html, 'lxml')
                        reports = soup.find('a', class_='_1-6r _3UDF').get('title')

                    if 'отз' not in reports:
                        reports = 0
                    else:
                        reports = reports.split(' отз')[0]
                except:
                    reports = 0
                #print(f"{href=}, {fotos=}, {price=}, {name=}, {stars=}, {reports=}")
                self.DF.at[self.ROW,'SKU'] = int(IDS[i])
                self.DF.at[self.ROW,'URL'] = str(href)
                self.DF.at[self.ROW,'NAME'] = str(name)
                self.DF.at[self.ROW,'PRICE'] = int(price)
                self.DF.at[self.ROW,'STARS'] = str(stars)
                try:
                    self.DF.at[self.ROW,'REPORTS'] = int(reports)
                except:
                    self.DF.at[self.ROW,'REPORTS'] = str(reports)
                self.DF.at[self.ROW,'FOTOS'] = str(fotos)
                self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i,1])
                self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i,0])

                self.ROW += 1
            else:

                self.DF.at[self.ROW,'SKU'] = str(IDS[i])
                # self.DF.at[self.ROW,'URL'] = str(None)
                # self.DF.at[self.ROW,'NAME'] = str(None)
                # self.DF.at[self.ROW,'PRICE'] = str(None)
                # self.DF.at[self.ROW,'STARS'] = str(None)
                # self.DF.at[self.ROW,'REPORTS'] = str(None)
                # self.DF.at[self.ROW,'FOTOS'] = str(None)
                try:
                    self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i,1])
                except:
                    # self.DF.at[self.ROW,'BARCODE'] = None
                    pass
                try:
                    self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i,0])
                except:
                    pass

                self.ROW += 1

    def main(self):
        start_time = time.time()
        self.page = 1
        self.ROW = 1
        self.drive = webdriver.Firefox(executable_path=self.GECKO, options=self.options, firefox_profile=self.profile)
        self.drive.set_page_load_timeout(30)
        time.sleep(1)
        IDS = []
        for i in self.xlsx.OZ:
            IDS.append(int(i))
        self.get_info_from_page(IDS)

        self.drive.close()
        self.drive.quit()
        self.DF.to_excel(f'{self.SAVE_FOLDER}Ozon_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx')
        print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    oz = ozon()
    oz.main()

def start():
    oz = ozon()
    oz.main()
