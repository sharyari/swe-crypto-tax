from cryptotax.coin import Coin, EUR
from datetime import datetime
from flask import Blueprint
from flask import request
from json import loads, dumps
from cryptotax.cfg import wallet

transaction_single = Blueprint('transaction_single', __name__, template_folder='templates')
transaction_collection = Blueprint('transaction_collection', __name__, template_folder='templates')


@transaction_collection.route('/transactions', methods = ['GET', 'POST'])
def transaction_r():
    if request.method == 'GET':
        return dumps(["123" or tr.id for tr in wallet.transactions])
    if not request.method == 'POST':
        return "nyvää"
    
    tr = Transaction.from_json(request.json())
    return wallet.transact(tr)

@transaction_single.route('/transaction/<tr_id>', methods = ['GET', 'DELETE'])
def transaction_r(tr_id):
    if request.methods == 'GET':
        return wallet.get(transaction=tr_id)
    elif request.method == 'DELETE':
        wallet.delete(transaction=tr_id)
        return "hyvää"

timeformat = "%Y-%m-%d %H:%M:%S.%f"


class Transaction():
    def __init__(self, time, fee, buy, sell):
        self.time = time
        self.buy = buy
        self.sell = sell
        self.fee = fee

    def __repr__(self):
        time = self.time.strftime("%y-%m-%d")
        return "{} -> {} ({} fee)".format(repr(self.sell), repr(self.buy), repr(self.fee))

    def to_json(self):
        data = {
            'time': datetime.strftime(self.time, timeformat),
            'buy': self.buy.to_json(),
            'sell': self.sell.to_json(),
            'fee': self.fee.to_json()
        }
        return data

    def from_json(self, data):
        time =  datetime.strptime(time, timeformat)

        data = {
            'time': self.time,
            'buy': self.buy.to_json(),
            'sell': self.sell.to_json(),
            'fee': self.fee.to_json()
        }
        
