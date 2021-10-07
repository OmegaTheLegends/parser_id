import requests, pandas, time, datetime
from bs4 import BeautifulSoup as bs


class rama():
    def __init__(self, IDS):
        self.IDS = IDS
        self.url = "https://www.castorama.ru/catalogsearch/result"
        self.payload = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Referer": "https://www.castorama.ru/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }

    def get_info(self, id):
        querystring = {"q":id}
        response = requests.request("GET", self.url, data=self.payload, headers=self.headers, params=querystring)
        soup = bs(response.text, 'lxml')

        try:
            name = soup.find('h1', itemprop="name").text
        except:
            name = None
        try:
            price = soup.find('span', class_="price").text
        except:
            price = None
        try:
            stars = soup.find('div', itemprop="aggregateRating").find(itemprop="ratingValue").get('content')
        except:
            stars = None
        try:
            reports = soup.find('a', class_='scroll-to-reviews-link ga-scroll-to-reviews').text
            reports = reports.strip()
        except:
            reports = None

        return response.url, name, price, stars, reports

    def main(self, DF):
        ROW = 1
        for i in self.IDS:
            INFO = self.get_info(i)
            time.sleep(2)
            DF.at[ROW,'URL'] = str(INFO[0])
            DF.at[ROW,'NAME'] = str(INFO[1])
            DF.at[ROW,'PRICE'] = str(INFO[2])
            DF.at[ROW,'STARS'] = str(INFO[3])
            DF.at[ROW,'REPORTS'] = str(INFO[4])
            ROW += 1
        DF.to_excel(f'/opt/reports/castorama/castorama_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx')
        # DF.to_excel(f'castorama_{datetime.datetime.today().strftime("%d.%m.%Y")}.xlsx')

def start():
    DF = pandas.DataFrame()
    xlsx = pandas.read_excel('/opt/parser_id/castorama_sku.xlsx')
    # xlsx = pandas.read_excel('castorama_sku.xlsx')
    temp_list = []

    for i in xlsx.SKU:
        temp_list.append(str(i))
    casta = rama(temp_list)
    casta.main(DF)

if __name__ == '__main__':
    start()
