# This is a sample Python script.
import csv
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# from tkinter import *
# from urllib.request import urlopen
# import webview
import re
import csv_opt

from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium import webdriver
from entities import Product, Fields
import time
import threading

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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


def binance_get(name):
    r = requests.get(binance_SITE)

    soup = BeautifulSoup(r.text, 'html.parser')
    s = soup.find_all("a", attrs={'data-bn-type': 'link'}, href=True)

    for a in s:
        is_price = bool(re.search(r'/price/', a['href']))

        if is_price:
            print(a.findParent().prettify())
            # print(a['href'])


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

    # price = re.sub(r"\s+", "", get_price.get_text(), flags=re.UNICODE).strip()

    return Product(title=title, price=total_price, currency=currency, category=category)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    table = create_table('Test')
    # threads = [threading.Thread(target=amazon_get_product,args=(link,))for url in amazon_SITE]

    data = amazon_get_product(amazon_SITE)

    obj = Product(title=data.title, price=data.price, currency=data.currency, category=data.category)
    prod_list.append(obj.as_data())

    csv_opt.append_to_csv('Test', prod_list)
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/

# tk = Tk()
#   screen_width = tk.winfo_screenwidth()
#   screen_height = tk.winfo_screenheight()
#
#   optimal_width = (screen_width / 4) * 3
#   optimal_height = (screen_height / 4) * 3

# tk.size = tk.geometry
# tk.geometry("600x480")

# webview.create_window('Scrape', site, width=optimal_width.__int__(), height=optimal_height.__int__())

# a = urlopen(site)
#
# data = a.read().decode('utf-8')
#
# print(data)


# webview.start()


# ----

# Use a breakpoint in the code line below to debug your script.
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "DNT": "1",
#     "Connection": "close",
#     "Upgrade-Insecure-Requests": "1"}

# r = requests.get(site, headers=headers)
# print(r)
#
# soup = BeautifulSoup(r.content, 'html.parser')
#
# s = soup.find_all('div', {'data-testid': 'B08BCSLJBC'},recursive=True)
#
# print(s)


# Try to find element using catch
#     try:
#         # Wait for the element with the ID of wrapper
#         wrapper = WebDriverWait(driver, 7).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, '//*[@id="DealsGridScrollAnchor"]/div[3]/div/div/div[2]/div[1]/div/div/div[1]'))
#         )
#         print("Element is present in the DOM now")
#     except TimeoutException:
#         print("Element did not show up")


# ---

# prod = []
#
# prod.append({price, title})

# WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[21]/div/div/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div")))

# print(driver.page_source.encode('utf-8'))
