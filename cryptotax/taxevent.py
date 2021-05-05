class TaxEvent():
    def __init__(self, coin, total_bought, total_sold):
        self.den = coin.den
        self.amount = coin.amount
        self.total_bought = total_bought
        self.total_sold = total_sold

    def __repr__(self):
        return "{:.2f} {} {:.4f} {:.4f} {:.4f}".format(self.amount, self.den, self.total_bought, self.total_sold, self.total_sold-self.total_bought)

    def diff(self):
        return self.total_sold - self.total_bought

    def __add__(self, o):
        self.total_bought = self.total_bought + o.total_bought
        self.total_sold = self.total_sold + o.total_sold
        self.amount = self.amount + o.amount
        return self

    def k4_line(self):
        if self.diff() > 0:
            earnings = self.diff()
            return [self.amount, self.den, self.total_sold, self.total_bought, 0, earnings]
        else:
            return [self.amount, self.den, self.total_sold, self.total_bought, -self.diff(), 0]