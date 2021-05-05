class Currency():
    def __init__(self, long_name, denominator, fiat=False):
        self.name = long_name
        self.den = denominator
        # To use when the value is small, e.g. mBTC for 1/1000 BTC
        self.milliden = "m"+denominator
        self.is_fiat = fiat

    def __repr__(self):
        return self.den

class Coin():
    ###
    # A general coin, it has a name and a value
    ###
    def __init__(self, den : Currency, amount : float):
        if type(amount) != float:
            raise Exception
        if not isinstance(den, Currency):
            print(type(den))
            raise Exception
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

    def __eq__(self, other):
        if self.den != other.den:
            print("Comparison between different currencies not supported!")
            exit(-1)

        return (self.amount == other.amount)

    def __ne__(self, other):
        if self.den != other.den:
            print("Comparison between different currencies not supported!")
            exit(-1)

        return not (self == other)

    def __lt__(self, other):
        if self.den != other.den:
            print("Comparison between different currencies not supported!")
            exit(-1)

        return (self.amount < other.amount)

    def __gt__(self, other):
        if self.den != other.den:
            print("Comparison between different currencies not supported!")
            exit(-1)

        return (self.amount > other.amount)

    def __repr__(self):
        return "{:.4f} {}".format(self.amount, self.den)



SEK = Currency("Swedish crowns", "SEK", fiat=True)
EUR = Currency("Euro", "EUR", fiat=True)
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