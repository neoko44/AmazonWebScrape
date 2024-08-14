import json
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from entities import Product, DataResult

# Amazon product url to scrape
amazon_product_URL = 'https://www.amazon.com/Anker-5-Pack-Charger-MacBook-Samsung/dp/B0CFZDHRPP?ref=dlx_deals_dg_dcl_B0CFZDHRPP_dt_sl14_d5'

# region driver options
headers = {
    "User-Agent": "ADD YOUR USER AGENT HERE",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"}

options = webdriver.EdgeOptions()

for h in headers:
    options.add_argument(h)
options.add_argument('--headless')

driver = webdriver.Edge(options=options)


# endregion

# region Method for getting amazon product by URL
def amazon_get_product(url):
    # Trying to load webpage by URL.
    # If throws an exception,
    # returns false in DataResult
    try:
        driver.get(url)
    except Exception as e:
        return DataResult(status=False,
                          message=e,
                          data=None)

    # soup1 trying to get page source by parsing currently working driver
    soup1 = BeautifulSoup(driver.page_source, 'html.parser')

    # soup2 prettifying the page source we just get
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    # Even URL is not correct, BeautifulSoup gets a page source.
    # We must search for something exist on our Amazon product page,
    # so we are looking for [id = 'productTitle']
    # if not exist returns false in DataResult
    title = soup2.find(id='productTitle')

    if title is None:
        return DataResult(status=False,
                          message="Please enter valid URL",
                          data=None)

    # If productTitle exists:
    # get text of element,
    # remove spaces at the beginning and at the end
    title = title.get_text().strip()

    # Get category node
    category = soup2.find(class_="a-unordered-list a-horizontal a-size-small")

    # Some amazon products do not have category node.
    # If there is no category node we will return ""
    if category:
        category = re.sub(r"\s+ ", "", category.get_text(), flags=re.UNICODE).replace('›', ' -- ').strip()

    # Get Price element
    get_price = soup2.find('span', class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")

    # Price example in get_price : 1.015,64 TL

    # Get whole price : 1015
    whole_price = get_price.find('span', class_="a-price-whole").get_text().replace('.', '').replace(',', '').strip()

    # Get fraction price : 64
    fraction_price = get_price.find('span', class_="a-price-fraction").get_text().strip()

    # Get currency : TL
    currency = get_price.find(class_="a-price-symbol").get_text().strip()

    # Total price : 1015.64
    total_price = whole_price + '.' + fraction_price

    # Create Product
    data = Product(title=title,
                   price=total_price,
                   currency=currency,
                   category=category or "").to_dict()

    # Return Product and return in DataResult
    return DataResult(data=data,
                      message="success",
                      status=True)


# endregion


if __name__ == '__main__':
    # returns DataResult object
    prod = amazon_get_product(amazon_product_URL)

    # Convert DataResult object to JSON
    as_json = json.dumps(prod.to_dict(),
                         default=str,
                         ensure_ascii=False,
                         indent=4)

    print(as_json)
