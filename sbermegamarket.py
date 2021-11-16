# -*- coding: utf-8 -*-
import requests, datetime, time, json
import pandas as pd
from bs4 import BeautifulSoup as bs

class sber:
    def __init__(self):
        self.xlsx = pd.read_excel('all_sku.xlsx')
        self.xlsx['SBER'] = self.xlsx['SBER'].fillna(0)
        # self.SAVE_FOLDER = '/opt/reports/sber/' #linux 
        self.SAVE_FOLDER = 'C:\\TEMP\\' # windows
        self.headers = {
        'authority': "sbermegamarket.ru",
        'accept': "application/json",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487",
        'content-type': "application/json;charset=UTF-8",
        'origin': "https://sbermegamarket.ru",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://sbermegamarket.ru/",
        'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        'cookie': "analytics_session_id=f3199f76-33b4-421d-b059-e1560b005c15; ssaid=b86ac400-a103-11ea-82fc-cd5f8e00d4b8; adspire_uid=AS.1749102013.1590684794; KFP_DID=a8b441de-efa1-2197-ab3e-3cef5241a690; uxs_uid=cabd0c50-c2f3-11ea-9d70-859690881c67; rrpvid=562532023533268; _gcl_au=1.1.1964033425.1604059557; rcuid=5f9c01a634acc0000199a933; __exponea_etc__=5c68abca-3e9f-40aa-abfd-ba2b514e9c9e; flocktory-uuid=27770b0f-7c89-42a8-bc5a-ff6af2b8ac11-9; tmr_lvid=7efbfed0495fba0413c2ec8ddc2c9a03; tmr_lvidTS=1604059559320; _ym_uid=1604059559469428858; _ym_d=1604059559; top100_id=t1.6795753.2019358990.1604059559396; _fbp=fb.1.1604059559901.1647425193; scarab.visitor=%226D188F2093D39D35%22; goodsLoyaltyCardNumber=gd008623871; hasAccount=1; _gac_UA-89387429-1=1.1610553314.Cj0KCQiA0fr_BRDaARIsAABw4Eup0fL-306qIBJwaZo93Y-Rc_iHk-kk94x8fwc_NRqKFQ4r-1WfNcQaAkmQEALw_wcB; uxs_mig=1; _gcl_aw=GCL.1610553314.Cj0KCQiA0fr_BRDaARIsAABw4Eup0fL-306qIBJwaZo93Y-Rc_iHk-kk94x8fwc_NRqKFQ4r-1WfNcQaAkmQEALw_wcB; rr-VisitorSegment=6%3A4; rrlevt=1610553327493; scarab.mayAdd=%5B%7B%22i%22%3A%22100000100773%22%7D%2C%7B%22i%22%3A%22600001063903%22%7D%5D; scarab.profile=%22600001063903%7C1610553328%22; last_visit=1610542528535::1610553328535; _ga_W49D2LL5S1=GS1.1.1610562312.3.0.1610562312.60; tmr_reqNum=44; PHPSESSID=h2ddsc3da1a7dqv86mdlh600k2; goods_user_token=cbb78a02-720e-4dde-9a86-8c3db91b3afa; region_id=50; ft=%255B%2522payment_card%2522%252C%2522switch_to_new_goods_phones%2522%255D; _ga=GA1.2.119193884.1604059557; _gid=GA1.2.1486816634.1612974842; goodsUserProfile=false; region_info=%7B%22displayName%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%20%D0%B8%20%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%22%2C%22kladrId%22%3A%227700000000000%22%2C%22isDeliveryEnabled%22%3Atrue%2C%22geo%22%3A%7B%22lat%22%3A55.755814%2C%22lon%22%3A37.617635%7D%2C%22id%22%3A%2250%22%7D; BpgPopoverShown=true; _ym_isad=2; _ym_visorc=w; cacc77b0a92b3772c67284f0a5dd0eaf_vc=1; cacc77b0a92b3772c67284f0a5dd0eaf_ac=1; __tld__=null"
        }
        # self.s = requests.Session()
        self.DF = pd.DataFrame()

    def get_url(self, t_id, i_row):
        payload = "{\"requestVersion\":5,\"limit\":42,\"offset\":0,\"collectionId\":\"\",\"sorting\":0,\"ageMore18\":0,\"showNotAvailable\":true,\"searchText\":\"%s\",\"auth\":{\"token\":\"cbb78a02-720e-4dde-9a86-8c3db91b3afa\",\"locationId\":\"50\",\"appPlatform\":\"WEB\",\"customerId\":null,\"operatorId\":\"\",\"deviceId\":\"\",\"analyticsDeviceId\":\"5c68abca-3e9f-40aa-abfd-ba2b514e9c9e\",\"experiments\":{\"4943\":\"1\",\"5568\":\"1\",\"39650\":\"1\",\"41512\":\"2\",\"41703\":\"2\",\"42962\":\"1\",\"43053\":\"2\",\"44768\":\"2\",\"46761\":\"1\",\"46938\":\"2\",\"47170\":\"2\",\"47584\":\"2\",\"49574\":\"2\",\"50265\":\"1\",\"50755\":\"2\",\"51950\":\"2\",\"53202\":\"1\",\"test0001\":\"2\"}}}" % (t_id)
        response = requests.post('https://sbermegamarket.ru/api/mobile/v1/catalogService/catalog/search', data=payload, headers=self.headers)
        response.encoding = response.apparent_encoding
        data = json.loads(response.text)
        if data['processor']:
            url = data['processor']['url']
            url = str(url)
            url = url.split('#related')
            url = url[0]
            with open('sber_id_url.txt', 'a+', encoding='utf-8') as file:
                file.write(str(t_id) + ' : ' + str(url) + '\n')
            self.get_info(url, t_id, i_row)
        else:
            self.DF.at[self.ROW,'SKU'] = int(t_id)
            self.DF.at[self.ROW,'URL'] = str('no url')
            self.ROW += 1


    def get_info(self, url, t_id, i_row):
        self.URLS.update({t_id : url})
        html = requests.get('https://sbermegamarket.ru' + url, headers=self.headers)
        html.encoding = html.apparent_encoding
        soup = bs(html.text, 'lxml')
        try:
            h1 = soup.find('header', class_='title-page').text
            h1 = h1.replace('\n','')
        except:
            try:
                h1 = soup.find('h1', class_='pdp-header__title page-title').text
                h1 = h1.replace('\n','')
            except:
                h1 = None
        try:
            foto = soup.find('div', class_='lory-slider__frame slide-list').findAll('img')
            foto = len(foto)
        except:
            try:
                foto = soup.find('div', class_='scroller__content-wrapper').findAll('img')
                foto = len(foto)
            except:
                foto = None
        try:
            price = soup.find('div', class_='price__final').text
            price = price.replace(' ₽','').replace(' ','').replace('â‚½','').strip()
        except:
            price = 0
        try:
            stars = soup.find('span', class_='reviews-average__number-view').text
        except:
            try:
                stars = 0
                star = soup.find('div', class_='card-prod--reviews-stars').find_all('div', class_='star')
                for i in star:
                    if 'star-on' in i.get('class'):
                        stars += 1
                    else:
                        pass
            except:
                stars = None
        try:
            otzivi = soup.find(title='Количество отзывов').text
            otzivi = otzivi.replace('(','').replace(')','')
            if 'отз' in otzivi:
                otzivi = otzivi.split('отз')
                otzivi = otzivi[0]
            if ' Ğ¾Ñ' in otzivi:
                otzivi = otzivi.split(' Ğ¾Ñ')
                otzivi = otzivi[0]
        except:
            try:
                otzivi = soup.find('span', class_='reviews-rating__reviews-count').text
                otzivi = otzivi.replace('(','').replace(')','')
                if 'отз' in otzivi:
                    otzivi = otzivi.split('отз')
                    otzivi = otzivi[0]
                if ' Ğ¾Ñ' in otzivi:
                    otzivi = otzivi.split(' Ğ¾Ñ')
                    otzivi = otzivi[0]
            except:
                otzivi = 0
        
        self.DF.at[self.ROW,'SKU'] = int(t_id)
        self.DF.at[self.ROW,'URL'] = str(html.url)
        self.DF.at[self.ROW,'NAME'] = str(h1)
        try:
            self.DF.at[self.ROW,'PRICE'] = int(price)
        except:
            self.DF.at[self.ROW,'PRICE'] = str(price)
        self.DF.at[self.ROW,'STARS'] = str(stars)
        try:
            self.DF.at[self.ROW,'REPORTS'] = int(otzivi)
        except:
            self.DF.at[self.ROW,'REPORTS'] = str(otzivi)
        self.DF.at[self.ROW,'FOTOS'] = str(foto)
        self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i_row,1])
        self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i_row,0])

        self.ROW += 1



    def start(self):
        start_time = time.time()
        self.URLS = {}
        with open('sber_id_url.txt', 'r+', encoding='utf-8') as file:
            f = file.readlines()
        for i in f:
            a = i.replace('\n','')
            a = a.split(' : ')
            self.URLS.update({a[0] : a[1]})
        self.ROW = 1
        IDS = []
        for i in self.xlsx.SBER:
            IDS.append(int(i))
        for i_row in range(len(IDS)):  # len(IDS)
            time.sleep(0.25)
            if self.xlsx.iat[i_row,4] != 0 and self.xlsx.iat[i_row,4] != '0':
                t_id = int(self.xlsx.iat[i_row,4])
                t_url = self.URLS.get(str(t_id))
                if t_url == None:
                    self.get_url(t_id, i_row)
                else:
                    self.get_info(t_url, t_id, i_row)
            else:
                self.DF.at[self.ROW,'SKU'] = int(self.xlsx.iat[i_row,4])
                try:
                    self.DF.at[self.ROW,'BARCODE'] = int(self.xlsx.iat[i_row,1])
                except:
                    pass
                try:
                    self.DF.at[self.ROW,'1C NAME'] = str(self.xlsx.iat[i_row,0])
                except:
                    pass

                self.ROW += 1

        self.DF.to_excel(f'{self.SAVE_FOLDER}Sber_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx')
        print("--- %s seconds ---" % (time.time() - start_time))



def main():
    SB = sber()
    SB.start()

if __name__ == "__main__":
    main()