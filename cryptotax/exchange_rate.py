from datetime import datetime, timedelta

EUROSEK_FILE = "EURSEK.csv"


def read_csv(filename):
    with open(filename, "r") as fp:
        fp.readline()  # skip first line, dc about colunmns
        for line in fp.readlines():
            date, _dc, sek = line.strip().split(",")
            yield (datetime.strptime(date, "%Y-%m-%d"), float(sek))

class ExchangeRate():

    def __init__(self, den_from, den_to, t_fr=None, t_to=None):
        if den_from == 'EUR' and den_to == 'SEK':
            filename = EUROSEK_FILE
        else:
            print("Unknown currency")

        self.rates = {}
        rates = list(read_csv(filename))
        if not t_fr:
            t_fr = rates[0][0]
        if not t_to:
            t_to = datetime.now()
        delta = timedelta(days=1)

        rates = dict(rates)
        last_known=-1
        while t_fr <= t_to:
            v = rates.get(t_fr, last_known)
            last_known = v
            self.rates[t_fr] = v
            t_fr = t_fr + delta

    def to_sek(self, dt, euro):
        dt_day = datetime(dt.year, dt.month, dt.day)
        rate = self.rates.get(dt_day)
        return float(euro)*rate

if __name__ == '__main__':
    rates = ExchangeRate('EUR', 'SEK')
    print(rates.rates)
    dt = datetime.now()
    dt_day = datetime(dt.year, dt.month, dt.day)
    print(dt_day-timedelta(days=1))
    print(rates.rates.get(dt_day-timedelta(days=1)))
