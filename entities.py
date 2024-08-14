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

    def to_dict(self):
        return dict(title=self.title, price=self.price, currency=self.currency, category=self.category, date=self.date)


class Result:
    def __init__(self, status, message):
        self.status = bool(status)
        self.message = message


class DataResult:
    def __init__(self, status, message, data):
        self.status = bool(status)
        self.message = message
        self.data = data

    def to_dict(self):
        return dict(status=self.status, message=self.message, data=self.data)



