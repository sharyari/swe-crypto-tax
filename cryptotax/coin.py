class Coin():
    ###
    # A general coin, it has a name and a value
    ###
    def __init__(self, den, amount):
        self.den = den
        self.amount = amount 

    def __sub__(self, o):
        # the average cost is not changed when we sell
        amount = self.amount-o.amount
        return Coin(self.den, amount)

    def __add__(self, o):
        amount = self.amount+o.amount
        return Coin(self.den, amount)

    def __radd__(self, other):
        if type(other) is not Coin:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return "{:.4f} {}".format(self.amount, self.den)
