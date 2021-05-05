from cryptotax.coin import Coin
from datetime import datetime

timeformat = "%Y-%m-%d %H:%M:%S.%f"


class Transaction():
    def __init__(self, time, buy : Coin, sell : Coin):
        self.time = time
        self.buy = buy
        self.sell = sell

    def __repr__(self):
        time = self.time.strftime("%y-%m-%d")
        return "{} -> {}".format(repr(self.sell), repr(self.buy))
