from transaction import Transaction
from datetime import datetime
from coin import Coin, EUR

class KrakenTransaction(Transaction):
    # mostly one to one, but at least euro appeared in two ways for me
    # and I can't find a definition for this.
    currencies = {
     'XXBT' : 'XBT',
     'XTZ': 'TZ',
     'XXRP': 'XRP',
     'XZEC': 'ZEC',
     'XETC': 'ETC',
     'LINK': 'LINK',
     'OXT': 'OXT',
     'KAVA': 'KAVA',
     'XMLN': 'MLN',
     'NANO': 'NANO',
     'XDG': 'DOGE',
     'XETH': 'ETH',
     'EUR': 'EUR',
     'ZEUR': 'EUR'}

    def get_trade_currencies(self, pair):
        # the second currency is assumed to be EURO
        for i in range(3, len(pair)-2):
            if pair[:i] in self.currencies and pair[i:] in self.currencies:
                crypto = self.currencies.get(pair[:i])
                return crypto, EUR  # always EUR in my data
        print("UNKNOWN CURRENCY PAIR: %s" % pair)
        exit(-1)

    def __init__(self, info):
        txid = info[0]
        ordertxid = info[1]
        pair = info[2]
        time = info[3]
        t = info[4]
        ordert = info[5]
        price = info[6]
        cost = info[7]
        fee = info[8]
        vol = info[9]
        margin = info[10]
        misc = info[11]
        ledgers = info[12]

        time =  datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        c1_name, c2_name = self.get_trade_currencies(pair)  # name of the cryptos, c2 == eur
        coin = Coin(float(vol), c1_name, euro=float(cost)) # total volume of crypto
#        price = Coin(float(price), EUR) # price of 1 crypto in euro 
        cost = Coin(float(cost), EUR) # total cost of vol crypto in euor
        fee = Coin(float(fee), EUR) # total transaction fee in euro
        if t == 'buy':
            super().__init__(time, fee, coin, cost)
        else:
            super().__init__(time, fee, cost, coin)


def parse_kraken_line(line):
    # Remove \n, \r and unneeded quotes
    info = line.replace('"', '').strip().split(',')

    return KrakenTransaction(info)

def parse_kraken_csv(path):
    with open(path, "r") as fp:
        for line in fp.readlines():
            # Skip the first line if it exists
            if line.startswith('"txid"'):
                continue
            yield parse_kraken_line(line)
