import requests, pandas, datetime, json, numpy as np

class WB_REQ:
    def __init__(self):
        self.url = "https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog"
        self.payload = ""
        self.headers = {
            "cookie": "__store=119261_122252_122256_117673_122258_122259_121631_122466_122467_122495_122496_122498_122590_122591_122592_123816_123817_123818_123820_123821_123822_124093_124094_124095_124096_124097_124098_124099_124100_124101_124583_124584_125238_125239_125240_132318_132320_132321_125611_135243_135238_133917_132871_132870_132869_132829_133084_133618_132994_133348_133347_132709_132597_132807_132291_132012_126674_126676_127466_126679_126680_127014_126675_126670_126667_125186_116433_119400_507_3158_117501_120602_6158_121709_120762_124731_1699_130744_2737_117986_1733_686_132043; __region=64_75_4_38_30_33_70_68_71_22_31_66_40_1_80_69_48; __pricemargin=1.0--; __cpns=12_3_18_15_21; ncache=119261_122252_122256_117673_122258_122259_121631_122466_122467_122495_122496_122498_122590_122591_122592_123816_123817_123818_123820_123821_123822_124093_124094_124095_124096_124097_124098_124099_124100_124101_124583_124584_125238_125239_125240_132318_132320_132321_125611_135243_135238_133917_132871_132870_132869_132829_133084_133618_132994_133348_133347_132709_132597_132807_132291_132012_126674_126676_127466_126679_126680_127014_126675_126670_126667_125186_116433_119400_507_3158_117501_120602_6158_121709_120762_124731_1699_130744_2737_117986_1733_686_132043%253B64_75_4_38_30_33_70_68_71_22_31_66_40_1_80_69_48%253B1.0--%253B12_3_18_15_21%253B%253B-1257786_-2162196_-102269_-1029256; __dst=-1257786_-2162196_-102269_-1029256",
            "Connection": "keep-alive",
            "sec-ch-ua": "^\^"
        }
        self.xlsx = pandas.read_excel('all_sku.xlsx')
        self.xlsx['WB'] = self.xlsx['WB'].fillna(0)
        self.DF = pandas.DataFrame()
        self.ROW = 1
        self.ses = requests.Session()

    def get_info(self,id):
        querystring = {
            "spp":"12",
            "regions":"64,75,4,38,30,33,70,68,71,22,31,66,40,1,80,69,48",
            "stores":"119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,124583,124584,125238,125239,125240,132320,132321,132871,132870,127466,132807,126675,116433,120762,119400,507,3158,117501,120602,6158,121709,130744,1699,2737,124731,117986,1733,686,132043,117413,119070,118106,119781",
            "pricemarginCoeff":"1.0",
            "reg":"1",
            "appType":"1",
            "offlineBonus":"0",
            "onlineBonus":"0",
            "emp":"0",
            "locale":"ru",
            "lang":"ru",
            "curr":"rub",
            "couponsGeo":"2,12,3,18,15,21",
            "dest":"-1255577,-1278703,-102269,-1029256",
            "nm": str(id)
            }
        response = self.ses.request("GET", self.url, data=self.payload, headers=self.headers, params=querystring)
        if len(json.loads(response.text)['data']['products']) < 1:
            return 400
        else:
            return json.loads(response.text)['data']['products'][0]

    def write_data(self,info,barcode,one_s):
        try:
            stock = ''
            stocks = info['sizes'][0]['stocks']
            for i in stocks:
                stock = stock+f"store id={i['wh']} : {i['qty']} | "
        except:
            stock = 'not in sale'
        self.DF.at[self.ROW,'SKU'] = info.get('id')
        self.DF.at[self.ROW,'URL'] = str(f"https://www.wildberries.ru/catalog/{str(info.get('id'))}/detail.aspx")
        self.DF.at[self.ROW,'BRAND'] = str(info.get('brand'))
        self.DF.at[self.ROW,'NAME'] = str(info.get('name'))
        self.DF.at[self.ROW,'STOCK'] = str(stock)
        if 'extended' in info:
            try:
                self.DF.at[self.ROW,'PRICE'] = info['extended'].get('basicPriceU') // 100
                self.DF.at[self.ROW,'SALE'] = info['extended'].get('basicSale')
            except:
                self.DF.at[self.ROW,'PRICE'] = info['extended'].get('clientPriceU') // 100
                self.DF.at[self.ROW,'SALE'] = info['extended'].get('clientSale')
        else:
            self.DF.at[self.ROW,'PRICE'] = info.get('priceU') // 100
            self.DF.at[self.ROW,'SALE'] = info.get('salePriceU')
        self.DF.at[self.ROW,'STARS'] = info.get('rating')
        self.DF.at[self.ROW,'REPORTS'] = info.get('feedbacks')
        self.DF.at[self.ROW,'FOTOS'] = info.get('pics')
        try:
            self.DF.at[self.ROW,'PROMO'] = str(info.get('promoTextCat'))
        except:
            pass
        try:
            self.DF.at[self.ROW,'BARCODE'] = int(barcode)
        except:
            pass
        try:
            self.DF.at[self.ROW,'1C NAME'] = str(one_s)
        except:
            pass
        self.ROW += 1

    def main(self):
        for i in range(len(self.xlsx.WB)):
            id, one_s, barcode = self.xlsx.iat[i,2], self.xlsx.iat[i,0], self.xlsx.iat[i,1]
            if str(id) not in [None,np.NaN,np.nan,np.NAN,'nan','',' '] and id != 0:
                data = self.get_info(int(id))
                if data == 400:
                    self.DF.at[self.ROW,'SKU'] = id
                    try:
                        self.DF.at[self.ROW,'BARCODE'] = int(barcode)
                    except:
                        pass
                    try:
                        self.DF.at[self.ROW,'1C NAME'] = str(one_s)
                    except:
                        pass
                    self.ROW += 1
                    continue
                self.write_data(data,barcode,one_s)
                # time.sleep(0.1 if i % 5 != 0 else 0.25)
            else:
                self.DF.at[self.ROW,'SKU'] = id
                try:
                    self.DF.at[self.ROW,'BARCODE'] = int(barcode)
                except:
                    pass
                try:
                    self.DF.at[self.ROW,'1C NAME'] = str(one_s)
                except:
                    pass
                self.ROW += 1
        self.DF.to_excel(f'/opt/reports/wb/WB_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx', index=False)

def start():
    wb = WB_REQ()
    wb.main()

if __name__ == '__main__':
    wb = WB_REQ()
    wb.main()
