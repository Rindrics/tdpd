class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []


    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        self.price_history.append(price)
