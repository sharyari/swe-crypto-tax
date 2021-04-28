from coin import Coin, EUR

class Transaction():
    def __init__(self, time, fee, buy, sell):
        self.time = time
        self.buy = buy
        self.sell = sell
        self.fee = fee

    def __repr__(self):
        time = self.time.strftime("%y-%m-%d")
        return "{} -> {} ({} fee)".format(repr(self.sell), repr(self.buy), repr(self.fee))