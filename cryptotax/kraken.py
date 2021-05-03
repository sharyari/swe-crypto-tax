from cryptotax.transaction import Transaction
from datetime import datetime
from cryptotax.exchange_rate import ExchangeRate
from cryptotax.coin import Coin


class KrakenTransaction(Transaction):
    # mostly one to one, but at least euro appeared in two ways for me
    # and I can't find a definition for this.
    currencies = {
     'XXBT' : 'XBT',
     'XTZ': 'TZ',
     'XXRP': 'XRP',
     'XZEC': 'ZEC',
     'EOS': 'EOS',
     'XETC': 'ETC',
     'LINK': 'LINK',
     'XXLM': 'XLM',
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
                fr = self.currencies.get(pair[:i])
                to = self.currencies.get(pair[i:])
                return fr, to  # always EUR in my data
        print("UNKNOWN CURRENCY PAIR: %s" % pair)
        exit(-1)

    def __init__(self, info):
        txid = info[0]
        ordertxid = info[1]
        pair = info[2]
        time = datetime.strptime(info[3], '%Y-%m-%d %H:%M:%S.%f')
        t = info[4]
        ordert = info[5]
        price = info[6]
        cost = float(info[7])
        fee = float(info[8])
        vol = float(info[9])
        margin = info[10]
        misc = info[11]
        ledgers = info[12]

        c1_den, c2_den = self.get_trade_currencies(pair)  # name of the cryptos, c2 == eur
        fr = Coin(c1_den, vol) # total volume of crypto
        to = Coin(c2_den, cost)
        if t == 'buy':
            super().__init__(time, fr, to)
        else:
            super().__init__(time, to, fr)


def parse_kraken_line(line):
    # Remove \n, \r and unneeded quotes
    info = line.replace('"', '').strip().split(',')
    if len(info) > 12:
        return KrakenTransaction(info)

def parse_kraken_file(lines):
    for line in lines:
        # Skip the first line if it exists
        if line.startswith('"txid"'):
            continue
        tr = parse_kraken_line(line)
        if tr:
            yield tr

def parse_kraken_csv(path):
    with open(path, "r") as fp:
        lines = fp.readlines()
        return parse_kraken_file(lines)
