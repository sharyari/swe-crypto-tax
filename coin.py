EUR = 'EUR'

class Coin(float):
    ###
    # A general coin, it has a name and a value
    ###
    def __new__(cls, value, name, euro=None):
        obj = float.__new__(cls, value)
        obj.name = name
        if euro:
            obj.average_cost = euro/value
        else:
            # This would mean the coin is euro itself, 1==1
            obj.average_cost = 1
        return obj

    def to_euro_at_price(self, price):
        # The value of this coin for a given price
        return self * price

    def _cost(self):
        return self * self.average_cost

    def cost(self):
        return Coin(self._cost(), EUR)

    def __sub__(self, o):
        res = super(Coin, self).__sub__(o)
        # the average cost is not changed when we sell
        total_cost = res*self.average_cost
        return self.__class__(res, self.name, euro=total_cost)

    def __add__(self, o):
        res = super(Coin, self).__add__(o)
        # If we've bought, the average cost needs to be re-calculated
        total_cost = self._cost() + o._cost()
        #+ o*o.average_cost
        return self.__class__(res, self.name, euro=total_cost)


    def __repr__(self):
        return "{:.4f} {}".format(self, self.name)
