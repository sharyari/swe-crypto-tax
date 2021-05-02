import tabulate
from cryptotax.coin import Coin, EUR, SEK
from cryptotax.exchange_rate import ExchangeRate

def is_small(v):
    return (v > -0.0001 and v <0.0001)

class Wallet():
    def __init__(self):
        self.balances = {}
        self.transactions = []
        self.earnings = {}
        self.losses = {}
        self.rates = ExchangeRate(EUR, SEK)
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

    def calculate_tax(self, dt, sold):
        if sold.name == SEK:
            #not a taxable event
            return
        bought = self.balances.get(sold.name)
        bought_for = sold.to_euro_at_price(bought.average_cost)
        sold_for = sold.cost()
        earnings = sold_for-bought_for
        cost_in_sek = bought_for

        if earnings > 0:
            # if it's a win, pay 30% in taxes
            prev_earnings = self.earnings.get(sold.name, [])
            prev_earnings.append((sold, cost_in_sek))
            self.earnings[sold.name] = prev_earnings
        else:
            # if it's a loss, we redact 70% of it from our taxes
            prev_losses = self.losses.get(sold.name, [])
            prev_losses.append((sold,cost_in_sek))
            self.losses[sold.name] = prev_losses

        return

    def aggregate_taxes(self, convert='SEK'):
        all_coins = set.union(set(self.earnings.keys()), set(self.losses.keys()))
        for c in all_coins:
            earnings = self.earnings.get(c, [])
            losses = self.losses.get(c, [])
            total_c = Coin(0, c)
            total_sek = 0

            for coin, sek in earnings:
                total_c = total_c + coin
                total_sek = total_sek + sek
            if total_c > 0:
                sold_for = (total_c.average_cost)*total_c
                yield float(total_c), c, sold_for, total_sek, 0, sold_for - total_sek
            total_sek = 0
            total_c = Coin(0, c)
            for coin, sek in losses:
                total_c = total_c + coin
                total_sek = total_sek + sek
            if total_c > 0:
                sold_for = (total_c.average_cost)*total_c
                yield float(total_c), c, sold_for, total_sek, total_sek - sold_for, 0


    def transact(self, tr):
        self.transactions.append(tr)
        self.calculate_tax(tr.time, tr.sell)
        self.add(tr.buy)
        self.sub(tr.sell)
        

    def __repr__(self):
        # don't show miniscule balances
        r_balances = dict([(k,v) for (k,v) in self.balances.items() if not is_small(v)])
        names = r_balances.keys()
        coins = r_balances.values()
        averages = [c.average_cost for c in coins]
        return str(tabulate.tabulate([names, coins, averages]))