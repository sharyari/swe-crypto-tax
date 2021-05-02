from cryptotax.transaction import Transaction
from datetime import datetime
from cryptotax.exchange_rate import ExchangeRate
from cryptotax.coin import Coin, EUR, SEK
from flask import Blueprint, request
from cryptotax.cfg import wallet
from json import dumps

kraken_csv = Blueprint('kraken_csv', __name__, template_folder='templates')

@kraken_csv.route('/input/kraken', methods = ['POST'])
def kraken_r():
    in_file = request.files['data']
    data = in_file.read().decode().split("\n")
    trs = parse_kraken_file(data)
    return dumps([tr.to_json() for tr in trs])
    

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

    def __init__(self, info, rates):
        txid = info[0]
        ordertxid = info[1]
        pair = info[2]
        time = info[3]
        t = info[4]
        ordert = info[5]
        price = info[6]
        cost = float(info[7])
        fee = float(info[8])
        vol = float(info[9])
        margin = info[10]
        misc = info[11]
        ledgers = info[12]

        time =  datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        c1_name, c2_name = self.get_trade_currencies(pair)  # name of the cryptos, c2 == eur
        fiat_cost = rates.to_sek(time, cost)
        coin = Coin(vol, c1_name, fiat_cost=fiat_cost) # total volume of crypto
#        price = Coin(float(price), EUR) # price of 1 crypto in euro 
        cost = Coin(fiat_cost, SEK) # total cost of vol crypto in euor
        fee = Coin(rates.to_sek(time, fee), SEK) # total transaction fee in euro
        if t == 'buy':
            super().__init__(time, fee, coin, cost)
        else:
            super().__init__(time, fee, cost, coin)


def parse_kraken_line(line, rates):
    # Remove \n, \r and unneeded quotes
    info = line.replace('"', '').strip().split(',')
    if len(info) > 12:
        return KrakenTransaction(info, rates)

def parse_kraken_file(lines):
    rates = ExchangeRate(EUR, SEK)

    for line in lines:
        # Skip the first line if it exists
        if line.startswith('"txid"'):
            continue
        tr = parse_kraken_line(line, rates)
        if tr:
            yield tr

def parse_kraken_csv(path):
    with open(path, "r") as fp:
        lines = fp.readlines()
        return parse_kraken_file(lines)
