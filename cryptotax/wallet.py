import tabulate
from cryptotax.coin import Coin, EUR

def is_small(v):
    return (v > -0.0001 and v <0.0001)

class Wallet():
    def __init__(self):
        self.balances = {}
        self.transactions = []
        self.taxes = []
        self.fees = Coin(0, EUR)
        pass

    def add(self, c):
        in_balance = self.balances.get(c.name, Coin(0, c.name))
        self.balances[c.name] = c + in_balance

    def sub(self, c):
        in_balance = self.balances.get(c.name, Coin(0, c.name))
        self.balances[c.name] = in_balance - c

    def get_fees(time_from=None, time_to=None):
        # todo: add filtering on time
        total_fees = sum([tr.fee for tr in transactions])
        return total_fees

    def tax(self, sold):
        if sold.name == EUR:
            #not a taxable event
            return
        bought = self.balances.get(sold.name)
        bought_for = sold.to_euro_at_price(bought.average_cost)
        sold_for = sold.cost()
        earnings = sold_for-bought_for
        if earnings > 0:
            # if it's a win, pay 30% in taxes
            self.taxes.append(Coin(earnings*0.3, EUR))
        else:
            # if it's a loss, we redact 70% of it from our taxes
            self.taxes.append(Coin(earnings*0.7, EUR))
        return
        

    def transact(self, tr):
        self.transactions.append(tr)
        self.tax(tr.sell)
        self.add(tr.buy)
        self.sub(tr.sell)
        

    def __repr__(self):
        # don't show miniscule balances
        r_balances = dict([(k,v) for (k,v) in self.balances.items() if not is_small(v)])
        names = r_balances.keys()
        coins = r_balances.values()
        averages = [c.average_cost for c in coins]
        return str(tabulate.tabulate([names, coins, averages]))