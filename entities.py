import datetime


class Product:
    def __init__(self, title, price, currency, category):
        self.title = title
        self.price = price
        self.currency = currency
        self.category = category
        self.date = datetime.datetime.now()

    def as_data(self):
        return [self.title, self.price, self.currency, self.category, self.date]


class Result:
    def __init__(self, status, message):
        self.status = bool(status)
        self.message = message


class Fields:
    def __init__(self):
        self.mainTitle = 'Title'
        self.mainPrice = 'Price'
        self.mainCurrency = 'Currency'
        self.mainCategory = 'Category'
        self.date = 'Date'

    def as_list(self):
        return_list = [self.mainTitle, self.mainPrice, self.mainCurrency, self.mainCategory, self.date]
        return return_list
