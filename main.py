import re
import csv_opt
from bs4 import BeautifulSoup
from selenium import webdriver
from entities import Product, Fields

binance_SITE = 'https://www.binance.com/tr/markets/overview'
amazon_SITE = 'https://www.amazon.com/Ice-Roller-Face-Massager-Puffiness/dp/B088WBLF5Z/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.tc2iVqhd9TxbTatkh28QSXkNiBl11hwlKrb09QXHK3fyCOGSbyoen5GaKsqXsQd7vrtl83ofENgDiyG3h7oaJThAYUsPIhFcvLunm_B9rI6cOCpThbTwjN2gzpTPKnKzXJhThdOYAzk8MbuP1OGIGY5SiFMKTWh37_m4ZeRAOSh2uugL6LAnjGpSJwDfU-RVV8b1UQBF4Biei5AMk8VhPRV6omhGWTL3qCev58w2oO9F_R8Rca2sfDq1CLeqETzMhtd3SonIrXx6Rfk8gDpGH4f4E_qOxcvJ2534GbmP1MY.75RxQzXtKH8v80QZCoDwEV90rZTgp-GPOIn25ClU4Nk&dib_tag=se&keywords=products&qid=1722820201&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"}

prod_list = []

def create_table(file_name):
    fields = Fields().as_list()
    is_table = csv_opt.create_csv(file_name, fields)

    return is_table

def amazon_get_product(link):
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')

    driver = webdriver.Edge(options=options)
    driver.get(link)

    soup1 = BeautifulSoup(driver.page_source, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id='productTitle').get_text().strip()
    category = soup2.find(class_='a-unordered-list a-horizontal a-size-small')
    category = re.sub(r"\s+ ", "", category.get_text(), flags=re.UNICODE).replace('›', ' -- ').strip()

    get_price = soup2.find('span', class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")

    whole_price = get_price.find('span', class_="a-price-whole").get_text().replace('.', '').replace(',', '').strip()
    fraction_price = get_price.find('span', class_="a-price-fraction").get_text().strip()
    currency = get_price.find(class_="a-price-symbol").get_text().strip()

    total_price = whole_price + '.' + fraction_price

    return Product(title=title, price=total_price, currency=currency, category=category)


if __name__ == '__main__':
    table = create_table('Test')

    data = amazon_get_product(amazon_SITE)

    obj = Product(title=data.title, price=data.price, currency=data.currency, category=data.category)
    prod_list.append(obj.as_data())

    csv_opt.append_to_csv('Test', prod_list)
