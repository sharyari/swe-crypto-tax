class Coin():
    ###
    # A general coin, it has a name and a value
    ###
    def __init__(self, den, amount):
        self.den = den
        self.amount = amount 

    def __sub__(self, o):
        # the average cost is not changed when we sell
        amount = self.amount-o.amount
        return Coin(self.den, amount)

    def __add__(self, o):
        amount = self.amount+o.amount
        return Coin(self.den, amount)

    def __radd__(self, other):
        if type(other) is not Coin:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return "{:.4f} {}".format(self.amount, self.den)


class Currency():
    def __init__(self, long_name, denominator):
        self.name = long_name
        self.den = denominator
        # To use when the value is small, e.g. mBTC for 1/1000 BTC
        self.milliden = "m"+denominator

    def __repr__(self):
        return self.den

SEK = Currency("Swedish crowns", "SEK")
EUR = Currency("Euro", "EUR")
USD = Currency("US dollars", "USD")
BTC = Currency("Bitcoin", "BTC")
ETH = Currency("Ethereum", "ETH")
ETC = Currency("Ethereum Classic", "ETC")
ZEC = Currency("ZCash", "ZEC")
MLN = Currency("Melon", "MLN")
KAVA = Currency("KAVA", "KAVA")
TZ = Currency("Tezos", "TZ")
XRP = Currency("Ripple", "XRP")
EOS = Currency("EOS", "EOS")
XDG = Currency("Dogecoin", "XDG")
NANO = Currency("NANO", "NANO")
LINK = Currency("Chainlink", "LINK")
XLM = Currency("Stellar Lumens", "XLM")
OXT = Currency("Orchid", "OXT")