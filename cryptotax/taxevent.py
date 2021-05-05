from cryptotax.coin import Coin
class TaxEvent():
    def __init__(self, coin : Coin, total_bought : float, total_sold : float):
        if type(total_bought) != float or type(total_sold) != float:
            print(type(total_bought))
            print(type(total_sold))
            raise Exception

        self.den = coin.den
        self.coin = coin
        self.total_bought = total_bought
        self.total_sold = total_sold

    def __repr__(self):
        return "{:.2f} {} {:.4f} {:.4f} {:.4f}".format(self.amount, self.den, self.total_bought, self.total_sold, self.total_sold-self.total_bought)

    def diff(self):
        return self.total_sold - self.total_bought

    def __add__(self, o):
        self.total_bought = self.total_bought + o.total_bought
        self.total_sold = self.total_sold + o.total_sold
        self.coin = self.coin + o.coin
        return self

    def k4_line(self):
        if self.coin.amount < 0.99:
            amount = self.coin.amount * 1000
            den = self.coin.den.milliden
        else:
            amount = self.coin.amount
            den = self.coin.den.den

        if self.diff() > 0:
            earnings = self.diff()
            return [amount, den, self.total_sold, self.total_bought, 0, earnings]
        else:
            return [amount, den, self.total_sold, self.total_bought, self.diff(), 0]