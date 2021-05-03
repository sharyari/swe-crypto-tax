import tabulate
from cryptotax.coin import Coin
from cryptotax.balance import Balance
from cryptotax.exchange_rate import ExchangeRate

def is_small(v):
    return (v > -0.0001 and v <0.0001)

class Wallet():
    def __init__(self, fiscal_year, rates, tax_den):
        self.tax_den = tax_den
        self.balances = {}
        self.fiscal_year = fiscal_year
        self.rates = rates
        self.losses = {}

    def transact(self, tr):
#        self.transactions.append(tr)
        buy_den = tr.buy.den
        sell_den = tr.sell.den
        b1 = self.balances.get(buy_den, Balance(Coin(buy_den, 0), self.fiscal_year, self.rates, self.tax_den))
        b2 = self.balances.get(sell_den, Balance(Coin(sell_den, 0), self.fiscal_year, self.rates, self.tax_den))
        self.balances[buy_den] = b1.buy(tr.buy, tr.sell, tr.time)
        self.balances[sell_den] = b2.sell(tr.sell, tr.buy, tr.time)

    def __repr__(self):
        dens = [b.coin.den for b in self.balances.values() if not is_small(b.coin.amount)]
        amounts = ["{:.4f}".format(b.coin.amount) for b in self.balances.values() if not is_small(b.coin.amount)]
        return tabulate.tabulate([dens, amounts])

    def get_taxes(self):
        total_earn = 0
        total_loss = 0
        for b in self.balances.values():
            earnings, losses = b.aggregate_taxes()
            total_earn = total_earn + earnings.diff()
            total_loss = total_loss + losses.diff()
            if not is_small(earnings.diff()):
                yield earnings.k4_line()
            if not is_small(losses.diff()):
                yield losses.k4_line()
        print("Total earnings: {}".format(total_earn))
        print("Total losses: {}".format(total_loss))