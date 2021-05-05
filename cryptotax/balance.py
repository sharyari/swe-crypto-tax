from cryptotax.taxevent import TaxEvent
from cryptotax.coin import Coin
class Balance():
    def __init__(self, coin, fiscal_year, rates, tax_den):
        self.tax_den = tax_den
        self.fiscal_year = fiscal_year
        self.coin = coin
        self.rates = rates
        self.average_cost = 0
        self.losses = []
        self.earnings = []
    
    def buy(self, bought, cost, dt):
        total_before = self.coin.amount*self.average_cost
        bought_cost = cost.amount
        total_after = total_before + self.rates.convert(dt, cost.amount)
        self.coin = self.coin + bought
        self.average_cost = total_after/self.coin.amount
        return self
        
    def sell(self, sold, cost, dt):
        self.coin = self.coin-sold
        if sold.den.is_fiat:
            # selling fiat => buying crypto which is not a tax event
            return self
        if dt.year != self.fiscal_year:
            return self
        sell_cost_in_tax_den = Coin(self.tax_den, self.rates.convert(dt, cost.amount))
        buy_cost_in_tax_den = Coin(self.tax_den, self.average_cost*sold.amount)
        tax_event = TaxEvent(sold, buy_cost_in_tax_den.amount, sell_cost_in_tax_den.amount)
        if sell_cost_in_tax_den > buy_cost_in_tax_den:
            self.earnings.append(tax_event)
        else:
            self.losses.append(tax_event)
        return self


    def _aggregate_taxes(self, taxes):
        if len(taxes) == 0:
            return TaxEvent(Coin(self.coin.den, 0.0), 0.0, 0.0)
        elif len(taxes) == 1:
            return taxes[0]
        else:
            total = taxes[0]
            for i in range (1, len(taxes)-1):
                total = total + taxes[i]
            return total

    def aggregate_taxes(self):
        earnings = self._aggregate_taxes(self.earnings)
        losses = self._aggregate_taxes(self.losses)
        return earnings, losses

    def __repr__(self):
        return "{} {}".format(self.coin, self.average_cost)